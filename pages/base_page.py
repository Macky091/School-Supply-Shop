import tkinter as tk
from tkinter import ttk

class BasePage(ttk.Frame):
    """Base page for all pages in the app."""
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

    def refresh(self):
        """Refresh the page content when raised."""
        pass
