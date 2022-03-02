import pandas as pd
from enum import Enum
import nltk
import logging
import sys
import torch
import os

DATASET_FPATH = "BESS_op_data.csv"
FIGURE1_FPATH = "figure_dataset.png"

# Invoked to write a message to a text logfile and also print it
def init_logging(logfilename, loglevel=logging.INFO):
  for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
  logging.basicConfig(level=loglevel, filename=logfilename, filemode="w",
                      format='%(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

  if len(logging.getLogger().handlers) < 2:
      outlog_h = logging.StreamHandler(sys.stdout)
      outlog_h.setLevel(loglevel)
      logging.getLogger().addHandler(outlog_h)

# Round the numbers in a list
def round_list_elems(ls, precision=2):
    rounded_ls = [round(elem, precision) for elem in ls]
    return rounded_ls

