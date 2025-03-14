import pandas as pd
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

# Laad de supply chain gegevens
def load_data():
    try:
        with open("C:\\creativity\\Team-4-Ctrl-Alt-Defeat-OMP\\stijn\\data.csv", "r") as file:
            return pd.read_csv(file)
    except FileNotFoundError:
        messagebox.showerror("Fout", "Bestand data.csv niet gevonden!")
        return None  # Voorkom een crash

# Zorg ervoor dat de applicatie correct afsluit
def exit_application():
    root.quit()
    root.destroy()
    os._exit(0)  # Kill alle processen volledig

# Functie die wordt aangeroepen als de gebruiker het kruisje rechtsboven klikt
def on_closing():
    exit_application()

# Simuleer verstoringen
def simulate_stock_disturbance(df, product, factor):
    df.loc[df['Product'] == product, 'Stock'] *= factor
    return df

def simulate_cost_disturbance(df, product, factor):
    df.loc[df['Product'] == product, 'Productie_cost'] *= factor
    return df

def simulate_co2_disturbance(df, product, factor):
    df.loc[df['Product'] == product, 'CO2_emission'] *= factor
    return df

# Bereken CO2-uitstoot
def calculate_co2_emission(df):
    df['Total_CO2'] = df['CO2_emission'] * df['Stock']
    total_co2 = df['Total_CO2'].sum()
    return df, total_co2

# Visualiseer de trends
def visualize_trends(df, window):
    fig, ax = plt.subplots()
    ax.plot(df['Product'], df['Stock'], label='Stock')
    ax.plot(df['Product'], df['Productie_cost'], label='Kosten')
    ax.plot(df['Product'], df['CO2_emission'], label='CO2-uitstoot')

    ax.set_xlabel('Product')
    ax.set_ylabel('Waarde')
    ax.set_title('Gevolgen van de verstoring')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Pas verstoring toe en ga naar volgende stap
def apply_changes(window, step, product, factor, change_type):
    global df  
    if df is None:
        return

    try:
        if change_type == 'Voorraad':
            df = simulate_stock_disturbance(df, product, factor)
        elif change_type == 'Kosten':
            df = simulate_cost_disturbance(df, product, factor)
        elif change_type == 'CO2':
            df = simulate_co2_disturbance(df, product, factor)
        else:
            raise ValueError("Ongeldige keuze voor veranderingstype")

        df, total_co2 = calculate_co2_emission(df)

        if step == 2:
            window.destroy()
            step3_window()

    except Exception as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden: {e}")

# Stap 1 - Kies verstoring
def step1_window():
    global df, root
    df = load_data()  
    if df is None:
        return
    
    root = tk.Tk()
    root.title("Stap 1: Kies wat er fout gaat")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    tk.Label(root, text="Kies wat er fout gaat:").pack()

    change_var = tk.StringVar()
    change_var.set("Voorraad") 
    tk.Radiobutton(root, text="Voorraad", variable=change_var, value="Voorraad").pack()
    tk.Radiobutton(root, text="Kosten", variable=change_var, value="Kosten").pack()
    tk.Radiobutton(root, text="CO2-uitstoot", variable=change_var, value="CO2").pack()

    def next_step():
        change_type = change_var.get()
        root.destroy()
        step2_window(change_type)

    tk.Button(root, text="Volgende", command=next_step).pack()
    root.mainloop()

# Stap 2 - Berekening uitvoeren
def step2_window(change_type):
    window = tk.Tk()
    window.title(f"Stap 2: {change_type} berekening")
    window.protocol("WM_DELETE_WINDOW", on_closing)

    tk.Label(window, text=f"Voer product en verstoringsfactor in voor {change_type}:").pack()

    tk.Label(window, text="Kies een product:").pack()
    product_entry = tk.Entry(window)
    product_entry.pack()

    tk.Label(window, text="Verstoringsfactor (bijv. 0.8 voor 80%):").pack()
    factor_entry = tk.Entry(window)
    factor_entry.pack()

    def next_step():
        product = product_entry.get()
        try:
            factor = float(factor_entry.get())
            apply_changes(window, 2, product, factor, change_type)
        except ValueError:
            messagebox.showerror("Fout", "Voer een geldig getal in voor de verstoringsfactor.")

    tk.Button(window, text="Toepassen", command=next_step).pack()
    window.mainloop()

# Stap 3 - Gevolgen tonen
def step3_window():
    window = tk.Tk()
    window.title("Stap 3: Gevolgen van de verstoring")
    window.protocol("WM_DELETE_WINDOW", on_closing)

    tk.Label(window, text="Hier is de trend van de gevolgen van de verstoring:").pack()
    visualize_trends(df, window)

    tk.Button(window, text="Begin opnieuw", command=lambda: restart_simulation(window)).pack()
    window.mainloop()

# Herstart de simulatie
def restart_simulation(window):
    global df
    df = None
    window.quit()
    window.destroy()
    step1_window()

# Start de simulatie
step1_window()
