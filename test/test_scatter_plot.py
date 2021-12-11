from scatter import make_scatter_plotter, find_json_files
from ase.io.trajectory import Trajectory
import sys
import os
import yaml 

config_file = open("test/config.yaml")
parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

out_file_list = find_json_files(parsed_config_file)
#Tests if the find_json_files function returns a list of .json files

def test_find_json_files():
    assert out_file_list[0].index(".json") and out_file_list[1].index(".json")
