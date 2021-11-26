from ase.io.trajectory import Trajectory
import numpy as np
from ase import units

def eV_to_J(eV):
  return eV*1.60218e-19

traj = Trajectory('Ar.traj')
dir(traj)
# [J]
total_energies = [atoms.get_total_energy() for atoms in traj]
var_e = np.var(total_energies)

# Boltzmann [J/K]
# k_B = 1.380649e-23
# Boltzmann [eV/K]
# k_B = 8.617333262145e-5

# Temperature [K]
T = 40
N = len(total_energies)

# Heat capacity [] if the NVT ensamble is used
C_v = 1/(units.kB*T**2) * var_e

# # Heat capacity [] if the NVE ensamble is used
# total_energies = [atoms.get_kinetic_energy() for atoms in traj]
# var_e = np.var(total_energies)
# C_v = ((3*N*units.kB)/2) * ((1- (2/(3*(units.kB*T)**2))*var_e)**-1)

print("Heat capacity for Ar:")
print(C_v)
