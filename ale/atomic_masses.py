from ase.data import atomic_masses, atomic_numbers

def atomic_masses(atoms_object) :
    """Returns the sum of the atomic masses for the molecule/elements specified by symbol
    in the config-file. It however does this by looking at the atoms_object and retrieving
    one molecule from one point in the lattice, i.e. it does not look in the config_file.
    This requires the set_tag function of Atoms() to save the size of the super cell
    when the atoms object is created by createAtoms()"""
    all_masses = atoms_object.get_masses() 
    size_cube = atoms_object.get_tags()[0]**3 # Tag should contain the size of super cell
    number_of_atoms = int(len(all_masses) / size_cube) # Number of atoms per molecule
    molecule_masses = all_masses[0:number_of_atoms] #Retrieve masses from one molecule

    return sum(molecule_masses)
