import streamlit as st

st.set_page_config(
    page_title="Guides",
    page_icon="ℹ️",
)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import subprocess
import time
import os


st.markdown("# 배터리팩 가이드")
tab1, tab2, tab3 = st.tabs(["🔋 충∙방전 시험", "🪫 불량품 유형", "🔎 불량품 탐지"])


with tab1:
    st.header("Battery Pack Test")
    with st.container(border=True):
        st.write("""
                #### 배터리팩 충∙방전 시험
                - **❓ 배터리팩 충∙방전 시험이란**  
                    전기차용 배터리팩의 불량품 여부를 판정하기 위한 충∙방전 시험입니다.  
                    배터리팩 전용 시험 설비를 사용하며, 엔지니어가 배터리팩의 각종 상태 데이터를 분석하여 최종 판정을 내리고 조립 및 납품을 지시합니다.   
                 
                - **❓ 문제 상황**  
                    선별 과정이 수작업으로 이루어지는 공장의 경우, 일관된 품질 보장이 어렵습니다.  
                    양/불 판정 시 경계성 판단이 요구될 경우, 숙련된 작업자가 필요합니다. 이로 인해 관련 사업 해외 진출 시 숙련된 검사 작업자 구인의 어려움이 따릅니다.  
                """)
    
    with st.container(border=True):
        st.write("""
                #### 따라서, AI 기반 솔루션을 제안합니다.  
                - **‼️  품질관리 강화 및 생산성 향상**  
                    AI 모델을 사용하여 품질관리를 강화하고, 불량 발생 원인을 분석하여 생산 공정을 최적화하고자 합니다.  
                 
                -  **‼️  지속 가능한 라이프사이클 관리**  
                    BMS 기반 제조데이터 수집 및 저장 체계에 기반한 배터리팩 공정의 라이프사이클을 효과적으로 관리할 수 있게 됩니다.
                """)
        
with tab2:
    st.header("Battery Pack Defective Types")

with tab3:
    st.header("Battery Pack Anomaly Detection")
    