# main.py
import tkinter as tk
from layout import Layout

def main():
    root = tk.Tk()
    layout = Layout(root)

    # Show home screen first
    layout.show_home_content()

    root.mainloop()

if __name__ == "__main__":
    main()
