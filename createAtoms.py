from ase import Atoms

def createAtoms(options):
    """createAtoms(options) takes the argument options which is the key to read from the 
    configuration files. Parameters are loaded from the config.yaml file and the function
    then returns an Atoms/lattice object with the chosen parameters that can be used 
    for simulations."""
    pbc = options["pbc"]
    symbol = options["symbol"]
    size = options["size"]
    latticeconstant = options["latticeconstant"]    
    positions = options["positions"]
    cell = options["cell"]
    cell = [[x*latticeconstant for x in y] for y in cell] #Add lattice constant to basis matrix

    atoms = Atoms(symbol, 
        positions = positions,
        cell=cell,
        pbc=pbc)
    atoms = atoms.repeat(size) #this is the same as: atoms = atoms * size
    atoms.set_tags(size) #Save the size of supercell for later use
    #print("Initial lattice constants [Å]:", atoms.cell.cellpar()[0:3] / size)
    return atoms