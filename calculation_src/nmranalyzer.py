"""Store attributes passed from GUI and perform integration."""

import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import io
import numpy as np
import matplotlib.pyplot as plt

class NmrAnalyzer:  # Make inherit from MainApp?
    """Encapsulates all NMR related integration data and methods."""
    def __init__(self, lower_lim, upper_lim, file_path, file_name):
        """Analysis attributes """ 
        self.__lower_limit = float(lower_lim.get())  # tkinter var
        self.__upper_lim = float(upper_lim.get())  # tkinter var
        self.__file_path = file_path
        self.__file_name = file_name.get()  # tkinter var
        self.__x_arr = []  # Chemical shift ppm
        self.__y_arr = []  # Peak intensity
        self.__area = None
        self.__figure = None
        self.__log_text = None


    def proc_data(self):
        """Opens file, computes, and returns results and plot"""
        # Open file and build arrays
        with open(self.__file_path, "r") as fobj:
            self.__build_arrays(fobj)

        # Get the log file
        self.__log_text = self.__log()

        # Get the matplotlib plot 
        self.__figure = self.__plot()

        # Return tuple
        return (self.__figure, self.__log_text)
  

    def __build_arrays(self, fobj):
        """Build x and y arrays from .asc file."""
        # Iterate through data file
        next(fobj)  # Skip first line that is categorical info
        for line in fobj:
            cur_x = float(line.split("\t")[0])
            cur_y = float(line.split("\t")[1])

            # Build lists for plotting
            if (cur_x >= self.__lower_limit and cur_x <= self.__upper_lim):
                self.__x_arr.append(cur_x)
                self.__y_arr.append(cur_y)

        return None


    def __plot(self):
        """Matplotlib to plot the figure.""" 
        # Instantiate Figure and Axes objects
        fig, ax = plt.subplots()

        # Plot Axes object to Figure and label it
        ax.plot(self.__x_arr, self.__y_arr)
        ax.set_xlabel("Chemical Shift")
        ax.set_ylabel("Signal Intensity")
        ax.set_title(f"Plot of {self.__file_name}")
        ax.set_xlim(ax.get_xlim()[::-1])  # Reverse tuple and set range

        # Convert plot to PhotoImage object
        buffer = io.BytesIO()  # Reserve memory for figure
        fig.savefig(buffer)    # Save figure in that memory
        plot_img = MyImage(Image.open(buffer))  # Use w/ tk

        # Return the PhotoImage object
        return plot_img

    
    def __log(self):
        """Integrates and returns outfile text."""
        # Reverse x & y list since np.trapz assumes ascending x & y
        self.__x_arr.reverse()
        self.__y_arr.reverse()

        # Area under the curve using trapezoidal integration
        self.__area = np.trapz(y=self.__y_arr, x=self.__x_arr)

        # Outfile text
        now = str(datetime.now())[:str(datetime.now()).index(".")]
        text = f"FILE PATH,TIME,AREA\n{self.__file_path},{now},{self.__area}\n"

        # Return outfile text
        return text


class MyImage:
    """Makes Image object used in PhotoImage init accessible."""
    def __init__(self, image=None ):
        """Construct PhotoImage and Image object."""
        self.__opened_img = image
        self.__photoimage = ImageTk.PhotoImage(self.__opened_img)

    
    def get_opened_img(self):
        """Return opened image private attr."""
        return self.__opened_img


    def get_photoimage(self):
        """Return PhotoImage private attr."""
        return self.__photoimage