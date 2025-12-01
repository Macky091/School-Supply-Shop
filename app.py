import tkinter as tk
from tkinter import ttk
from pathlib import Path
from datastore import datastore
from pages.home_page import HomePage
from pages.shop_page import ShopPage
from pages.cart_page import CartPage
from pages.admin_page import AdminPage

DATA_DIR = Path("data")
RECEIPTS_DIR = Path("receipts")

def center_window(self, width, height):
    self.update_idletasks()
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    self.geometry(f"{width}x{height}+{x}+{y}")

def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    RECEIPTS_DIR.mkdir(exist_ok=True, parents=True)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Supply Shop — Advanced")
        self.geometry("900x600")
        self.minsize(820, 540)
        self.configure(bg="#f7f7f7")
        center_window(self, 900, 600)

        # Initialize data
        ensure_dirs()
        self.store = datastore()
        self.cart = {}  # product_id -> quantity

        # Container for pages
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=12, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Pages
        self.pages = {}
        for Page in (HomePage, ShopPage, CartPage, AdminPage):
            page = Page(container, self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, name):
        page = self.pages.get(name)
        if page:
            page.refresh()
            page.tkraise()

    # ---------------- Cart helpers ----------------
    def add_to_cart(self, prod_id, qty=1):
        product = self.store.get_product(prod_id)
        if not product:
            return False
        if product["stock"] < qty:
            tk.messagebox.showwarning("Out of stock", f"Only {product['stock']} left for {product['name']}")
            return False
        self.cart[prod_id] = self.cart.get(prod_id, 0) + qty
        return True

    def set_cart_qty(self, prod_id, qty):
        if qty <= 0:
            self.cart.pop(prod_id, None)
        else:
            self.cart[prod_id] = qty

    def clear_cart(self):
        self.cart.clear()
