import tkinter as tk
from tkinter import messagebox

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class POS:
    def __init__(self, root):
        self.root = root
        self.products = []
        self.sales = []

        # Create product management frame
        self.product_frame = tk.Frame(self.root)
        self.product_frame.pack()

        # Create product name label and entry
        self.product_name_label = tk.Label(self.product_frame, text="Product Name:")
        self.product_name_label.pack()
        self.product_name_entry = tk.Entry(self.product_frame)
        self.product_name_entry.pack()

        # Create product price label and entry
        self.product_price_label = tk.Label(self.product_frame, text="Product Price:")
        self.product_price_label.pack()
        self.product_price_entry = tk.Entry(self.product_frame)
        self.product_price_entry.pack()

        # Create product quantity label and entry
        self.product_quantity_label = tk.Label(self.product_frame, text="Product Quantity:")
        self.product_quantity_label.pack()
        self.product_quantity_entry = tk.Entry(self.product_frame)
        self.product_quantity_entry.pack()

        # Create add product button
        self.add_product_button = tk.Button(self.product_frame, text="Add Product", command=self.add_product)
        self.add_product_button.pack()

        # Create sales frame
        self.sales_frame = tk.Frame(self.root)
        self.sales_frame.pack()

        # Create sales listbox
        self.sales_listbox = tk.Listbox(self.sales_frame)
        self.sales_listbox.pack()

        # Create make sale button
        self.make_sale_button = tk.Button(self.sales_frame, text="Make Sale", command=self.make_sale)
        self.make_sale_button.pack()

        # Create total label
        self.total_label = tk.Label(self.sales_frame, text="Total: $0.00")
        self.total_label.pack()

    def add_product(self):
        name = self.product_name_entry.get()
        price = float(self.product_price_entry.get())
        quantity = int(self.product_quantity_entry.get())
        self.products.append(Product(name, price, quantity))
        self.product_name_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.product_quantity_entry.delete(0, tk.END)
        messagebox.showinfo("Product Added", f"Product {name} added successfully")

    def make_sale(self):
        if not self.products:
            messagebox.showerror("No Products", "Please add products before making a sale")
            return
        sale_window = tk.Toplevel(self.root)
        sale_window.title("Make Sale")
        sale_label = tk.Label(sale_window, text="Select Product:")
        sale_label.pack()
        product_var = tk.StringVar(sale_window)
        product_var.set(self.products[0].name)
        product_option = tk.OptionMenu(sale_window, product_var, *[product.name for product in self.products])
        product_option.pack()
        quantity_label = tk.Label(sale_window, text="Quantity:")
        quantity_label.pack()
        quantity_entry = tk.Entry(sale_window)
        quantity_entry.pack()
        def confirm_sale():
            product_name = product_var.get()
            quantity = int(quantity_entry.get())
            for product in self.products:
                if product.name == product_name:
                    if product.quantity < quantity:
                        messagebox.showerror("Insufficient Quantity", "Not enough quantity in stock")
                        return
                    product.quantity -= quantity
                    self.sales.append((product_name, quantity, product.price * quantity))
                    self.sales_listbox.insert(tk.END, f"{product_name} x {quantity} = ${product.price * quantity:.2f}")
                    self.total_label['text'] = f"Total: ${sum([sale[2] for sale in self.sales]):.2f}"
                    sale_window.destroy()
                    break
        confirm_button = tk.Button(sale_window, text="Confirm Sale", command=confirm_sale)
        confirm_button.pack()

root = tk.Tk()
root.title("Point of Sale System")
pos = POS(root)
root.mainloop()