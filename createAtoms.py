from ase.lattice.cubic import SimpleCubic, BodyCenteredCubic, FaceCenteredCubic
from ase import Atoms
from aleErrors import ConfigError


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
    positions = options["positions"]

    if bravaislattice:
        atoms = createBravaislattice(options)
    else :
        try:
            latticeconstants[0]
        except IndexError:
            # set error context to None to prevent printout of indexError
            raise ConfigError(
                    message="The latticeconstants must be set when not specifying a bravaislattice",
                    config_properties=["latticeconstants","bravaislattice"],
                ) from None

        cell = options["cell"]
        cell = [[x*latticeconstants[0] for x in y] for y in cell]
        atoms = Atoms(symbol, 
            positions = positions,
            cell=cell,
            pbc=pbc)
        atoms = atoms.repeat(size) #this is the same as: atoms = atoms * size
    atoms.set_tags(size[0])
    print("Initial lattice constants [Å]:", atoms.cell.cellpar()[0:3] / size)
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
    # default latticeconstant to None which uses ase built-in default lattice constant
    try:
        latticeconstant = latticeconstants[0]
    except IndexError:
        latticeconstant = None
    if(bravaislattice == "SC") :
        return SimpleCubic(directions = directions,
                            symbol = symbol,
                            size = size, pbc = pbc,
                            latticeconstant = latticeconstant)
    if(bravaislattice == "BCC") :
        return BodyCenteredCubic(directions = directions,
                            symbol = symbol,
                            size = size, pbc = pbc,
                            latticeconstant = latticeconstant)
    if(bravaislattice == "FCC") :
        return FaceCenteredCubic(directions = directions,
                            symbol = symbol,
                            size = size, pbc = pbc,
                            latticeconstant = latticeconstant)