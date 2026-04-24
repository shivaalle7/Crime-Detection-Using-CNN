import streamlit as st

def metrics():
    c1,c2,c3 = st.columns(3)
    c1.metric('Active Cameras','03')
    c2.metric('Alerts Today','07')
    c3.metric('Health','99%')