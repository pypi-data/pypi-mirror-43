#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import pandas as pd

def get_df_top_k(df, col_user="user", col_item="item", col_rating="rating", k=3):
    """
    Truncate user-item-rating dataframe by top K rating

    Every user will only keep top K best rating items
    """
    grouped_user_top_k_df = df.groupby(col_user, as_index=False)\
        .apply(lambda x: x.nlargest(k, col_rating))\
        .reset_index(drop=True)

    return grouped_user_top_k_df


def merge_ranking_true_pred(rating_true,
                            rating_pred,
                            col_user="user",
                            col_item="item",
                            col_rating="rating",
                            col_prediction="rating",
                            k=3):
    # prediction dataframe only need the top K items for each user
    rating_pred_top_k = get_df_top_k(rating_pred, k=k)

    common_user_list = list(set(rating_true[col_user]).intersection(set(rating_pred_top_k[col_user])))

    rating_pred_in_calc = rating_pred_top_k[rating_pred_top_k[col_user].isin(common_user_list)]
    rating_true_in_calc = rating_true[rating_true[col_user].isin(common_user_list)]

    number_users = len(common_user_list)

    rating_pred_in_calc["ranking"] = rating_pred_in_calc.groupby(col_user)[col_prediction].rank(method="first", ascending=False)

    # print('--- in calc pred')
    # print(rating_pred_in_calc)
    # print('--- in calc true')
    # print(rating_true_in_calc)

    hit_df = pd.merge(
        rating_true_in_calc, rating_pred_in_calc,
        how="inner", on=[col_user, col_item]
    )[[col_user, col_item, "ranking"]]

    # print(hit_df)
    return rating_true_in_calc, hit_df, number_users




def precision_top_k(rating_true,
                    rating_pred,
                    col_user="user",
                    col_item="item",
                    col_rating="rating",
                    col_prediction="rating",
                    k=3):
    """
    Precition at K
    """
    _, df_hit, number_users = merge_ranking_true_pred(
        rating_true, rating_pred, col_user, col_item, col_prediction, k=k)

    if len(df_hit) == 0:
        print("Prediction didn't hit any in ground truth dataframe")
        return 0.0

    # print(df_hit)
    # groupby the user and count each users' hit times
    df_hit_count = (df_hit.groupby(col_user)\
                    .agg({col_item: "count"})\
                    .reset_index()\
                    .rename(columns={col_item: "hit_count"}))
    # print(df_hit_count)

    df_hit_count["precision"] = df_hit_count.apply(lambda x: x["hit_count"] / k, axis=1)
    # print(df_hit_count)
    return np.float64(df_hit_count.agg({"precision": "sum"})) / number_users


def recall_top_k(rating_true, rating_pred,
                 col_user="user", col_item="item",
                 col_rating="rating", col_prediction="rating", k=3):
    """
    Recall at K

    """
    rating_true_df, df_hit, number_users = merge_ranking_true_pred(
        rating_true, rating_pred, col_user, col_item, col_prediction, k=k)

    if len(df_hit) == 0:
        return 0.0

    df_hit_count = (df_hit.groupby(col_user)\
                    .agg({col_item: "count"})\
                    .reset_index()\
                    .rename(columns={col_item: "hit_count"}))

    df_true_count = (rating_true_df.groupby(col_user)\
                     .agg({col_item: "count"})\
                     .reset_index()\
                     .rename(columns={col_item: "actual_count"}))

    df_count_all = pd.merge(df_hit_count, df_true_count, on=col_user)
    df_count_all["recall"] = df_count_all.apply(lambda x: (x["hit_count"] / x["actual_count"]), axis=1)

    return np.float64(df_count_all.agg({"recall" : "sum"})) / number_users


def ndcg_top_k(rating_true, rating_pred,
               col_user="user", col_item="item",
               col_rating="rating", col_prediction="rating", k=3):
    """
    Normalized Discounted Cumulative Gain
    """
    rating_true_df, df_hit, number_users = merge_ranking_true_pred(
        rating_true, rating_pred, col_user, col_item, col_prediction, k=k)

    if len(df_hit) == 0:
        return 0.0

    df_dcg = df_hit.sort_values([col_user, "ranking"])
    df_dcg["dcg"] = df_dcg.apply(lambda x: 1 / np.log(x["ranking"]+1), axis=1)

    df_dcg_sum = df_dcg.groupby(col_user).agg({"dcg": "sum"}).reset_index()

    def log_sum(iter_length):
        _sum = 0
        for l in range(iter_length):
            _sum = _sum + 1 / np.log(l + 2)

        return _sum

    # print(rating_true_df)
    df_true_count = (rating_true_df.groupby(col_user)\
                   .agg({col_item: "count"})\
                   .reset_index()\
                   .rename(columns={col_item: "actual_count"}))

    # print(df_true_count)

    df_true_count["mdcg"] = df_true_count.apply(lambda x: log_sum(min(x["actual_count"], k)), axis=1)

    df_ndcg = pd.merge(df_dcg_sum, df_true_count, on=col_user)
    df_ndcg["ndcg"] = df_ndcg.apply(lambda x: x["dcg"] / x["mdcg"], axis=1)

    return np.float64(df_ndcg.agg({"ndcg": "sum"})) / number_users


def map_top_k(rating_true, rating_pred,
              col_user="user", col_item="item",
              col_rating="rating", col_prediction="rating", k=3):
    """
    Mean Average Precision
    """
    rating_true_df, df_hit, number_users = merge_ranking_true_pred(
        rating_true, rating_pred, col_user, col_item, col_prediction, k=k)

    if len(df_hit) == 0:
        return 0.0

    df_hit = df_hit.sort_values([col_user, "ranking"])
    df_hit["group_index"] = df_hit.groupby(col_user).cumcount() + 1
    df_hit["precision"] = df_hit.apply(lambda x: x["group_index"] / x["ranking"], axis=1)
    df_sum_hit = df_hit.groupby(col_user).agg({"precision": "sum"}).reset_index()

    df_true_count = (rating_true_df.groupby(col_user)\
                     .agg({col_item: "count"})\
                     .reset_index()\
                     .rename(columns={col_item: "actual_count"}))

    df_sum_all = pd.merge(df_sum_hit, df_true_count, on=col_user)
    df_sum_all["map"] = df_sum_all.apply(lambda x: x["precision"] / x["actual_count"], axis=1)

    return np.float64(df_sum_all.agg({"map": "sum"})) / number_users


from .rating import merge_rating_true_pred


#from sklearn.metrics import roc_curve, roc_auc_score
#def binar(y_true, y_score):
#    # ensure binary classification if pos_label is not specified
#    classes = np.unique(y_true)
#
#    # sort scores and corresponding truth values
#    desc_score_indices = np.argsort(y_score, kind="mergesort")[::-1]
#    y_score = y_score[desc_score_indices]
#    y_true = y_true[desc_score_indices]
#    weight = 1.
#
#    # y_score typically has many tied values. Here we extract
#    # the indices associated with the distinct values. We also
#    # concatenate a value for the end of the curve.
#    distinct_value_indices = np.where(np.diff(y_score))[0]
#    threshold_idxs = np.r_[distinct_value_indices, y_true.size - 1]
#
#    # accumulate the true positives with decreasing threshold
#    # tps = stable_cumsum(y_true * weight)[threshold_idxs]
#    tps = np.cumsum(y_true * weight)[threshold_idxs]
#
#    fps = 1 + threshold_idxs - tps
#
#    return fps, tps, y_score[threshold_idxs]
#
#def roc_curve_own(rating_true, rating_pred,
#              col_user="user", col_item="item",
#              col_rating="rating", col_prediction="rating"):
#
#    rating_true_pred = merge_rating_true_pred(
#        rating_true, rating_pred, col_user, col_item, col_rating, col_prediction)
#
#    print("-----")
#
#    y_true = rating_true_pred["ground_truth_rating"].values
#    y_score= rating_true_pred["prediction_rating"].values
#    print("=======ORI")
#    fpr, tpr, thres = roc_curve(y_)
#    print("=======END")
#
#    fps, tps, thres  = binar(y_true, y_score)
#    print(fps)
#    print(tps)
#    print(thres)
#
#
#def auc(rating_true, rating_pred,
#        col_user="user", col_item="item",
#        col_rating="rating", col_prediction="rating"):
#    """
#    Area Under Curve
#    """
#    rating_true_pred = merge_rating_true_pred(
#        rating_true, rating_pred, col_user, col_item, col_rating, col_prediction)
#
#    fpr, tpr, thresholds = roc_curve(rating_true_pred["ground_truth_rating"], rating_true_pred["prediction_rating"])
#
#    auc_score = roc_auc_score(
#        rating_true_pred["ground_truth_rating"].values,
#        rating_true_pred["prediction_rating"].values)
#
#    return auc_score
