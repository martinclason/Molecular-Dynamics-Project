import numpy as np
from ase import Atoms


def pressure(forces, volume, positions, temperature, number_of_atoms, kinetic_energy):

    forces_times_positions = sum(np.dot(x,y) for x, y in zip(positions, forces))

    instant_pressure = (1/3 * volume) * ((2 * number_of_atoms * kinetic_energy)
                            + forces_times_positions)

    print("The instant pressure is: " + str(instant_pressure))

    return instant_pressure



def printpressure(atoms):
     """Function to calculate and print the instant pressure in XXX for every timestep """
     forces_times_positions = sum(np.dot(x,y) for x, y in
                            zip(atoms.get_positions(), atoms.get_forces()))

     instant_pressure = ((1/(3 * atoms.get_volume())) * ((2 * len(atoms) *
     atoms.get_kinetic_energy()) + forces_times_positions))

     print("The instant pressure is: " + str(instant_pressure))
