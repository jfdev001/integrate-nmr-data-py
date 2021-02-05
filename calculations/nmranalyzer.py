"""Store attributes passed from GUI and perform integration."""

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

class NmrAnalyzer:
    """Encapsulates all NMR related integration data and methods."""
    def __init__(self, lower_lim, upper_lim, file_path):
        """Analylsis attributes """ 
        self.__lower_limit = float(lower_lim.get())  # tkinter var
        self.__upper_lim = float(upper_lim.get())  # tkinter var
        self.__file_path = file_path
        self.__x_arr = []  # Chemical shift ppm
        self.__y_arr = []  # Peak intensity
        self.__plot = None
        self.__log_text = None


    def proc_data(self):
        """Opens file, computes, and returns results and plot"""
        # Open file and build arrays
        with open(self.__file_path, "r") as fobj:
            self.__build_arrays(fobj)

        # Get the log file
        outfile_text = self.__log()

        # Get the matplotlib plot 
        figure = self.__plot()

        # Return tuple
        return (figure, outfile_text)
  

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
        return plot 

    
    def __log(self):
        """Integrates and returns outfile text."""
        return text

