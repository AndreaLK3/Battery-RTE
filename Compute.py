from Utilities import init_logging, get_data


def get_local_maxima(k=10):
    # Param. k: time slots of monotonic increase of the SOC followed by monotonic decrease
    init_logging("Local_maxima.log")
    _y1_ed, _y2_er, y3_soc = get_data()

    local_maxima_indices = [0]  # the start is included
    # l1 = [5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3]  # debug
    # y3_soc = l1
    for i in range(k,len(y3_soc)-k):
        prev = y3_soc[i-k:i]
        next = y3_soc[i+1:i+k+1]
        if all([y3_soc[i] > soc for soc in prev]):
            if all([y3_soc[i] > soc for soc in next]):
                local_maxima_indices.append(i)

    return local_maxima_indices


def get_recharge_points(local_maxima_indices):
    """Given:
    - the list of local maxima, which are taken as the starting point of a discharge+charge
    Get: the points on the SOC line where we have again the same value of a local maximum, with a LIFO (stack) logic """


