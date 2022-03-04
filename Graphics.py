import pandas as pd

import Compute
import Utilities
import matplotlib.pyplot as plt
from math import nan

def fig_dataset():

    y1_ed, y2_er, y3_soc = Utilities.get_data()
    x = list(range(len(y1_ed)))

    fig = plt.figure(figsize=(8,6))
    ax = plt.gca()
    ax.set_xlabel("time")
    ax.set_ylabel("kWh")
    plt.plot(x, y1_ed, label="Energy delivered", color="tab:green")
    plt.plot(x, y2_er, label="Energy received", color="darkred")

    ax2 = ax.twinx()
    ax2.set_ylabel("%")
    ax2.plot(x, y3_soc, label="State Of Charge")
    ax.legend(loc=0)
    ax2.legend(loc=1)

    plt.savefig(Utilities.FIGURE1_FPATH, dpi=500)
    fig.show()


def plot_trip_extremes():
    _y1_ed, _y2_er, y3_soc = Utilities.get_data()
    x = list(range(len(y3_soc)))

    trips = Compute.process_roundtrips()
    trip_starts = [t.start_idx for t in trips]
    trip_ends = [t.end_idx for t in trips]

    fig = plt.figure(figsize=(8, 6))
    ax = plt.gca()
    ax.set_xlabel("time")
    ax.set_ylabel("%")

    ax.plot(x, y3_soc, label="State Of Charge")

    y_scatter = []
    for i in range(len(y3_soc)):
        if i in trip_starts:
            y_scatter.append(y3_soc[i])
        else:
            y_scatter.append(nan)
    plt.scatter(x, y_scatter, color='green', marker="o", label="trip start")

    y_scatter2 = []
    for i in range(len(y3_soc)):
        if i in trip_ends:
            y_scatter2.append(y3_soc[i])
        else:
            y_scatter2.append(nan)
    plt.scatter(x, y_scatter2, color='red', marker=8, label="trip end")

    ax.legend(loc=4)
    plt.grid()
    plt.savefig("figure_trips.png", dpi=500)
    fig.show()