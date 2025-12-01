import tkinter as tk
from tkinter import ttk, messagebox
from .base_page import BasePage

class ShopPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        # Top bar with back button and header
        top = ttk.Frame(self)
        top.pack(fill="x", padx=12, pady=(8,0))
        ttk.Button(top, text="Back", command=lambda: app.show_page("HomePage")).pack(side="left")
        ttk.Label(top, text="Shop", font=("Segoe UI", 18, "bold")).pack(side="left", padx=12)

        # Search bar
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=12, pady=8)
        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", padx=(4,8), fill="x", expand=True)
        ttk.Button(search_frame, text="Clear", command=lambda: self.search_var.set("")).pack(side="left")

        # Treeview for products
        columns = ("id","name","price","stock")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", height=16)
        for c in columns:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=8)

        # Controls for quantity and add to cart
        ctrl = ttk.Frame(self)
        ctrl.pack(fill="x", padx=12, pady=8)
        ttk.Label(ctrl, text="Quantity:").pack(side="left")
        self.qty_var = tk.IntVar(value=1)
        qty_spin = ttk.Spinbox(ctrl, from_=1, to=999, textvariable=self.qty_var, width=6)
        qty_spin.pack(side="left", padx=(4,8))
        ttk.Button(ctrl, text="Add to Cart", command=self.on_add).pack(side="left")
        ttk.Button(ctrl, text="View Cart", command=lambda: app.show_page("CartPage")).pack(side="left", padx=6)

    def refresh(self):
        query = self.search_var.get()
        products = self.app.store.search(query)

        # Clear tree
        for r in self.tree.get_children():
            self.tree.delete(r)

        # Insert products
        for p in products:
            self.tree.insert("", tk.END, values=(p["id"], p["name"], f"₱{p['price']:.2f}", p["stock"]))

    def on_add(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select item", "Please select an item to add.")
            return
        item = self.tree.item(sel)
        pid = int(item["values"][0])
        qty = int(self.qty_var.get())
        p = self.app.store.get_product(pid)
        if not p:
            messagebox.showerror("Error", "Product not found.")
            return
        if p["stock"] <= 0:
            messagebox.showwarning("Out of stock", "This product is out of stock.")
            return
        if qty > p["stock"]:
            messagebox.showwarning("Not enough stock", f"Only {p['stock']} left.")
            return
        self.app.add_to_cart(pid, qty=qty)
        messagebox.showinfo("Added", f"{p['name']} x{qty} added to cart.")
        shop_card = ttk.Frame(card_frame, style='Card.TFrame', padding=(12, 12))
        cart_card = ttk.Frame(card_frame, style='Card.TFrame', padding=(12, 12))
        admin_card = ttk.Frame(card_frame, style='Card.TFrame', padding=(12, 12))

        

