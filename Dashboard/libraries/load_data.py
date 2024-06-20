import streamlit as st
from PIL import Image
import pandas as pd

@st.cache_data
def load_img(img_name):
    return Image.open('./Dashboard/images/' + img_name + '_img.jpg')

@st.cache_data
def load_df(df_dir):
    return pd.read_csv(df_dir)