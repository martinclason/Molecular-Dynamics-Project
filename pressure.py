from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
# from asap3.md.verlet import VelocityVerlet

from ase import units
from ase.visualize import view
from asap3 import Trajectory
#from asap3 import LennardJones
#from xtb.ase.calculator import XTB
#from ase.io import read

import numpy as np


atoms = FaceCenteredCubic(
      directions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
      symbol = "Cu",
      size = (2, 2, 2),
      pbc = True)

#atoms_volume_init = atoms.get_volume()
#print ("Initial volume is: " + str(atoms_volume_init))

#atoms_temp_init = atoms.get_temperature()
#print ("Initial temperature is: " + str(atoms_temp_init))



#view(atoms)

# Use Asap for a huge performance increase if it is installed
use_asap = False

if use_asap:
       from asap3 import EMT
       size = 10
else:
       from ase.calculators.emt import EMT
       #size = 3

# Describe the interatomic interactions with the Effective Medium Theory
atoms.calc = EMT()
#atoms.calc = LennardJones("cu", "1", "1")
#atoms.calc = XTB(method="GFN2-xTB")



    # Set the momenta corresponding to T=300K
MaxwellBoltzmannDistribution(atoms, temperature_K=300)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.


traj = Trajectory("cu.traj", "w", atoms, properties="forces")
dyn.attach(traj.write, interval=1)
dyn.run(10)

traj.close()
traj_read = Trajectory("cu.traj")

atoms_volume = traj_read[1].get_volume()
atoms_positions = traj_read[1].get_positions()
atoms_kinetic_energy = traj_read[1].get_kinetic_energy()
atoms_forces = traj_read[1].get_forces()
atoms_temperature = traj_read[1].get_temperature()
atoms_number_of_atoms = len(atoms)

def pressure_calc(forces, volume, positions, temperature,
 number_of_atoms, kinetic_energy):

    forces_times_positions = sum(np.dot(x,y) for x, y in zip(positions, forces))

    instant_pressure = (1/3 * volume) * ((2 * number_of_atoms * kinetic_energy)
                            + forces_times_positions)

    print("The instant pressure is: " + str(instant_pressure))

    #return instant_pressure

pressure_calc(atoms_forces, atoms_volume, atoms_positions,
    atoms_temperature, atoms_number_of_atoms, atoms_kinetic_energy)

#print("The instant pressure is: " + str(instant_pressure))

#def instant_pressure(atoms_volume, atoms_number_of_atoms, atoms_kinetic_energy_one,
#                    forces_times_positions):


#print("The instant pressure is " + str(instant_pressure))

#print("Volume of atom one: " + str(atoms_volume_one))
#print("Position of atom one: " + str(atoms_position_one))
#print("Kinetic energy of atom one: " + str(atoms_kinetic_energy_one))
#print("Forces on atom one: " + str(atoms_forces_one))
#print("Temperature of atom one: " + str(atoms_temperature_one))
#print("Number of atoms: " + str(atoms_number_of_atoms))

#print("Force times position for atom one: " + str(force_times_position_one))

#print ("atoms_volume_final = " + str(atoms_volume_final))
#print("Final volume is: " + str(atoms_volume_final))
#print("Final volume is: " +  str(traj_read[10].get_volume()))
#print("Final temperature is: " +  str(traj_read[0].get_temperature()))

#print("Position of atom one: " + str(traj_read[0].get_positions()[0]))
#print("Initial position of second atom: " + str(traj_read[0].get_positions()[1]))
#print("Second position of first atom: " + str(traj_read[1].get_positions()[0]))
#print("Kinetic energy after 10 timesteps: " + str(traj_read[1].get_kinetic_energy()))
#print("Kinetic energy after 20 timesteps: " + str(traj_read[2].get_kinetic_energy()))
#print("Initial forces on first atom: " + str(traj_read[0].get_forces()[0]))
#print("Number of atoms: " + str(atoms_number_of_atoms))
