import numpy as np
import matplotlib.pyplot as plt

from simulationDataIO import inputSimulationData

def scatter_plot(filelist,data_type1,data_type2):
    """The function scatter_plot takes the arguments filelist, 
    data_type1 and data_type2. Filelist is a list of names 
    of the output files from analyse. data_type1 and data_type2 specifies
    what two data_types the functions is to do a scatter plot of. The function
    returns a scatter plot. """

    for file in filelist:
        data = inputSimulationData(file)
        x = data[data_type1]
        y = data[data_type2]
        plt.scatter(x,y)
        plt.xlabel(data_type1)
        plt.ylabel(data_type2)
    plt.show()