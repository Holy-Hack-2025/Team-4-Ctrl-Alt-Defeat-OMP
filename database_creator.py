import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Function to insert some imaginary suppliers and items into the database
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

# Insert sample data into the database
insert_sample_data()

# Close the connection after inserting data
conn.close()
