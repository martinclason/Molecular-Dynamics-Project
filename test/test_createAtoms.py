# from createAtoms import createAtoms

# import yaml 

# config_file = open("test/config.yaml")
# parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

# #Make sure all data from config file was stored in Atoms corerctly
# def test_createAtoms(): 
#     atoms = createAtoms(parsed_config_file)
#     config_cell = parsed_config_file["cell"]
#     config_positions = parsed_config_file["positions"]
#     config_pbc = parsed_config_file["pbc"]
#     config_size = parsed_config_file["size"]

#     atoms_size = atoms.get_tags()[0]
#     atoms_cell = atoms.cell / atoms_size
#     atoms_positions = atoms.get_positions()
#     atoms_pbc = atoms.get_pbc()

#     assert (atoms_cell == config_cell and 
#         atoms_positions == config_positions and
#         atoms_pbc == config_pbc)
