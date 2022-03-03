import logging

import Utilities
from Utilities import init_logging, get_data
from math import nan, isnan
import numpy as np


def get_local_extremes(soc_ls, k=40):
    # Param. k: time slots of monotonic increase of the SOC followed by monotonic decrease

    local_maxima_indices = [0]  # the start is included
    local_minima_indices = []
    # l1 = [5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3]  # debug
    # y3_soc = l1
    for i in range(k,len(soc_ls)-k):
        prev = soc_ls[i-k:i]
        next = soc_ls[i+1:i+k+1]
        if all([soc_ls[i] > soc for soc in prev]):
            if all([soc_ls[i] > soc for soc in next]):
                local_maxima_indices.append(i)
        if all([soc_ls[i] < soc for soc in prev]):
            if all([soc_ls[i] < soc for soc in next]):
                local_minima_indices.append(i)

    return local_maxima_indices, local_minima_indices


def process_roundtrips_stack():
    Utilities.init_logging("roundtrips.log")
    y1_ed, y2_er, y3_soc = Utilities.get_data()
    lmax_indices, lmin_indices = get_local_extremes(y3_soc)

    stack_of_trips = []
    completed_trips = []
    # For each dict, key: starting point of the partial round trip;
    # value: tuple of (indices_ls, starting_lmax, energy_delivered_values_ls, energy_retrieved_values_ls)
    passed_lmin = False
    last_lmax_value = 0
    for i in range(len(y3_soc)):
        current_value = y3_soc[i]
        # is it a starting point for a trip?
        if i in lmax_indices:
            logging.info("Starting trip at i=" + str(i))
            stack_of_trips.append(([i], current_value,  [y1_ed[i]], [y2_er[i]]))
            passed_lmin = False
        elif i in lmin_indices:
            logging.info("Passed local minimum at i=" + str(i))
            passed_lmin = True
        # is it the ending point of a trip? It must have gone beyond a minimum, with both discharge and recharge
        elif passed_lmin and (abs(current_value - stack_of_trips[-1][1]) < 1):
            logging.info("Ending trip that started at " + str(stack_of_trips[-1][0][0]) + ", at i=" + str(i))
            completed_trips.append(stack_of_trips.pop())
            last_lmax_value = 0
        else:  # general case: add e.r. and e.d. to the dictionary of the current trip
            current_trip = stack_of_trips[-1]
            if not(isnan(y1_ed[i])) and not(isnan(y1_ed[i])):
                current_trip[0].append(i)
                current_trip[1].append(y1_ed[i])
                current_trip[2].append(y1_ed[i])

    return completed_trips











