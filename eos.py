import numpy as np

from asap3 import Atoms
from asap3 import Trajectory
from asap3 import EMT

"""
This function creates atoms objects with varying lattice constants from a guessed
value, a, of the chosen element. Using the linspace function to choose range
and number of variations created, and saves them all in a traj file.

"""

a = 4.0  # approximate lattice constant
b = a / 2
ag = Atoms('Cu',
           cell=[(0, b, b), (b, 0, b), (b, b, 0)],
           pbc=1,
           calculator=EMT())  # use EMT potential
cell = ag.get_cell()
traj = Trajectory('Cu.traj', 'w')
for x in np.linspace(0.85, 1.15, 100):
    ag.set_cell(cell * x, scale_atoms=True)
    ag.get_potential_energy()
    traj.write(ag)
