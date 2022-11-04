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

#user 1
user_id = "9k9z4O001JPYOFg3akDrzCA7btx2"
input_time = 60
input_cat = "thinking"


model = Recommender()
model.load_state_dict(torch.load("models/model_v2.pt"))
model.eval()

top3 = recommendation(user_id,input_time,input_cat, model)

print(top3)