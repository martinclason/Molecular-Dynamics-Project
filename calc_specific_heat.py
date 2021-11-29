from ase.io.trajectory import Trajectory
import numpy as np
from ase import units

def eV_to_J(eV):
  return eV*1.60218e-19

traj = Trajectory('Cu.traj')
dir(traj)
# [J]
# total_energies = [atoms.get_total_energy() for atoms in traj]
# var_e = np.var(total_energies)

# Boltzmann [J/K]
# k_B = 1.380649e-23
# Boltzmann [eV/K]
# k_B = 8.617333262145e-5

total_energies = [atoms.get_kinetic_energy() for atoms in traj]
squared_total_energies = [energy**2 for energy in total_energies]
time_avg_energies = 1/len(total_energies) * np.sum(total_energies)
time_avg_energies_squared = 1/len(total_energies) * np.sum(squared_total_energies)
time_avg_var_e = time_avg_energies_squared - time_avg_energies**2 

# Temperature [K]
T = 300
N = len(total_energies)

# # Heat capacity [] if the NVT ensamble is used
# C_v = 1/(units.kB*T**2) * var_e

# # Heat capacity [] if the NVE ensamble is used
C_v = ((3*N*units.kB)/2) * ((1- (2/(3*(units.kB*T)**2))*time_avg_var_e)**-1)

print("Heat capacity for Cu:")
print(C_v)
