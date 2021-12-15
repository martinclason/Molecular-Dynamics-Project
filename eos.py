import numpy as np

<<<<<<< HEAD
from asap3 import Atoms
from asap3 import Trajectory
from asap3 import EMT
=======
from ase import Atoms
from asap3 import Trajectory
from ase.calculators.emt import EMT
>>>>>>> ale_analyse

"""
This function creates atoms objects with varying lattice constants from a guessed
value, a, of the chosen element. Using the linspace function to choose range
and number of variations created, and saves them all in a traj file.

"""

def create_lattice_traj(symbol):

    a = 4.0  # approximate lattice constant
    b = a / 2
    ag = Atoms(symbol,
           cell=[(0, b, b), (b, 0, b), (b, b, 0)],
           pbc=1,
           calculator=EMT())  # use EMT potential
    cell = ag.get_cell()
    traj = Trajectory(symbol + ".traj", 'w')

    for x in np.linspace(0.85, 1.15, 100):
        ag.set_cell(cell * x, scale_atoms=True)
        ag.get_potential_energy()
        traj.write(ag)

    return traj

#create_lattice_traj(Pt)
#print(create_lattice_traj("Pt")[0].get_temperature())
