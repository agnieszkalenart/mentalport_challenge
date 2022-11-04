"""
File for final testing
"""
# standard library imports

# 3rd party imports
import pandas as pd
import numpy as np
import torch


# local imports (i.e. our own code)
from final_filtering import recommendation
from ensemble  import Recommender


user_id = "3FTsO3V9ACTkMNYu1lh8"
#user_id = "3ubZLnRhsmTEvuqQ8SLB"
input_time = 5
input_cat = "breathing"
model = Recommender()
model.load_state_dict(torch.load("models/model_v2.pt"))
model.eval()

top3 = recommendation(user_id,input_time,input_cat, model)

print(top3)