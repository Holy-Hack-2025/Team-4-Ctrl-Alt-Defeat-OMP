import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class CSVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")
        self.root.geometry("800x500")

        self.csv_file = None  # Store the currently opened file
        self.data = None  # Store the CSV data
        
        # UI Elements
        self.create_widgets()
    
    def create_widgets(self):
        # File Selection Button
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.load_btn = tk.Button(btn_frame, text="Load CSV", command=self.load_csv)
        self.load_btn.pack(side="left", padx=5)

        self.save_btn = tk.Button(btn_frame, text="Save CSV", command=self.save_csv, state=tk.DISABLED)
        self.save_btn.pack(side="left", padx=5)

        # Table for CSV Data
        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        self.tree.bind("<Double-1>", self.on_double_click)  # Make cells editable

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        
        self.csv_file = file_path
        self.data = pd.read_csv(file_path)

        # Clear old table data
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data.columns)

        # Setup column headings
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Insert data into the table
        for i, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.save_btn.config(state=tk.NORMAL)  # Enable save button

    def on_double_click(self, event):
        """Make treeview cells editable on double-click."""
        item = self.tree.selection()[0]  # Get selected row
        col_id = self.tree.identify_column(event.x)  # Get clicked column
        col_idx = int(col_id[1:]) - 1  # Convert to zero-based index
        col_name = self.tree["columns"][col_idx]  # Get column name
        
        # Get current cell value
        value = self.tree.item(item, "values")[col_idx]

        # Create Entry box for editing
        entry = tk.Entry(self.root)
        entry.insert(0, value)
        entry.focus()
        entry.place(x=event.x_root - self.root.winfo_rootx(), y=event.y_root - self.root.winfo_rooty())

        def save_edit():
            new_value = entry.get()
            row_values = list(self.tree.item(item, "values"))
            row_values[col_idx] = new_value  # Update the selected column
            self.tree.item(item, values=row_values)
            entry.destroy()

        entry.bind("<Return>", lambda e: save_edit())  # Save on Enter key
        entry.bind("<FocusOut>", lambda e: save_edit())  # Save when losing focus

    def save_csv(self):
        """Save changes back to CSV."""
        if not self.csv_file:
            return
        
        # Collect data from Treeview
        updated_data = []
        for row in self.tree.get_children():
            updated_data.append(self.tree.item(row)["values"])
        
        # Convert to DataFrame and save
        df = pd.DataFrame(updated_data, columns=self.data.columns)
        df.to_csv(self.csv_file, index=False)

        messagebox.showinfo("Success", "CSV file saved successfully!")

# Run Tkinter App
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditor(root)
    root.mainloop()
