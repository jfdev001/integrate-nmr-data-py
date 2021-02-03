"""Driver file.
No need for __init__.py in this directory?
"""

from frontend.gui import GUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
