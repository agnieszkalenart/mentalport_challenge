"""
File for final filtering
"""

# standard library imports

# 3rd party imports
import pandas as pd
import numpy as np

# local imports (i.e. our own code)
from helper import preprocess_time, filter_time

exercises=pd.read_csv("mp_data-main/mp_data/exercise-original-fixed.csv")

def filter(model_data, exercises_data, input_time, input_cat):
    list_of_indexes = 
    #filter exercise data depending on the input time (maximal time that user has) 
    filtered_data = filter_time (input_time, exercises_data, "Zeitaufwand", "Bez.")
    #
