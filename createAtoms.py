from asap3 import Atoms
from bulk_modulus import calc_lattice_constant, read_cell, read_lattice_constant

def createAtoms(options):
    """createAtoms(options) takes the argument options which is the key to read from the 
    configuration files. Parameters are loaded from the config.yaml file and the function
    then returns an Atoms/lattice object with the chosen parameters that can be used 
    for simulations."""
    pbc = options["pbc"]
    symbol = options["symbol"]
    size = options["size"]
    scaled_positions = options["scaled_positions"]
    cell = read_cell(options)
    latticeconstant = read_lattice_constant(options)
    cell = [[x*latticeconstant for x in y] for y in cell] #Add lattice constant to basis matrix
    atoms = Atoms(symbol, 
        scaled_positions = scaled_positions,
        cell=cell,
        pbc=pbc)
    atoms = atoms.repeat(size) #this is the same as: atoms = atoms * size
    atoms.set_tags(size) #Save the size of supercell for later use
    return atoms