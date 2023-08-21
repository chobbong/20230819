import streamlit as st
from pyparsing import empty

st.set_page_config(
    page_icon=":goose:",
    page_title="떼돈팀",
    layout="wide",
)

empty1,col1,empty2 = st.columns([0.3,1.0,0.3])
empty1,col2,col3,empty2 = st.columns([0.3,0.5,0.5,0.3])
empty1,col4,col5,empty2 = st.columns([0.3,0.5,0.5,0.3])


with empty1 :
    empty() # 여백부분1

with col1 :
    st.header("""
            😎 떼 돈 팀 😎
            #### 떼인 돈 받아들입니다!!! 
            """)
with col2:
    st.image('./img/imjinwoo.png', width=200)
    st.write("""
    ## 임진우
    """)
    st.write("""
    아이디어와 의욕이 넘치는 팀장!! 💯
    """)

with col3:
    st.image('./img/kimbyumsung.png', width=200)
    st.write("""
    ## 김범성
    """)
    st.write("""
    차분하게 떼인 돈을 받아 올 방법을 기획하는 코딩리스트! 🎸
    """)

with col4:
    st.image('./img/kimwooyoung', width=200)
    st.write("""
    ## 김우영
    """)
    st.write("""
    실행력과 문제해결능력을 갖춘 모델링러! 🦚
    """)

with col5:
    st.image('./img/jys.png', width=200)
    st.write("""
    ## 조윤서
    """)
    st.write("""
    배후에 가려진 알게 모르게 서포터! 🐝
    """)

with empty2 :
    empty() # 여백부분1