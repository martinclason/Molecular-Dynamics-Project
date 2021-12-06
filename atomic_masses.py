from ase.data import atomic_masses, atomic_numbers

def atomic_masses(atom_list) :
    all_masses = atom_list[0].get_masses() 
    size_cube = atom_list[0].get_tags()[0]**3 # Tag should contain the size of super cell
    number_of_atoms = int(len(all_masses) / size_cube) # Number of atoms per molecule
    molecule_masses = all_masses[0:number_of_atoms] #Retrieve masses from one molecule

    return sum(molecule_masses)

