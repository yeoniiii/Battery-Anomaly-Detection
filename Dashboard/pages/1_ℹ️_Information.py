import streamlit as st
import pandas as pd
import altair as alt
from libraries.load_data import *

st.set_page_config(
    page_title="Guides",
    page_icon="ℹ️",
    layout = "wide"
)

st.sidebar.info("✅ Check out our Battery Pack Information")
st.markdown("# 배터리팩 안내")
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
    NG5 = load_test_df(5)
    NG6 = load_test_df(6)
    NG7 = load_test_df(7)

    col21, col22 = st.columns(2)
    with col21:
        with st.container(border=True):
            st.write("#### 1️⃣ 용량 불량")
            type1 = NG5.iloc[800:2500, 23:199]
            type1['time'] = pd.to_datetime(NG5.iloc[800:2500, 1])
            type1 = pd.melt(type1, id_vars=['time'], var_name='Column', value_name='Voltage')

            chart1 = (
                alt.Chart(type1)
                .mark_line()
                .encode(
                    x = alt.X("time"),
                    y = alt.Y("Voltage", scale=alt.Scale(domain=[3.6, 3.85])),
                    color = alt.Color("Column", legend=None)
                )
            )
            st.altair_chart(chart1)

            st.write("""
                    충·방전 시험 과정에서 특정 배터리셀에서 급격하게 전압이 상승/하강하는 구간이 발견된다. 충전의 경우 초기에 비슷하게 출발하나 충전이 완료된 후 비교해 보면 그 차이가 뚜렷하다. 하지만 배터리모듈 간의 평균 전압 차이도 고려해야 하기 때문에 불량 판정 시 경계성 판단이 요구되므로 전문가 검토가 필수적이다.
                    """)
            

        with st.container(border=True):
            st.write("#### 3️⃣ 센싱 와이어 불량")
            type3 = NG7.iloc[4000:, 23:199]
            type3['time'] = pd.to_datetime(NG7.iloc[4000:, 1])
            type3 = pd.melt(type3, id_vars=['time'], var_name='Column', value_name='Voltage')

            chart3 = (
                alt.Chart(type3)
                .mark_line()
                .encode(
                    x = alt.X("time"),
                    y = alt.Y("Voltage", scale=alt.Scale(domain=[3, 4.4])),
                    color = alt.Color("Column", legend=None)
                )
            )
            st.altair_chart(chart3)

            st.write("""
                    배터리모듈을 구성하는 배터리셀들의 온도나 전압을 측정하기 위해 센싱와이어로 서로 연결되어있다. 와이어에서 불량이 발생하는 경우 인접한 배터리셀들의 전압에 차이가 발생하게 된다.
                    """)
            

    with col22:
        with st.container(border=True):
            st.write("#### 2️⃣ 용접 불량")
            type2 = NG5.iloc[:1000, 23:199]
            type2['time'] = pd.to_datetime(NG5.iloc[:1000, 1])
            type2 = pd.melt(type2, id_vars=['time'], var_name='Column', value_name='Voltage')

            chart2 = (
                alt.Chart(type2)
                .mark_line()
                .encode(
                    x = alt.X("time"),
                    y = alt.Y("Voltage", scale=alt.Scale(domain=[3.62, 3.73])),
                    color = alt.Color("Column", legend=None)
                )
            )
            st.altair_chart(chart2)

            st.write("""
                    입고 검사 과정에서 통과된 배터리셀들은 배터리모듈의 형태로 조립되어 용접이 진행된다. 용접한 부위는 외관상 문제가 없어 보이더라도 특정 배터리셀에서 전압이 측정되지 않거나 배터리셀 전체 전압이 떨어져 있는 현상이 나타날 수 있는데, 이 경우 용접불량을 의심해봐야 한다.
                    """)


        with st.container(border=True):
            st.write("#### 4️⃣ 센서 불량")
            type4 = NG6.iloc[:, 199:231]
            type4['time'] = pd.to_datetime(NG6.iloc[:, 1])
            type4 = pd.melt(type4, id_vars=['time'], var_name='Column', value_name='Temperature')

            chart4 = (
                alt.Chart(type4)
                .mark_line()
                .encode(
                    x = alt.X("time"),
                    y = alt.Y("Temperature", scale=alt.Scale(domain=[23, 28])),
                    color = alt.Color("Column", legend=None)
                )
            )
            st.altair_chart(chart4)

            st.write("""
                    배터리모듈에 장착된 온도센서의 측정값이 너무 높거나 낮게 출력되는 경우 센서불량을 의심해야 한다. 일반적으로 센서를 교체하면 해당 문제를 해결 할 수 있으나 간혹 배터리모듈에 장착된 BMS의 파라미터 설정이 잘못되어 값이 이상하게 측정될 수 있으므로 양측 점검이 필요하다.
                    """)



with tab3:
    st.header("Battery Pack Anomaly Detection")
    
    with st.container(border=True):

        col1, col2 = st.columns([0.4, 0.6])

        with col1:
            tadgan_img = load_img('tadgan')
            st.image(tadgan_img)

        with col2:
            st.write("""
                     #### TadGAN
                     ###### 시계열 기반 비지도 학습 모델
                     - 학습 데이터에 양/불 여부에 대한 정보가 존재하지 않으므로, 비지도 학습 기반의 시계열 분석 모델인 TadGAN 활용  
                     - 양품 배터리팩 데이터 분포를 학습 후 생성된 불량품 데이터를 판별할 수 있도록 훈련
            """)

    with st.container(border=True):
        col3, col4 = st.columns([0.4, 0.6])

        with col3:
            st.write("""
                     #### MLOps Pipeline
                     ###### 모델 구축 및 운영, 배포
                     - 운영계와 개발계로 분리하여 MLOps 파이프라인 구축  
                     - 개발계에서 불량 데이터 검출 모델 학습, 적절한 성능을 보일 경우 운영계로 배포 시작
            """)

        with col4:
            mlops_img = load_img('mlops')
            st.image(mlops_img)