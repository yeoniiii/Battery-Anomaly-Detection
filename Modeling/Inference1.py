import pandas as pd
import numpy as np
from scipy import stats
from scipy import interpolate
import os

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import tensorflow as tf
from tensorflow.python.ops.gen_data_flow_ops import ResourceAccumulatorTakeGradient
from tensorflow.keras.models import load_model

 
from Anomaly import *


def predict(X):
    folder_dir = os.getcwd() + '/Modeling/models/'
    encoder = load_model(folder_dir + 'encoder_model.keras')
    generator = load_model(folder_dir + 'generator_model.keras')
    critic_x = load_model(folder_dir + 'critic_x_model.keras')
    critic_z = load_model(folder_dir + 'critic_z_model.keras')

    X = X.reshape((-1, 10, 3))
    z_ = encoder.predict(X, verbose=0)
    y_hat = generator.predict(z_, verbose=0)
    critic = critic_x.predict(X, verbose=0)

    return y_hat, critic


def anomaly(X, y_hat, critic, X_index):
    anomaly = Anomaly()
    final_scores, true_index, true, predictions = anomaly.score_anomalies(X, y_hat, critic, X_index, comb="mult")
    final_scores = np.array(final_scores)
    anomalies = anomaly.find_anomalies(final_scores, true_index)
    #anom_labels = known_anomalies['label']
    time = true_index

    #true0 = anom_labels

    pred_length =len(final_scores)
    avg = np.average(final_scores)
    sigma = math.sqrt(sum((final_scores-avg) * (final_scores-avg)) /len(final_scores))
    Z_score1 = (final_scores-avg) / sigma
    pred_bin=[0]*pred_length
    for i in range(len(anomalies)):
        # print( anomalies[i][0], anomalies[i][1])
        for k in range(anomalies[i][0]-1, anomalies[i][1]):
            pred_bin[k]=1

    #true = []
    #true = true0[: pred_length]
    pred = np.array(pred_bin)
    #gt = np.array(true)
    #n_pred =len(pred)

    result = pd.DataFrame({'final_score' : final_scores, 'pred' : pred})
    return result
    







