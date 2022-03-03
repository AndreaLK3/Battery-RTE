import pandas as pd
import Utilities


# Assumptions to verify:
# 1) When the State Of Charge is decreasing, Energy delivered increases and Energy received does not change
# 2) When the State Of Charge is increasing, Energy received increases and Energy delivered does not change
# These requirements are not considered when dealing with missing (nan) values
def check_assumptions():
    df = pd.read_csv(Utilities.DATASET_FPATH)


def exe():
    df = pd.read_csv(Utilities.DATASET_FPATH)