import pandas as pd
import Utilities
import matplotlib.pyplot as plt



# def fig_incr_decr():
#     df = pd.read_csv(Utilities.DATASET_FPATH)
#     fig = plt.figure(figsize=(8, 6))
#
#     ed_ls = df["ENERGY_DELIVERED"].to_list()
#     x = list(range(len(ed_ls)-1))
#     er_ls = df["ENERGY_RECEIVED"].to_list()
#
#     ed_diffs = [-ed_ls[i]+ ed_ls[i+1] for i in range(0,len(ed_ls)-1)]
#     er_diffs = [-er_ls[i] + er_ls[i+1] for i in range(0, len(er_ls) - 1)]
#
#     fig = plt.figure(figsize=(8, 6))
#     ax = plt.gca()
#     ax.set_xlabel("time")
#     ax.set_ylabel("kWh")
#     plt.plot(x, ed_diffs, label="Δ Energy delivered", color="tab:green")
#     plt.plot(x, er_diffs, label="Δ Energy received", color="darkred")
#
#     plt.savefig(Utilities.FIGURE2_DETA_FPATH, dpi=500)
#     fig.show()


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