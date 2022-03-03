import pandas as pd
import Utilities
from math import isnan
import logging

# Assumptions to verify:
# 1) When the State Of Charge is decreasing, Energy delivered increases (or==) and Energy received does not change
# 2) When the State Of Charge is increasing, Energy received increases (or==) and Energy delivered does not change
# These requirements are not considered when dealing with missing (nan) values
def check_assumptions():
    Utilities.init_logging("Assumptions.log")
    y1_ed, y2_er, y3_soc = Utilities.get_data()

    a1_not_true_idx = []
    a2_not_true_idx = []

    for i in range(len(y1_ed)-1):

        # exclude missing values
        if isnan(y1_ed[i]) or isnan(y1_ed[i+1]):
            continue

        pre_soc = y3_soc[i]
        next_soc = y3_soc[i+1]

        if pre_soc > next_soc: # charge decreasing
            ed_inc = y1_ed[i+1] >= y1_ed[i]
            er_equal = y2_er[i+1] == y2_er[i]
            if (not ed_inc) or (not er_equal):
                logging.info("i=" + str(i) + ", discharging: pre_soc= " + str(round(pre_soc,3)) + " > next_soc=" + str(round(next_soc,3)))
                logging.info("y1_ed = " + str(y1_ed[i]) + ", " + str(y1_ed[i+1]))
                logging.info("y2_er = " + str(y2_er[i]) + ", " + str(y2_er[i + 1]))
                logging.info("*")
                a1_not_true_idx.append(i)
        if pre_soc < next_soc: # charge increasing
            ed_equal = y1_ed[i+1] == y1_ed[i]
            er_inc = y2_er[i+1] >= y2_er[i]
            if (not er_inc) or (not ed_equal):
                a2_not_true_idx.append(i)
                logging.info("i=" + str(i) + ", charging: pre_soc= " + str(round(pre_soc,3)) + " < next_soc=" + str(round(next_soc,3)))
                logging.info("y1_ed = " + str(y1_ed[i]) + ", " + str(y1_ed[i + 1]))
                logging.info("y2_er = " + str(y2_er[i]) + ", " + str(y2_er[i + 1]))
                logging.info("*")

    return a1_not_true_idx, a2_not_true_idx






def exe():
    df = pd.read_csv(Utilities.DATASET_FPATH)