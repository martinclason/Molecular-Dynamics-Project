from ale.createAtoms import createAtoms
from ale.scatter import make_scatter_plotter
from ale.simulation_data_IO import input_simulation_data
from ale.MSD import make_MSD_plotter
from ale.plotting.generic_plotter import make_generic_time_plotter
from ale.errors import ConfigError

import matplotlib.pyplot as plt
from ase.visualize import view
import pprint


pp = pprint.PrettyPrinter(indent=4)


def visualize(options, data_file_path):
    """This function visualizes properties specified by
    the user in the config-file.
    """

    print(f"Visualizing data from file: {data_file_path}")

    data = input_simulation_data(data_file_path)

    if not options.get('visualize'):
        raise ConfigError(['visualize'], "Nothing to visualize, please add some options below 'visualize' in config.")

    dt = options['dt']
    interval = options['interval'] if ('interval' in options) else 1
    dt = dt * interval

    print("Visualizing data:")
    pp.pprint(data)

    # Dictionary mapping keys to functions which create visualizations when called
    known_visualizers = {
        'Lattice': make_lattice_viewer(options),
        'Temperature': make_generic_time_plotter(
            retrieve_data=lambda: data['Temperature'],
            label='Temperature',
            dt=dt,
            time_unit='fs',
            title=f"Temperature of ensemble for {options['symbol']}",
            unit='K',
        ),
        'MSD': make_MSD_plotter(
            data,
            options.get('dt')
        ),
        'Scatter': make_scatter_plotter(
            options,
            data_type1=options['scatter_type_d1'],
            data_type2=options['scatter_type_d2']
        ),
    }

    # Generate chosen visualizations
    for visualizer_name, visualizer in known_visualizers.items():
        if not 'visualize' in options:
            print("Nothing to visualize")
            return

        if visualizer_name in options['visualize']:
            visualizer()

    # Plot all generated figures
    plt.show()


def make_lattice_viewer(options):
    def viewer():
        atoms = createAtoms(options)
        view(atoms)

    return viewer
