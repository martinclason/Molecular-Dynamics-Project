import matplotlib.pyplot as plt
import numpy as np

from simulationDataIO import inputSimulationData

def s_to_fs(t):
  return t*10e-15

def visualize(options, data_file_name="out.json"):
  """This function visualizes properties specified by 
  the user in the config-file.
  """
  
  print("Visualizing data")
  data = inputSimulationData(data_file_name)
  dt = options['dt']
  dt = s_to_fs(dt)

  interval = options['interval'] if ('interval' in options) else 1
  dt = dt * interval

  known_visualizers = {
    'temperature' : make_temperature_plotter(data, dt),
  }

  for visualizer_name, visualizer in known_visualizers.items():
    if not 'visualize' in options:
      print("Nothing to visualize")
      return

    if visualizer_name in options['visualize']:
      visualizer()

  plt.show()


def make_temperature_plotter(data, dt):
  def plotter():
    temperatures = data['temperature']
    dt = 2
    t = np.arange(0, len(temperatures)*dt, dt)

    fig = plt.figure()
    ax = plt.axes()

    plt.title("Temperature of ensemble")
    plt.xlabel("Time [fs]")
    plt.ylabel("Temperature [K]")

    ax.plot(t, temperatures, marker = 'o')

  return plotter