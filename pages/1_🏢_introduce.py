import streamlit as st


st.set_page_config(
    page_icon=":goose:",
    page_title="떼돈팀",
    layout="wide",
)

st.header("""
          Introduction
          """)

st.image('./img/lease_sago.png', width=700)

st.write("""
         전세 사기의 피해자 10명중 7명은 2030세대.  
         관련 법과 안전한 전세계약을 하는 법을 잘 모르는 2030세대를 위해
         '안전한 전세 계약'을 위해  '역전세 여부'를 한눈에 알아볼 수 있는 서비스를 제공합니다.
         """)

st.write("""
         2019년도부터 2023년도까지 전국 실거래가 데이터를 활용하여 
         실매매가 대비 전세가율을 확인하고, 
         역전세 위험이 있는 물건을 지도에서 확인할 수 있습니다.
         """)

st.write("""
         또한, 최신의 Deep_Learning 기술을 활용하여
         매매가와 전세가를 예측하는 모델을 통해 향후 역전세가 발생하는지 예측할 수 있습니다.
         """)

