from ale.createAtoms import createAtoms
from ale.scatter import make_scatter_plotter
from ale.simulationDataIO import inputSimulationData
from ale.MSD import make_MSD_plotter
from ale.plotting.generic_plotter import make_generic_time_plotter

import matplotlib.pyplot as plt
from ase.visualize import view


def visualize(options, data_file_path):
    """This function visualizes properties specified by
    the user in the config-file.
    """

    print(f"Visualizing data from file: {data_file_path}")

    data = inputSimulationData(data_file_path)

    dt = options['dt']
    interval = options['interval'] if ('interval' in options) else 1
    dt = dt * interval

    print("Visualizing data:")
    print(data)

    # Dictionary mapping keys to functions which create visualizations when called
    known_visualizers = {
        'Lattice': make_lattice_viewer(options),
        'Temperature': make_generic_time_plotter(
            data=data['Temperature'],
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
