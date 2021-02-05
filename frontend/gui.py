"""Tkinter interface for integrate NMR script."""

import tkinter as tk 
import tkinter.filedialog as fd
from PIL import ImageTk
import os
from pathlib import Path
from calculations.nmranalyzer import NmrAnalyzer
# from calculations.intclass import DoCalculus 


class GUI:
    """GUI for integration script"""
    def __init__(self, master=None):
        """Initialize master Frame and define other Widgets."""
        # Master frame
        self.master = master
        self.frame = tk.Frame(self.master)

        # Tuple (figure photoimage, str log) returned from NmrAnalyzer
        self.analysis_result = None

        # Set icon
        self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.img_path = os.path.join(self.THIS_FOLDER, "imgs/icon.png") 
        self.icon = ImageTk.PhotoImage(file=self.img_path)
        self.master.iconphoto(False, self.icon)

        # Set title
        self.master.title("NMR Inte-great!")

        # Grid master frame
        self.frame.grid(sticky=tk.N + tk.S + tk.E + tk.W)

        # -------Define Widgets--------
        # Label frames
        self.input_frame = tk.LabelFrame(self.master, 
                                         text="Entry Frame",
                                         padx=5,
                                         pady=10)
        self.analysis_frame = tk.LabelFrame(self.master, 
                                            text="Analysis Frame",
                                            padx=5,
                                            pady=5)
                    

        # Entry Widget styles
        self.entry_style = {"relief": tk.SUNKEN, "width": 49}

        # Title
        self.title_label = tk.Label(self.master, 
                                    text="Outfile Title:",
                                    relief=tk.RAISED,
                                    bg="floral white")
        self.title_var = tk.StringVar(self.master, 
                                      value=".txt")
        self.title_entry = tk.Entry(self.master, 
                                    textvariable=self.title_var,
                                    **self.entry_style)

        # Upper limit of integration
        self.upper_limit_label = tk.Label(self.master,
                                          text="Upper Limit of Integration:",
                                          relief=tk.RAISED,
                                          bg="floral white")
        self.upper_limit_var = tk.StringVar(self.master, value="")
        self.upper_limit_entry = tk.Entry(self.master,
                                          textvariable=self.upper_limit_var,
                                          **self.entry_style)

        # Lower limit of integration
        self.lower_limit_label = tk.Label(self.master,
                                    text="Lower Limit of Integration:",
                                    relief=tk.RAISED,
                                    bg="floral white")
        self.lower_limit_var = tk.StringVar(self.master, value="")
        self.lower_limit_entry = tk.Entry(self.master,
                                          textvariable=self.lower_limit_var,
                                          **self.entry_style)

        # File dialog
        self.home = str(Path.home())  # Path to home directory
        self.file_types = (("asc files", "*.asc"),)
        self.file_path = None
        self.file_name_var = tk.StringVar(self.master, 
                                          value="File Name Displays Here")
        self.file_button = tk.Button(self.master, 
                              text="Click to Choose .ASC File",
                              command=self.fdialog,
                              bg = "bisque")
        self.file_label = tk.Label(self.master, 
                                   textvariable=self.file_name_var,
                                   width=40,
                                   bd=4,
                                   relief=tk.SUNKEN,
                                   wraplength=280)

        # Analyze button
        self.analysis_button = tk.Button(self.master,
                                         text="Click to Analyze Data",
                                         command=self.do_analysis,
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
        # LabelFrames
        self.input_frame.grid(row=0, column=0)
        self.analysis_frame.grid(row=1, column=0, sticky=tk.W)

        # Title
        self.title_label.grid(row=0, column=0, sticky=tk.W+tk.E, 
                              **self.padding, in_=self.input_frame)
        self.title_entry.grid(row=0, column=1, **self.padding, columnspan=2,
                              in_=self.input_frame)

        # Upper limit of integration
        self.upper_limit_label.grid(row=1, column=0, **self.padding, 
                                    sticky=tk.W+tk.E, in_=self.input_frame)
        self.upper_limit_entry.grid(row=1, column=1, **self.padding, 
                                    columnspan=2, in_=self.input_frame)

        # Lower limit of integration
        self.lower_limit_label.grid(row=2, column=0, **self.padding, 
                                    sticky=tk.W+tk.E, in_=self.input_frame )
        self.lower_limit_entry.grid(row=2, column=1, **self.padding,
                                    columnspan=2, in_=self.input_frame)

        # File dialog button
        self.file_button.grid(row=3, column=0, sticky=tk.W,
                              ipady=5, ipadx=5, padx=5, pady=5, 
                              in_=self.analysis_frame)
        self.file_label.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E,
                             **self.padding, in_=self.analysis_frame)

        # Data analysis button
        self.analysis_button.grid(row=3, column=1, sticky=tk.W,
                                  ipady=5, ipadx=5, padx=5, pady=5,
                                  in_=self.analysis_frame)

        # Save button
        self.save_button.grid(row=3, column=2, sticky=tk.W,
                              ipady=5, ipadx=5, padx=5, pady=5,
                              in_=self.analysis_frame)

    
    def fdialog(self):
        """Popup for file dialog and set file path/name"""
        # Dialog
        self.file_path = fd.askopenfilename(title="Select ASC file",
                                                  initialdir=self.home,
                                                  filetypes=self.file_types)

        # Set the file name
        fname = "".join(reversed(self.file_path[
                                    -1:self.file_path.rfind("/"):-1]))

        self.file_name_var.set(fname)

        
    def do_analysis(self):
        """Instantiate NmrAnalysis and return plots"""
        analyzer = NmrAnalyzer(self.lower_limit_var, self.upper_limit_var,
                               self.file_path, self.file_name_var)
        self.analysis_result = analyzer.proc_data()