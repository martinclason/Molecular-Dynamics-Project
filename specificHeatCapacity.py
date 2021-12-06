from ase.io.trajectory import Trajectory
import numpy as np
from ase import atoms, units
import sys

def specificHeatCapacity(ensemble, traj):
  """This function calculates the specific heat capacity from the trajectory output
  file and the ensemble that has been simulated."""

  # Calculates the number of atoms and the temperature of the simulated system.
  N = len(traj[1].get_positions()) # Number of atoms is the same as number of positions
  T = np.sum([atoms.get_temperature() for atoms in traj[-20:]])/20 # Average of last 10 itterations

  if ensemble == "NVE":
    # Calculates the kinetic energy per atom and then proceeds to calculate the 
    # variance in the kinetic energy per atom.
    total_energies = [atoms.get_kinetic_energy() for atoms in traj]
    total_energies = [energy / N for energy in total_energies] 
    var_e = np.var(total_energies)
    
    # Calculates the specific heat capacity when the NVE ensemble has been simulated.
    C_v = ((3*N*units.kB)/2) / (1 - (2/(3*(units.kB*T)**2))*var_e)

  elif ensemble == "NVT":
    # Calculates the variance in the total energy per atom
    total_energies = [atoms.get_total_energy() for atoms in traj]
    total_energies = [energy / N for energy in total_energies] 
    var_e = np.var(total_energies)

    # Calculates the specific heat capacity when the NVT ensemble has been simulated.
    C_v = 1/(units.kB*T**2) * var_e

  else:
    # Throws an exception if the specified ensemble isn't supported.
    raise Exception("Unknown ensemble: {}".format(ensemble))

  # Atomic mass unit in kg
  u = 1.66e-27 #kg
  # Calculates the mass of the simulated system in kg.
  m = np.sum(traj[0].get_masses()) * u

  # Converts the unit eV/K to kJ/kgK
  C_v = (1/ (units.kJ*m)) * C_v

  return C_v