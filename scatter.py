import numpy as np
import matplotlib.pyplot as plt

import glob, os, sys

from simulationDataIO import inputSimulationData

#A help function to extract the .json files in the outfiles directory
def find_json_files(options):
    file_list = []
    outdir = options["scatter_dir"] if options["scatter_dir"] else ''
    if os.path.isdir(os.getcwd() + "/" + outdir): #Checks if chosen directory exists
        os.chdir(os.getcwd() + "/" + outdir)
        for file in glob.glob("*.json"):
            file_list.append(file)
        os.chdir(os.getcwd().replace(outdir,''))
        if file_list == []:
            print("There where no .json files in the chosen diectory" + os.getcwd() + "/" + outdir + ".")
        return file_list
    else:
        print("The chosen directory " + os.getcwd() + "/" + outdir + " does not exist.")


def make_scatter_plotter(options,data_type1,data_type2,filelist=[]):
    """The function scatter_plot takes the arguments filelist, 
    data_type1 and data_type2. Filelist is a list of names 
    of the output files from analyse. data_type1 and data_type2 specifies
    what two data_types the functions is to do a scatter plot of. The function
    returns a scatter plot. """
    filelist = options["scatter_files"] if options["scatter_files"] != [] else find_json_files(options)  
    def scatter_plotter():
        if filelist is None:
            print("ERROR: Scatterplot could not be created!")
        else:
            fig = plt.figure()
            ax = plt.axes()
            for file in filelist:
                if not os.path.isfile(file): #Checks if file in filelist exists in chosen directory
                    print("File " + file + " does not exist.")
                else:
                    if options["scatter_dir"]:
                        os.chdir(os.getcwd() + "/" + options["scatter_dir"])
                        data = inputSimulationData(file)
                        os.chdir(os.getcwd().replace(options["scatter_dir"],''))
                    else:
                        data = inputSimulationData(file)
                    
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

