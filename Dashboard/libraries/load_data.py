import streamlit as st
from PIL import Image
import pandas as pd
import os

@st.cache_data
def load_img(img_name):
    return Image.open('./Dashboard/images/' + img_name + '_img.jpg')

@st.cache_data
def load_test_df(num):
    folder_dir = './Dataset/data/raw_data/test'
    files = os.listdir(folder_dir)
    file = [f for f in files if str(num) in f]
    file_dir = os.path.join(folder_dir, file[0])
    return pd.read_csv(file_dir)