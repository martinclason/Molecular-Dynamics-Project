from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState
import math as m
from asap3 import Trajectory

"""
This function takes a traj-file containing atom-objects wirh varying
lattice constants, calculates the Bulk modulus B, optimal volume v0 and optimal
lattice constant a0 through equation of state.

"""

configs = Trajectory('Ag.traj')

# Extract volumes and energies:

volumes = [ag.get_volume() for ag in configs]
energies = [ag.get_potential_energy() for ag in configs]
eos = EquationOfState(volumes, energies)
v0, e0, B = eos.fit()
print(B / kJ * 1.0e24, 'GPa')
eos.plot('Pt-eos.png', show = False)
a0 = (4 * v0)**(1/3)


print("Optimal volume is: " + str(v0))
print("Optimal lattice constant is: " + str(a0))
