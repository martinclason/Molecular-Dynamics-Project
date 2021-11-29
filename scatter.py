import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def scatter_plot(filelist,data_type1,data_type2):
    for file in filelist:
        data = pd.read_csv(file)
        x = data.data_type1
        y = data.data_type2
        plt.scatter(x,y,alpha=0.5)
    plt.show()


