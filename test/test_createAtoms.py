from createAtoms import createAtoms

import yaml 

config_file = open("test/config.yaml")
parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

def test_createAtoms():
    atoms = createAtoms(parsed_config_file)