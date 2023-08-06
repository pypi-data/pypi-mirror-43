#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score

def merge_rating_true_pred(rating_true,
                           rating_pred,
                           col_user="user",
                           col_item="item",
                           col_rating="rating",
                           col_prediction="rating"):
    """
    Join truth and prediction data frames on userID and itemID

    Parameters:
        rating_true (pd.DataFrame): True data.
        rating_pred (pd.DataFrame): Predicted data.
        col_user (str): column name for user.
        col_item (str): column name for item.
        col_rating (str): column name for rating.
        col_prediction (str): column name for prediction.
    Returns:
        pd.DataFrame: Merged pd.DataFrame
    """

    rating_true = rating_true[[col_user, col_item, col_rating]]
    rating_pred = rating_pred[[col_user, col_item, col_prediction]]

    if col_rating == col_prediction:
        rating_true_pred = pd.merge(
            rating_true,
            rating_pred,
            on=[col_user, col_item],
            suffixes=["_true", "_pred"],
        )
        rating_true_pred.rename(
            columns={col_rating + "_true": "ground_truth_rating"}, inplace=True
        )
        rating_true_pred.rename(
            columns={col_prediction + "_pred": "prediction_rating"}, inplace=True
        )
    else:
        rating_true_pred = pd.merge(rating_true, rating_pred, on=[col_user, col_item])
        rating_true_pred.rename(columns={col_rating: "ground_truth_rating"}, inplace=True)
        rating_true_pred.rename(columns={col_prediction: "prediction_rating"}, inplace=True)

    return rating_true_pred



def rmse(df_true, df_pred,
         col_user="user", col_item="item", col_rating="rating", col_prediction="rating"):
    """Calculate Root Mean Squared Error

    Args:
        rating_true (pd.DataFrame): True data. There should be no duplicate (userID, itemID) pairs.
        rating_pred (pd.DataFrame): Predicted data. There should be no duplicate (userID, itemID) pairs.
        col_user (str): column name for user.
        col_item (str): column name for item.
        col_rating (str): column name for rating.
        col_prediction (str): column name for prediction.

    Returns:
        float: Root mean squared error.
    """
    df_merged = merge_rating_true_pred(
        df_true, df_pred, col_user, col_item, col_rating, col_prediction
    )

    output_errors = np.average((df_merged["ground_truth_rating"] - df_merged["prediction_rating"]) ** 2, axis=0)

    a = np.sqrt(output_errors)

    b = np.sqrt(mean_squared_error(
        df_merged["ground_truth_rating"], df_merged["prediction_rating"]
    ))
    return (a,b)


def mae(df_true, df_pred,
        col_user="user", col_item="item", col_rating="rating", col_prediction="rating"):
    """Calculate Mean Absolute Error

    Args:
        - rating_true (pd.DataFrame): True data. There should be no duplicate (userID, itemID) pairs.
        - rating_pred (pd.DataFrame): Predicted data. There should be no duplicate (userID, itemID) pairs.
        - col_user (str): column name for user.
        - col_item (str): column name for item.
        - col_rating (str): column name for rating.
        - col_prediction (str): column name for prediction.

    Returns:
        float: Root mean squared error.
    """
    df_merged = merge_rating_true_pred(
        df_true, df_pred, col_user, col_item, col_rating, col_prediction
    )

    output_errors = np.average(np.abs(df_merged["ground_truth_rating"] - df_merged["prediction_rating"]), axis=0)

    b = mean_absolute_error(
                df_merged["ground_truth_rating"], df_merged["prediction_rating"]
    )
    return (output_errors, b)


def r2(df_true, df_pred,
        col_user="user", col_item="item", col_rating="rating", col_prediction="rating"):
    """
    Calculate R Squared Score: 1 - SS_res/SS_tot

    Reference:
        https://en.wikipedia.org/wiki/Coefficient_of_determination

    Args:
        rating_true (pd.DataFrame): True data. There should be no duplicate (userID, itemID) pairs.
        rating_pred (pd.DataFrame): Predicted data. There should be no duplicate (userID, itemID) pairs.
        col_user (str): column name for user.
        col_item (str): column name for item.
        col_rating (str): column name for rating.
        col_prediction (str): column name for prediction.

    Returns:
        float: Root mean squared error.

    """
    df_merged = merge_rating_true_pred(
        df_true, df_pred, col_user, col_item, col_rating, col_prediction
    )

    ground_truth_ave = np.average(df_merged["ground_truth_rating"])

    SS_tot = np.sum((df_merged["ground_truth_rating"] - ground_truth_ave)**2)


    SS_res = np.sum((df_merged["prediction_rating"] - df_merged["ground_truth_rating"])**2)

    c = 1 - SS_res / SS_tot

    b = r2_score(
                df_merged["ground_truth_rating"], df_merged["prediction_rating"]
    )
    return (c, b)


def exp_var(df_true, df_pred,
        col_user="user", col_item="item", col_rating="rating", col_prediction="rating"):
    """
    Calculate explained variance. VAR(ei) / VAR(yi)


    Args:
        rating_true (pd.DataFrame): True data. There should be no duplicate (userID, itemID) pairs.
        rating_pred (pd.DataFrame): Predicted data. There should be no duplicate (userID, itemID) pairs.
        col_user (str): column name for user.
        col_item (str): column name for item.
        col_rating (str): column name for rating.
        col_prediction (str): column name for prediction.
    Returns:
        float: Explained variance (min=0, max=1).
    """
    df_merged = merge_rating_true_pred(
        df_true, df_pred, col_user, col_item, col_rating, col_prediction
    )

    ground_truth_ave = np.average(df_merged["ground_truth_rating"])
    var_y = np.average((df_merged["ground_truth_rating"] - ground_truth_ave)**2, axis=0)


    rr =  df_merged["ground_truth_rating"] - df_merged["prediction_rating"]
    rra = np.average(rr)
    resd = np.average((rr - rra)**2, axis=0)

    a = 1 - resd / var_y

    b =  explained_variance_score(df_merged["ground_truth_rating"], df_merged["prediction_rating"])

    return (a,b)
