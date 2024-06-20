import pandas as pd
import sys
import time

serial_num = sys.argv[1]
def calculate_score(serial_num):
    df = pd.DataFrame({'i':[serial_num], 'score':[100]})
    df.to_csv('./Dashboard/score.csv', index=False)
    return df

time.sleep(5)
print(calculate_score(serial_num))