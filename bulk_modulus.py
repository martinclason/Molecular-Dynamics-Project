from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState
import math as m
from asap3 import Trajectory
from ase.lattice.cubic import FaceCenteredCubic

"""
This function takes a traj-file containing atom-objects wirh varying
lattice constants, calculates the Bulk modulus B, optimal volume v0 and optimal
lattice constant a0 through equation of state.

"""



ag = FaceCenteredCubic(directions = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
                        , size = (1,1,1), symbol = 'Ag', pbc=1)

def calc_lattice_constant(element):

    configs = Trajectory(element)
    volumes = [element.get_volume() for element in configs]
    energies = [element.get_potential_energy() for element in configs]

    eos = EquationOfState(volumes, energies)
    v0, e0, B = eos.fit()
    #print(B / kJ * 1.0e24, 'GPa')
    eos.plot('Pt-eos.png', show = False)
    a0 = (4 * v0)**(1/3)
    return [a0, B]

print("Optimal lattice constant (calculated) is: " + str(calc_lattice_constant('Ag.traj')) + " Å")
print("Optimal lattice constant (table) is: " + ag.latticeconstant() + " Å")


#print("Optimal volume is: " + str(v0))
#print("Optimal lattice constant is: " + str(a0))
