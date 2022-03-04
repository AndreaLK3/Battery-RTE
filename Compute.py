import logging
import Utilities
from Utilities import init_logging, get_data
from math import nan, isnan
import numpy as np


class Trip:
    def __init__(self, start_idx):
        self.start_idx = start_idx
        self.end_idx = 0
        self.energy_delivered = 0
        self.energy_received = 0


def get_local_max(soc_ls, k=20, min_value=60):
    # Parameters: k = time slots of monotonic increase of the SOC followed by monotonic decrease
    #             min_value = the minimum SOC value for a point to be recognized as a local maximum

    local_maxima_indices = [0]  # the start is included

    for i in range(k,len(soc_ls)-k):
        prev = soc_ls[i-k:i]
        next = soc_ls[i+1:i+k+1]
        if all([soc_ls[i] > soc for soc in prev]):
            if all([soc_ls[i] > soc for soc in next]):
                if soc_ls[i] > min_value:
                    local_maxima_indices.append(i)

    return local_maxima_indices


def conclude_trip(end_idx, trip, y1_ed, y2_er, y3_soc):
    proposed_endpoint_soc = y3_soc[end_idx]
    if abs(y3_soc[trip.start_idx] - proposed_endpoint_soc) < 1:
        trip.end_idx = end_idx
    else:  # we must change the extremes of the roundtrip. Either:
        if proposed_endpoint_soc >= y3_soc[trip.start_idx]:  # 1) backtrack
            for j in range(end_idx, trip.start_idx , -1):
                if abs(y3_soc[trip.start_idx] - y3_soc[j]) < 1:
                    trip.end_idx = j
                    break
                trip.end_idx = None
        else:  # 2) bring the starting index forward
            for s in range(trip.start_idx, end_idx):
                trip.end_idx = end_idx  # endpoint unchanged
                if abs(y3_soc[s] - y3_soc[end_idx]) < 1:
                    trip.start_idx = s
                    break
                trip.start_idx = None  # if there is no way to obtain a valid trip (e.g. at the end of the SOC line)

    # update the values of energy delivered and energy retrieved
    trip.energy_delivered = y1_ed[trip.end_idx] - y1_ed[trip.start_idx]
    trip.energy_received = y2_er[trip.end_idx] - y2_er[trip.start_idx]

    return trip


def process_roundtrips():
    y1_ed, y2_er, y3_soc = Utilities.get_data()
    lmax_indices = get_local_max(y3_soc)

    trips_ls = [Trip(0)]

    for i in range(1,len(y3_soc)):
        trip = trips_ls[-1]  # select the current trip
        # if we have to start a new trip from a local maximum: conclude the previous one, record its energy values
        if i in lmax_indices:
            conclude_trip(i, trip, y1_ed, y2_er, y3_soc)
            if i != max(lmax_indices):
                new_trip = Trip(i)
                trips_ls.append(new_trip)

    trips_ls = [t for t in trips_ls if t.start_idx is not None and t.end_idx is not None]

    return trips_ls


