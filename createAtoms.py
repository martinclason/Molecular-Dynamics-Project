from ase.lattice.cubic import SimpleCubic, BodyCenteredCubic, FaceCenteredCubic
from ase import Atoms


def createAtoms(options,symbol, size, pbc, latticeconstants, bravaislattice):
    """createAtoms takes 5 arguements. Symbol is the chemical notation (string), 
    size is repetitions of the cell in (x,y,z) directions (int,int,int), pbc is True
    or False for periodic boundary conditions (bool), bravaislattice is the structure
    of the unit cell (currently SC, BCC and FCC supported) (string). The function
    returns an atoms/lattice object that can be used for simulations."""
    if bravaislattice:
        atoms = createBravaislattice(options,symbol, size, pbc, latticeconstants, bravaislattice)
    else :
        cell = options["cell"]
        cell = [[x*latticeconstants[0] for x in y] for y in cell]
        atoms = Atoms(symbol,
            cell=cell,
            pbc=pbc)
        atoms = atoms.repeat(size) #this is the same as: atoms = atoms * size
    return atoms

def createBravaislattice(options,symbol, size, pbc, latticeconstants, bravaislattice):
    """createBravaislattice takes 5 arguements. Symbol is the element (string), 
    size is repetitions of the cell in (x,y,z) directions (int,int,int), pbc is True
    or False for periodic boundary conditions (bool), bravaislattice is the lattice 
    structure of the unit cell (currently SC, BCC and FCC supported) (string). The function 
    returns a lattice object."""
    directions = options["directions"]
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