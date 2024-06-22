import pandas as pd
import numpy as np

from scipy import interpolate

from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from sklearn.base import BaseEstimator, TransformerMixin
import os, sys

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from datetime import datetime




def time_segments_aggregate(X, interval, time_column, method=['mean']):

    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)
    X = X.sort_values(time_column).set_index(time_column)
    if isinstance(method, str):
        method = [method]
    start_ts = X.index.values[0]
    max_ts = X.index.values[-1]
    values = list()
    index = list()
    while start_ts <= max_ts:
        end_ts = start_ts + interval
        subset = X.loc[start_ts:end_ts-1]
        aggregated = [getattr(subset, agg)(skipna=True).values for agg in method]
        values.append(np.concatenate(aggregated))
        index.append(start_ts)
        start_ts = end_ts
    return np.asarray(values), np.asarray(index)


def simple_minmax(X):
    X = SimpleImputer().fit_transform(X)
    X = MinMaxScaler(feature_range = (-1, 1)).fit_transform(X)
    return X

def rolling_window_sequences(X, index, window_size, target_size, step_size, target_column, drop=None, drop_windows=False):

    out_X = list()
    out_y = list()
    X_index = list()
    y_index = list()
    target = X[:, target_column]
    if drop_windows:
        if hasattr(drop, '__len__') and (not isinstance(drop, str)):
            if len(drop) != len(X):
                raise Exception('Arrays `drop` and `X` must be of the same length.')
        else:
            if isinstance(drop, float) and np.isnan(drop):
                drop = np.isnan(X)
            else:
                drop = X == drop
    start =0
    max_start = len(X) - window_size - target_size + 1
    while start < max_start:
        end = start + window_size
        if drop_windows:
            drop_window = drop[start:end+target_size]
            to_drop = np.where(drop_window)[0]
            if to_drop.size:
                start += to_drop[-1] + 1
                continue
        out_X.append(X[start:end])
        out_y.append(target[end:end+target_size])
        X_index.append(index[start])
        y_index.append(index[end])
        start = start + step_size
    return np.asarray(out_X), np.asarray(out_y), np.asarray(X_index), np.asarray(y_index)

