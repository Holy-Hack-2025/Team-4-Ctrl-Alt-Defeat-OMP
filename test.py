import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from ttkthemes import ThemedStyle  # For modern themes

class CSVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 CSV Editor")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        # Apply Theme
        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  # Try 'radiance', 'breeze', 'arc', etc.

        self.csv_file = None
        self.data = None

        self.create_widgets()

    def create_widgets(self):
        # === Top Bar with Buttons ===
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        self.load_btn = ttk.Button(top_frame, text="📂 Load CSV", command=self.load_csv)
        self.load_btn.pack(side="left", padx=10, pady=5)

        self.save_btn = ttk.Button(top_frame, text="💾 Save CSV", command=self.save_csv, state=tk.DISABLED)
        self.save_btn.pack(side="left", padx=5, pady=5)

        self.exit_btn = ttk.Button(top_frame, text="❌ Exit", command=self.root.quit)
        self.exit_btn.pack(side="right", padx=10, pady=5)

        # === Table Frame ===
        table_frame = ttk.Frame(self.root)
        table_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Scrollbar
        self.tree_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        self.tree_scroll.pack(side="right", fill="y")

        # Treeview (Table)
        self.tree = ttk.Treeview(table_frame, show="headings", yscrollcommand=self.tree_scroll.set)
        self.tree.pack(expand=True, fill="both")

        self.tree_scroll.config(command=self.tree.yview)

        self.tree.bind("<Double-1>", self.on_double_click)  # Editable cells

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        
        self.csv_file = file_path
        self.data = pd.read_csv(file_path)

        # Clear old table
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data.columns)

        # Set column headings
        for col in self.data.columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=120, anchor="center")

        # Insert data
        for i, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.save_btn.config(state=tk.NORMAL)  # Enable save button

    def on_double_click(self, event):
        """Make treeview cells editable on double-click."""
        item = self.tree.selection()[0]  
        col_id = self.tree.identify_column(event.x)
        col_idx = int(col_id[1:]) - 1
        col_name = self.tree["columns"][col_idx]

        value = self.tree.item(item, "values")[col_idx]

        # Create Entry box
        entry = ttk.Entry(self.root, font=("Arial", 12))
        entry.insert(0, value)
        entry.focus()
        entry.place(x=event.x_root - self.root.winfo_rootx(), y=event.y_root - self.root.winfo_rooty())

        def save_edit():
            new_value = entry.get()
            row_values = list(self.tree.item(item, "values"))
            row_values[col_idx] = new_value
            self.tree.item(item, values=row_values)
            entry.destroy()

        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def save_csv(self):
        """Save changes back to CSV."""
        if not self.csv_file:
            return
        
        # Collect updated data
        updated_data = []
        for row in self.tree.get_children():
            updated_data.append(self.tree.item(row)["values"])
        
        # Convert to DataFrame and save
        df = pd.DataFrame(updated_data, columns=self.data.columns)
        df.to_csv(self.csv_file, index=False)

        messagebox.showinfo("✅ Success", "CSV file saved successfully!")

# === Run Application ===
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditor(root)
    root.mainloop()
