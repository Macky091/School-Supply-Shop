import tkinter as tk
from tkinter import ttk, messagebox

class ProductDialog(tk.Toplevel):
    def __init__(self, parent, title, product=None):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.result = None

        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.name_var = tk.StringVar(value=product['name'] if product else "")
        ttk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(self, text="Price:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.price_var = tk.DoubleVar(value=product['price'] if product else 0.0)
        ttk.Entry(self, textvariable=self.price_var).grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(self, text="Stock:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        self.stock_var = tk.IntVar(value=product['stock'] if product else 0)
        ttk.Entry(self, textvariable=self.stock_var).grid(row=2, column=1, padx=6, pady=6)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right", padx=4)
        ttk.Button(btn_frame, text="OK", command=self.on_ok).pack(side="right", padx=4)

        self.bind('<Return>', lambda e: self.on_ok())
        self.bind('<Escape>', lambda e: self.destroy())

        self.update_idletasks()
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{parent.winfo_rootx()+50}+{parent.winfo_rooty()+50}")
        self.focus()

    def on_ok(self):
        name = self.name_var.get().strip()
        price = self.price_var.get()
        stock = self.stock_var.get()
        if not name:
            messagebox.showwarning("Input Error", "Name cannot be empty.")
            return
        if price < 0 or stock < 0:
            messagebox.showwarning("Input Error", "Price and stock must be non-negative.")
            return
        self.result = (name, price, stock)
        self.destroy()
