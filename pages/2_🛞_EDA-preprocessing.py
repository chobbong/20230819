import streamlit as st
from pyparsing import empty


st.set_page_config(
    page_icon=":goose:",
    page_title="떼돈팀",
    layout="wide",
)

tab1, tab2, tab3 = st.tabs(["김우영", "김범성", "임진우"])

with tab1:
     st.header("""
               김우영
               """)

     # 예제 이미지 파일 리스트
     image_files = [f"./img/kwy/kwy_page_{str(i).zfill(2)}.jpg" for i in range(1, 31)]

     # 세션 상태를 관리하기 위한 클래스 (Streamlit의 state 기능을 사용)
     if 'current_image_idx' not in st.session_state:
          st.session_state.current_image_idx = 0

     # 이미지 표시
     st.image(image_files[st.session_state.current_image_idx], caption=f"Image {st.session_state.current_image_idx + 1}/{len(image_files)}", use_column_width=True)

     # 이전/다음 버튼 생성
     empty1,col2,col3,empty2 = st.columns([1,0.2,0.2,1])
     
     
     with empty1 :
          empty() # 여백부분1
     with col2:
          if st.button("이전"):
               st.session_state.current_image_idx -= 1
               if st.session_state.current_image_idx < 0:
                    st.session_state.current_image_idx = len(image_files) - 1
     with col3:
          if st.button("다음"):
               st.session_state.current_image_idx += 1
               if st.session_state.current_image_idx >= len(image_files):
                    st.session_state.current_image_idx = 0  
     with empty2 :
          empty() # 여백부분1                                                                                                                                          







with tab2:
     st.header("""
               김범성
               """)
     


     # 예제 이미지 파일 리스트
     image_files_2 = [f"./img/kbs/kbs_{str(i).zfill(2)}.jpg" for i in range(1, 13)]

     # 세션 상태를 관리하기 위한 클래스 (Streamlit의 state 기능을 사용)
     if 'current_image_idx_tab2' not in st.session_state:
          st.session_state.current_image_idx_tab2 = 0

     # 이미지 표시
     st.image(image_files_2[st.session_state.current_image_idx_tab2], caption=f"Image {st.session_state.current_image_idx_tab2 + 1}/{len(image_files_2)}", use_column_width=True)

     # 이전/다음 버튼 생성
     empty1,col2,col3,empty2 = st.columns([1,0.2,0.2,1])
     
     
     with empty1 :
          empty() # 여백부분1
     with col2:
          if st.button("prev"):
               st.session_state.current_image_idx_tab2 -= 1
               if st.session_state.current_image_idx_tab2 < 0:
                    st.session_state.current_image_idx_tab2 = len(image_files_2) - 1
     with col3:
          if st.button("next"):
               st.session_state.current_image_idx_tab2 += 1
               if st.session_state.current_image_idx_tab2 >= len(image_files_2):
                    st.session_state.current_image_idx_tab2 = 0  
     with empty2 :
          empty() # 여백부분1  


with tab3:
     st.header("""
               임진우
               """)
     
     # 예제 이미지 파일 리스트
     image_files_3 = [f"./img/ijw/ijw_{str(i).zfill(2)}.jpg" for i in range(1, 9)]

     # 세션 상태를 관리하기 위한 클래스 (Streamlit의 state 기능을 사용)
     if 'current_image_idx_tab3' not in st.session_state:
          st.session_state.current_image_idx_tab3 = 0

     # 이미지 표시
     st.image(image_files_3[st.session_state.current_image_idx_tab3], caption=f"Image {st.session_state.current_image_idx_tab3 + 1}/{len(image_files_3)}", use_column_width=True)

     # 이전/다음 버튼 생성
     empty1,col2,col3,empty2 = st.columns([1,0.2,0.2,1])
     
     
     with empty1 :
          empty() # 여백부분1
     with col2:
          if st.button("<이전"):
               st.session_state.current_image_idx_tab3 -= 1
               if st.session_state.current_image_idx_tab3 < 0:
                    st.session_state.current_image_idx_tab3 = len(image_files_3) - 1
     with col3:
          if st.button("다음>"):
               st.session_state.current_image_idx_tab3 += 1
               if st.session_state.current_image_idx_tab3 >= len(image_files_3):
                    st.session_state.current_image_idx_tab3 = 0  
     with empty2 :
          empty() # 여백부분1  