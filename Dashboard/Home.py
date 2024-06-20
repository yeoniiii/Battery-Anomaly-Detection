import streamlit as st
import os
from libraries.check_output import check_score

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.sidebar.write("""
    Battery Pack Test Dashboard
""")

st.title('배터리팩 이상치 탐지 대시보드')

st.markdown(
    """
    전기차용 배터리팩 충∙방전
    """
)

if check_score():
    os.remove('./Dashboard/score.csv')