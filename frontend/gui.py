"""Tkinter interface for integrate NMR script."""


# TRY REMOVING __init__.py from nmr folder
import tkinter as tk 
import tkinter.filedialog as fd
from PIL import ImageTk
import os
from pathlib import Path
# from calculations.intclass import DoCalculus 

class GUI:
    """GUI for integration script"""
    def __init__(self, master=None):
        """Initialize master Frame and define other Widgets."""
        # Master frame
        self.master = master
        self.frame = tk.Frame(self.master)

        # Set icon
        self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.img_path = os.path.join(self.THIS_FOLDER, "imgs/icon.png") 
        self.icon = ImageTk.PhotoImage(file=self.img_path)
        self.master.iconphoto(False, self.icon)

        # Set title
        self.master.title("NMR Inte-great!")

        # Grid master frame
        self.frame.grid()

        # -------Define Widgets--------
        # Title 
        self.title_label = tk.Label(self.master, 
                                    text="Outfile Title:",
                                    relief=tk.RAISED,
                                    bg="floral white")
        self.title_var = tk.StringVar(self.master, 
                                      value=".txt")
        self.title_entry = tk.Entry(self.master, 
                                    textvariable=self.title_var,
                                    width=40, 
                                    relief=tk.SUNKEN)

        # Limits of integration
        self.upper_limit_label = tk.Label(self.master,
                                          text="Upper Limit of Integration:",
                                          relief=tk.RAISED,
                                          bg="floral white")
        self.upper_limit_var = tk.StringVar(self.master, value="")
        self.upper_limit_entry = tk.Entry(self.master,
                                          textvariable=self.upper_limit_var,
                                          width=40, 
                                          relief=tk.SUNKEN)
        self.lower_limit_label = tk.Label(self.master,
                                    text="Lower Limit of Integration:",
                                    relief=tk.RAISED,
                                    bg="floral white")
        self.lower_limit_var = tk.StringVar(self.master, value="")
        self.lower_limit_entry = tk.Entry(self.master,
                                          textvariable=self.lower_limit_var,
                                          width=40,
                                          relief=tk.SUNKEN)

        # File dialog
        self.home = str(Path.home()) 
        self.file_types = (("asc files", "*.asc"), ("all files", "*.*"))
        self.file_path = None
        self.file_name_var = tk.StringVar(self.master, value="File Name Displays Here")
        self.file_button = tk.Button(self.master, 
                              text="Click to Choose .ASC File",
                              command=self.fdialog,
                              bg = "bisque")
                              #width=24)
        self.file_label = tk.Label(self.master, 
                                   textvariable=self.file_name_var,
                                   width=40,
                                   bd=4,
                                   relief=tk.SUNKEN,
                                   wraplength=280)

        # Analyze button
        self.analysis_button = tk.Button(self.master,
                                         text="Click to Analyze Data",
                                         command=None,
                                         bg="bisque")
                                         #width=24)

        # Save button
        self.save_button = tk.Button(self.master,
                                     text="Click to Save Analysis",
                                     command=None,
                                     bg="bisque")
                                     #width=24)

        #-------End Define Widgets--------

        # Grid Widgets to screen
        self.padding = {"padx": 2, "pady": 2, "ipady": 2, "ipadx": 2}
        self.grid_widgets()


    def grid_widgets(self):
        """Control the geometry of the Widgets."""
        # Title
        self.title_label.grid(row=0, column=0, sticky=tk.W+tk.E, 
                              **self.padding)
        self.title_entry.grid(row=0, column=1, **self.padding, columnspan=2)

        # Limits of integration
        self.upper_limit_label.grid(row=1, column=0, **self.padding, 
                                    sticky=tk.W+tk.E)
        self.upper_limit_entry.grid(row=1, column=1, **self.padding, 
                                    columnspan=2)
        self.lower_limit_label.grid(row=2, column=0, **self.padding, 
                                    sticky=tk.W+tk.E)
        self.lower_limit_entry.grid(row=2, column=1, **self.padding,
                                    columnspan=2)

        # File dialog button
        self.file_button.grid(row=3, column=0, sticky=tk.W,
                              ipady=5, ipadx=5, padx=5, pady=5)
        self.file_label.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E,
                             **self.padding)

        # Data analysis button
        self.analysis_button.grid(row=3, column=1, sticky=tk.W,
                                  ipady=5, ipadx=5, padx=5, pady=5)

        # Save button
        self.save_button.grid(row=3, column=2, sticky=tk.W,
                              ipady=5, ipadx=5, padx=5, pady=5)

    
    def fdialog(self):
        """Popup for file dialog and set file path/name"""
        self.file_path = fd.askopenfilename(title="Select ASC file",
                                                  initialdir=self.home,
                                                  filetypes=self.file_types)
        fname = "".join(reversed(self.file_path[
                                    -1:self.file_path.rfind("/"):-1]))
        self.file_name_var.set(fname)
        