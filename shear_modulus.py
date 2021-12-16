from ase import Atoms
import math
from ase.calculators.kim.kim import KIM
from create_potential import create_potential
from bulk_modulus import read_cell, read_lattice_constant

def shear_modulus(options) :
    """Shear_modulus takes one argument, options (a config-file), 
    and returns the shear modulus for the element/molecule defined
    by the config-file."""
    symbols = options["symbol"]
    interatomic_positions = options["scaled_positions"]
    size = options["size"]
    latticeconstant = read_lattice_constant(options)
    old_basis_matrix = read_cell(options)
    old_cell = [[x*latticeconstant for x in y] for y in old_basis_matrix] #Add lattice constant to basis matrix
    new_cell = old_cell #Initialize the sheared cell
    displacement_angle = math.radians(5)
    for i in range(2):
        old_x = old_cell[i][0]
        old_z = old_cell[i][2]
        
        new_x = old_x + old_z * math.sin(displacement_angle)
        new_cell[i][0] = new_x
        
        new_z = old_z * math.cos(displacement_angle)
        new_cell[i][2] = new_z

    atoms = Atoms(symbols, scaled_positions = interatomic_positions, cell = new_cell, pbc = True)
    atoms = atoms.repeat([size,size,size])
    atoms.calc = create_potential(options)
    stress_z = (atoms.get_stress()[3]**2 + atoms.get_stress()[4]**2)**(1/2)
    unit_conversion = 160.21766208 * 10**9 # ev/Angstrom^3 to GPa to Pascal
    # shear stress z-component divided by tan of displacement angle
    # ASE provides stress-component in ev/A^3 which is converted to
    # pascal by unit_conversion. The factor 0.5 comes from the
    # definition of engineering shear strain
    G = stress_z/(math.tan(displacement_angle)) * unit_conversion * 0.5 
    return G