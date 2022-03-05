import numpy as np
import Utilities
import Compute
from math import isnan
import logging

def exe():
    Utilities.init_logging("rte.log")
    trips = Compute.process_roundtrips()

    rte_ls = []
    for trip in trips:
        trip_efficiency = trip.energy_delivered / trip.energy_received
        rte_ls.append(trip_efficiency)

    logging.debug("Trips efficiency: " + str(rte_ls))
    logging.info("Average over "+ str(len(trips)) + " trips = " + str(round(sum(rte_ls)/ len(rte_ls)*100, 2)) + "%")

    soc_deltas = [t.max_soc - t.min_soc for t in trips]
    weights = [delta/ sum(soc_deltas) for delta in soc_deltas]

    weighted_avg = sum([weights[i]*rte_ls[i] for i in range(len(trips))])
    logging.info("Average over "+ str(len(trips)) + " trips (weighted by each trip's Δ SOC) = " + str(round(weighted_avg*100, 2)) + "%")



