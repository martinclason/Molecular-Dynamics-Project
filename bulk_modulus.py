from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState

#from asap3 import EMT
from ase.calculators.emt import EMT
from ase import atoms

from asap3 import Trajectory


atoms.calc = EMT()

configs = read("Cu.traj@0:5") # read 5 configurations

# Extract volumes and energies:

volumes = [cu.get_volume() for cu in configs]
energies = [cu.get_potential_energy() for cu in configs]
eos = EquationOfState(volumes, energies)
v0, e0, B = eos.fit()
print(B / kJ * 1.0e24, 'GPa')
eos.plot('Cu-eos.png')
