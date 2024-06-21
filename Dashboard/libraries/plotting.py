import pandas as pd
from libraries.load_data import load_test_df
import plotly.express as px
import streamlit as st

NG5 = load_test_df(5)
NG6 = load_test_df(6)
NG7 = load_test_df(7)


@st.cache_resource
def plot_defective(n):
    if n == 1:
        type1 = NG5.iloc[800:2500, 23:199]
        type1['time'] = pd.to_datetime(NG5.iloc[800:2500, 1])
        type1 = pd.melt(type1, id_vars=['time'], var_name='Column', value_name='Voltage')

        fig1 = px.line(type1, x='time', y='Voltage', color='Column')
        fig1.update_layout(showlegend=False)

        return fig1
    
    if n == 2:
        type2 = NG5.iloc[:1000, 23:199]
        type2['time'] = pd.to_datetime(NG5.iloc[:1000, 1])
        type2 = pd.melt(type2, id_vars=['time'], var_name='Column', value_name='Voltage')

        fig2 = px.line(type2, x='time', y='Voltage', color='Column')
        fig2.update_layout(showlegend=False)

        return fig2
    
    if n == 3:
        type3 = NG7.iloc[4000:, 23:199]
        type3['time'] = pd.to_datetime(NG7.iloc[4000:, 1])
        type3 = pd.melt(type3, id_vars=['time'], var_name='Column', value_name='Voltage')

        fig3 = px.line(type3, x='time', y='Voltage', color='Column')
        fig3.update_layout(showlegend=False)
        
        return fig3
    
    if n == 4:
        type4 = NG6.iloc[:, 199:231]
        type4['time'] = pd.to_datetime(NG6.iloc[:, 1])
        type4 = pd.melt(type4, id_vars=['time'], var_name='Column', value_name='Temperature')

        fig4 = px.line(type4, x='time', y='Temperature', color='Column')
        fig4.update_layout(showlegend=False)

        return fig4