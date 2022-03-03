import pandas as pd

import Compute
import Utilities
import matplotlib.pyplot as plt
from math import nan

def fig_dataset():

    # The data
    # Timestamp: The date and time of the measurement.
    # Energy Received: The energy (in kWh) received from the power grid, i.e. the energy going into the battery
    # Energy Delivered: The energy (in kWh) delivered to the power grid, taken from the battery when it is being discharged
    # SOC (State Of Charge): State of Charge of the battery. 0% when empty, 100% when fully charged.
    # This value is average over the measured period, in this case it is average over 5-mins interval.
    # Observation: missing values are nan

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


def fig_scatter_on_line(points_of_interest, label):
    _y1_ed, _y2_er, y3_soc = Utilities.get_data()
    x = list(range(len(y3_soc)))

    fig = plt.figure(figsize=(8, 6))
    ax = plt.gca()
    ax.set_xlabel("time")
    ax.set_ylabel("%")

    ax.plot(x, y3_soc, label="State Of Charge")

    y_scatter = []
    for i in range(len(y3_soc)):
        if i in points_of_interest:
            y_scatter.append(y3_soc[i])
        else:
            y_scatter.append(nan)
    ax.scatter(x, y_scatter, label=label)
    ax.legend()

    plt.savefig("figure_" + label + ".png", dpi=500)
    fig.show()


def plot_trips():
    _ed, _er, soc_ls = Utilities.get_data()
    x = list(range(len(soc_ls)))
    local_maxima_indices = Compute.get_local_maxima(soc_ls, k=50)
    trips = Compute.get_recharge_points(soc_ls, local_maxima_indices)
    rt_extremes = []
    for trip in trips:
        rt_extremes.append(trip[0])
        rt_extremes.append(trip[1])

    fig_scatter_on_line(rt_extremes, "extremes of partial trips")



