from ase.io.trajectory import Trajectory
import numpy as np
from ase import atoms, units

def eV_to_J(eV):
  return eV*1.60218e-19

traj = Trajectory('Ar.traj')
dir(traj)
# [J]
# total_energies = [atoms.get_total_energy() for atoms in traj]
# var_e = np.var(total_energies)

# Boltzmann [J/K]
# k_B = 1.380649e-23
# Boltzmann [eV/K]
# k_B = 8.617333262145e-5
# Atomic mass unit
u = 1.66e-27 #kg

total_energies = [atoms.get_kinetic_energy() for atoms in traj]
N = len(traj[1].get_positions()) # Number of atoms is the same as number of positions
total_energies = [energy / N for energy in total_energies] # Energy per particle

# squared_total_energies = [energy**2 for energy in total_energies]
# time_avg_energies = 1/len(total_energies) * np.sum(total_energies)
# time_avg_energies_squared = 1/len(total_energies) * np.sum(squared_total_energies)
# time_avg_var_e = time_avg_energies_squared - time_avg_energies**2 

var_e = np.var(total_energies)

# Temperature [K]
T = np.sum([atoms.get_temperature() for atoms in traj]) / N
m = np.sum(traj[0].get_masses()) * u

# # Heat capacity [] if the NVT ensamble is used
# C_v = 1/(units.kB*T**2) * var_e

# # Heat capacity [] if the NVE ensamble is used
C_v = ((3*N*units.kB)/2) / (1 - (0.2/(3*(units.kB*T)**2))*var_e)
C_v = (1/ (units.kJ*m)) * C_v

print("Heat capacity for Ar:")
print(C_v)
