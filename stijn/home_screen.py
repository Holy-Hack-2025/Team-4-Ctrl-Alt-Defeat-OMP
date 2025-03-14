import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class HomeScreen:
    def __init__(self, root, show_simulation_content_callback):
        self.root = root
        self.show_simulation_content_callback = show_simulation_content_callback
        self.data = None
        self.file_path = None
        self.filename = "normal"

    def create_home_screen(self):
        self.home_frame = tk.Frame(self.root, bg="#A2D4CD")
        self.home_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        # Title - Centered
        title_label = tk.Label(self.home_frame, text="VitalLink",
                               font=("Verdana", 35, "bold"), bg="#A2D4CD")
        title_label.grid(row=0, column=0, padx=10, pady=20, columnspan=2, sticky="nsew")

        # Description - Centered
        description_text = (
            "A SMARTER, MORE COLLABORATIVE HEALTHCARE ECOSYSTEM."
        )
        description_label = tk.Label(self.home_frame, text=description_text, font=("Helvetica", 18), justify="center",
                                     wraplength=400, bg="#A2D4CD")
        description_label.grid(row=1, column=0, padx=10, pady=20, columnspan=2, sticky="nsew")

        # Start Simulation button
        start_button = tk.Button(self.home_frame, text="Start Simulation", command=lambda: self.start_simulation(),
                                 font=("Helvetica", 12), width=15, height=2)
        start_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # Modify Data button
        modify_button = tk.Button(self.home_frame, text="Modify Data", command=self.open_dropdown_window,
                                  font=("Helvetica", 12), width=15, height=2, bg="#f4b400")
        modify_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        # Center content in the frame and allow it to expand
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)
        self.home_frame.grid_rowconfigure(3, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)

        # Make sure the frame expands to fit the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    def start_simulation(self):
        print(self.filename)
        self.show_simulation_content_callback(self.filename)
    def open_dropdown_window(self):
        """Opens a window with a dropdown menu to select Hospital or Supplier."""
        self.filename = "Hypo"
        dropdown_window = tk.Toplevel(self.root)
        dropdown_window.title("Select Type")
        dropdown_window.geometry("300x200")

        tk.Label(dropdown_window, text="Select entity type:", font=("Arial", 12)).pack(pady=10)

        entity_var = tk.StringVar()
        entity_dropdown = ttk.Combobox(dropdown_window, textvariable=entity_var, values=["Hospital", "Supplier"],
                                       state="readonly", font=("Arial", 12))
        entity_dropdown.pack(pady=10)
        entity_dropdown.current(0)

        def confirm_selection():
            entity_type = entity_var.get().lower()
            dropdown_window.destroy()
            self.load_csv_data(entity_type)

        tk.Button(dropdown_window, text="Confirm", command=confirm_selection, font=("Arial", 12),
                  bg="#34a853", fg="white").pack(pady=10)

    def load_csv_data(self, entity_type):
        """Loads CSV data for the selected entity type."""
        if entity_type == "hospital":
            self.file_path = fr"C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\other_required_files\Hospitals.csv"
        else:
            self.file_path = fr"C:\creativity\Team-4-Ctrl-Alt-Defeat-OMP\stijn\other_required_files\Suppliers.csv"

        try:
            self.data = pd.read_csv(self.file_path)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"{self.file_path} not found. Please ensure the file exists.")
            return

        # Ask for affected entities
        self.select_affected_entities(entity_type)

    def select_affected_entities(self, entity_type):
        """Dialog box to select affected hospitals/suppliers."""
        unique_options = list(self.data["name"].unique())  # Assuming column name is 'Name'

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Select {entity_type.capitalize()}s")
        dialog.geometry("300x400")

        tk.Label(dialog, text=f"Select affected {entity_type}s:", font=("Arial", 12)).pack(pady=10)

        listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE, height=15)
        for option in unique_options:
            listbox.insert(tk.END, option)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        selected_values = []

        def submit():
            selected_indices = listbox.curselection()
            for i in selected_indices:
                selected_values.append(unique_options[i])
            dialog.destroy()
            self.edit_window(selected_values)

        tk.Button(dialog, text="Confirm", command=submit, font=("Arial", 12), bg="#34a853", fg="white").pack(pady=10)
        dialog.wait_window()

    def edit_window(self, selected_entities):
        """Window to edit CSV data dynamically."""
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Data")
        edit_win.geometry("1200x500")

        frame = tk.Frame(edit_win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree_scroll = ttk.Scrollbar(frame, orient="vertical")
        tree_scroll.pack(side="right", fill="y")

        # Dynamically create treeview with CSV columns
        columns = list(self.data.columns)
        tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set, height=10)
        tree.pack(fill="both", expand=True)
        tree_scroll.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        filtered_data = self.data[self.data["name"].isin(selected_entities)]
        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=tuple(row))

        def update_cell(event):
            """Allows double-click editing of table cells."""
            selected_item = tree.selection()
            if not selected_item:
                return

            col = tree.identify_column(event.x)  # Column clicked
            row_id = tree.identify_row(event.y)  # Row clicked
            col_index = int(col[1:]) - 1  # Convert '#1' to index 0

            entry_popup = tk.Toplevel(edit_win)
            entry_popup.geometry("200x90")
            entry_popup.title("Edit Value")

            tk.Label(entry_popup, text=f"Edit {columns[col_index]}:").pack()

            new_value_var = tk.StringVar()
            new_value_entry = tk.Entry(entry_popup, textvariable=new_value_var)
            new_value_entry.pack()
            new_value_entry.focus()

            def save_edit():
                new_value = new_value_var.get()
                if new_value:
                    tree.item(selected_item, values=[new_value if i == col_index else val
                                                     for i, val in enumerate(tree.item(selected_item)["values"])])
                entry_popup.destroy()

            tk.Button(entry_popup, text="Save", command=save_edit).pack()

        tree.bind("<Double-1>", update_cell)  # Bind double-click to edit cells

        def update_csv():
            """Updates the CSV with modified values."""
            updated_data = []
            for row in tree.get_children():
                values = tree.item(row)["values"]
                updated_data.append(values)

            new_df = pd.DataFrame(updated_data, columns=columns)
            new_df.to_csv("hypo.csv", index=False)
            messagebox.showinfo("Success", "Data saved successfully to hypo.csv")
            edit_win.destroy()

        save_btn = tk.Button(edit_win, text="Save Changes", command=update_csv, font=("Arial", 12),
                             bg="#4285f4", fg="white", width=15, height=2)
        save_btn.pack(pady=10)