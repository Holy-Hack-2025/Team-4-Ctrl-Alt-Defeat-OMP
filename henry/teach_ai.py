import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Connect to the database
conn = sqlite3.connect("supply_chain.db")

# Load data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM supply_data", conn)

# Close the connection
conn.close()

# Define the target (1 = Shortage risk, 0 = Safe)
df["shortage_risk"] = (df["current_stock"] < df["min_stock"]).astype(int)

# Select features for AI training
features = ["current_stock", "min_stock", "supplier_stock", "orders_placed", "restock_time_days", "demand_forecast"]
X = df[features]  # Input features
y = df["shortage_risk"]  # Target variable (0 or 1)

# Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the AI model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
