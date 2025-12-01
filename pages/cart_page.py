import tkinter as tk
from tkinter import ttk, messagebox
from .base_page import BasePage
from datetime import datetime
from pathlib import Path

RECEIPTS_DIR = Path("receipts")

class CartPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        top = ttk.Frame(self)
        top.pack(fill="x", padx=12, pady=(8,0))
        ttk.Button(top, text="Back", command=lambda: app.show_page("HomePage")).pack(side="left")
        ttk.Label(top, text="Cart", font=("Segoe UI", 18, "bold")).pack(side="left", padx=12)

        # Treeview for cart
        columns = ("id","name","price","qty","total")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", height=16)
        for c in columns:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=8)

        # Controls
        ctrl = ttk.Frame(self)
        ctrl.pack(fill="x", padx=12, pady=8)

        ttk.Label(ctrl, text="Quantity:").pack(side="left")
        self.qty_var = tk.IntVar(value=1)
        qty_spin = ttk.Spinbox(ctrl, from_=1, to=999, textvariable=self.qty_var, width=6)
        qty_spin.pack(side="left", padx=(4,8))

        ttk.Button(ctrl, text="Update Quantity", command=self.on_update).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Remove Item", command=self.on_remove).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Checkout", command=self.on_checkout).pack(side="left", padx=10)

        self.total_label = ttk.Label(self, text="", font=("Segoe UI", 12, "bold"))
        self.total_label.pack(pady=8)

    def refresh(self):
        # Clear tree
        for r in self.tree.get_children():
            self.tree.delete(r)

        total_price = 0
        for pid, qty in self.app.cart.items():
            p = self.app.store.get_product(pid)
            if not p:
                continue
            total = p['price'] * qty
            total_price += total
            self.tree.insert("", tk.END, values=(p['id'], p['name'], f"₱{p['price']:.2f}", qty, f"₱{total:.2f}"))
        self.total_label.config(text=f"Total: ₱{total_price:.2f}")

    def on_update(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select item", "Please select an item.")
            return
        item = self.tree.item(sel)
        pid = int(item["values"][0])
        qty = self.qty_var.get()
        p = self.app.store.get_product(pid)
        if qty > p['stock']:
            messagebox.showwarning("Not enough stock", f"Only {p['stock']} left.")
            return
        self.app.set_cart_qty(pid, qty)
        self.refresh()

    def on_remove(self):
        sel = self.tree.selection()
        if not sel:
            return
        pid = int(self.tree.item(sel)["values"][0])
        self.app.set_cart_qty(pid, 0)
        self.refresh()

    def on_checkout(self):
        if not self.app.cart:
            messagebox.showinfo("Cart Empty", "Your cart is empty.")
            return

        # Deduct stock
        for pid, qty in self.app.cart.items():
            self.app.store.update_product(pid, stock=self.app.store.get_product(pid)['stock'] - qty)

        # Save receipt
        RECEIPTS_DIR.mkdir(exist_ok=True)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        receipt_file = RECEIPTS_DIR / f"receipt_{now}.txt"
        with open(receipt_file, 'w', encoding='utf-8') as f:
            f.write(f"Receipt - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*40 + "\n")
            total_price = 0
            for pid, qty in self.app.cart.items():
                p = self.app.store.get_product(pid)
                total = p['price'] * qty
                total_price += total
                f.write(f"{p['name']} x{qty} - ₱{total:.2f}\n")
            f.write("="*40 + "\n")
            f.write(f"Total: ₱{total_price:.2f}\n")

        messagebox.showinfo("Checkout Complete", f"Receipt saved as {receipt_file.name}")
        self.app.clear_cart()
        self.refresh()
