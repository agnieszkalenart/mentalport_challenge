# standard library imports
import json

# 3rd party imports
import numpy as np

def get_user_exercise_results(df):
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
    #return df["user_id"]


def get_user_users(df):
    """
    Extracts the user_id from the users dataframe
    :param df: the users dataframe
    :return: the newly created column "user_id"
    """
    return df["__key__"].apply(lambda x: json.loads(x)["__key__"]["name"])
    #return df["user_id"]


def get_satisfaction(df):
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


def get_date(df):
    """
    Extracts the date from the exercise_results dataframe
    :param df: the exercise_results dataframe
    :return: the newly created column "date"
    """
    return df["endTime"].apply(lambda x: json.loads(x)["endTime"]["date_time"])

    #return df["endtime"]


def predict(ratings, similarity, mode="user"):
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
