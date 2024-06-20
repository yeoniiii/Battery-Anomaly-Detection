import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import subprocess
import time
import os


st.set_page_config(
    page_title="Testing...",
    page_icon="🪫",
)

st.markdown("# 배터리팩 충∙방전 시험")
tab1, tab2 = st.tabs(["⚙️ 시험 세팅", "🔎 시험 진행 상황"])


with tab1:
    st.header("Battery Pack Test Settings")

    if 'test_running' not in st.session_state:
        st.session_state.test_running = False
    if 'test_finished' not in st.session_state:
        st.session_state.test_finished = False


    with st.container(border=True):
        st.write("""
                 #### 1️⃣ 배터리팩 선택
                 배터리팩 충∙방전 시험을 진행할 시리얼 넘버를 선택해주세요.
                 """)
        slider_value = st.slider(
            "배터리팩 시리얼 넘버 슬라이더",
            1, 9, step=1,
            label_visibility='collapsed'
            )
        slider_value = slider_value
        st.write("- Selected Serial Number:", slider_value)
    

    with st.container(border=True):
        sidebar_before = st.sidebar.warning("시험 시작 전입니다.")

        st.write("#### 2️⃣ 시험 시작")
        st.write(slider_value, "번 배터리팩 시험을 시작하려면 아래 버튼을 누르세요.")
        
        button_start = st.button("Start", type="primary")
        
        if button_start:
            st.session_state.test_running = True
            command = ["python3", "../Modeling/run.py", str(slider_value)]
            test = subprocess.Popen(command)

            sidebar_before.empty()
            sidebar_ing = st.sidebar.info(f"{slider_value}번 배터리팩 충∙방전 시험 중입니다.")
            message_ing1 = st.info("시험을 진행 중입니다.")
            message_ing2 = st.caption("시험을 중단하려면 시리얼 넘버를 다시 선택하거나 아래 버튼을 누르세요.")

            button_stop = st.button("Stop", disabled=st.session_state.test_finished)
            if button_stop:
                test.kill()
                st.rerun()
            
            time.sleep(6)
            if test and test.poll() is not None:
                test = None
                st.session_state.test_finished = True
                st.session_state.test_running = False

                sidebar_ing.empty()
                message_ing1.empty()
                message_ing2.empty()

                st.success("시험이 완료되었습니다! 다음 탭에서 진행 상황을 확인하세요.")
                sidebar_end = st.sidebar.success(f"{slider_value}번 배터리팩 충∙방전 시험이 완료되었습니다.")

            

with tab2:
    st.header("Battery Pack Test Progress Chart")
    if not button_start:
            st.warning("이전 탭에서 시험을 시작해주세요.")

    else:
        with st.container(border=True):
            st.write(f"#### {slider_value}번 배터리팩 충∙방전 시험 차트")

            folder_dir = '../Dataset/data/raw_data/test'
            files = os.listdir(folder_dir)
            file = [f for f in files if str(slider_value) in f]
            file_dir = os.path.join(folder_dir, file[0])

            data = pd.read_csv(file_dir)

            placeholder = st.empty()

            for seconds in range(len(data)//10):
                if not st.session_state.test_running and not st.session_state.test_finished:
                    break

                df = data.iloc[:10 * (seconds + 1), :]  

                with placeholder.container():
                    plot1, plot2 = st.columns(2)

                    with plot1:
                        st.markdown("###### ⚡️ Voltage Chart")
                        TIME = df.iloc[:, 1]
                        TIME = pd.to_datetime(TIME)
                        CV = df.iloc[:, 23 : 199]
                        fig, ax = plt.subplots()
                        
                        plt.style.use(['ggplot'])
                        for i in CV.columns:
                            plt.plot(TIME, CV[i], linewidth = 1)
                        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                        plt.xticks(rotation=45)
                        plt.xlabel("Time")
                        plt.ylabel("Voltage")
                        plt.ylim(min(CV.min() * 0.99), max(CV.max()) * 1.01)
                        st.pyplot(fig)


                    with plot2:
                        st.markdown("###### 🌡️ Temperature Chart")
                        TE = df.iloc[:, 199 : 231]
                        fig2, ax = plt.subplots()
                        
                        plt.style.use(['ggplot'])
                        for i in TE.columns:
                            plt.plot(TIME, TE[i], linewidth = 1)
                        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                        plt.xticks(rotation=45)
                        plt.xlabel("Time")
                        plt.ylabel("Temperature")
                        plt.ylim(min(TE.min() * 0.9), max(TE.max()) * 1.1)
                        st.pyplot(fig2)

                    time.sleep(.5)