# integrate-nmr-data-py
Basic Script to perform trapezoidal sum on NMR peak list data (*.asc)

Documentation:
   Tkinter:
   https://www.python-course.eu/tkinter_dialogs.php
   https://wiki.python.org/moin/TkInter
   

Plans:
1. https://matplotlib.org/3.1.3/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py    
2. Figure out how this integral is displayed!!
   https://matplotlib.org/3.1.1/gallery/showcase/integral.html
3. Improve file reading mechanism to stop when all needed data is integrated.

Purpose: This program parses the chemical shift and real intensity values 
of NMR data (.asc format) into two separate lists. 
It then calculates the integral on the desired interval based on the 
trapezoidal sum. 

Data Format and Parsing: Each line of data is formatted as the
following: "chemicalShift\trealValue\timaginaryValue\n".
I split each line of data into a list based on the \t separator.
Therefore, an individual instance of this line list may look like the following:
["12.31", "0.008", "-0.007\n"].
I have the program start making the chemical shift and peak list when
the first chemical shift within the specified bounds is encountered. For
example, the program begins to construct the alkenyl chemical shift and 
peak list when the chemical shift is 5.9 ppm and 
then it stops constructing this list when the chemical shift is less than 5.4 ppm. 
It then constructs the ferrocene chemical shift and peak list in the same way. 

Mathematics: After parsing the data and creating the appropriate lists
the trapezoidal sum formula is used.
Tn = Δx/2 [f(x0)+ 2f(x1) + 2f(x2) + ... + 2f(xn−1) +f(xn)].
Delta x is the average of delta x over all x values within the specified interval. 
I constructed a list of delta x's as follows:
[x0 - x1, x1 - x2, (xn - 1) - xn] then summed that list and took the average
to define delta x in the formula Tn.
The sum from 2f(x1) + 2f(x2) + ... + 2f(xn−1) is calculated independently and
then plugged into the trapezoidal sum formula Tn.

Validated Maths: numpy has composite trapezoidal rule function. Its 
result matches my own.

9.2 mg/mL OA-QD
20200410_JGF_Oleate-capped_CdSe_QD_PROTON.asc 

4.6 mg/mL OA-QD
20200410_JGF_oleate-capped_CdSe_QD_Quality_Control_PROTON.asc
