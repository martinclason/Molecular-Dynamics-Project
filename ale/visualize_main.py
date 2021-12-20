import matplotlib.pyplot as plt
import os

from ale.scatter import make_scatter_plotter

from ale.simulationDataIO import inputSimulationData
from ale.MSD import make_MSD_plotter
from ale.plotting.generic_plotter import make_generic_time_plotter

def s_to_fs(t):
  return t*10e-15

def visualize(options, data_file_path):
  """This function visualizes properties specified by
  the user in the config-file.
  """

  print(f"Visualizing data with file {data_file_path}")
  print(f"Visualizing scatter data from dir {options['scatter_dir']}")

  data = inputSimulationData(data_file_path)
  dt = options['dt']
  dt = s_to_fs(dt)

  interval = options['interval'] if ('interval' in options) else 1
  dt = dt * interval

  print("Data:")
  print(data)

  known_visualizers = {
    'Temperature' : make_generic_time_plotter(
                        data=data['Temperature'],
                        label='Temperature',
                        dt=dt,
                        time_unit='fs',
                        title=f"Temperature of ensemble for {options['symbol']}",
                        unit='K',
                    ),
    'MSD' : make_MSD_plotter(data,options.get('dt')),
    'Scatter' : make_scatter_plotter(options,data_type1=options['scatter_type_d1'],data_type2 = options['scatter_type_d2']),
  }

  for visualizer_name, visualizer in known_visualizers.items():
    if not 'visualize' in options:
      print("Nothing to visualize")
      return

    if visualizer_name in options['visualize']:
      visualizer()

  plt.show()

