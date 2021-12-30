from ale.scatter import make_scatter_plotter, find_json_files
from ase.io.trajectory import Trajectory
from ale.md_config_reader import parse_config
import matplotlib.pyplot as plt
import sys
import os
import subprocess
import signal


#Tests if the find_json_files function returns a list of .json files

def test_find_json_files():
    parsed_config_file = parse_config(open("test/config.yaml"))

    out_file_list = find_json_files(parsed_config_file)
    for i in range(len(out_file_list)):
        assert out_file_list[i].index(".json")

def test_scatter_plotter():
    try:
        process = subprocess.Popen(
                    f"python3 scatter_plot.py",
                    shell=True,
                    preexec_fn=os.setsid)
        plt.show()
        # sleep(1)
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except:
        assert False, "Scatter plot couldn't be created"
