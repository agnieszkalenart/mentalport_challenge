#%%

import pandas as pd
import numpy as np
import json
import ast

pd.set_option("display.max_columns", None)


#%%

#roman paths
# C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\exercises.csv
# C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\exerciseResults.csv
# C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\users.csv

# jp paths
# mentalport_challenge/mp_data-main/mp_data/exercises.csv
# mentalport_challenge/mp_data-main/mp_data/exerciseResults.csv
# mentalport_challenge/mp_data-main/mp_data/users.csv

#%%

import csv

with open(
    "mp_data-main\\mp_data\\exercise-original.csv",
    newline="\n",
    encoding="utf-8",
    errors="ignore",
) as csvfile:
    csv_reader = list(csv.reader(csvfile, delimiter=";"))
    # print(csv_reader)

cols = csv_reader[0]
content = csv_reader[1:]
exercises_df = pd.DataFrame.from_records(content, columns=cols)

exercises_df.replace("", np.nan, inplace=True)
exercises_df = exercises_df.dropna(how="all")
exercises_df = exercises_df.drop(exercises_df.columns[-2], axis=1)

# exercises_df.to_csv('C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\exercise-original-fixed.csv')

#%%

# exercises_df = pd.read_csv("C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\exercise-original.csv", encoding = "iso-8859-1", sep=";")
exerciseResults_df = pd.read_csv("mp_data-main\\mp_data\\exerciseResults.csv")
users_df = pd.read_csv("mp_data-main\\mp_data\\users.csv")
test = pd.read_csv("mp_data-main\\mp_data\\exercises.csv")

#%%

def getUser_exerciseResults(df):
    df["__key__user"] = df["__key__"].apply(
        lambda x: json.loads(x)["__key__"]["path"]
        .replace(" ", "")
        .replace('"', "")
        .split(",")[1]
    )
    return df["__key__user"]


def getUser_users_df(df):
    df["__key__user"] = df["__key__"].apply(lambda x: json.loads(x)["__key__"]["name"])
    return df["__key__user"]


# def getExercise(df):
#     df["__key__exercise"] = exerciseResults_df["__key__"].apply(lambda x:
#         json.loads(x)["__key__"]["name"]
#     )
#     return df["__key__exercise"]


def getRating(df):
    df["satisfaction"] = df["feedback"].apply(
        lambda x: json.loads(x)["feedback"]["exerciseRating"]["satisfaction"]
    )
    df["satisfaction"] = df["satisfaction"].apply(
        lambda x: None if (x is None) else int(x[0])
    )
    return df["satisfaction"]


#%%

users_df["__key__user"] = getUser_users_df(users_df)

exerciseResults_df["__key__user"] = getUser_exerciseResults(exerciseResults_df)
exerciseResults_df["satisfaction"] = getRating(exerciseResults_df)

# filter out all rows where exerciseId is a string of length > 7
exerciseResults_df = exerciseResults_df[exerciseResults_df["exerciseId"].apply(lambda x: len(x) < 7)]

#%%
# exploration
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

exerciseResults_df.groupby(["__key__user"]).size().hist(
    bins=50, grid=False, xlabelsize=12, ylabelsize=12
)
plt.xlim([0, 150])
plt.xlabel("Number of movies being rated", fontsize=15)
plt.ylabel("Frequency of users", fontsize=15)
plt.show()


#%%
def getTime(df):
    df["endtime"] = df["endTime"].apply(lambda x: json.loads(x)["endTime"]["date_time"])

    return df["endtime"]


#%%
exerciseResults_df["date"] = getTime(exerciseResults_df)

exerciseResults_df["date"] = pd.to_datetime(exerciseResults_df["date"])


#%%
# drop duplicates from exerciseResults_df and only keep cases with max value in date (so the latest ratings)
exerciseResults_df_unique = exerciseResults_df.sort_values(
    "date", ascending=False
).drop_duplicates(subset=["__key__user", "exerciseId"], keep="first")

#%%
ratings = exerciseResults_df_unique[["__key__user", "exerciseId", "satisfaction"]]

# filter out nan values
ratings = ratings[ratings["satisfaction"].notna()]


#%%

ratings_f2 = ratings.pivot(
    index="exerciseId", columns="__key__user", values="satisfaction"
).fillna(0)
ratings_f2.head(3)

#%%
# find users not yet in pivot table
users_not_in_pivot = list(set(users_df.__key__user.unique()) - set(ratings_f2.columns))

# rename Bez. column in exercises df to exerciseId
exercises_df.rename(columns={"Bez.": "exerciseId"}, inplace=True)

# remove all cases where exerciseId is nan
# exercises_df = exercises_df[exercises_df.exerciseId.notna()]

# find exercises not yet in pivot table
exercises_not_in_pivot = list(
    set(exercises_df.exerciseId.unique()) - set(ratings_f2.index)
)


# #%%
# # for all users not in pivot table, add a column with all zeros
# for user in users_not_in_pivot:
#     ratings_f2[user] = 0

# #%%
# # for all exercises not in pivot table, add a row with all zeros
# for exercise in exercises_not_in_pivot:
#     ratings_f2.loc[exercise] = 0

#%%
# compute user and item similarities
from sklearn.metrics.pairwise import pairwise_distances

# User Similarity Matrix
user_correlation = 1 - pairwise_distances(ratings_f2.T, metric="cosine")
user_correlation[np.isnan(user_correlation)] = 0

# replace indices with column indices from ratings_f2
user_correlation_df = pd.DataFrame(
    user_correlation, index=ratings_f2.columns, columns=ratings_f2.columns
)

##%
print("Shape of User Similarity Matrix:", user_correlation.shape)
# Item Similarity Matrix
item_correlation = 1 - pairwise_distances(ratings_f2, metric="cosine")
item_correlation[np.isnan(item_correlation)] = 0
print("Shape of Item Similarity Matrix:", item_correlation.shape)

# replace indices with row indices from ratings_f2
# item_correlation_df = pd.DataFrame(item_correlation, index=ratings_f2.index, columns=ratings_f2.index)


#%%


def predict(ratings, similarity, mode="user"):
    if mode == "user":
        mean_user_rating = np.array(ratings.replace(0, np.nan).mean(axis=1))
        # Use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = np.array(ratings) - mean_user_rating[:, np.newaxis]
        pred = (
            mean_user_rating[:, np.newaxis]
            + similarity.dot(ratings_diff)
            / np.array([np.abs(similarity).sum(axis=1)]).T
        )
    elif mode == "item":
        mean_item_rating = np.array(ratings.replace(0, np.nan).mean(axis=0))
        ratings_diff = np.array(ratings) - mean_item_rating[np.newaxis, :]
        pred = mean_item_rating[np.newaxis, :] + ratings_diff.dot(
            similarity
        ) / np.array([np.abs(similarity).sum(axis=1)])
    elif mode == "content":
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return np.clip(pred, a_min=0, a_max=5)
    # return pred


item_prediction = predict(ratings_f2.T, item_correlation, mode="item")
user_prediction = predict(ratings_f2.T, user_correlation, mode="user")


# replace indices with row indices from ratings_f2
user_prediction_df = pd.DataFrame(
    user_prediction, index=ratings_f2.columns, columns=ratings_f2.index
)
item_prediction_df = pd.DataFrame(
    item_prediction, index=ratings_f2.columns, columns=ratings_f2.index
)

# transpose the ratings_f2 dataset
ratings_f2_T = ratings_f2.T


#%%

ratings_f2_T.to_csv('C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\user-item-matrix.csv')
user_prediction_df.to_csv('C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\user-predictions.csv')
item_prediction_df.to_csv('C:\\Users\\roman\PycharmProjects\\semester_3\\mentalport_challenge\\mp_data-main\\mp_data\\item-predictions.csv')


print("ok")
# TODO: debug pred function
# TODO: normalize ratings
# TODO: remove unnecessary exercises
