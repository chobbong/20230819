import streamlit as st

st.set_page_config(
    page_icon=":goose:",
    page_title="떼돈팀",
    layout="wide",
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Modeling 개요", "Model-1", "Model-2", "Model-3","Model-4"])

with tab1:
     st.header("""
               Modeling 개요
               """)

with tab2:
     st.header("""
               Model-1
               """)

with tab3:
     st.header("""
               Model-2
               """)
with tab4:
     st.header("""
               Model-3
               """)
with tab5:
     st.header("""
               Model-4
               """)