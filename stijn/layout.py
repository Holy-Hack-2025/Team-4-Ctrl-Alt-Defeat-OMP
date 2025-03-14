import tkinter as tk
from home_screen import HomeScreen
from supply_chain_simulation import SupplyChainSimulation

class Layout:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")  # Make the window larger (800x600)
        
        # Initialize frames for home and simulation
        self.home_screen = HomeScreen(self.root, self.show_simulation_content)
        self.simulation_screen = SupplyChainSimulation(self.root)

    def show_home_content(self):
        self.home_screen.create_home_screen()

    def show_simulation_content(self):
        # Clear home screen and show the simulation content
        for widget in self.root.winfo_children():
            widget.destroy()  # Remove all widgets from the window
        self.simulation_screen.create_simulation_screen()  # Now show the simulation content