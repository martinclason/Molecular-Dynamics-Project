import pytest
import yaml 

if __name__ == "__main__":
    config_file = open("test/config.yaml")
    parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

#Make sure all data from config file gets stored in Atoms correctly
@pytest.mark.openkim
def test_createAtoms(): 
    from ale.createAtoms import createAtoms
    atoms = createAtoms(parsed_config_file)
    config_cell = parsed_config_file["cell"]
    config_scaled_positions = parsed_config_file["scaled_positions"]
    config_pbc = parsed_config_file["pbc"]
    config_size = parsed_config_file["size"]

    atoms_size = atoms.get_tags()[0]
    atoms_cell = atoms.cell / atoms_size
    number_of_atoms = int(len(atoms.get_scaled_positions())/atoms_size**3) # Atoms per molecule
    atoms_scaled_positions = atoms.get_scaled_positions()[0:number_of_atoms] #Taking only interatomic positions
    atoms_pbc_x = atoms.get_pbc()[0]
    atoms_pbc_y = atoms.get_pbc()[1]
    atoms_pbc_z = atoms.get_pbc()[2]

    pbc_bool = ((atoms_pbc_x == config_pbc) and
               (atoms_pbc_y == config_pbc) and 
               (atoms_pbc_z == config_pbc))

    errors = [] #List of possible errors

    if (atoms_scaled_positions - config_scaled_positions).any():
        errors.append("Interatomic positions intialized incorrectly.")
    if not pbc_bool:
        errors.append("Periodic boundary conditions intialized incorrectly.")
    if not (atoms_cell - config_cell).any():
        errors.append("Primitive unit cell intialized incorrectly.")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
