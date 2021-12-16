import numpy as np
from ase import atoms


def pressure(atoms_object):
    forces = atoms_object.get_forces()
    volume = atoms_object.get_volume()
    kinetic_energy = atoms_object.get_kinetic_energy()
    positions = atoms_object.get_positions()
    number_of_atoms_object = len(positions) #TODO: Is this indexed correctly?
    temperature = atoms_object.get_temperature()

    forces_times_positions = sum(np.dot(x,y) for x, y in zip(positions, forces))

    instant_pressure = (1/3 * volume) * ((2 * number_of_atoms_object * kinetic_energy)
                            + forces_times_positions)
    return instant_pressure

def avg_pressure(traj):
    pressure_sum = sum(pressure(atoms) for atoms in traj)
    avg_pressure = pressure_sum / len(traj)
    return avg_pressure



    def printpressure(atoms_object):
        """Function to calculate and print the instant pressure in XXX for every timestep """
        forces_times_positions = sum(np.dot(x,y) for x, y in
        zip(atoms_object.get_positions(), atoms_object.get_forces()))

        instant_pressure = ((1/(3 * atoms_object.get_volume())) * ((2 * len(atoms_object) *
        atoms_object.get_kinetic_energy()) + forces_times_positions))

        print("The instant pressure is: " + str(instant_pressure))
