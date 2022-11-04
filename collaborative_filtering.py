"""
File for creating the user-item matrices
"""

# standard library imports

# 3rd party imports
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

# local imports (i.e. our own code)
from helper import get_user_exercise_results, get_user_users, get_satisfaction, get_date, predict

# import datasets
exercises = pd.read_csv("data\\mp_data\\exercise-original-fixed.csv")
exercise_results = pd.read_csv("data\\mp_data\\exerciseResults.csv")
users = pd.read_csv("data\\mp_data\\users.csv")

# extract user_ids
users["user_id"] = get_user_users(users)
exercise_results["user_id"] = get_user_exercise_results(exercise_results)

# extract satisfaction scores
exercise_results["satisfaction"] = get_satisfaction(exercise_results)

# filter out wrongly included "exercises"
exercise_results = exercise_results[exercise_results["exerciseId"].apply(lambda x: len(x) < 7)]

# extract the date
exercise_results["date"] = get_date(exercise_results)
exercise_results["date"] = pd.to_datetime(exercise_results["date"])

# drop duplicates from exercise_results and only keep the latest rating
exercise_results_unique = exercise_results.sort_values(
    "date", ascending=False
).drop_duplicates(subset=["user_id", "exerciseId"], keep="first")

# create df containing all valid user-item rating pairs
ratings = exercise_results_unique[["user_id", "exerciseId", "satisfaction"]]
ratings = ratings[ratings["satisfaction"].notna()]

# create an item-user matrix containing the ratings
iu_matrix = ratings.pivot(
    index="exerciseId", columns="user_id", values="satisfaction"
).fillna(0)

# create the user similarity matrix
user_similarities = 1 - pairwise_distances(iu_matrix.T, metric="cosine")
user_similarities[np.isnan(user_similarities)] = 0

# use the user keys as index and column names
user_similarities_df = pd.DataFrame(
    user_similarities, index=iu_matrix.columns, columns=iu_matrix.columns
)

# create the item similarity matrix
item_similarities = 1 - pairwise_distances(iu_matrix, metric="cosine")
item_similarities[np.isnan(item_similarities)] = 0

# use the item keys as index and column names
item_similarities_df = pd.DataFrame(item_similarities, index=iu_matrix.index, columns=iu_matrix.index)

# create the item-based collaborative filtering prediction matrix
ui_matrix_item_based = predict(iu_matrix.T, item_similarities, mode="item")

# create the user-based collaborative filtering prediction matrix
ui_matrix_user_based = predict(iu_matrix.T, user_similarities, mode="user")

# replace indices user and item IDs
ui_matrix_item_based_df = pd.DataFrame(
    ui_matrix_user_based, index=iu_matrix.columns, columns=iu_matrix.index
)
ui_matrix_user_based_df = pd.DataFrame(
    ui_matrix_item_based, index=iu_matrix.columns, columns=iu_matrix.index
)

# transpose the item-user matrix to get a user-item matrix
ui_matrix = iu_matrix.T

# store the user-item matrices (1. actual ratings, 2. item-based CF predictions, 3. user-based CF predictions)
'''
ui_matrix.to_csv("data\\out\\user-item-matrix.csv")
ui_matrix_item_based_df.to_csv("data\\out\\user-predictions.csv")
ui_matrix_user_based_df.to_csv("data\\out\\item-predictions.csv")
'''

# additionally create collaborative filtering predictions without clipping
# create the item-based collaborative filtering prediction matrix
ui_matrix_item_based_no_clip = predict(iu_matrix.T, item_similarities, mode="item", clip=False)

# create the user-based collaborative filtering prediction matrix
ui_matrix_user_based_no_clip = predict(iu_matrix.T, user_similarities, mode="user", clip=False)

# replace indices user and item IDs
ui_matrix_item_based_df_no_clip = pd.DataFrame(
    ui_matrix_user_based_no_clip, index=iu_matrix.columns, columns=iu_matrix.index
)
ui_matrix_user_based_df_no_clip = pd.DataFrame(
    ui_matrix_item_based_no_clip, index=iu_matrix.columns, columns=iu_matrix.index
)

# store the user-item matrices without clipping (1. item-based CF predictions, 2. user-based CF predictions)
'''
ui_matrix_user_based_df_no_clip.to_csv("data\\out\\item-predictions-noclip.csv")
ui_matrix_item_based_df_no_clip.to_csv("data\\out\\user-predictions-noclip.csv")
'''

