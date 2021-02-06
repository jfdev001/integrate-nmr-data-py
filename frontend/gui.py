"""GUI for processing nmr data, plotting it, and writing it to disk."""

import tkinter as tk 
import tkinter.filedialog as fd
from PIL import ImageTk
import os
from pathlib import Path
from calculations.nmranalyzer import NmrAnalyzer


class MainApp:
    """GUI for integration script."""
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

        # Grid Widgets to screen
        self.padding = {"padx": 2, "pady": 2, "ipady": 2, "ipadx": 2}
        self.grid_widgets()


    def grid_widgets(self):
        """Control the geometry of the Widgets."""
        # LabelFrames
        self.input_frame.grid(row=0, column=0)
        self.analysis_labelframe.grid(row=1, column=0, sticky=tk.W)

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
                              in_=self.analysis_labelframe)
        self.file_label.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E,
                             **self.padding, in_=self.analysis_labelframe)

        # Data analysis button
        self.analysis_button.grid(row=3, column=1, sticky=tk.W,
                                  ipady=5, ipadx=5, padx=5, pady=5,
                                  in_=self.analysis_labelframe)

        # Save button
        self.save_button.grid(row=3, column=2, sticky=tk.W,
                              ipady=5, ipadx=5, padx=5, pady=5,
                              in_=self.analysis_labelframe)


    def new_window(self):
        """Create the window for the matplotlib figure.

        This is analagous to tk.Frame(self.master) where 
        self.master = tk.Tk(). Toplevel allows for the creation of a 
        window instance under the existing tk.Tk() object versus 
        creating a completely new tk.Tk() object.
        """
        self.analysis_window = AnalysisWindow(tk.Toplevel(self.master), 
                                                self.analysis_result)

        return None


class EntryFrame:
    """Encapsulates Widgets for 'Entry Frame' LabelFrame.

    This class is bound to the MainApp window.
    """
    def __init__(self, mainappwindow=None):
        """Define Widgets for this LabelFrame."""
        # Master of MainApp is also master of this class
        self.master = mainappwindow

        # LabelFrame
        self.entry_frame = tk.LabelFrame(self.master, 
                                    text="Entry Frame",
                                    padx=5,
                                    pady=10)

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


class AnalysisFrame:
    """Encapsulates Widgets for 'Analysis Frame' LabelFrame.

    This class is bound to the MainApp window.
    """
    def __init__(self, mainappwindow=None):
        """Define widgets for this LabelFrame."""
        # Master of MainApp is also master of this class
        self.master = mainappwindow

        # LabelFrame
        self.analysis_labelframe = tk.LabelFrame(self.master, 
                                            text="Analysis Frame",
                                            padx=5,
                                            pady=5) 
        
        # File dialog
        self.home = str(Path.home())  # Path to home directory
        self.file_types = (("asc files", "*.asc"),)
        self.file_path = None
        self.file_name_var = tk.StringVar(self.master, 
                                          value="File Name Displays Here")
        self.file_button = tk.Button(self.master, 
                              text="Click to Choose .ASC File",
                              command=self.opendialog,
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


    def opendialog(self):
        """Popup for file dialog and set file path/name"""
        # Dialog
        self.file_path = fd.askopenfilename(title="Select ASC file",
                                                  initialdir=self.home,
                                                  filetypes=self.file_types)

        # Set the file name
        fname = "".join(reversed(self.file_path[
                                    -1:self.file_path.rfind("/"):-1]))

        self.file_name_var.set(fname)

        return None

        
    def do_analysis(self):
        """Instantiate NmrAnalysis and return plots."""
        # Instantiate NmrAnalyzer
        analyzer = NmrAnalyzer(self.lower_limit_var, self.upper_limit_var,
                               self.file_path, self.file_name_var)
        self.analysis_result = analyzer.proc_data()

        # Create new window for matplotlib figure
        self.new_window()

        return None


class AnalysisWindow:
    """Displays the graph and should have a menu."""
    def __init__(self, window=None, analysis_result=None):
        """Initialize new analysis window and some configuration."""
        # Control window
        self.window = window
        self.frame = tk.Frame(self.window)

        # Title
        self.window.title("Data Analysis Window")

        # Pack the window
        self.frame.pack()

        # Tuple (figure ImageTk.PhotoImage, str log)
        self.analysis_result = analysis_result

        # Plot label
        self.plot_label = tk.Label(self.window, 
                                   image=self.analysis_result[0]).pack()

        
