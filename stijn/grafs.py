import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphGenerator:
    def __init__(self, hospital):
        self.hospital = hospital

    def create_graph_for_hospital(self):
        """Maak een grafiek voor het geselecteerde ziekenhuis."""
        # Dynamisch de lijst van producten halen uit de voorraad van het ziekenhuis
        products = list(self.hospital.inventory.keys())  # Dit haalt de productnamen op
        inventory = [self.hospital.inventory[product] for product in products]
        min_inventory = [self.hospital.min_inventory[product] for product in products]

        fig, ax = plt.subplots(figsize=(8, 6))  # Grootte van de grafiek
        bars = ax.bar(products, inventory, label="Stock", color='lightblue')

        # Kleine balkjes voor de minimum voorraad naast de voorraadbalken
        min_bars = ax.bar([product + '_min' for product in products], min_inventory, width=0.3, label="Min Stock", color='red')


        # Verplaats de minimale voorraad balkjes naar de rechterkant van de hoofdvoorraad balken
        for i, rect in enumerate(min_bars):
            rect.set_x(bars[i].get_x() + bars[i].get_width())

        return fig

    def add_graph_to_canvas(self, figure, graph_frame):
        """Voeg een grafiek toe aan de canvas."""
        canvas = FigureCanvasTkAgg(figure, graph_frame)
        canvas.get_tk_widget().grid(row=graph_frame.grid_size()[1], column=0, pady=10)
        canvas.draw()

    def show_graph(self, graph_frame):
        """Toon de grafieken van het geselecteerde ziekenhuis."""
        # Maak grafiek
        fig = self.create_graph_for_hospital()

        # Voeg de grafiek toe aan de frame
        self.add_graph_to_canvas(fig, graph_frame)

        return fig