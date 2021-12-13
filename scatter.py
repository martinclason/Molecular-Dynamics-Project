import numpy as np
import matplotlib.pyplot as plt
from aleErrors import ConfigError

from pudb import set_trace

import glob, os, sys

from simulationDataIO import inputSimulationData

#A help function to extract the .json files in the outfiles directory
def find_json_files(options):
    file_list = []
    outdir = options.get("scatter_dir") if options.get("scatter_dir") is not None else os.getcwd() 
    try:
        if os.path.isdir(os.path.join(os.getcwd(),outdir)):
            for file in glob.glob(os.path.join(os.getcwd(),outdir,"*.json")):
                file_list.append(file)
                print(file_list)
            return file_list
        else:
            raise ConfigError
    except ConfigError(outdir,"Does not exist"): 
        print(ERRROOOORRR)
    #if os.path.isdir(os.path.join(os.getcwd(),outdir)): #Checks if chosen directory exists
     #   for file in glob.glob(os.path.join(os.getcwd(),outdir,"*.json")):
      #      file_list.append(file)
       #     print(file_list)
        #if file_list == []:
         #   print("There where no .json files in the chosen diectory" + os.getcwd() + "/" + outdir + ".")
        #return file_list
    #else:
     #  print("The chosen directory " + os.getcwd() + "/" + outdir + " does not exist.")


def make_scatter_plotter(options,data_type1,data_type2,filelist=[]):
    """The function scatter_plot takes the arguments filelist, 
    data_type1 and data_type2. Filelist is a list of names 
    of the output files from analyse. data_type1 and data_type2 specifies
    what two data_types the functions is to do a scatter plot of. The function
    returns a scatter plot. """
    filelist = options.get("scatter_files") if options.get("scatter_files") != [] else find_json_files(options) 
    def scatter_plotter():
        if filelist is None:
            print("ERROR: Scatterplot could not be created!")
        else:
            fig = plt.figure()
            ax = plt.axes()
            for file in filelist:
                #if not os.path.isfile(file): #Checks if file in filelist exists in chosen directory
                    #print("File " + file + " does not exist.")
                #else:
                try:
                    data = inputSimulationData(file)
                except OSError:
                    print("Thats no file")
                    sys.exit()  
                if data_type1 == "time":
                    dt = 2
                    x = np.arange(0, len(data[data_type2])*dt, dt)
                else:
                    x = data[data_type1]                    
                y = data[data_type2]
                ax.scatter(x,y)
                plt.xlabel(data_type1)
                plt.ylabel(data_type2)

    return scatter_plotter
