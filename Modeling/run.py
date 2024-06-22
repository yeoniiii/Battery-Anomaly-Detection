import os
import sys
import pandas as pd
from preprocessing import *
from preprocessing2 import *
from Inference1 import *

serial_num = sys.argv[1]

def calculate_score(serial_num):

    folder_dir = './Dataset/data/raw_data/test'
    files = os.listdir(folder_dir)
    file = [f for f in files if str(serial_num) in f]
    file_dir = os.path.join(folder_dir, file[0])
    df_test = pd.read_csv(file_dir)

    preprocess = PreprocessPipe()
    df = preprocess.fit_transform(df_test)
    X, index = time_segments_aggregate(df, interval = 1, time_column = 'date')
    X = simple_minmax(X)
    X, y, X_index, y_index = rolling_window_sequences(X, index, window_size = 10,   target_size = 1, step_size =1, target_column=0)
    y_hat, critic = predict(X)
    final_result = anomaly(X, y_hat, critic, X_index)
    # final_result.to_csv('./Dashboard/result.csv')
    open('./Dashboard/result.csv', 'w').write(final_result.to_csv())

calculate_score(serial_num)
