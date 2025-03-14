import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Add risk_score column if it doesn't exist
cursor.execute("ALTER TABLE suppliers ADD COLUMN risk_score INTEGER DEFAULT 0")

conn.commit()
conn.close()