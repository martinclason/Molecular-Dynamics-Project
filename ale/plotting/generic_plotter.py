import matplotlib.pyplot as plt
import numpy as np

def make_generic_time_plotter(
        retrieve_data,
        label,
        dt,
        time_unit=None,
        title=None,
        unit=None,
    ):
    """Factory function for creating plotters that can plot data over time.
    The function returns a function which can be called whenever the plot should be drawn.
    This function takes no arguments and will create a new figure and plot the given data when called.
    This function doesn't call plt.show() so this must be done by the calling code.

    :param retrive_data: function that returns data to plot over time when called with no arguments.
    :param str label: Label representing the data.
    :param number dt: delta time between time steps in data.
    :param str time_unit: unit of time, e.g. 'fs'.
    :param str title: title of plot.
    :param str unit: unit of data, e.g. 'K'.
    """

    def plotter():
        data = retrieve_data()
        t = np.arange(0, len(data)*dt, dt)

        fig = plt.figure()
        ax = plt.axes()

        plt.title(title if title else label)
        plt.xlabel(f"Time [{time_unit}]" if time_unit else f"Time")
        plt.ylabel(f"{label} [{unit}]" if unit else f"{label}")

        ax.plot(t, data, marker = 'o')

    return plotter
