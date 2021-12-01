from ase.io.trajectory import Trajectory
import numpy as np
import sys
from ase import atoms, units

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ensambleError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def specificHeatCapacity(ensamble, trajectory_file):
  """This function calculates the specific heat capacity from a trajectory file but the ensamble
  used during the simulation needs to be specified in the 'ensamble' argument."""

  traj = Trajectory(trajectory_file)
  dir(traj)

  # Reads the number of particles and temperature of the simulated system.
  N = len(traj[1].get_positions()) # Number of atoms is the same as number of positions
  T = np.sum([atoms.get_temperature() for atoms in traj]) / N
  try:
    if ensamble == "NVE":
      # Reads the energy from the .traj-file and divides it by the number of atoms to get
      # the energy per atom.
      total_energies = [atoms.get_kinetic_energy() for atoms in traj]
      total_energies = [energy / N for energy in total_energies]

      # Calculates the variance of the kinetic energy.
      var_e = np.var(total_energies)

      # Calculates the specific heat capacity when the NVE ensamble has been simulated.
      C_v = ((3*N*units.kB)/2) / (1 - (0.2/(3*(units.kB*T)**2))*var_e)

    elif ensamble == "NVT":
      # Reads the energy from the .traj-file and divides it by the number of atoms to get
      # the energy per atom.
      total_energies = [atoms.get_total_energy() for atoms in traj]
      total_energies = [energy / N for energy in total_energies]

      var_e = np.var(total_energies)

      # Calculates the specific heat capacity when the NVT ensamble has been simulated.
      C_v = 1/(units.kB*T**2) * var_e

  except ensambleError:
    print("Unkown ensamble. Ensamble specified:")
    print(ensamble)

  # Atomic mass unit
  u = 1.66e-27 #kg
  # Calculates the mass of the system in kg
  m = np.sum(traj[0].get_masses()) * u

  # Converting the unit from eV/K to kJ/(kgK)
  C_v = (1/ (units.kJ*m)) * C_v

  return C_v
