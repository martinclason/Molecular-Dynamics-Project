from ase.lattice.cubic import SimpleCubic, BodyCenteredCubic, FaceCenteredCubic
from ase import Atoms


def createAtoms(options):
    """createAtoms(options) takes the argument options which is the key to read from the 
    configuration files. Parameters are loaded from the config.yaml file and the function
    then returns an Atoms/lattice object with the chosen parameters that can be used 
    for simulations."""
    pbc = options["pbc"]
    symbol = options["symbol"]
    size = options["size"]
    latticeconstants = options["latticeconstants"]
    bravaislattice = options["bravaislattice"]

    if bravaislattice:
        atoms = createBravaislattice(options)
    else :
        cell = options["cell"]
        cell = [[x*latticeconstants[0] for x in y] for y in cell]
        atoms = Atoms(symbol,
            cell=cell,
            pbc=pbc)
        atoms = atoms.repeat(size) #this is the same as: atoms = atoms * size
    return atoms

def createBravaislattice(options):
    """createBravaislattice takes the argument options which is the key to read from the 
    configuration files. Parameters are loaded from the config.yaml file and the function
    then returns a lattice object with the chosen parameters that can be used 
    for simulations."""
    directions = options["directions"]
    pbc = options["pbc"]
    symbol = options["symbol"]
    size = options["size"]
    latticeconstants = options["latticeconstants"]
    bravaislattice = options["bravaislattice"]
    if(bravaislattice == "SC") :
        return SimpleCubic(directions = directions,
                            symbol = symbol,
                            size = size, pbc = pbc,
                            latticeconstant = latticeconstants[0] if latticeconstants else None)
    if(bravaislattice == "BCC") :
        return BodyCenteredCubic(directions = directions,
                            symbol = symbol,
                            size = size, pbc = pbc,
                            latticeconstant = latticeconstants[0] if latticeconstants else None)
    if(bravaislattice == "FCC") :
        return FaceCenteredCubic(directions = directions,
                            symbol = symbol,
                            size = size, pbc = pbc,
                            latticeconstant = latticeconstants[0] if latticeconstants else None)