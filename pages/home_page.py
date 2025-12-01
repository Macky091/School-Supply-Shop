import tkinter as tk
from tkinter import ttk
from .base_page import BasePage

class HomePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        header = ttk.Label(self, text="School Supply Shop", font=("Segoe UI", 20, "bold"))
        header.pack(pady=(20, 10))

        subheader = ttk.Label(self, text="Clean, modern, and ready for presentation", font=("Segoe UI", 12))
        subheader.pack(pady=(0, 20))

        # Card container
        card_frame = ttk.Frame(self)
        card_frame.pack(expand=True, fill="both", padx=20, pady=10)
        card_frame.columnconfigure((0,1,2), weight=1)

        # Shop Card
        shop_card = ttk.Frame(card_frame, relief="raised", borderwidth=2, padding=12)
        shop_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ttk.Label(shop_card, text="Shop Items", font=("Segoe UI", 14, "bold")).pack(pady=8)
        ttk.Button(shop_card, text="Browse Shop", command=lambda: app.show_page("ShopPage")).pack(pady=8, ipadx=10, ipady=5)

        # Cart Card
        cart_card = ttk.Frame(card_frame, relief="raised", borderwidth=2, padding=12)
        cart_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ttk.Label(cart_card, text="Cart", font=("Segoe UI", 14, "bold")).pack(pady=8)
        ttk.Button(cart_card, text="View Cart", command=lambda: app.show_page("CartPage")).pack(pady=8, ipadx=10, ipady=5)

        # Admin Card
        admin_card = ttk.Frame(card_frame, relief="raised", borderwidth=2, padding=12)
        admin_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ttk.Label(admin_card, text="Admin", font=("Segoe UI", 14, "bold")).pack(pady=8)
        ttk.Button(admin_card, text="Inventory Manager", command=lambda: app.show_page("AdminPage")).pack(pady=8, ipadx=10, ipady=5)

        # Footer summary
        self.summary = ttk.Label(self, text="", font=("Segoe UI", 11))
        self.summary.pack(pady=12)

    def refresh(self):
        total_stock = sum(p.get("stock",0) for p in self.app.store.products)
        total_products = len(self.app.store.products)
        total_cart = sum(self.app.cart.values())
        self.summary.config(text=f"Products: {total_products} • Total Stock: {total_stock} • Cart Items: {total_cart}")
