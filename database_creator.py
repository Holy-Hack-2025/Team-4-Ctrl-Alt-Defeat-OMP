import sqlite3
import random

# Connect to the existing database
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Generate random suppliers
def generate_test_data(num_suppliers=500):
    cursor.execute("DELETE FROM suppliers")  # Clear existing data

    for _ in range(num_suppliers):
        name = f"Supplier_{random.randint(1000, 9999)}"
        reliability = random.randint(50, 100)  # Reliability score (higher is better)
        lead_time = random.randint(1, 15)  # Lead time in days
        historical_events = random.randint(0, 10)  # Number of past issues

        cursor.execute("INSERT INTO suppliers (name, reliability, lead_time, historical_events) VALUES (?, ?, ?, ?)", 
                       (name, reliability, lead_time, historical_events))

    conn.commit()
    print(f"{num_suppliers} test suppliers added successfully!")

generate_test_data()
conn.close()
