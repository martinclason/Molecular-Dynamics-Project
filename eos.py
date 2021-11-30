import numpy as np

from asap3 import Atoms
from asap3 import Trajectory
from asap3 import EMT


a = 3.52  # approximate lattice constant
b = a / 2
ag = Atoms('Pt',
           cell=[(0, b, b), (b, 0, b), (b, b, 0)],
           pbc=1,
           calculator=EMT())  # use EMT potential
cell = ag.get_cell()
traj = Trajectory('Pt.traj', 'w')
for x in np.linspace(0.95, 1.05, 1000):
    ag.set_cell(cell * x, scale_atoms=True)
    ag.get_potential_energy()
    traj.write(ag)
