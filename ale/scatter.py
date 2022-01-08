from ale.errors import ConfigError
from ale.simulation_data_IO import input_simulation_data

import glob, os, sys
import numpy as np
import matplotlib.pyplot as plt


#A help function to extract the .json files in the outfiles directory
def find_json_files(options):
    file_list = []
    outdir = options.get("scatter_dir") if options.get("scatter_dir") is not None else os.getcwd()

    if os.path.isdir(os.path.join(os.getcwd(),outdir)):
        for file in glob.glob(os.path.join(os.getcwd(),outdir,"*.json")):
            file_list.append(file)
        return file_list
    else:
        raise ConfigError(
                message= "Chosen directory path " + os.path.join(os.getcwd(),outdir) + " doesnt exist.",
                config_properties = ["scatter_dir"]
    )


def make_scatter_plotter(options,data_type1,data_type2,filelist=[]):
    """Creates and returns a plotter function that creates a scatter plot

    :param options: parsed options from config file.
    :param data_type1: data type to write on the x-axis.
    :param data_type2: data type to write on the y-axis.
    :param filelist: list of .json files, if specification of which files to do plotter of is needed, default=[]."""
    filelist = options.get("scatter_files") if options.get("scatter_files") != [] else find_json_files(options)
    if options.get("scatter_dir"):
        for file in filelist:
            file = os.path.join(options.get("scatter_dir"),file)

    print(f"Scatter using files: {filelist}")

    def scatter_plotter():
        print(f"Visualizing scatter data from dir: {options['scatter_dir']}")

        if filelist is None:
            raise ConfigError(
                    message = "List of files is of type None",
                    config_properties = ["scatter_files"]
        )
        else:
            fig = plt.figure()
            ax = plt.axes()
            for file in filelist:
                try:
                    data = input_simulation_data(file)
                except OSError:
                    raise ConfigError(
                            message = "Filename " + file + " does not exist.",
                            config_properties = ["scatter_files"]
                )
                if data_type1 == "time":
                    dt = 2
                    x = np.arange(0, len(data[data_type2])*dt, dt)
                else:
                    try:
                        x = data[data_type1]
                    except KeyError:
                        raise ConfigError(
                                message = "Must specify which data type to plot on the x-axis.",
                                config_properties = ["data_type1"]
                    )
                try:
                    y = data[data_type2]
                except KeyError:
                    raise ConfigError(
                            message = "Must specify which data type to plot on the y-axis.",
                            config_properties = ["data_type2"]
                )
                y = data[data_type2]

                # ax.scatter(x,y,label=os.path.basename(file).removesuffix('.json').removesuffix('_out'))
                ax.scatter(x,y,label=os.path.basename(file).split('.json')[0].split('_out')[0])

                plt.xlabel(data_type1)
                plt.ylabel(data_type2)
                ax.legend()

    return scatter_plotter
