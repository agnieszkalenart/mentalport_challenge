"""
This file contains useful functions for the project
"""

# standard library imports
import json
import re

# 3rd party imports
import numpy as np


#### helper functions for the filters ##################################################################################
def preprocess_time(data, time_col):
    """
    TODO: Add docstring
    :param data:
    :param time_col: the name of the time column
    :return:
    """
    pattern = re.compile("\d")
    data[time_col] = data[time_col].fillna("0")
    mapping = [((pattern.search(item) is not None)  == False) for item in data[time_col]]
    data[time_col][mapping] = "0"
    data[time_col] = [item.split('/')[-1] for item in data[time_col]]
    data[time_col] = [item.split('*')[-1] for item in data[time_col]]
    data[time_col] = [item.split('-')[0] for item in data[time_col]]
    data[time_col].replace(to_replace="[A-Z]", value="", regex=True)
    pattern3 = re.compile("[a-z]")
    patternSpace = re.compile(" ")
    data[time_col]= [re.sub(string = item, pattern=pattern3, repl ="") for item in data[time_col]]
    data[time_col] = [re.sub(string = item, pattern=patternSpace, repl ="") for item in data[time_col]]
    return data

def filter_time (maxTime, data, time_col):
    """

    :param maxTime:
    :param data:
    :param time_col: the name of the time column
    :return:
    """
    preprocess_time(data, time_col)
    filtered_data = data[(data[time_col].astype(int)) < maxTime]
    return filtered_data

#### helper functions for collaborative filtering ######################################################################
def get_user_exercise_results(df) -> np.ndarray:
    """
    Extracts the user_id from the exercise_results dataframe
    :param df: the exercise_results dataframe
    :return: the newly created column "user_id"
    """
    return df["__key__"].apply(
        lambda x: json.loads(x)["__key__"]["path"]
        .replace(" ", "")
        .replace('"', "")
        .split(",")[1]
    )


def get_user_users(df) -> np.ndarray:
    """
    Extracts the user_id from the users dataframe
    :param df: the users dataframe
    :return: the newly created column "user_id"
    """
    return df["__key__"].apply(lambda x: json.loads(x)["__key__"]["name"])


def get_satisfaction(df) -> np.ndarray:
    """
    Extracts the satisfaction score from the exercise_results dataframe
    :param df: the exercise_results dataframe
    :return: the newly created column "satisfaction"
    """
    sat = df["feedback"].apply(
        lambda x: json.loads(x)["feedback"]["exerciseRating"]["satisfaction"]
    )
    sat = sat.apply(
        lambda x: None if (x is None) else int(x[0])
    )
    return sat


def get_date(df) -> np.ndarray:
    """
    Extracts the date from the exercise_results dataframe
    :param df: the exercise_results dataframe
    :return: the newly created column "date"
    """
    return df["endTime"].apply(lambda x: json.loads(x)["endTime"]["date_time"])


def predict(ratings, similarity, mode="user") -> np.ndarray:
    """
    Creates the user or item based collaborative filtering prediction matrix
    :param ratings: The user-item matrix containing the ratings
    :param similarity: The user-user or item-item similarity matrix
    :param mode: The mode of the collaborative filtering algorithm ("user" or "item")
    :return: The user or item based collaborative filtering prediction matrix
    """
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
    return np.clip(pred, a_min=0, a_max=5)
