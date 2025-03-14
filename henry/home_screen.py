
import tkinter as tk

class HomeScreen:
    def __init__(self, root, show_simulation_content_callback):
        self.root = root
        self.show_simulation_content_callback = show_simulation_content_callback

    def create_home_screen(self):
        self.home_frame = tk.Frame(self.root)
        self.home_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        # Title - Centered
        title_label = tk.Label(self.home_frame, text="Welcome to the Healthcare Supply Chain Simulation", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=20, columnspan=2, sticky="nsew")

        # Description - Centered
        description_text = (
            "This application simulates the distribution of medicines between hospitals and suppliers.\n"
            "Click 'Start Simulation' to begin."
        )
        description_label = tk.Label(self.home_frame, text=description_text, font=("Helvetica", 12), justify="center", wraplength=400)
        description_label.grid(row=1, column=0, padx=10, pady=20, columnspan=2, sticky="nsew")

        # Start Simulation button - Smaller size
        start_button = tk.Button(self.home_frame, text="Start Simulation", command=self.show_simulation_content_callback, font=("Helvetica", 12), width=15, height=2)
        start_button.grid(row=2, column=0, padx=10, pady=20, columnspan=2)

        # Center content in the frame and allow it to expand
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)
        
        # Make sure the frame expands to fit the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
