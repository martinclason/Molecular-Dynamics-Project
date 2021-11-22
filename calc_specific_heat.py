from ase.io.trajectory import Trajectory
import numpy as np

def eV_to_J(eV):
  return eV*1.60218e-19

traj = Trajectory('Ar.traj')
dir(traj)
# [J]
total_energies = [eV_to_J(atoms.get_total_energy()) for atoms in traj]
var_e = np.var(total_energies)

# Boltzmann [J/K]
k_B = 1.380649e-23
# Boltzmann [eV/K]
#k_B = 8.617333262145e-5

# Temperature [K]
T = 40

# Heat capacity []
C_v = 1/(k_B*T**2) * var_e

print("Heat capacity for Ar:")
print(C_v)
