import tkinter as tk
from home_screen import HomeScreen
import csv
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

        # Header for Problems Section
        self.problems_header = tk.Label(self.left_frame, text="Problems", font=("Helvetica", 14, "bold"))
        self.problems_header.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Header for Solutions Section
        self.solutions_header = tk.Label(self.right_frame, text="Solutions", font=("Helvetica", 14, "bold"))
        self.solutions_header.grid(row=0, column=0, padx=10, pady=5, sticky="w")

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
        """Show the message for insufficient stock in the left frame."""
        # Populate problems (left list)
        problems_text = "Some hospitals do not have enough stock:\n"
        problem_labels = []

        for hospital, missing_products in insufficient_hospitals:
            problems_text += f"\n{hospital.name} needs:\n"
            for product, amount in missing_products:
                problems_text += f"- {product}: {amount} units\n"
            problem_label = tk.Label(self.left_frame, text=problems_text, font=("Helvetica", 10), justify="left")
            problem_label.grid(row=len(problem_labels) + 1, column=0, padx=10, pady=5, sticky="w")
            problem_labels.append(problem_label)

        # Populate solutions (right list)
        solutions = resolve_shortages_with_distance(insufficient_hospitals, self.hospitals, self.suppliers)
        solutions_text = "Solutions:\n"
        solution_labels = []

        for solution in solutions:
            solutions_text += f"{solution}\n"
            solution_label = tk.Label(self.right_frame, text=solution, font=("Helvetica", 10), justify="left")
            solution_label.grid(row=len(solution_labels) + 1, column=0, padx=10, pady=5, sticky="w")
            solution_labels.append(solution_label)

        self.simulation_result_label.config(text=solutions_text, fg="green")

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

# Load hospitals
def load_hospitals(filename=r"C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\other_required_files\Hospitals.csv"):
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
def load_suppliers(filename=r"C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\other_required_files\Suppliers.csv"):
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

def resolve_shortages_with_distance(insufficient_hospitals, hospitals, suppliers):
    solutions = []

    for hospital, shortages in insufficient_hospitals:
        for product, shortage in shortages:
            # Blijf proberen totdat het tekort is opgelost
            while shortage > 0:
                # Probeer eerst de dichtstbijzijnde leveranciers
                possible_suppliers = [
                    (supplier, calculate_distance(hospital.coordinates, supplier.coordinates))
                    for supplier in suppliers if supplier.can_supply([(product, shortage)])
                ]
                possible_suppliers.sort(key=lambda x: x[1])  # Sorteer leveranciers op afstand

                # Test de leveranciers
                supplier_found = False
                for supplier, dist in possible_suppliers:
                    if supplier.can_supply([(product, shortage)]):
                        supplier.supply([(product, shortage)])
                        solutions.append(f"Supplied {shortage} units of {product} from {supplier.name} ({dist:.2f} km) to {hospital.name}")
                        shortage = 0  # Het tekort is opgelost
                        supplier_found = True
                        break  # Stop bij de eerste oplossing

                # Als we geen leverancier hebben gevonden, probeer andere ziekenhuizen
                if shortage > 0 and not supplier_found:
                    possible_donors = [
                        (donor_hospital, calculate_distance(hospital.coordinates, donor_hospital.coordinates))
                        for donor_hospital, _ in insufficient_hospitals if donor_hospital != hospital
                    ]
                    possible_donors.sort(key=lambda x: x[1])  # Sorteer donor ziekenhuizen op afstand

                    donor_found = False
                    for donor_hospital, dist in possible_donors:
                        available_stock = donor_hospital.inventory[product] - donor_hospital.min_inventory[product]
                        if available_stock >= shortage:
                            donor_hospital.inventory[product] -= shortage
                            hospital.inventory[product] += shortage
                            solutions.append(f"Transferred {shortage} units of {product} from {donor_hospital.name} ({dist:.2f} km) to {hospital.name}")
                            shortage = 0  # Het tekort is opgelost
                            donor_found = True
                            break  # Stop bij de eerste oplossing

                    # Als er nog steeds een tekort is, geef een foutmelding
                    if shortage > 0 and not donor_found:
                        solutions.append(f"Error: {hospital.name} still has a shortage of {shortage} units of {product}. No possible solution found.")
                        break  # Stop met proberen voor dit product

    return solutions
