import heapq
from geopy.distance import geodesic

# Step 1: Define the graph
class Graph:
    def __init__(self):
        self.nodes = {}  # Stores nodes (hospitals and suppliers)
        self.edges = {}  # Stores edges (distances)

    def add_node(self, name, coordinates):
        self.nodes[name] = coordinates
        self.edges[name] = []

    def add_edge(self, node1, node2):
        distance = geodesic(self.nodes[node1], self.nodes[node2]).km
        self.edges[node1].append((distance, node2))
        self.edges[node2].append((distance, node1))  # Assume bidirectional

    def get_neighbors(self, node):
        return self.edges[node]
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
# Step 2: Dijkstra's Algorithm to find the shortest path
def dijkstra(graph, start):
    # Priority queue to store (distance, node)
    queue = [(0, start)]  # Distance to start is 0
    distances = {start: 0}  # Distance to start is 0
    previous_nodes = {start: None}  # To reconstruct the path

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        for distance, neighbor in graph.get_neighbors(current_node):
            new_distance = current_distance + distance

            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (new_distance, neighbor))

    return distances, previous_nodes

# Step 3: Function to get the shortest path
def get_shortest_path(previous_nodes, start, end):
    path = []
    current_node = end
    while current_node != start:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    path.insert(0, start)
    return path

# Step 4: Resolve Shortages by Minimizing Distance
def resolve_shortages_with_minimum_distance(insufficient_hospitals, hospitals, suppliers):
    graph = Graph()

    # Add hospitals and suppliers to the graph
    for hospital in hospitals:
        graph.add_node(hospital.name, hospital.coordinates)
    for supplier in suppliers:
        graph.add_node(supplier.name, supplier.coordinates)

    # Add edges (distances) between all hospitals and suppliers
    for hospital in hospitals:
        for supplier in suppliers:
            graph.add_edge(hospital.name, supplier.name)

    # Add edges between hospitals as well
    for hospital1 in hospitals:
        for hospital2 in hospitals:
            if hospital1 != hospital2:
                graph.add_edge(hospital1.name, hospital2.name)

    solutions = []
    for hospital, shortages in insufficient_hospitals:
        for product, shortage in shortages:
            remaining_shortage = shortage

            # Step 5: Use Dijkstra to find the shortest paths
            distances, previous_nodes = dijkstra(graph, hospital.name)

            # Step 6: Resolve the shortage with the minimum distance
            while remaining_shortage > 0:
                # Find the nearest supplier or donor hospital with stock available
                nearest_supplier = None
                nearest_distance = float('inf')
                for supplier in suppliers:
                    if supplier.can_supply([(product, remaining_shortage)]) and distances[supplier.name] < nearest_distance:
                        nearest_supplier = supplier
                        nearest_distance = distances[supplier.name]

                if nearest_supplier:
                    supply_amount = min(remaining_shortage, nearest_supplier.get_available_stock(product))
                    nearest_supplier.supply([(product, supply_amount)])
                    remaining_shortage -= supply_amount
                    solutions.append(f"Supplied {supply_amount} units of {product} from {nearest_supplier.name} ({nearest_distance:.2f} km) to {hospital.name}")
                else:
                    break

            # If the shortage still exists
            if remaining_shortage > 0:
                solutions.append(f"Error: {hospital.name} still has a shortage of {remaining_shortage} units of {product}. No possible solution found.")

    return solutions
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

# Example usage:
hospitals = [Hospital("Hospital A",100,300, (52.3676, 4.9041)), Hospital("Hospital B",100,300, (52.3755, 4.9167))]
suppliers = [Supplier("Supplier X",100,300, (52.3904, 4.9180)), Supplier("Supplier Y",100,300, (52.3800, 4.8900))]
insufficient_hospitals = [(hospitals[0], [("Product A", 50)]), (hospitals[1], [("Product A", 30)])]

solutions = resolve_shortages_with_minimum_distance(insufficient_hospitals, hospitals, suppliers)
for solution in solutions:
    print(solution)
