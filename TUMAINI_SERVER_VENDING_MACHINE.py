import socket
import mysql.connector

class VendingMachineServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stock = {}

    def start(self):
        self.load_stock_from_storage()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, _ = server_socket.accept()
                print("Client connected")

                with client_socket:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break

                        request = data.decode()
                        response = self.handle_request(request)

                        client_socket.sendall(response.encode())
        
    def load_stock_from_storage(self):
        try:
            connection = self.connect_to_database()
            cursor = connection.cursor()

            cursor.execute("SELECT Product_id, Product_name, Price, Quantity FROM TRANSACTIONS")

            self.stock = {}
            for (Product_id, Product_name, Price, Quantity,) in cursor:
                self.stock[Product_id] = {
                    "Product_name": Product_name,
                    "Price": float(Price),
                    "Quantity": int(Quantity),
                }

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print(f"Error loading stock from database: {error}")

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jul132003&",
            database="vendingmachine"
        )

    def get_product_details(self):
        if not self.stock:
            return "No products available."

        products_info = []
        for Product_id, product_info in self.stock.items():
            product_details = (
                f"ID: {Product_id}, "
                f"Name: {product_info['Product_name']}, "
                f"Price: ${product_info['Price']}, "
                f"Quantity: {product_info['Quantity']}, "
            )
            products_info.append(product_details)

        return "\n".join(products_info)

    
    def handle_request(self, request):
        parts = request.strip().split(" ")
        action = parts[0]

        if action == "get_products":
            return self.serialize_stock()
        elif action == "place_order":
            try:
                Product_id, Quantity = parts[1], int(parts[2])
                return self.process_order(Product_id, Quantity)
            except (IndexError, ValueError):
                return "Invalid request"
        else:
            return "Invalid action"

    def serialize_stock(self):
        stock_str = ""
        for Product_id, product_info in self.stock.items():
            stock_str += f"ID: {Product_id}: {product_info['Product_name']}: ${product_info['Price']}: Quantity {product_info['Quantity']}\n"
        return stock_str

    def process_order(self, Product_id, Quantity):
        if Product_id not in self.stock:
            return "Invalid Product ID"

        if self.stock[Product_id]["Quantity"] < Quantity:
            return "Insufficient stock"

        # Deduct quantity from stock
        self.stock[Product_id]["Quantity"] -= Quantity

        # Generate receipt
        total_price = self.stock[Product_id]['Price'] * Quantity
        receipt = f"Transaction Confirmation: Product: {self.stock[Product_id]['Product_name']}, Quantity: {Quantity}, Total Price: ${total_price}"
        print(receipt)  # Print receipt for server's reference

        return receipt

def main():
    server = VendingMachineServer("localhost", 8889)
    server.start()

if __name__ == "__main__":
    main()
