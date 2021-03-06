import matplotlib.pyplot as plt
import math
import numpy as np
import os


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
def make_MSD_plotter(data,dt):
    """The make_MSD_plotter function takes in data dictionary from .json file, takes
    the MSD data out from it and returns a plotter that can plot MSD over time"""
    def plotter():
        MSD_data = data["MSD"]
        t = np.arange(0, len(MSD_data)*dt, dt)

        fig = plt.figure()
        ax = plt.axes()

        plt.ylabel("MSD-[Å^2]")
        plt.xlabel("Time[fs]")
        plt.title("Mean Square Displacement")


        ax.plot(t,MSD_data)
    return plotter

def self_diffusion_coefficient(options, atom_list) :
    """The self_diffusion_coefficient(atom_list) function calculates and returns the
    self diffusion coefficient. The function takes an atom_list at different time steps
    which it sends to the MSD(t,atom_list) function to retrieve the MSD. It also takes
    options to convert time_step to seconds (time_step length may vary).
    The lindemann_critertion() first checks if the element is a solid or liquid. For
    solids we approximate the self_diffusion_coefficient as 0 and for liquids the self
    diffusion coefficient is taken as the slope of the mean-square-displacement.
    Self diffusion coefficient is returned in units m^2/s."""
    time_step = len(atom_list) - 1 #Take the system at the last accessible time
    step_length = options["dt"] # in fs
    t = time_step * step_length * 1E-15 #Convert time_step to seconds
    MSD_meter = 1E-20 * MSD(time_step, atom_list) #Convert from Å^2 to m^2
    if lindemann_criterion(atom_list) :
        return 1/(6*t) * MSD_meter #Self diffusion coefficient given in m^2/s
    else :
        return 0

def lindemann_criterion(atom_list) :
    """Checks if melting has occurred. The functions takes a list of atoms at different time steps.
    The lindemann criterion states that melting happens when the the root mean vibration exceeds 10%
    of the nearest neighbor (NN) distance. The function checks this condition by calling MSD() and
    returns True if the condition is met"""

    # TODO: Maybe dangerous to use tags like this if the order/index changes...

    size = atom_list[0].get_tags()[0]
    super_cell_x = atom_list[0].cell[0]
    unit_cell_x = super_cell_x / size
    #Nearest Neighbor distance from basis matrix
    NN = (unit_cell_x[0]**2 + unit_cell_x[1]**2 + unit_cell_x[2]**2)**(1/2)
    t = len(atom_list) - 1 #Take the system at the last accessible time
    return bool(math.sqrt(MSD(t,atom_list)) > 0.1 * NN)

