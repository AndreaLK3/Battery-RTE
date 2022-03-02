import pandas as pd
import Utilities
import matplotlib.pyplot as plt

def exe():
    df = pd.read_csv(Utilities.DATASET_FPATH)

    # The data
    # Timestamp: The date and time of the measurement.
    # Energy Received: The energy (in kWh) received from the power grid, i.e. the energy going into the battery
    # Energy Delivered: The energy (in kWh) delivered to the power grid, taken from the battery when it is being discharged
    # SOC (State Of Charge): State of Charge of the battery. 0% when empty, 100% when fully charged.
    # This value is average over the measured period, in this case it is average over 5-mins interval.

    # preliminary check: data columns
    fig, ax = plt.subplots()
    y1 = df["ENERGY_DELIVERED"].to_list()
    x = list(range(len(y1)))
    y2 = df["ENERGY_RECEIVED"].to_list()
    y3 = df["SOC"].to_list()
    # plt.plot(x,y1, label="Energy delivered")
    # plt.plot(x,y2, label="Energy received")
    # ax.legend()
    # fig.show()
    #
    # fig, ax = plt.subplots()
    # plt.plot(x, y3, label="State Of Charge")
    # ax.legend()
    # fig.show()

    fig = plt.figure(figsize=(7,7))
    ax = plt.gca()
    ax.set_label("timestamp")
    ax.set_ylabel("kWh")
    plt.plot(x, y1, label="Energy delivered", color="tab:green")
    plt.plot(x, y2, label="Energy received", color="darkred")

    ax2 = ax.twinx()
    ax2.set_ylabel("%")
    ax2.plot(x, y3, label="State Of Charge")
    ax.legend(loc=0)
    ax2.legend(loc=1)

    plt.savefig(Utilities.FIGURE1_FPATH, dpi=500)
    fig.show()