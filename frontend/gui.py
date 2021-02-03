"""Tkinter interface for integrate NMR script."""


# TRY REMOVING __init__.py from nmr folder
import tkinter as tk
from PIL import ImageTk
import os
# from calculations.intclass import DoCalculus 

class GUI:
    """GUI for integration script"""
    def __init__(self, master=None):
        """Initialize master frame and all widgets"""
        # Master frame
        self.master = master
        self.frame = tk.Frame(self.master)

        # Set icon
        self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.PARENT_FOLDER = self.THIS_FOLDER[:self.THIS_FOLDER.find(__file__)]
        self.img_path = os.path.join(self.THIS_FOLDER, "imgs/icon.png")         
        self.icon = ImageTk.PhotoImage(file=self.img_path)
        self.master.iconphoto(False, self.icon)

        # Set title
        self.master.title("NMR Inte-great!")

        # Grid master frame
        self.frame.grid()

        # Widgets #
        self.title_label = tk.Label(self.master, 
                                    text="Outfile Title:",
                                    relief=tk.RAISED,
                                    bg="floral white")
        self.title_input_var = tk.StringVar(self.master, 
                                      value="")
        self.title_input = tk.Entry(self.master, 
                                    textvariable=self.title_input_var,
                                    width=40, 
                                    relief=tk.SUNKEN)


        self.lower_limit_var = tk.DoubleVar(self.master)
        self.lower_limit = tk.Entry(self.master) 

        self.upper_limit_var = tk.DoubleVar(self.master)
        self.upper_limit = tk.Entry(self.master)

        self.file = tk.Button(self.master)

        # Grid Widgets to Screen
        self.grid_widgets()


    def grid_widgets(self):
        """Control the geometry of the Widgets."""
        self.title_label.grid(row=0, column=0)
        self.title_input.grid(row=0, column=1)

        

