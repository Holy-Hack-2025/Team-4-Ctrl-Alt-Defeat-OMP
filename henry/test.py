import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load AI Model
def train_ai():
    conn = sqlite3.connect("supply_chain.db")
    df = pd.read_sql_query("SELECT * FROM supply_data", conn)
    conn.close()

    df["shortage_risk"] = (df["current_stock"] < df["min_stock"]).astype(int)
    features = ["current_stock", "min_stock", "supplier_stock", "orders_placed", "restock_time_days", "demand_forecast"]
    X = df[features]
    y = df["shortage_risk"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model

# AI Model Instance
ai_model = train_ai()


# Tkinter Simulation Class
class SupplyChainSimulation:
    def __init__(self, root):
        self.root = root
        self.create_simulation_screen()

    def create_simulation_screen(self):
        self.root.title("Healthcare Supply Chain Simulation")

        self.hospitals = load_hospitals()
        self.supplier_labels = []

        # Display Hospitals
        tk.Label(self.root, text="Hospital Inventory", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
        for idx, hospital in enumerate(self.hospitals):
            label_text = f"{hospital.name}: A = {hospital.inventory['A']}, B = {hospital.inventory['B']}"
            risk_text = self.get_ai_prediction(hospital)
            label = tk.Label(self.root, text=f"{label_text} {risk_text}")
            label.grid(row=idx + 1, column=0, padx=10, pady=5)

        # Predict Shortages Button
        predict_button = tk.Button(self.root, text="Predict Shortages", command=self.update_predictions, font=("Helvetica", 12))
        predict_button.grid(row=len(self.hospitals) + 2, column=0, columnspan=2, pady=20)

    def get_ai_prediction(self, hospital):
        """Runs AI prediction for a hospital."""
        X_new = [[hospital.inventory['A'], hospital.min_inventory['A'], 500, 2, 3, 100]]  # Sample Data
        prediction = ai_model.predict(X_new)[0]
        return "🚨 Shortage Risk!" if prediction == 1 else "✅ Sufficient Stock"

    def update_predictions(self):
        """Updates hospital labels with AI predictions."""
        for idx, hospital in enumerate(self.hospitals):
            risk_text = self.get_ai_prediction(hospital)
            self.hospital_labels[idx].config(text=f"{hospital.name}: {risk_text}")


# Load hospital data
def load_hospitals():
    hospitals = [
        Hospital("Hospital A", {'A': 50, 'B': 30}, {'A': 100, 'B': 50}, "Coords1"),
        Hospital("Hospital B", {'A': 120, 'B': 80}, {'A': 90, 'B': 70}, "Coords2"),
    ]
    return hospitals


class Hospital:
    def __init__(self, name, inventory, min_inventory, coordinates):
        self.name = name
        self.inventory = inventory
        self.min_inventory = min_inventory
        self.coordinates = coordinates


# Run the App
root = tk.Tk()
app = SupplyChainSimulation(root)
root.mainloop()
