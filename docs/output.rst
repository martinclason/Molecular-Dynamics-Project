Output from `ale`
=================

The simulation output consists of three files (which can be placed in a directory
if specified by the user), one called `raw<element(s)>.traj` (if the equilibirium check 
is enabled) which stores the entire simulation from start to finnish, on file named 
`<element(s)>.traj` which stores the simulation from equilibirium and onwards and this 
file is what `ale analyze` uses to calculate the output properties (specified in the 
config file) in the last output file named `<element(s)>.json`. 

The properties .json-file is a line json file which enables large data sets to be handled 
since the computer only reads a single line into memory each time rather than the entire 
file. The unit on each calculated property is specified in the entry name of each property.

Output from `ale multi`
=======================

The nameing of the output files (of each simulation) is the same for `ale multi` as for 
the normal mode in `ale` but `ale multi` requires the user to specify an output directory 
to enable organising the output files and later specify the entire directory to ale visualize,  
when creating scatter plots. 