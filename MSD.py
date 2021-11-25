import matplotlib.pyplot as plt
import math

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
    return normsum
#Calculates MSD for all the time steps and plots them
def MSD_plot(time,atom_list):
    """The MSD_plot(time,atom_list) function calculates the MSD for every timestep in the simulation 
    from .traj file. It returns a plot of the MSD over time."""
    MSD_data = []
    for t in range(time):
        MSD_data.append(MSD(t,atom_list))
    plt.plot(range(time),MSD_data)
    plt.ylabel("MSD-[Å]")
    plt.xlabel("Measured time step")
    plt.title("Mean Square Displacement")
    plt.show()

def self_diffusion_coefficient(t, atom_list) : #for liquids only
    """The self_diffusion_coefficient(t, atom_list) function calculates and returns the
    self diffusion coefficient for a liquid. The function takes two arguments, the time
    t and an atom_list which it sends to the MSD(t,atom_list) function to retrieve the
    MSD. The self diffusion coefficient is then taken as the slope of the
    mean-square-displacement."""
    return 1/(6*t) * MSD(t, atom_list)