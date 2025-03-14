import tkinter as tk
from home_screen import HomeScreen

class SupplyChainSimulation:
    def __init__(self, frame):
        self.frame = frame
        self.hospitals = load_hospitals()
        self.suppliers = load_suppliers()
        self.simulation_result_label = None  # Label to show the result inside the window
        self.return_button = None  # Button to return after simulation

    def create_simulation_screen(self):
        """Create the simulation screen content."""
        self.simulation_frame = tk.Frame(self.frame)
        self.simulation_frame.grid(row=0, column=0, sticky="nsew")

        # Create the centered label for the title
        title_label = tk.Label(self.simulation_frame, text="Supply Chain Simulation", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Labels for hospitals and suppliers
        self.hospital_labels = []
        self.supplier_labels = []

        # Create hospital inventory labels
        tk.Label(self.simulation_frame, text="Hospital Inventory", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
        for idx, hospital in enumerate(self.hospitals):
            label = tk.Label(self.simulation_frame, text=f"{hospital.name}: A = {hospital.inventory['A']}, B = {hospital.inventory['B']}")
            label.grid(row=idx + 2, column=0, padx=10, pady=5)
            self.hospital_labels.append([label])

        # Create supplier inventory labels
        tk.Label(self.simulation_frame, text="Supplier Inventory", font=("Helvetica", 12)).grid(row=1, column=1, padx=10, pady=5)
        for idx, supplier in enumerate(self.suppliers):
            label = tk.Label(self.simulation_frame, text=f"{supplier.name}: A = {supplier.inventory['A']}, B = {supplier.inventory['B']}")
            label.grid(row=idx + 2, column=1, padx=10, pady=5)
            self.supplier_labels.append([label])

        # Simulate button and other widgets
        simulate_button = tk.Button(self.simulation_frame, text="Simulate Supply Chain", command=self.simulate_supply, font=("Helvetica", 12))
        simulate_button.grid(row=len(self.hospitals) + 3, column=0, columnspan=2, pady=20)

        # Add a label for displaying simulation result in the same window
        self.simulation_result_label = tk.Label(self.simulation_frame, text="", font=("Helvetica", 12), fg="red", justify="left", wraplength=500)
        self.simulation_result_label.grid(row=len(self.hospitals) + 4, column=0, columnspan=2, padx=10, pady=10)

    def destroy_simulation_screen(self):
        """Clear the simulation content."""
        if hasattr(self, 'simulation_frame'):
            self.simulation_frame.destroy()
            self.simulation_frame = None

    def simulate_supply(self):
        """Simulate the supply chain process."""
        ai_supply_decision(self.hospitals, self.suppliers)
        insufficient_hospitals = check_hospitals_stock(self.hospitals)

        if insufficient_hospitals:
            self.show_insufficient_stock_screen(insufficient_hospitals)
        else:
            self.simulation_result_label.config(text="All hospitals are sufficiently supplied.", fg="green")

        # After simulation, show the return button
        self.show_return_button()

    def show_insufficient_stock_screen(self, insufficient_hospitals):
        """Show the message for insufficient stock in the same window."""
        insufficient_hospitals_text = "Some hospitals do not have enough stock for the following products:\n"
        for hospital, missing_products in insufficient_hospitals:
            insufficient_hospitals_text += f"\n{hospital.name} needs:\n"
            for product, amount in missing_products:
                insufficient_hospitals_text += f"- {product}: {amount} units\n"
        
        # Update the label in the same window
        self.simulation_result_label.config(text=insufficient_hospitals_text, fg="red")
        self.simulation_result_label.grid(row=len(self.hospitals) + 4, column=0, columnspan=2, padx=10, pady=10)

        # After simulation, show the return button
        self.show_return_button()

    def show_return_button(self):
        """Show the return button to go back to the home screen."""
        if not self.return_button:
            self.return_button = tk.Button(self.simulation_frame, text="Return to Home", command=self.return_to_home, font=("Helvetica", 12))
            self.return_button.grid(row=len(self.hospitals) + 5, column=0, columnspan=2, pady=20)

    def return_to_home(self):
        """Return to the home screen and refresh the simulation content."""
        self.simulation_result_label = None
        self.return_button = None
        self.simulation_frame.destroy()
        # Create an instance of HomeScreen and show it
        home_screen = HomeScreen(self.frame, self.create_simulation_screen)  # Pass the callback function to HomeScreen
        home_screen.create_home_screen()

# Loading data
def load_hospitals():
    # Example loading method for hospitals
    return [Hospital('Hospital A', {'A': 50, 'B': 20}), Hospital('Hospital B', {'A': 0, 'B': 100})]

def load_suppliers():
    # Example loading method for suppliers
    return [Supplier('Supplier A', {'A': 100, 'B': 100}), Supplier('Supplier B', {'A': 50, 'B': 50})]

# Models for Hospital and Supplier
class Hospital:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def needs_supply(self):
        return any(value < 10 for value in self.inventory.values())

    def request_supply(self):
        return [(product, 10 - qty) for product, qty in self.inventory.items() if qty < 10]

class Supplier:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def can_supply(self, required_items):
        return all(self.inventory.get(product, 0) >= amount for product, amount in required_items)

    def supply(self, required_items):
        for product, amount in required_items:
            if self.inventory.get(product, 0) >= amount:
                self.inventory[product] -= amount

def ai_supply_decision(hospitals, suppliers):
    for hospital in hospitals:
        if hospital.needs_supply():
            required_items = hospital.request_supply()
            for supplier in suppliers:
                if supplier.can_supply(required_items):
                    supplier.supply(required_items)
                    for product, amount in required_items:
                        hospital.inventory[product] += amount
                    break

def check_hospitals_stock(hospitals):
    insufficient_hospitals = []
    for hospital in hospitals:
        missing_products = [(product, 10 - qty) for product, qty in hospital.inventory.items() if qty < 10]
        if missing_products:
            insufficient_hospitals.append((hospital, missing_products))
    return insufficient_hospitals
