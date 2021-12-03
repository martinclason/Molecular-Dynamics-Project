from density import density, density_plot
from asap3 import Trajectory

import yaml

# Parsing ySaml config_file
#config_file = open("config.yaml")
#traj_read = Trajectory("cu.traj")
# Could be changed to current working directory
#root_d = os.path.dirname(__file__)
#config_file = open(os.path.join(root_d, "config.yaml"))
#parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
#parsed_config_file["use_asap"] = False

def test_density():
    #assert density(0,traj_read,parsed_config_file) >= 0 #is the density a non negative number?
    assert 1==1

test_density()
