import tkinter as tk
from home_screen import HomeScreen
import csv
from itertools import permutations, combinations
from math import radians, sin, cos, sqrt, atan2

class SupplyChainSimulation:
    def __init__(self, frame):
        self.frame = frame
        self.hospitals = load_hospitals()
        self.suppliers = load_suppliers()
        self.simulation_result_label = None  
        self.return_button = None  
        self.solutions_label = None

    def create_simulation_screen(self):
        """Create the simulation screen content."""
        self.simulation_frame = tk.Frame(self.frame)
        self.simulation_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid to make sure it fills the whole window
        self.simulation_frame.grid_rowconfigure(0, weight=0)  # Title row, fixed size
        self.simulation_frame.grid_rowconfigure(1, weight=0)  # Hospital selector row, fixed size
        self.simulation_frame.grid_rowconfigure(2, weight=1)  # Middle row for problems and solutions, expandable
        self.simulation_frame.grid_rowconfigure(3, weight=0)  # Simulate button row, fixed size
        self.simulation_frame.grid_rowconfigure(4, weight=0)  # Return button row, fixed size

        self.simulation_frame.grid_columnconfigure(0, weight=1)  # Left column (problems), expandable
        self.simulation_frame.grid_columnconfigure(1, weight=1)  # Middle column (simulator button), expandable
        self.simulation_frame.grid_columnconfigure(2, weight=1)  # Right column (solutions), expandable

        # Title Label
        title_label = tk.Label(self.simulation_frame, text="Supply Chain Simulation", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        # Create a hospital selector dropdown
        self.hospital_selector_label = tk.Label(self.simulation_frame, text="Select Hospital:", font=("Helvetica", 12))
        self.hospital_selector_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Populate dropdown with hospital names
        self.hospital_selector = tk.StringVar()
        hospital_names = [hospital.name for hospital in self.hospitals]
        self.hospital_selector.set(hospital_names[0])  # Set default to the first hospital
        hospital_dropdown = tk.OptionMenu(self.simulation_frame, self.hospital_selector, *hospital_names)
        hospital_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Left and Right frames for the problems and solutions with borders
        self.left_frame = tk.Frame(self.simulation_frame, relief="solid", bd=2)  # Add border
        self.left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.right_frame = tk.Frame(self.simulation_frame, relief="solid", bd=2)  # Add border
        self.right_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        self.middle_frame = tk.Frame(self.simulation_frame)  # Middle frame for the simulation button
        self.middle_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    
        # Simulate supply chain button (moved to middle bottom)
        simulate_button = tk.Button(self.simulation_frame, text="Simulate Supply Chain", command=self.simulate_supply, font=("Helvetica", 12))
        simulate_button.grid(row=3, column=1, pady=20, sticky="nsew")

        # Return Button in the center, below simulate button
        self.return_button = None
        self.show_return_button()  # Show the return button

        # Label for simulation result (for problems)
        self.problems_label = tk.Label(self.left_frame, text="Problems:", font=("Helvetica", 12, "bold"))
        self.problems_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Label for solutions (on the right)
        self.solutions_label = tk.Label(self.right_frame, text="Solutions:", font=("Helvetica", 12, "bold"))
        self.solutions_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")


    def simulate_supply(self):
        """Check hospital stock and simulate supply chain."""
        insufficient_hospitals = check_hospitals_stock(self.hospitals)

        # Clear previous labels in the left and right frames
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        if insufficient_hospitals:
            self.show_insufficient_stock_screen(insufficient_hospitals)
        else:
            self.simulation_result_label.config(text="All hospitals are sufficiently supplied.", fg="green")

        self.show_return_button()

    def show_insufficient_stock_screen(self, insufficient_hospitals):
        """Show the message for insufficient stock in the left and right frames."""
        # Clear any existing labels in the problems and solutions sections
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Header for Problems Section
        self.problems_header = tk.Label(self.left_frame, text="Problems:", font=("Helvetica", 12, "bold"))
        self.problems_header.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Header for Solutions Section
        self.solutions_header = tk.Label(self.right_frame, text="Solutions:", font=("Helvetica", 12, "bold"))
        self.solutions_header.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Populate problems (left list)
        problem_labels = []
        row = 1  # Start adding problems below the header
        for hospital, missing_products in insufficient_hospitals:
            problem_text = f"{hospital.name} needs:\n"
            for product, amount in missing_products:
                problem_text += f"- {product}: {amount} units\n"
            problem_label = tk.Label(self.left_frame, text=problem_text, font=("Helvetica", 10), justify="left")
            problem_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            row += 1  # Increment row for the next problem
            problem_labels.append(problem_label)

        # Populate solutions (right list)
        solutions = resolve_shortages_with_minimum_distance(insufficient_hospitals, self.hospitals, self.suppliers)
        solutions_text = "Solutions:\n"
        solution_labels = []
        row = 1  # Start adding solutions below the header
        for solution in solutions:
            solutions_text += f"{solution}\n"
            solution_label = tk.Label(self.right_frame, text=solution, font=("Helvetica", 10), justify="left")
            solution_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            row += 1  # Increment row for the next solution
            solution_labels.append(solution_label)

        self.simulation_result_label = tk.Label(self.right_frame, text=solutions_text, font=("Helvetica", 10, "bold"), fg="green", justify="left")
        self.simulation_result_label.grid(row=row+1, column=0, padx=10, pady=5, sticky="w")


    def show_return_button(self):
        """Show the return button to go back to the home screen."""
        if not self.return_button:
            self.return_button = tk.Button(self.simulation_frame, text="Return to Home", command=self.return_to_home, font=("Helvetica", 12))
            self.return_button.grid(row=4, column=1, pady=20, sticky="nsew")

    def return_to_home(self):
        """Return to the home screen and refresh the simulation content."""
        self.hospitals = load_hospitals()  # Reload hospital data
        self.suppliers = load_suppliers()
        self.simulation_result_label = None
        self.return_button = None
        self.solutions_label = None  # Remove solutions when going back
        self.simulation_frame.destroy()
        home_screen = HomeScreen(self.frame, self.create_simulation_screen)
        home_screen.create_home_screen()



class Hospital:
    def __init__(self, name, inventory, min_inventory, coordinates):
        self.name = name
        self.inventory = inventory
        self.min_inventory = min_inventory 
        self.coordinates =  coordinates

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
    
    def get_available_stock(self, product):
        """Retourneer de beschikbare voorraad voor een bepaald product."""
        return self.inventory.get(product, 0)

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
                    min_inventory={"A": int(row["min_stock_A"]), "B": int(row["min_stock_B"])},
                    coordinates=tuple(map(float, row["coordinates"].split(", ")))
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

def generate_combinations(all_sources, remaining_shortage):
    """Generate all possible combinations of sources that could potentially fulfill the shortage"""
    combinations_list = []
    
    # Check combinations that may fulfill the shortage
    for r in range(1, len(all_sources) + 1):  # Try combinations from 1 to the full set
        for comb in combinations(all_sources, r):
            selected_combination = []
            temp_shortage = remaining_shortage
            for source, dist, stock in comb:
                supply_amount = min(stock, temp_shortage)
                selected_combination.append((source, dist, supply_amount))
                temp_shortage -= supply_amount
                if temp_shortage <= 0:
                    break
            if temp_shortage <= 0:
                combinations_list.append(selected_combination)
    
    return combinations_list


def calculate_distance(coord1, coord2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radius of the Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Distance in km
    return distance

def resolve_shortages_with_minimum_distance(insufficient_hospitals, hospitals, suppliers):
    solutions = []
    best_solution = None
    best_distance_per_unit = float('inf')  # Start with an infinitely large distance per unit

    for hospital, shortages in insufficient_hospitals:
        for product, shortage in shortages:
            remaining_shortage = shortage
            all_sources = []

            # Combine hospitals and suppliers into one list of sources
            for source in hospitals + suppliers:
                if source != hospital:  # Exclude the hospital itself
                    available_stock = source.inventory.get(product, 0)
                    if available_stock > 0:
                        distance = calculate_distance(hospital.coordinates, source.coordinates)
                        all_sources.append((source, distance, available_stock))

            # Generate all combinations of sources that can satisfy the shortage
            all_combinations = generate_combinations(all_sources, remaining_shortage)

            # Check each combination
            for combination in all_combinations:
                total_distance = 0
                total_units = 0
                for source, dist, stock in combination:
                    supply_amount = min(stock, remaining_shortage)
                    total_distance += dist * supply_amount
                    total_units += supply_amount
                    remaining_shortage -= supply_amount

                # If the combination satisfies the shortage, calculate distance per unit
                if remaining_shortage <= 0:
                    distance_per_unit = total_distance / total_units if total_units > 0 else float('inf')

                    if distance_per_unit < best_distance_per_unit:
                        best_distance_per_unit = distance_per_unit
                        best_solution = combination

            # Record the best solution
            if best_solution:
                solutions.append(f"Best solution for {hospital.name} shortage of {product}:")
                for source, dist, stock in best_solution:
                    solutions.append(f"  - {source.name} supplied {min(stock, shortage)} units at {dist:.2f} km")
                solutions.append(f"Distance per unit: {best_distance_per_unit:.2f} km per unit")

    return solutions