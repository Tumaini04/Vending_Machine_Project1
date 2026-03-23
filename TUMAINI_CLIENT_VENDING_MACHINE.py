import tkinter as tk
import socket

class VendingMachineClientGUI(tk.Frame):
    def __init__(self, root, products, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.products = products
        self.root = root
        self.root.title("Tumaini's Vending Machine")
        self.root.geometry("1000x800")  # Adjusted window size for better visibility
        self.root.configure(bg="black")

        # Create the canvas for displaying an image
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="black")
        self.canvas.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N)  # Grid placement for canvas

        # Load and display the image on the canvas
        self.image = tk.PhotoImage(file=r"C:\Users\TM1046\Documents\Programming SOBs\Vending machine coursework\display.png")
        self.canvas.create_image(300, 300, image=self.image)

        # Create a frame to hold the main content next to the canvas
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky=tk.N)  # Grid placement for main frame

        # Create a box (frame) to hold the widgets
        self.widget_frame = tk.Frame(self.main_frame, bg="black")
        self.widget_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Widgets for placing an order
        self.order_label = tk.Label(self.widget_frame, text="Place Your Order:", bg="black", fg="white")
        self.order_label.grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.W)

        self.product_id_label = tk.Label(self.widget_frame, text="Product ID:", fg="blue", bg="yellow")
        self.product_id_label.grid(row=1, column=0, pady=5, sticky=tk.W)

        self.product_id_entry = tk.Entry(self.widget_frame, bg="green")
        self.product_id_entry.grid(row=1, column=1, pady=5, sticky=tk.W)

        self.quantity_label = tk.Label(self.widget_frame, text="Quantity:", fg="blue", bg="yellow")
        self.quantity_label.grid(row=2, column=0, pady=5, sticky=tk.W)

        self.quantity_entry = tk.Entry(self.widget_frame, bg="green")
        self.quantity_entry.grid(row=2, column=1, pady=5, sticky=tk.W)

        self.order_button = tk.Button(self.widget_frame, text="Place Order", command=self.place_order, fg="blue", bg="yellow")
        self.order_button.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.cancel_order_button = tk.Button(self.widget_frame, text="Cancel Order", command=self.cancel_order, fg="blue", bg="yellow")
        self.cancel_order_button.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.W)

        # Payment options for OptionMenu
        self.payment_var = tk.StringVar()
        self.payment_var.set("Cash")  # Default payment method
        self.payment_options = ["Cash", "Credit Card", "Mobile Payment"]

        self.payment_label = tk.Label(self.widget_frame, text="Payment Method:", fg="blue", bg="yellow")
        self.payment_label.grid(row=5, column=0, pady=5, sticky=tk.W)

        self.payment_menu = tk.OptionMenu(self.widget_frame, self.payment_var, *self.payment_options)
        self.payment_menu.grid(row=5, column=1, pady=5, sticky=tk.W)

        self.receipt_label = tk.Label(self.widget_frame, text="Receipt:")
        self.receipt_label.grid(row=7, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.receipt_text = tk.Text(self.widget_frame, width=50, height=4)
        self.receipt_text.grid(row=8, column=0, columnspan=2, pady=5, sticky=tk.W)

        self.orders = []

        # Display welcome message in the receipt area
        self.receipt_text.insert(tk.END, "Welcome to the Vending Machine!\n")

        # Server connection details
        self.server_host = "localhost"
        self.server_port = 8889
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.server_socket.connect((self.server_host, self.server_port))
            print("Connected to server")
        except ConnectionRefusedError:
            print("Failed to connect to server")

    def place_order(self):
        product_id = self.product_id_entry.get()
        quantity = self.quantity_entry.get()

        try:
            quantity = int(quantity)
        except ValueError:
            print("Invalid quantity")
            return

        # Send order request to the server
        request = f"place_order {product_id} {quantity}"
        self.server_socket.sendall(request.encode())

        # Receive and process response from the server
        response = self.server_socket.recv(1024).decode()

        if response.startswith("Transaction Confirmation"):
            self.receipt_text.insert(tk.END, f"Placed order: Product ID: {product_id}, Quantity: {quantity}\n")
        else:
            self.receipt_text.insert(tk.END, "Invalid transaction. Please try again.\n")

    def cancel_order(self):
        if self.orders:
            product_id, quantity = self.orders.pop()
            self.receipt_text.insert(tk.END, f"Canceled order: Product ID: {product_id}, Quantity: {quantity}\n")
        else:
            print("No orders to cancel")

        # Display goodbye message in the receipt area after canceling order
        if not self.orders:
            self.receipt_text.insert(tk.END, "Thank you for using the Vending Machine!\n")

def main():
    root = tk.Tk()
    root.title("Product List")
    root.configure(bg="black")

    products = []

    app = VendingMachineClientGUI(root, products)
    app.grid(row=0, column=0, padx=20, pady=20)  # Grid placement for the main app

    # Connect to the server upon launching the client application
    app.connect_to_server()

    root.mainloop()

if __name__ == "__main__":
    main()
