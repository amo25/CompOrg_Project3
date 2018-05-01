To run this program: Run the Python 3.6 script
"simulate.py" on your system in your preferred way.
On Windows, one can open Powershell and type "python .\simulate.py".
Make sure you have Python 3.6 installed.
This program takes no arguments, but requires a trace file located
in the same directory as the script to run. The default name 
for this input file is "test.trace".
If you wish to change the name of the default input file, please 
change the line:

                #parse the file
                file = open("test.trace", "r")
				
In "simulate.py". (This is around line 79, though cntrl+f is faster).
Change "test.trace" to whatever file name you want. Ensure that the input file matches the conventions seen in "test.trace".

The program outputs a file with the simulation results. By default this output file is called "test.result"