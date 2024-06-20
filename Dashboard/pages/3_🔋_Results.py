import streamlit as st
import pandas as pd
import os
from libraries.check_output import check_score

st.set_page_config(
    page_title="Results",
    page_icon="🔋",
)

st.markdown("# 배터리팩 이상치 탐지 결과")

if not check_score():
    st.warning("이전 페이지에서 시험을 시작해주세요.")
else:
    file_dir = os.path.join(os.getcwd(), 'Dashboard/score.csv')
    data = pd.read_csv(file_dir)
    st.write('yeah!')
