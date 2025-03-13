import tkinter as tk
from tkinter import ttk
import sqlite3

class SalesTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Tracking System")
        
        # Database setup
        self.conn = sqlite3.connect("sales.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
        
        # Sales Table
        self.sales_frame = ttk.LabelFrame(root, text="Sales Data")
        self.sales_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.sales_tree = ttk.Treeview(self.sales_frame, columns=("Item", "Quantity", "Price", "Total"), show="headings")
        self.sales_tree.heading("Item", text="Item")
        self.sales_tree.heading("Quantity", text="Quantity")
        self.sales_tree.heading("Price", text="Price")
        self.sales_tree.heading("Total", text="Total")
        self.sales_tree.pack(fill="both", expand=True)
        
        # Input Fields
        self.input_frame = ttk.LabelFrame(root, text="Add Sale")
        self.input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.input_frame, text="Item:").grid(row=0, column=0, padx=5, pady=2)
        self.item_entry = ttk.Entry(self.input_frame)
        self.item_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(self.input_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=2)
        self.quantity_entry = ttk.Entry(self.input_frame)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(self.input_frame, text="Price:").grid(row=0, column=4, padx=5, pady=2)
        self.price_entry = ttk.Entry(self.input_frame)
        self.price_entry.grid(row=0, column=5, padx=5, pady=2)
        
        self.add_button = ttk.Button(self.input_frame, text="Add Sale", command=self.add_sale)
        self.add_button.grid(row=0, column=6, padx=5, pady=2)
        
        # Inventory Section
        self.inventory_frame = ttk.LabelFrame(root, text="Inventory Levels")
        self.inventory_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=("Item", "Stock"), show="headings")
        self.inventory_tree.heading("Item", text="Item")
        self.inventory_tree.heading("Stock", text="Stock Level")
        self.inventory_tree.pack(fill="both", expand=True)
        
        # Placeholder for AI recommendations
        self.recommendation_label = ttk.Label(root, text="AI Recommendations: (Coming Soon)", font=("Arial", 12, "bold"))
        self.recommendation_label.pack(pady=10)
        
        self.load_inventory()
        self.load_sales()
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT,
                quantity INTEGER,
                price REAL,
                total REAL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item TEXT PRIMARY KEY,
                stock INTEGER
            )
        """)
        self.conn.commit()
    
    def add_sale(self):
        item = self.item_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        total = quantity * price
        
        if item and quantity and price:
            self.cursor.execute("INSERT INTO sales (item, quantity, price, total) VALUES (?, ?, ?, ?)",
                                (item, quantity, price, total))
            self.conn.commit()
            self.sales_tree.insert("", "end", values=(item, quantity, price, total))
            
            # Update inventory
            self.cursor.execute("SELECT stock FROM inventory WHERE item = ?", (item,))
            result = self.cursor.fetchone()
            if result:
                new_stock = max(0, result[0] - quantity)
                self.cursor.execute("UPDATE inventory SET stock = ? WHERE item = ?", (new_stock, item))
            else:
                self.cursor.execute("INSERT INTO inventory (item, stock) VALUES (?, ?)", (item, max(0, -quantity)))
            
            self.conn.commit()
            self.load_inventory()
            
            self.item_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
    
    def load_inventory(self):
        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)
        
        self.cursor.execute("SELECT * FROM inventory")
        for row in self.cursor.fetchall():
            self.inventory_tree.insert("", "end", values=row)
    
    def load_sales(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)
        
        self.cursor.execute("SELECT item, quantity, price, total FROM sales")
        for row in self.cursor.fetchall():
            self.sales_tree.insert("", "end", values=row)
    
    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesTrackingApp(root)
    root.mainloop()