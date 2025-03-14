import tkinter as tk
from grafs import GraphGenerator  # Zorg ervoor dat deze import goed is
from tkinter import messagebox
from home_screen import HomeScreen
import csv
from itertools import permutations, combinations
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SupplyChainSimulation:
    def __init__(self, frame):
        self.frame = frame
        self.hospitals = load_hospitals()  # Assuming this loads the hospitals
        self.suppliers = load_suppliers()  # Assuming this loads the suppliers
        self.simulation_result_label = None
        self.return_button = None
        self.solutions_label = None
        self.graph_frame = None  # To hold the graph

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
        hospital_dropdown = tk.OptionMenu(self.simulation_frame, self.hospital_selector, *hospital_names, command=self.update_graph)
        hospital_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Left and Right frames for the problems and solutions with borders
        self.left_frame = tk.Frame(self.simulation_frame, relief="solid", bd=2)  # Add border
        self.left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.right_frame = tk.Frame(self.simulation_frame, relief="solid", bd=2)  # Add border
        self.right_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        self.middle_frame = tk.Frame(self.simulation_frame)  # Middle frame for the simulation button
        self.middle_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Create a frame for the hospital graphs (between left and right)
        self.graph_frame = tk.Frame(self.simulation_frame)
        self.graph_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

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

        self.frame.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        """Handle the window close event to cleanly exit the program."""
        print("Closing the application...")
        # Here you can add additional cleanup steps if needed
        self.frame.quit()  # Close the tkinter window gracefully
        self.frame.destroy()

    def update_graph(self, selected_hospital_name):
        """Update and show the graph for the selected hospital."""
        # Find the selected hospital object
        selected_hospital = next(hospital for hospital in self.hospitals if hospital.name == selected_hospital_name)

        # Clear the previous graph in the graph_frame
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Generate and display the graph for the selected hospital
        self.display_graph(selected_hospital)

    def display_graph(self, hospital):
        """Create and display a graph for the selected hospital."""
        # Check if there is already an existing graph and clear it before creating a new one
        fig, ax = plt.subplots(figsize=(5, 3))

        # Example: Bar chart of the hospital's stock (You can adjust this part to your product data)
        products = list(hospital.inventory.keys())  # Dynamically fetch product names from inventory
        stocks = [hospital.inventory.get(product, 0) for product in products]
        min_stocks = [hospital.min_inventory.get(product, 0) for product in products]  # Get min inventory

        # Set the width for the bars
        bar_width = 0.35

        # Create the bars for the stock level and min stock
        bars1 = ax.bar([p - bar_width / 2 for p in range(len(products))], stocks, bar_width, label="Stock", color='lightblue')
        bars2 = ax.bar([p + bar_width / 2 for p in range(len(products))], min_stocks, bar_width, label="Min Stock", color='orange')

        # Set titles and labels
        ax.set_title(f"Inventory of {hospital.name}")
        ax.set_xlabel('Products')
        ax.set_ylabel('Stock Level')

        # Set product names on x-axis
        ax.set_xticks(range(len(products)))
        ax.set_xticklabels(products)

        # Add the legend
        ax.legend()

        # Render the graph into the tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()

        # Properly pack the canvas into the grid
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

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

    def show_return_button(self):
        """Show the return button."""
        self.return_button = tk.Button(self.simulation_frame, text="Return", command=self.return_to_main_screen, font=("Helvetica", 12))
        self.return_button.grid(row=4, column=1, pady=10, sticky="nsew")

    def return_to_main_screen(self):
        """Return to the main screen."""
        print("Returning to the main screen...")
        # Implement the logic to go back to the main screen here.
        pass

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
        row = 1  # Start adding problems below the header
        for hospital, missing_products in insufficient_hospitals:
            problem_text = f"{hospital.name} needs:\n"
            for product, amount in missing_products:
                problem_text += f"- {product}: {amount} units\n"
            problem_label = tk.Label(self.left_frame, text=problem_text, font=("Helvetica", 10), justify="left")
            problem_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            row += 1  # Increment row for the next problem

        # Create min_inventory_levels dictionary
        min_inventory_levels = {hospital.name: hospital.min_inventory for hospital in self.hospitals}

        # Populate solutions (right list)
        solutions = resolve_shortages_with_minimum_distance(insufficient_hospitals, self.hospitals, self.suppliers, min_inventory_levels)
        row = 1  # Start adding solutions below the header
        for solution in solutions:
            solution_label = tk.Label(self.right_frame, text=solution, font=("Helvetica", 10), justify="left")
            solution_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            row += 1  # Increment row for the next solution

        self.simulation_result_label = tk.Label(self.right_frame, text="See solutions above.", font=("Helvetica", 10, "bold"), fg="green", justify="left")
        self.simulation_result_label.grid(row=row + 1, column=0, padx=10, pady=5, sticky="w")

    def close_window(self):
        """Afsluiten van het venster en stoppen van de applicatie."""
        print("Afsluiten van de applicatie...")
        self.frame.quit()  # Dit zorgt ervoor dat de tkinter loop stopt
        self.frame.destroy()  # Dit sluit het venster volledig af
        exit()  # Dit zorgt ervoor dat ook de terminal wordt afgesloten

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
def load_hospitals(filename=r"C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\other_required_files\Hospitals.csv"):
    """Load hospital data from a CSV file with support for multiple products dynamically."""
    hospitals = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Dynamisch de producten bepalen op basis van kolomnamen
                product_keys = [key for key in row.keys() if key.startswith("stock_")]
                min_product_keys = [key.replace("stock_", "min_stock_") for key in product_keys]

                # Inventaris en minimum voorraad dynamisch vullen
                inventory = {key.replace("stock_", ""): int(row[key]) for key in product_keys}
                min_inventory = {key.replace("min_stock_", ""): int(row[key]) for key in min_product_keys}

                hospitals.append(Hospital(
                    name=row["name"],
                    inventory=inventory,
                    min_inventory=min_inventory,
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
                    inventory={
                        "A": int(row["stock_A"]),
                        "B": int(row["stock_B"]),
                        "C": int(row["stock_C"]),
                        "D": int(row["stock_D"]),
                        "E": int(row["stock_E"])  # Add product E to inventory
                    },
                    production={
                        "A": int(row["production_A"]),
                        "B": int(row["production_B"]),
                        "C": int(row["production_C"]),
                        "D": int(row["production_D"]),
                        "E": int(row["production_E"])  # Add product E to production
                    },
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

def resolve_shortages_with_minimum_distance(insufficient_hospitals, hospitals, suppliers, min_inventory_levels):
    solutions = []

    for hospital, shortages in insufficient_hospitals:
        for product, shortage in shortages:
            remaining_shortage = shortage
            used_sources = []

            # Combineer alle mogelijke leveranciers (ziekenhuizen + leveranciers)
            all_sources = []
            for source in hospitals + suppliers:
                if source != hospital:  # Voorkom dat een ziekenhuis zichzelf bevoorraden kan
                    available_stock = source.inventory.get(product, 0)
                    min_stock = min_inventory_levels.get(source.name, {}).get(product, 0)  # Haal de minimumvoorraad op
                    
                    if available_stock > min_stock:  # Alleen leveren als er boven de minimumvoorraad blijft
                        max_deliverable = available_stock - min_stock
                        distance = calculate_distance(hospital.coordinates, source.coordinates)
                        all_sources.append((source, distance, max_deliverable))

            # Sorteer bronnen op efficiëntie (afstand per eenheid)
            all_sources.sort(key=lambda x: x[1] / x[2])  # Distance per unit

            # Gebruik bronnen totdat het tekort is opgelost
            total_distance = 0
            for source, dist, max_stock in all_sources:
                if remaining_shortage <= 0:
                    break  # Stop als het tekort is opgelost

                supply_amount = min(max_stock, remaining_shortage)

                # Pas voorraad aan
                source.inventory[product] -= supply_amount
                hospital.inventory[product] += supply_amount

                total_distance += dist * supply_amount
                remaining_shortage -= supply_amount
                used_sources.append((source, supply_amount, dist))

            # Maak een oplossingstekst
            if remaining_shortage > 0:
                solutions.append(f"⚠️ {hospital.name} still has a shortage of {remaining_shortage} units of {product}!")

            else:
                solutions.append(f"✅ {hospital.name} shortage of {product} resolved!")
                for source, amount, dist in used_sources:
                    solutions.append(f"  - {source.name} supplied {amount} units at {dist:.2f} km")

                avg_distance_per_unit = total_distance / shortage if shortage > 0 else 0
                solutions.append(f"  ➡️ Average distance per unit: {avg_distance_per_unit:.2f} km/unit")

    return solutions
