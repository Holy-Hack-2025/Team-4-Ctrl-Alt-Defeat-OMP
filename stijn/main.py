import pandas as pd
import matplotlib.pyplot as plt

# Laad de supply chain gegevens
df = pd.read_csv('C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\data.csv')

# Simuleer verstoring door de voorraad te verminderen
def simulate_disturbance(df, product, disturbance_factor):
    # Verminder de voorraad van een product door de verstoring
    df.loc[df['Product'] == product, 'Stock'] *= disturbance_factor
    print(f"Verstoring simulatie voor {product}: voorraad verminderd met factor {disturbance_factor}")
    return df

# Bereken de CO2-uitstoot door productie
def calculate_co2_emission(df):
    df['Total_CO2'] = df['CO2_emission'] * df['Stock']
    total_co2 = df['Total_CO2'].sum()
    print(f"Totaal CO2-uitstoot: {total_co2} eenheden")
    return df, total_co2

# Visualiseer de CO2-uitstoot voor de producten
def visualize_co2(df):
    plt.bar(df['Product'], df['Total_CO2'])
    plt.xlabel('Product')
    plt.ylabel('CO2-uitstoot')
    plt.title('CO2-uitstoot per product')
    plt.show()

# Start van het simulatieproces
print("Simulatie van de supply chain verstoringen")

# Simuleer verstoringen
df = simulate_disturbance(df, 'Laptop', 0.8)  # Verstoringsfactor = 80% van de voorraad
df = simulate_disturbance(df, 'Smartphone', 0.9)

# Bereken en toon CO2-uitstoot
df, total_co2 = calculate_co2_emission(df)

# Visualiseer de CO2-uitstoot
visualize_co2(df)
