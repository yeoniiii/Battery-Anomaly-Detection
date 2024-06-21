import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠"
)

import os
from PIL import Image
from libraries.check_output import check_score
from libraries.load_data import load_img



st.sidebar.info("""
    👋 Welcome to Battery Pack Test Dashboard!
""")

home_img = load_img('home')
st.image(home_img)

st.title('배터리팩 불량품 탐지 대시보드')

st.write(
    """
    > ##### 전기차용 배터리팩 충∙방전 시험 및 불량품 탐지 대시보드입니다.
    `🪫 Testing` 페이지에서 배터리팩 충∙방전 시험을 진행하실 수 있습니다.  
    `🔋 Results` 페이지에서 배터리팩 불량품 탐지 결과를 확인하실 수 있습니다.
    """
)

st.markdown("""
            <br><hr>
            <p style='text-align: right; color: gray;'><small>
            고려대학교 일반대학원 통계학과 <br> 고정현 김아롬 김혜연 이다경
            </small></p>""", unsafe_allow_html=True)
st.caption("")

if check_score():
    os.remove('./Dashboard/results/score.csv')