from main import density

import yaml

# Parsing yaml config_file
config_file = open("config.yaml")
# Could be changed to current working directory
#root_d = os.path.dirname(__file__)
#config_file = open(os.path.join(root_d, "config.yaml"))
parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
parsed_config_file["use_asap"] = False

def test_density():
    assert density(parsed_config_file) >= 0 #is the density a non negative number?

test_density()
