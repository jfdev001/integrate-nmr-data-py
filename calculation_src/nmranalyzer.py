"""Store attributes passed from GUI and perform integration."""

import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import io
import numpy as np
import matplotlib.pyplot as plt

class NmrAnalyzer:  # Make inherit from MainApp?
    """Encapsulates all NMR related integration data and methods."""
    def __init__(self, info=None):
        """Analysis attributes """ 
        # Constructor
        self.info = info

        # Convert tkinter var limits to floats
        self.lower_lim = float(self.info.entry_section.lower_lim_var.get())
        self.upper_lim = float(self.info.entry_section.upper_lim_var.get())

        # Results
        self.x_arr = []  # Chemical shift ppm
        self.y_arr = []  # Peak intensity
        self.area = None
        self.figure = None
        self.log_text = None


    def proc_data(self):
        """Opens file, computes, and returns results and plot"""
        # Open file and build arrays
        with open(self.info.analysis_section.file_path, "r") as fobj:
            self.__build_arrays(fobj)

        # Get the log file
        self.log_text = self.__log()

        # Get the matplotlib plot 
        self.figure = self.__plot()

        # Return tuple
        return (self.figure, self.log_text)
  

    def __build_arrays(self, fobj):
        """Build x and y arrays from .asc file."""
        # Iterate through data file
        next(fobj)  # Skip first line that is categorical info
        for line in fobj:
            cur_x = float(line.split("\t")[0])
            cur_y = float(line.split("\t")[1])

            # Build lists for plotting
            if (cur_x >= self.lower_lim and cur_x <= self.upper_lim):
                self.x_arr.append(cur_x)
                self.y_arr.append(cur_y)

        return None


    def __plot(self):
        """Matplotlib to plot the figure.""" 
        # Instantiate Figure and Axes objects
        fig, ax = plt.subplots()

        # Plot Axes object to Figure and label it
        ax.plot(self.x_arr, self.y_arr)
        ax.set_xlabel("Chemical Shift")
        ax.set_ylabel("Signal Intensity")
        ax.set_title(f"Plot of {self.info.analysis_section.file_name_var.get()}")
        ax.set_xlim(ax.get_xlim()[::-1])

        # Convert plot to PhotoImage object
        buffer = io.BytesIO()  # Reserve memory for figure
        fig.savefig(buffer)    # Save figure in that memory
        plot_img = PlotImage(Image.open(buffer))  # Use w/ tk

        # Return the PhotoImage object
        return plot_img

    
    def __log(self):
        """Integrates and returns outfile text."""
        # Reverse x & y list since np.trapz assumes ascending x & y
        self.x_arr.reverse()
        self.y_arr.reverse()

        # Area under the curve using trapezoidal integration
        self.area = np.trapz(y=self.y_arr, x=self.x_arr)

        # Outfile text
        now = str(datetime.now())[:str(datetime.now()).index(".")]
        text = f"FILE PATH,TIME,AREA\n{self.info.analysis_section.file_path},{now},{self.area}\n"

        # Return outfile text
        return text


class PlotImage:
    """Makes Image object used in PhotoImage init accessible."""
    def __init__(self, image=None ):
        """Construct PhotoImage and Image object."""
        self.__opened_img = image
        self.__photoimage = ImageTk.PhotoImage(self.__opened_img)

    
    def get_opened_img(self):
        """Return opened image private attr.
        
        One might do this because the PhotoImage has no write method.
        """
        return self.__opened_img


    def get_photoimage(self):
        """Return PhotoImage private attr.
        
        One might do this to display it using tk.Label(image=...).
        """
        return self.__photoimage