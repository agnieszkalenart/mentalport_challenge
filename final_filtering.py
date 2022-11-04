"""
File for final filtering or re-ranking, based on user inputs.
"""

# standard library imports

# 3rd party imports
import pandas as pd
import numpy as np

# local imports (i.e. our own code)
from helper import preprocess_time, filter_time, filter_exercises, change_ranking

exercises=pd.read_csv("data/mp_data/exercise-original-fixed.csv")


def filter(model_data, exercises_data, input_time, input_cat, ex_col, score_col):
    #filter exercise data depending on the input time (maximal time that user has) 
    filtered_data = filter_time (input_time, exercises_data, "Zeitaufwand", "Bez.")
    #filter by the category
    list_ex = filter_exercises(filtered_data, input_cat)
    #change ranking
    top3 = change_ranking(model_data, list_ex, score_col, ex_col)
    return top3

def recommendation(user_id,input_time,input_cat, model):
    user_based = pd.read_csv("data/out/user-predictions.csv", index_col=0)
    item_based = pd.read_csv("data/out/item-predictions.csv", index_col=0)
    content_based = pd.read_csv("data/out/content_based.csv", index_col=0)
    exercises=pd.read_csv("data/mp_data/exercise-original-fixed.csv")
    model_data = pd.DataFrame(columns = ["ex_col","score_col"])
    model_data["ex_col"] = exercises["Bez."]
    model_data.set_index('ex_col')
    for exercise in exercises["Bez."]:
        x1 = user_based [exercise][user_id]
        x2 = item_based[exercise][user_id]
        x3 = content_based[exercise][user_id]
        prediction = model(x1,x2,x3)
        model_data.at[exercise,"score_col"] = prediction
    top3 = filter(model_data, exercises, input_time, input_cat, "ex_col", "score_col")
    return top3
