from createAtoms import createAtoms, createBravaislattice

import yaml 

config_file = open("test/config.yaml")
parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

def test_createAtoms():
    atoms = createAtoms(parsed_config_file)

def test_createBravaislattice():
    atoms = createBravaislattice(parsed_config_file)