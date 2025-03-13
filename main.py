import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to the SQLite database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Function to create the database tables
def create_tables():
    # Create Suppliers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        supplier_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')

    # Create Supplies table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Supplies (
        supply_id INTEGER PRIMARY KEY,
        supplier_id INTEGER,
        item_name TEXT NOT NULL,
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
    )
    ''')

    conn.commit()
    print("Tables created successfully.")

# Function to insert sample suppliers and items into the database
def insert_sample_data():
    # Insert suppliers
    suppliers = [
        ('Supplier A'),
        ('Supplier B'),
        ('Supplier C')
    ]
    
    cursor.executemany('INSERT INTO Suppliers (name) VALUES (?)', [(name,) for name in suppliers])

    # Get the supplier IDs (to associate with items)
    cursor.execute('SELECT supplier_id FROM Suppliers')
    supplier_ids = cursor.fetchall()

    # Insert supplies (items delivered by each supplier)
    supplies = [
        (supplier_ids[0][0], 'Item 1A'),
        (supplier_ids[0][0], 'Item 2A'),
        (supplier_ids[1][0], 'Item 1B'),
        (supplier_ids[1][0], 'Item 2B'),
        (supplier_ids[2][0], 'Item 1C'),
        (supplier_ids[2][0], 'Item 2C')
    ]

    cursor.executemany('INSERT INTO Supplies (supplier_id, item_name) VALUES (?, ?)', supplies)

    # Commit the changes
    conn.commit()
    print("Sample data inserted successfully.")

# Function to get all suppliers and their items
def get_suppliers():
    cursor.execute('''SELECT s.name, i.item_name FROM Suppliers s
                      JOIN Supplies i ON s.supplier_id = i.supplier_id''')
    return cursor.fetchall()

# Function to exclude a supplier and show impacted items
def exclude_supplier(supplier_name):
    # Get all items that depend on the excluded supplier
    cursor.execute('''SELECT item_name FROM Supplies s
                      JOIN Suppliers p ON s.supplier_id = p.supplier_id
                      WHERE p.name = ?''', (supplier_name,))
    items = cursor.fetchall()
    
    if not items:
        messagebox.showinfo("No Impact", "This supplier is not supplying any items.")
        return
    
    # Show the items that will run out
    messagebox.showinfo("Exclusion Impact", f"Excluding supplier {supplier_name} will impact the following products:\n" + '\n'.join([item[0] for item in items]))

# Tkinter UI
root = tk.Tk()
root.title("Supplier Management")

# Create table and insert sample data if not already done
create_tables()
insert_sample_data()

# Display list of suppliers
def show_suppliers():
    suppliers = get_suppliers()
    for row in suppliers:
        supplier_name = row[0]
        items = row[1]
        supplier_label = ttk.Label(root, text=f"Supplier: {supplier_name}, Item: {items}")
        supplier_label.pack()

# Add Exclude button
def exclude_supplier_ui():
    supplier_name = supplier_name_entry.get()
    exclude_supplier(supplier_name)

# Input to exclude a supplier
supplier_name_label = ttk.Label(root, text="Enter Supplier Name to Exclude:")
supplier_name_label.pack()
supplier_name_entry = ttk.Entry(root)
supplier_name_entry.pack()

exclude_button = ttk.Button(root, text="Exclude Supplier", command=exclude_supplier_ui)
exclude_button.pack()

# Display suppliers and their items
show_suppliers()

# Start Tkinter main loop
root.mainloop()

# Close the connection after the Tkinter window is closed
conn.close()
