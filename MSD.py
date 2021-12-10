import matplotlib.pyplot as plt
import math
from simulationDataIO import inputSimulationData
import numpy as np

def MSD(t,atom_list):
    """The MSD(t,atom:list) function calculates and returns the mean square displacement for one time t.
    The function takes two arguments, the time t and atom_list which is a list of atom objects from .traj file.
    The time t is at what timestep of the simulation that the MSD is wanted to be calculated"""
    r0 = atom_list[0].get_positions()
    rt = atom_list[t].get_positions()
    N = len(r0)
    diff= rt-r0
    squareddiff = diff**2
    summ = sum(sum(squareddiff))
    normsum = (1/N) * summ
    return normsum #Å^2
#Calculates MSD for all the time steps and plots them
def make_MSD_plotter(data):
    """The make_MSD_plotter function takes in data dictionary from .json file, takes 
    the MSD data out from it and returns a plotter that can plot MSD over time"""
    def plotter():
        MSD_data = data["MSD"]
        dt = 2
        t = np.arange(0, len(MSD_data)*dt, dt)

        fig = plt.figure()
        ax = plt.axes()
        
        plt.ylabel("MSD-[Å]")
        plt.xlabel("Measured time step")
        plt.title("Mean Square Displacement") 

        ax.plot(t,MSD_data)
    return plotter  

def self_diffusion_coefficient(t, atom_list) :
    """The self_diffusion_coefficient(t, atom_list) function calculates and returns the
    self diffusion coefficient. The function takes two arguments, the time t and an 
    atom_list which it sends to the MSD(t,atom_list) function to retrieve the MSD. 
    The Lindemann_critertion() first checks if the element is a solid or liquid. For
    solids we approximate the self_diffusion_coefficient as 0 and for liquids the self 
    diffusion coefficient is taken as the slope of the mean-square-displacement."""
    if Lindemann_criterion(t, atom_list) or t==0 :
        return 0
    else :
        return 1/(6*t) * MSD(t, atom_list)

def Lindemann_criterion(t, atom_list) :
    """Checks if melting has occured. The functions takes the time t and a list of atoms as arguments.
    The lindemann criterion states that melting happens when the the root mean vibration exceeds 10%
    of the nearest neighbor (NN) distance. The function checks this condition by calling MSD() and
    returns True if the condition is met"""
    NN = atom_list[0].get_distance(0,1)
    return MSD(t,atom_list) > 0.1 * NN