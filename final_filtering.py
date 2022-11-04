"""
File for final filtering or re-ranking, based on user inputs.
"""

# standard library imports

# 3rd party imports
import pandas as pd
import numpy as np
import torch

# local imports (i.e. our own code)
from helper import preprocess_time, filter_time, filter_exercises, change_ranking

exercises=pd.read_csv("data/mp_data/exercise-original-fixed.csv")


def filter(model_data, exercises_data, input_time, input_cat, ex_col, score_col):
    #filter exercise data depending on the input time (maximal time that user has) 
    filtered_data = filter_time(input_time, exercises_data, "Zeitaufwand", "Bez.")
    #filter by the category
    list_ex = filter_exercises(filtered_data, input_cat)
    #change ranking
    top3 = change_ranking(model_data, list_ex, score_col, ex_col)
    return top3

def recommendation(user_id,input_time,input_cat, model):
    item_based = pd.read_csv("data/out/item-predictions-noclip.csv", index_col=0).reset_index(drop=True)
    item_mean = np.nanmean(item_based.replace(0, np.nan).to_numpy(dtype=np.single))
    item_based = item_based.replace(0, item_mean)

    user_based = pd.read_csv("data/out/user-predictions-noclip.csv", index_col=0).reset_index(drop=True)
    user_mean = np.nanmean(user_based.replace(0, np.nan).to_numpy(dtype=np.single))
    user_based = user_based.replace(0, user_mean)
    content_based = pd.read_csv("data/out/content_based.csv", index_col=0)
    exercises=pd.read_csv("data/mp_data/exercise-original-fixed.csv")
    model_data = pd.DataFrame(columns = ["ex_col","score_col"])
    model_data["ex_col"] = exercises["Bez."]
    #breakpoint()
    model_data = model_data.set_index('ex_col')
    i = 0
    for exercise in exercises["Bez."]:
        i+=1
        try:
            x1 = user_based[exercise][user_id]
        except KeyError:
            x1 = user_mean
        try:
            x2 = item_based[exercise][user_id]
        except KeyError:
            x2 = item_mean
        try:
            x3 = content_based[exercise][user_id]
        except KeyError:
            x3 = 0
        prediction = model(torch.tensor((x1,x2,x3)))
        #model_data[model_data["ex_col"] == exercise]["score_col"] = prediction.detach().item()
        model_data.loc[exercise, "score_col"] = prediction.detach().item()
    top3 = filter(model_data, exercises, input_time, input_cat, "ex_col", "score_col")
    return top3
