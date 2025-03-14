import tkinter as tk
from home_screen import HomeScreen
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SupplyChainSimulation:
    def __init__(self, frame):
        self.frame = frame
        self.hospitals = load_hospitals()
        self.suppliers = load_suppliers()
        self.simulation_result_label = None  
        self.return_button = None  
        self.canvas = None  # To store the Matplotlib canvas
        self.selected_hospital = tk.StringVar()

    def create_simulation_screen(self):
        """Create the simulation screen content."""
        self.simulation_frame = tk.Frame(self.frame)
        self.simulation_frame.grid(row=0, column=0, sticky="nsew")

        # Title Label
        title_label = tk.Label(self.simulation_frame, text="Supply Chain Simulation", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Simulate button
        simulate_button = tk.Button(self.simulation_frame, text="Simulate Supply Chain", command=self.simulate_supply, font=("Helvetica", 12))
        simulate_button.grid(row=1, column=0, columnspan=2, pady=20)

        # Dropdown menu for hospital selection
        hospital_names = [h.name for h in self.hospitals]
        self.selected_hospital.set(hospital_names[0])
        hospital_dropdown = tk.OptionMenu(self.simulation_frame, self.selected_hospital, *hospital_names, command=self.display_stock_graph)
        hospital_dropdown.grid(row=2, column=0, columnspan=2, pady=10)

        # Label for simulation result
        self.simulation_result_label = tk.Label(self.simulation_frame, text="", font=("Helvetica", 12), fg="red", justify="left", wraplength=500)
        self.simulation_result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Initial Graph Display
        self.display_stock_graph()

    def simulate_supply(self):
        """Check hospital stock without transferring supplies."""
        insufficient_hospitals = check_hospitals_stock(self.hospitals)

        if insufficient_hospitals:
            self.show_insufficient_stock_screen(insufficient_hospitals)
        else:
            self.simulation_result_label.config(text="All hospitals are sufficiently supplied.", fg="green")

        self.display_stock_graph()
        self.show_return_button()

    def display_stock_graph(self, *args):
        """Displays a bar chart for the selected hospital's stock."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        selected_hospital = next(h for h in self.hospitals if h.name == self.selected_hospital.get())

        fig, ax = plt.subplots(figsize=(3, 2))
        stock_items = list(selected_hospital.inventory.keys())
        stock_values = [selected_hospital.inventory[item] for item in stock_items]
        min_stock_values = [selected_hospital.min_inventory[item] for item in stock_items]

        x = range(len(stock_items))
        ax.bar(x, stock_values, label="Current Stock", color='blue', alpha=0.7)
        ax.plot(x, min_stock_values, marker='o', linestyle='--', color='red', label="Min Required Stock")
        ax.set_xticks(x)
        ax.set_xticklabels(stock_items, rotation=45, ha='right')
        ax.set_ylabel("Stock Levels")
        ax.set_title(f"Stock Inventory: {selected_hospital.name}")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.simulation_frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=10)
        self.canvas.draw()

    def show_insufficient_stock_screen(self, insufficient_hospitals):
        """Show the message for insufficient stock in the same window."""
        insufficient_hospitals_text = "Some hospitals do not have enough stock:\n"
        for hospital, missing_products in insufficient_hospitals:
            insufficient_hospitals_text += f"\n{hospital.name} needs:\n"
            for product, amount in missing_products:
                insufficient_hospitals_text += f"- {product}: {amount} units\n"
        
        self.simulation_result_label.config(text=insufficient_hospitals_text, fg="red")

    def show_return_button(self):
        """Show the return button to go back to the home screen."""
        if not self.return_button:
            self.return_button = tk.Button(self.simulation_frame, text="Return to Home", command=self.return_to_home, font=("Helvetica", 12))
            self.return_button.grid(row=5, column=0, columnspan=2, pady=20)

    def return_to_home(self):
        """Return to the home screen and refresh the simulation content."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.simulation_result_label = None
        self.return_button = None
        self.simulation_frame.destroy()
        home_screen = HomeScreen(self.frame, self.create_simulation_screen)
        home_screen.create_home_screen()

# Rest of the code remains unchanged



class Hospital:
    def __init__(self, name, inventory, min_inventory):
        self.name = name
        self.inventory = inventory
        self.min_inventory = min_inventory  

    def needs_supply(self):
        return any(self.inventory[product] < self.min_inventory[product] for product in self.inventory)

    def request_supply(self):
        return [
            (product, self.min_inventory[product] - qty) 
            for product, qty in self.inventory.items() 
            if qty < self.min_inventory[product]
        ]

class Supplier:
    def __init__(self, name, inventory, production, coordinates):
        self.name = name
        self.inventory = inventory
        self.production = production
        self.coordinates = coordinates  

    def can_supply(self, required_items):
        return all(self.inventory.get(product, 0) >= amount for product, amount in required_items)

    def supply(self, required_items):
        for product, amount in required_items:
            if self.inventory.get(product, 0) >= amount:
                self.inventory[product] -= amount

# Load hospitals
def load_hospitals(filename=r"C:\Users\HC\Documents\own\Holy_Hack\Team-4-Ctrl-Alt-Defeat-OMP\henry\other_required_files\Hospitals.csv"):
    """Load hospital data from a CSV file."""
    hospitals = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                hospitals.append(Hospital(
                    name=row["name"],
                    inventory={"A": int(row["stock_A"]), "B": int(row["stock_B"])},
                    min_inventory={"A": int(row["min_stock_A"]), "B": int(row["min_stock_B"])}
                ))
        print(f"Loaded {len(hospitals)} hospitals successfully.")  
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return hospitals

# Load suppliers
def load_suppliers(filename=r"C:\Users\HC\Documents\own\Holy_Hack\Team-4-Ctrl-Alt-Defeat-OMP\henry\other_required_files\Suppliers.csv"):
    """Load supplier data from a CSV file."""
    suppliers = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                suppliers.append(Supplier(
                    name=row["name"],
                    inventory={"A": int(row["stock_A"]), "B": int(row["stock_B"])},
                    production={"A": int(row["production_A"]), "B": int(row["production_B"])},
                    coordinates=tuple(map(float, row["coordinates"].split(", "))) 
                ))
        print(f"Loaded {len(suppliers)} suppliers successfully.")  
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return suppliers

# Check hospital stock levels
def check_hospitals_stock(hospitals):
    insufficient_hospitals = []
    for hospital in hospitals:
        print(f"Checking {hospital.name}: Inventory {hospital.inventory}, Min {hospital.min_inventory}")
        missing_products = [
            (product, hospital.min_inventory[product] - qty) 
            for product, qty in hospital.inventory.items() 
            if qty < hospital.min_inventory[product]
        ]
        if missing_products:
            insufficient_hospitals.append((hospital, missing_products))
    return insufficient_hospitals
