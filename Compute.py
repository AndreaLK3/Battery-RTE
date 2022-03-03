from Utilities import init_logging, get_data
from math import nan

def get_local_maxima(soc_ls, k=10):
    # Param. k: time slots of monotonic increase of the SOC followed by monotonic decrease
    init_logging("Local_maxima.log")

    local_maxima_indices = [0]  # the start is included
    # l1 = [5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3]  # debug
    # y3_soc = l1
    for i in range(k,len(soc_ls)-k):
        prev = soc_ls[i-k:i]
        next = soc_ls[i+1:i+k+1]
        if all([soc_ls[i] > soc for soc in prev]):
            if all([soc_ls[i] > soc for soc in next]):
                local_maxima_indices.append(i)

    return local_maxima_indices


def get_recharge_points(soc_ls, local_maxima_indices, epsilon=0.01, min_dist=200):
    """Given:
    - the list of State-Of-Charge values
    - the list of local maxima, which are taken as the starting point of a discharge+charge
    Get: the points on the SOC line where we have again the same value of a local maximum, with a LIFO (stack) logic """

    stack = [local_maxima_indices[0]]  # i.e. 0
    trips = []

    for i in range(0, len(soc_ls)):
        if i in local_maxima_indices:
            stack.append(i)
        elif len(stack) > 0:
            last_localmax_value = soc_ls[stack[-1]]
            if soc_ls[i] - last_localmax_value < epsilon and i - stack[-1] > min_dist:
                trips.append((stack[-1], i))
                stack.pop()

    return trips









