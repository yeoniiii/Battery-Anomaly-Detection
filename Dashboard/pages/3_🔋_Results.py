import streamlit as st

st.set_page_config(
    page_title="Results",
    page_icon="🔋",
    layout = "wide"
)

import pandas as pd
import os
from libraries.check_output import check_score
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")



st.markdown("# 배터리팩 이상치 탐지 결과")

if not check_score():
    st.warning("이전 페이지에서 시험을 시작해주세요.")
else:
    result_dir = os.getcwd() + '/Dashboard/results/result.csv'
    result = pd.read_csv(result_dir)
    result['pred'] = result['pred'].map({0: '양품', 1: '불량품'})
    result.rename(columns={'Unnamed: 0':'idx'}, inplace=True)

    fig_color = px.colors.qualitative.Plotly
    fig_score = px.line(result, x='idx', y='final_score', color='pred', 
                        labels={
                            'idx': "Time",
                            'final_score': "Score",
                            'pred': "탐지 결과"
                        },
                        color_discrete_sequence=fig_color)


    st.header("Battery Pack Anomaly Detection Result")
    st.caption("💁 배터리팩 불량품 탐지 결과입니다.")
    st.sidebar.success(f"배터리팩 충∙방전 시험이 완료되었습니다.")

    with st.container(border=True):
        st.write("#### 불량품 탐지 점수 차트")
        st.plotly_chart(fig_score)


