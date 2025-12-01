import tkinter as tk
from tkinter import ttk, messagebox
from .base_page import BasePage

class AdminPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        top = ttk.Frame(self)
        top.pack(fill="x", padx=12, pady=(8,0))
        ttk.Button(top, text="Back", command=lambda: app.show_page("HomePage")).pack(side="left")
        ttk.Label(top, text="Admin - Inventory", font=("Segoe UI", 18, "bold")).pack(side="left", padx=12)

        # Treeview for products
        columns = ("id","name","price","stock")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", height=16)
        for c in columns:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=8)

        # Controls
        ctrl = ttk.Frame(self)
        ctrl.pack(fill="x", padx=12, pady=8)

        ttk.Button(ctrl, text="Add Product", command=self.on_add).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Edit Product", command=self.on_edit).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Delete Product", command=self.on_delete).pack(side="left", padx=4)

    def refresh(self):
        # Clear tree
        for r in self.tree.get_children():
            self.tree.delete(r)

        # Insert products
        for p in self.app.store.products:
            self.tree.insert("", tk.END, values=(p['id'], p['name'], f"₱{p['price']:.2f}", p['stock']))

    def on_add(self):
        from dialogs.product_dialog import ProductDialog
        dialog = ProductDialog(self, "Add Product")
        self.wait_window(dialog)
        if dialog.result:
            name, price, stock = dialog.result
            self.app.store.add_product(name, price, stock)
            self.refresh()

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select item", "Please select an item to edit.")
            return
        pid = int(self.tree.item(sel)["values"][0])
        p = self.app.store.get_product(pid)
        from dialogs.product_dialog import ProductDialog
        dialog = ProductDialog(self, "Edit Product", product=p)
        self.wait_window(dialog)
        if dialog.result:
            name, price, stock = dialog.result
            self.app.store.update_product(pid, name, price, stock)
            self.refresh()

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            return
        pid = int(self.tree.item(sel)["values"][0])
        p = self.app.store.get_product(pid)
        if messagebox.askyesno("Confirm Delete", f"Delete {p['name']}?"):
            self.app.store.delete_product(pid)
            self.refresh()