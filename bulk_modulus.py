from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState
import math as m
from asap3 import Trajectory



configs = Trajectory('Ag.traj')



# Extract volumes and energies:

volumes = [ag.get_volume() for ag in configs]
energies = [ag.get_potential_energy() for ag in configs]
eos = EquationOfState(volumes, energies)
v0, e0, B = eos.fit()
print(B / kJ * 1.0e24, 'GPa')
eos.plot('Pt-eos.png', show = False)
a0 = (4 * v0)**(1/3)
#a0 = m.pow(v0, 1/3) * m.sqrt(2)
#print(B)
print("Optimal volume is: " + str(v0))
print("Optimal lattice constant is: " + str(a0))
