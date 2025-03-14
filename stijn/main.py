# main.py
import tkinter as tk
from layout import Layout

def main():
    root = tk.Tk()
    root.config(bg="#A2D4CD")
    layout = Layout(root)

    # Show home screen first
    layout.show_home_content()

    root.mainloop()

if __name__ == "__main__":
    main()
