import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database
conn = sqlite3.connect("supply_chain.db")
cursor = conn.cursor()

# Ensure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS supply_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_name TEXT,
    date TEXT,
    product TEXT,
    current_stock INTEGER,
    min_stock INTEGER,
    supplier_stock INTEGER,
    orders_placed INTEGER,
    restock_time_days INTEGER,
    demand_forecast INTEGER
);
""")

# Generate 10,000 random records
hospital_names = ["Hospital A", "Hospital B", "Hospital C", "Hospital D"]
products = ["Gloves", "Masks", "Ventilators", "Syringes", "Bandages"]

start_date = datetime(2023, 1, 1)
num_records = 10_000
data = []

for _ in range(num_records):
    hospital = random.choice(hospital_names)
    product = random.choice(products)
    date = start_date + timedelta(days=random.randint(0, 365))
    date_str = date.strftime("%Y-%m-%d")

    current_stock = random.randint(10, 500)
    min_stock = random.randint(50, 200)
    supplier_stock = random.randint(100, 1000)
    orders_placed = random.randint(0, 50)
    restock_time_days = random.randint(1, 7)
    demand_forecast = random.randint(20, 400)

    data.append((hospital, date_str, product, current_stock, min_stock, supplier_stock, orders_placed, restock_time_days, demand_forecast))

# Insert into database
cursor.executemany("""
INSERT INTO supply_data (hospital_name, date, product, current_stock, min_stock, supplier_stock, orders_placed, restock_time_days, demand_forecast)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
""", data)

# Commit and close
conn.commit()
conn.close()

print(f"{num_records} records inserted successfully!")
