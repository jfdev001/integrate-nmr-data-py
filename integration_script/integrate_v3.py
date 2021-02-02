# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:38:52 2020

@author: dionysus
"""
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

#GLOBALS
UPPER_OA = 5.90
LOWER_OA = 5.40
UPPER_FERRO = 4.05
LOWER_FERRO = 3.90
f1 = "20200410_JGF_Oleate-capped_CdSe_QD_PROTON.asc "
f2 = "20200410_JGF_oleate-capped_CdSe_QD_Quality_Control_PROTON.asc"

def main():
    #Lists
    alkenyl_shift_list = []
    alkenyl_peak_list = []
    ferrocene_shift_list = []
    ferrocene_peak_list = []
    
    #Open files -- f1 is 9.2 mg/mL data while f2 is 4.6 mg/mL data
    infile = open (f2, "r")
    outfile = open ("v2_log.txt", "a+")
        
    #Read and parse data
    line = infile.readline()
    line = infile.readline()
    while (line != ""):
        cur_res = GetCurShift(line)
        BuildLists(line,cur_res, alkenyl_shift_list, alkenyl_peak_list, 
                   ferrocene_shift_list, ferrocene_peak_list)
        line = infile.readline()
    
    #Reverse peak list since np.trapz assumes y values correspond with
    #ascending x values 
    alkenyl_peak_list.reverse()
    ferrocene_peak_list.reverse()
    alkenyl_shift_list.reverse()
    ferrocene_shift_list.reverse()

    #--------------------------------------------------------------------------
    #Data for matplotlib
    alkenyl_x_array = np.array(alkenyl_shift_list)
    alkenyl_y_array = np.array(alkenyl_peak_list)
    ferrocene_x_array = np.array(ferrocene_shift_list)
    ferrocene_y_array = np.array(ferrocene_peak_list)
    
    #Integral limits
    #Refer to globals -> UPPER_OA, LOWER_OA and UPPER_FERRO, LOWER_FERRO
    fig, ax = plt.subplots()
    #plt.figure(figsize = (9,3))
    ax.plot(alkenyl_x_array, alkenyl_y_array)
    #ax.plot(ferrocene_x_array, ferrocene_y_array)
    #--------------------------------------------------------------------------

    #Alkenyl Peak Integration
    alkenyl_avg_dx = -1 * GetAvgDeltaX(alkenyl_shift_list)
    alkenyl_intermed_sum = IntermediateValueSum(alkenyl_peak_list)
    alkenyl_integral = TrapezoidalSum(alkenyl_avg_dx, alkenyl_intermed_sum, 
                                      alkenyl_peak_list)
    
    #Verify trapezoidal sum with numpy function
    a1 = np.trapz(y = alkenyl_peak_list, x = alkenyl_shift_list)
    
    #Ferrocene Peak Integration
    ferrocene_avg_dx = -1 * GetAvgDeltaX(ferrocene_shift_list)
    ferrocene_intermed_sum = IntermediateValueSum(ferrocene_peak_list)    
    ferrocene_integral = TrapezoidalSum(ferrocene_avg_dx, ferrocene_intermed_sum,
                                        ferrocene_peak_list)
    
    #Verify trapezoidal sum with numpy function
    a2 = np.trapz(y = ferrocene_peak_list, x = ferrocene_shift_list)
    
    #Ratio of OA Integral to Ferocene Integral
    now = str(datetime.now())[:str(datetime.now()).index(".")] #Slice str datetime obj until "."
    ratio = (alkenyl_integral/ferrocene_integral)
    outfile.write(now + "\n" + str(infile).split("'")[1]
                      + "\nAlkenyl integral Trapz: " + str(alkenyl_integral) 
                      + "\nAlkenyl sum peaks: " + str(sum(alkenyl_peak_list)) 
                      + "\nFerrocene Integral Trapz: " + str(ferrocene_integral)
                      + "\nFerrocene sum peaks: " + str(sum(ferrocene_peak_list))
                      + "\nOA:Ferrocene Ratio: " + str(ratio) + "\n")
    
    #Close file
    infile.close()
    outfile.close()
    
#-----------------------------------------------------------------------------
#Get current chemical shift
#-----------------------------------------------------------------------------
def GetCurShift(line):
    return float(line.split("\t")[0])

#-----------------------------------------------------------------------------
#Build the x and y-axes lists
#-----------------------------------------------------------------------------
def BuildLists(line, cur_res, OA_shift_list, OA_peak_list, 
               Ferro_shift_list, Ferro_peak_list):
    lst = line.split("\t")
    if(cur_res <= UPPER_OA and cur_res >= LOWER_OA):
        peak = float(lst[1])
        OA_shift_list.append(cur_res)
        OA_peak_list.append(peak)
    elif (cur_res <= UPPER_FERRO and cur_res >= LOWER_FERRO):
        peak = float(lst[1])
        Ferro_shift_list.append(cur_res)
        Ferro_peak_list.append(peak)       
 
#-----------------------------------------------------------------------------
#Get avg delta x on the interval
#-----------------------------------------------------------------------------
def GetAvgDeltaX(lst):
    #local vars
    dif_list = []   #List to hold difference between adjacent elements 
                    #(i.e. [(x0 - x1), (x1 - x2), (xN-1 - xN)])
    size = len(lst) #Size of x lis
    
    #Iterate through file until you get to n - 1 element
    for ele in range (size - 1):
            dif = lst[ele] - lst[ele + 1]
            dif_list.append(dif)
            
    return (sum(dif_list))/(len(dif_list))     


#-----------------------------------------------------------------------------
#It calcualates the sum of the values from 2f(x1) + 2f(x2) + ... + 2f(xn−1)
#-----------------------------------------------------------------------------
def IntermediateValueSum(lst):
    summation = 0
    x = 1
    #Begin while loop at 2nd ele of list
    while (x < len(lst) - 1):
        summation += 2 * lst[x]
        x += 1
    
    return summation  

#-----------------------------------------------------------------------------
#Trapezoidal sum formula
#-----------------------------------------------------------------------------
def TrapezoidalSum(delta_x, intermed_sum, y_list):
    return (1/2) * delta_x * (y_list[0] + intermed_sum + y_list[-1])
   
#-----------------------------------------------------------------------------
#Prints an input number of rows of the list
#-----------------------------------------------------------------------------
def PrintList(x, y):
    rows = input("How many rows would you like to print? ")
    for ele in range(rows):
        print(str(x[ele]) + " " + str(y[ele]))
        

main()