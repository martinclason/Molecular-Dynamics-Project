import matplotlib.pyplot as plt
import math


def density(atoms_object):
    """The function 'density()' takes a time t, a list of atoms from .traj file
    and config options as argument and calculates the density of the chosen
    time step t. Prints and returns density in g/cm^3"""
    m = sum(atoms_object.get_masses()) * (1.6605387E-24)
    V = atoms_object.cell.volume*10**(-24)
    density = m/V

    return density

# TODO: Should we keep density plot? Might need some restructuring since density() now takes atoms_object instead of atom_list
def density_plot(time,atom_list,options):
    """The function 'density_plot()' takes an amount of timesteps, a list of atoms
    from a .traj file amd options from config file and plots the density over time.
    This can be used if the Volume is not constant over time."""
    density_data=[]
    for t in range(time):
        density_data.append(density(t,atom_list,options))
    plt.plot(range(time),density_data)
    plt.ylabel("g/cm^3")
    plt.xlabel("Measured time step")
    plt.title("The density of " + options["symbol"] + " over time")
    plt.show()

