from ase import Atoms

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
    atoms = Atoms(symbol, 
        scaled_positions = scaled_positions,
        cell=cell,
        pbc=pbc)
    atoms = atoms.repeat(size) #this is the same as: atoms = atoms * size
    atoms.set_tags(size) #Save the size of supercell for later use
    return atoms

def read_cell(options):
    cell = options["cell"]
    if cell in ["fcc", "FCC", "facecenteredcubic", "FaceCenteredCubic"] :
        cell = [[0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0]]
    elif cell in ["bcc", "BCC","bodycenteredcubic", "BodyCenteredCubic"] :
        cell = [[-0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5]]
    elif cell in ["sc", "SC","simplecubic","SimpleCubic"] :
        cell = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    latticeconstant = options["latticeconstant"]
    cell = [[x*latticeconstant for x in y] for y in cell] #Add lattice constant to basis matrix
    return cell