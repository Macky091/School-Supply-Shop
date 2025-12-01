import json
from pathlib import Path
from tkinter import messagebox

DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"

SAMPLE_PRODUCTS = [
    {"id": 1, "name": "Ballpen", "price": 10.0, "stock": 50},
    {"id": 2, "name": "Notebook (A5)", "price": 35.0, "stock": 40},
    {"id": 3, "name": "Bond Paper (A4) - 1pc", "price": 3.0, "stock": 500},
    {"id": 4, "name": "Highlighter", "price": 25.0, "stock": 30},
]

class datastore:
    def __init__(self, filepath=PRODUCTS_FILE):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self._write_products(SAMPLE_PRODUCTS)
        self.products = self._read_products()

    def _read_products(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Data Error", f"Failed to load products.json: {e}")
            return []

    def _write_products(self, data):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Data Error", f"Failed to save products.json: {e}")

    def save(self):
        self._write_products(self.products)

    def add_product(self, name, price, stock):
        max_id = max((p.get('id', 0) for p in self.products), default=0)
        new_product = {"id": max_id + 1, "name": name, "price": float(price), "stock": int(stock)}
        self.products.append(new_product)
        self.save()
        return new_product

    def update_product(self, prod_id, name=None, price=None, stock=None):
        for p in self.products:
            if p['id'] == prod_id:
                if name is not None:
                    p['name'] = name
                if price is not None:
                    p['price'] = float(price)
                if stock is not None:
                    p['stock'] = int(stock)
                self.save()
                return p
        return None

    def delete_product(self, prod_id):
        self.products = [p for p in self.products if p['id'] != prod_id]
        self.save()

    def get_product(self, prod_id):
        for p in self.products:
            if p['id'] == prod_id:
                return p
        return None

    def search(self, query):
        q = query.strip().lower()
        if not q:
            return list(self.products)
        return [p for p in self.products if q in p['name'].lower()]
