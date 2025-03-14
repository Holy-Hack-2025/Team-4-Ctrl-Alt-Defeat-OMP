import tkinter as tk
from tkinter import messagebox
import csv


# Home Screen Class
class HomeScreen:
    def __init__(self, root, switch_to_simulation_screen_callback):
        self.root = root
        self.switch_to_simulation_screen_callback = switch_to_simulation_screen_callback
        self.create_home_screen()

    def create_home_screen(self):
        self.root.title("Healthcare Supply Chain Simulation - Home")

        # Title
        tk.Label(self.root, text="Welcome to the Healthcare Supply Chain Simulation", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=20, columnspan=2)

        # Description of the application
        description_text = (
            "This application simulates the distribution of medicines between hospitals and suppliers.\n"
            "It helps to manage supply chain disruptions, optimize logistics, and ensure that hospitals are "
            "adequately supplied. Click 'Start Simulation' to begin."
        )
        tk.Label(self.root, text=description_text, font=("Helvetica", 12), justify="left", wraplength=400).grid(row=1, column=0, padx=10, pady=20, columnspan=2)

        # Start Simulation button
        start_button = tk.Button(self.root, text="Start Simulation", command=self.switch_to_simulation_screen, font=("Helvetica", 12))
        start_button.grid(row=2, column=0, padx=10, pady=20, columnspan=2)

    def switch_to_simulation_screen(self):
        self.root.withdraw()  # Hide the home screen
        self.switch_to_simulation_screen_callback()  # Call the callback to show the simulation screen


# Supply Chain Simulation Class
class SupplyChainSimulation:
    def __init__(self, root):
        self.root = root
        self.create_simulation_screen()

    def create_simulation_screen(self):
        self.root.title("Healthcare Supply Chain Simulation")

        # Hospital and supplier data
        self.hospitals = load_hospitals()
        self.suppliers = load_suppliers()

        # Labels to display hospital and supplier inventories
        self.hospital_labels = []
        self.supplier_labels = []

        # Create hospital inventory labels
        tk.Label(self.root, text="Hospital Inventory", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
        for idx, hospital in enumerate(self.hospitals):
            label = tk.Label(self.root, text=f"{hospital.name}: A = {hospital.inventory['A']}, B = {hospital.inventory['B']}")
            label.grid(row=idx + 1, column=0, padx=10, pady=5)
            self.hospital_labels.append([label])

        # Create supplier inventory labels
        tk.Label(self.root, text="Supplier Inventory", font=("Helvetica", 12)).grid(row=0, column=1, padx=10, pady=5)
        for idx, supplier in enumerate(self.suppliers):
            label = tk.Label(self.root, text=f"{supplier.name}: A = {supplier.inventory['A']}, B = {supplier.inventory['B']}")
            label.grid(row=idx + 1, column=1, padx=10, pady=5)
            self.supplier_labels.append([label])

        # Label for transfer messages
        self.transfer_message_label = tk.Label(self.root, text="", font=("Helvetica", 10), wraplength=400)
        self.transfer_message_label.grid(row=len(self.hospitals) + 2, column=0, columnspan=2, pady=5)

        # Simulate button
        simulate_button = tk.Button(self.root, text="Simulate Supply Chain", command=self.simulate_supply, font=("Helvetica", 12))
        simulate_button.grid(row=len(self.hospitals) + 3, column=0, columnspan=2, pady=20)

        # Instantiate logistics with update_transfer_message as a callback
        self.logistics = Logistics(update_callback=self.update_transfer_message)

    def update_transfer_message(self, message):
        self.transfer_message_label.config(text=message)

    def simulate_supply(self):
        ai_supply_decision(self.hospitals, self.suppliers, self.logistics)

        # Check if all hospitals have enough stock after the simulation
        insufficient_hospitals = check_hospitals_stock(self.hospitals)

        # Show result screen after simulation
        if insufficient_hospitals:
            self.show_insufficient_stock_screen(insufficient_hospitals)
        else:
            messagebox.showinfo("Simulation Complete", "All hospitals are sufficiently supplied.")

    def show_insufficient_stock_screen(self, insufficient_hospitals):
        insufficient_hospitals_text = "Some hospitals do not have enough stock for the following products:\n"
        for hospital, missing_products in insufficient_hospitals:
            insufficient_hospitals_text += f"\n{hospital.name} needs:\n"
            for product, amount in missing_products:
                insufficient_hospitals_text += f"- {product}: {amount} units\n"

        # Display message box for missing products
        messagebox.showwarning("Insufficient Stock", insufficient_hospitals_text)


# Load hospital data from CSV
def load_hospitals():
    hospitals = []
    with open(r'C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\Hospitals.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Adjusting column names to match your CSV file
            name = row['name']
            inventory = {
                'A': int(row['stock_A']),  # Using 'stock_A' from the CSV
                'B': int(row['stock_B'])   # Using 'stock_B' from the CSV
            }
            min_inventory = {
                'A': int(row['min_stock_A']),  # Using 'min_stock_A' from the CSV
                'B': int(row['min_stock_B'])   # Using 'min_stock_B' from the CSV
            }
            coordinates = row['coordinates']  # You can use this for future enhancements
            hospitals.append(Hospital(name, inventory, min_inventory, coordinates))
    return hospitals


# Load supplier data from CSV
def load_suppliers():
    suppliers = []
    with open(r'C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\Suppliers.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            inventory = {
                'A': int(row['stock_A']),  # Use 'stock_A' from the CSV
                'B': int(row['stock_B'])   # Use 'stock_B' from the CSV
            }
            suppliers.append(Supplier(name, inventory))
    return suppliers


class Hospital:
    def __init__(self, name, inventory, min_inventory, coordinates):
        self.name = name
        self.inventory = inventory
        self.min_inventory = min_inventory
        self.coordinates = coordinates  # Store the coordinates for future use

    def needs_supply(self):
        for product, amount in self.inventory.items():
            if amount < self.min_inventory.get(product, 0):
                return True
        return False

    def request_supply(self):
        needed_items = []
        for product, amount in self.inventory.items():
            if amount < self.min_inventory.get(product, 0):
                needed_items.append((product, self.min_inventory.get(product) - amount))
        return needed_items


class Supplier:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def can_supply(self, required_items):
        for product, amount in required_items:
            if self.inventory.get(product, 0) < amount:
                return False
        return True

    def supply(self, required_items):
        for product, amount in required_items:
            if self.inventory.get(product, 0) >= amount:
                self.inventory[product] -= amount


class Logistics:
    def __init__(self, update_callback):
        self.update_callback = update_callback  # Callback function to update GUI

    def transfer(self, from_entity, to_entity, product, amount):
        # Instead of printing, update the GUI
        transfer_message = f"Transferring {amount} of {product} from {from_entity} to {to_entity}."
        self.update_callback(transfer_message)


def ai_supply_decision(hospitals, suppliers, logistics):
    for hospital in hospitals:
        if hospital.needs_supply():
            required_items = hospital.request_supply()
            for supplier in suppliers:
                if supplier.can_supply(required_items):
                    for product, amount in required_items:
                        logistics.transfer(supplier.name, hospital.name, product, amount)
                        supplier.supply(required_items)
                    break


def check_hospitals_stock(hospitals):
    insufficient_hospitals = []
    for hospital in hospitals:
        missing_products = []
        for product, min_amount in hospital.min_inventory.items():
            if hospital.inventory.get(product, 0) < min_amount:
                missing_products.append((product, min_amount - hospital.inventory.get(product, 0)))
        
        if missing_products:
            insufficient_hospitals.append((hospital, missing_products))
    
    return insufficient_hospitals


# Main
def main():
    root = tk.Tk()

    # Create home screen
    home_screen = HomeScreen(root, switch_to_simulation_screen_callback=lambda: SupplyChainSimulation(root))

    root.mainloop()

if __name__ == "__main__":
    main()
