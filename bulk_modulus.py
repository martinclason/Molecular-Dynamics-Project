from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState



from asap3 import Trajectory
configs = Trajectory('Ag.traj')
#configs = read('Ag.traj@0:5')
#configs = read('Cu.traj')


# Extract volumes and energies:

volumes = [ag.get_volume() for ag in configs]
energies = [ag.get_potential_energy() for ag in configs]
eos = EquationOfState(volumes, energies)
v0, e0, B = eos.fit()
#print(B / kJ * 1.0e24, 'GPa')
eos.plot('Ag-eos.png')
print(B)
