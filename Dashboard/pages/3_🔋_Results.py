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



st.markdown("# 배터리팩 이상치 탐지 결과")

if not check_score():
    st.warning("이전 페이지에서 시험을 시작해주세요.")
else:
    score_dir = os.path.join(os.getcwd(), './Dashboard/results/final_score_예시.csv')
    pred_dir = os.path.join(os.getcwd(), './Dashboard/results/pred_예시.csv')
    score = pd.read_csv(score_dir)
    pred = pd.read_csv(pred_dir)


    result = pd.merge(score, pred, on='idx')
    result['prediction'] = result['prediction'].map({0: '양품', 1: '불량품'})

    st.header("Battery Pack Anomaly Detection Result")
    st.caption("💁 배터리팩 불량품 탐지 결과입니다.")

    fig_color = px.colors.qualitative.Plotly
    fig_score = px.line(result, x='idx', y='final_scores', color='prediction', 
                        labels={
                            'idx': "Time",
                            'final_scores': "Score",
                            'prediction': "탐지 결과"
                        },
                        color_discrete_sequence=fig_color)
    st.plotly_chart(fig_score)


