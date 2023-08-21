import streamlit as st

st.set_page_config(
    page_icon=":goose:",
    page_title="떼돈팀",
    layout="wide",
)

tab1, tab2, tab3 = st.tabs(["Data 개요", "EDA", "Preprocessing"])

with tab1:
     st.header("""
               Data 개요
               """)

with tab2:
     st.header("""
               EDA
               """)

with tab3:
     st.header("""
               Preprocessing
               """)