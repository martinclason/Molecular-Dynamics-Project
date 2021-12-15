from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState
import math as m
from asap3 import Trajectory
from ase.lattice.cubic import FaceCenteredCubic
import numpy as np
from asap3 import Atoms
from asap3 import EMT

#from ase.calculators.kim.kim import KIM
#import kimpy



"""
This function creates atoms objects with varying lattice constants from a guessed
value, a, of the chosen element. Using the linspace function to choose a range
and number of variations created, and saves them all in a traj file.

"""

def create_lattice_traj(symbol):

    a = 4.0  # approximate lattice constant
    b = a / 2
    ag = Atoms(symbol,
           cell=[(0, b, b), (b, 0, b), (b, b, 0)],
           #cell=[(-b, b, b), (b, -b, b), (b, b, -b)],
           pbc=1,
           calculator=EMT())#KIM("LJ_ElliottAkerson_2015_Universal__MO_959249795837_003"))
    cell = ag.get_cell()
    traj = Trajectory(symbol + "_X.traj", 'w')

    for x in np.linspace(0.85, 1.15, 1000):
        ag.set_cell(cell * x, scale_atoms=True)
        ag.get_potential_energy()
        traj.write(ag)

    return traj


"""
This function takes a traj-file containing atom-objects wirh varying
lattice constants, calculates the Bulk modulus B, optimal volume v0 and optimal
lattice constant a0 through equation of state.

"""



#ag = FaceCenteredCubic(directions = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
#                        , size = (1,1,1), symbol = 'Ag', pbc=1)

def calc_lattice_constant(element):

    create_lattice_traj(str(element))

    configs = Trajectory(element + "_X.traj")
    volumes = [element.get_volume() for element in configs]
    energies = [element.get_potential_energy() for element in configs]

    eos = EquationOfState(volumes, energies)
    v0, e0, B = eos.fit()
    #print(B / kJ * 1.0e24, 'GPa')
    eos.plot('Pt-eos.png', show = False)
    a0 = (4 * v0)**(1/3)
    B0 = (B / kJ * 1.0e24)
    return [a0, B0]


#print("Optimal lattice constant (calculated) is: " + str(calc_lattice_constant("Au")[0]) + " Å")
#print("The bulk modulus is :" + str(calc_lattice_constant("Al")[1]) +" GPa" )
#print("Optimal lattice constant (table) is: " + "BLABLA " + " Å")


#print("Optimal volume is: " + str(v0))
#print("Optimal lattice constant is: " + str(a0))
