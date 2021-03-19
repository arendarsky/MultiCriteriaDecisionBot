import pandas as pd
import numpy as np
from paretoset import paretoset


score_col = "score"


def sort(df, asc):
    return df.sort_values(by=[score_col], ascending=asc)


def pareto_set(df):
    ps = pd.DataFrame(df[~paretoset(df)])
    return ps


def weighted_sum(df, weights):
    df_copy = df.copy()
    weights = np.array(weights).reshape(len(weights), 1)
    df_copy[score_col] = df.dot(weights)
    df_copy = sort(df_copy, False)
    return df_copy


def ideal_point_method(df):
    df_copy = df.copy()
    ideal_point = df_copy.max()
    df_copy["score"] = np.sqrt(np.square(df_copy - ideal_point).sum(axis=1))
    df_copy = sort(df_copy, True)
    return df_copy
