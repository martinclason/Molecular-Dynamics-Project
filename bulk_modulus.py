from ase.io import read
from ase.units import kJ
from ase.eos import EquationOfState
import math as m
from asap3 import Trajectory
import numpy as np
from asap3 import Atoms
from create_potential import create_potential

def create_lattice_traj(options):
    """ This function creates atoms objects with varying lattice constants from a guessed
    value, a, of the chosen element. Using the linspace function to choose a range
    and number of variations created, and saves them all in a traj file."""
    a = 4 # approximate lattice constant, default value = 4
    if options["guess_latticeconstant"] :
        a = options["guess_latticeconstant"]
    symbol = options["symbol"]
    basis_matrix = read_cell(options)
    primitive_cell = [[x*a for x in y] for y in basis_matrix] #Add lattice constant to basis matrix
    calc = create_potential(options)
    interatomic_positions = options["scaled_positions"]
    atoms = Atoms(symbol,
           cell = primitive_cell,
           pbc=1,
           scaled_positions = interatomic_positions,
           calculator=calc)
    cell = atoms.get_cell()
    traj = Trajectory(symbol + "_X.traj", 'w')

    for x in np.linspace(0.85, 1.15, 1000):
        atoms.set_cell(cell * x, scale_atoms=True)
        atoms.get_potential_energy()
        traj.write(atoms)

    return traj

def calc_lattice_constant(options):
    """ This function takes a traj-file containing atom-objects wirh varying
    lattice constants, calculates the Bulk modulus B, optimal volume v0 and optimal
    lattice constant a0 through equation of state."""
    create_lattice_traj(options)
    element = options["symbol"]
    configs = Trajectory(element + "_X.traj")
    volumes = [element.get_volume() for element in configs]
    energies = [element.get_potential_energy() for element in configs]

    eos = EquationOfState(volumes, energies)
    v0, e0, B = eos.fit()
    #print(B / kJ * 1.0e24, 'GPa')
    eos.plot('Pt-eos.png', show = False)
    a0 = (4 * v0)**(1/3)
    B0 = (B / kJ * 1.0e24)
    return [a0, B0, v0]

def read_cell(options):
    cell = options["cell"]
    if cell in ["fcc", "FCC", "facecenteredcubic", "FaceCenteredCubic"] :
        cell = [[0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0]]
    elif cell in ["bcc", "BCC","bodycenteredcubic", "BodyCenteredCubic"] :
        cell = [[-0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5]]
    elif cell in ["sc", "SC","simplecubic","SimpleCubic"] :
        cell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    return cell

def read_lattice_constant(options) :
    if options["latticeconstant"] :
        return options["latticeconstant"]
    else :
        return calc_lattice_constant(options)[0]
