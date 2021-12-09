import numpy as np
import matplotlib.pyplot as plt

import glob, os

from simulationDataIO import inputSimulationData

#A help function to extract the .json files in the outfiles directory
def find_json_files():
    file_list = []
    os.chdir(os.getcwd() + "/outfiles")
    for file in glob.glob("*.json"):
        file_list.append(file)
    os.chdir(os.getcwd().replace("/outfiles",''))
    return file_list


def make_scatter_plotter(data_type1,data_type2,filelist=find_json_files()):
    """The function scatter_plot takes the arguments filelist, 
    data_type1 and data_type2. Filelist is a list of names 
    of the output files from analyse. data_type1 and data_type2 specifies
    what two data_types the functions is to do a scatter plot of. The function
    returns a scatter plot. """
    def scatter_plotter():
        fig = plt.figure()
        ax = plt.axes()

        for file in filelist:
            os.chdir(os.getcwd() + "/outfiles")
            data = inputSimulationData(file)
            os.chdir(os.getcwd().replace("/outfiles",''))
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

