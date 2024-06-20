import streamlit as st
import os
from PIL import Image
from libraries.check_output import check_score

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.sidebar.info("""
    👋 Welcome to Battery Pack Test Dashboard!
""")

img = Image.open('./Dashboard/images/home_img.jpg')
st.image(img)

if check_score():
    os.remove('./Dashboard/score.csv')


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