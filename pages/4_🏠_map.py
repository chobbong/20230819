import pandas as pd
import pymysql
import folium
import streamlit as st
from streamlit_folium import st_folium



st.set_page_config(
    page_icon=":goose:",
    page_title="떼돈팀",
    layout="wide",
)

class RealEstateDB:
     def __init__(self):
          self.conn = None
          self.cursor = None
          self.connect()
          # self.create_table()

     def connect(self):
          # MariaDB 연결
          user = st.secrets["db_user"]
          password = st.secrets["db_password"]
          self.conn = pymysql.connect(host="khrpa.com",user=user, password=password, charset='utf8', database="joyunseo77")
          self.cursor = self.conn.cursor()

     def is_connected(self):
          # 연결 상태 확인
          return self.conn and self.conn.open

     # def create_table(self):
     #      create_table_query = """
     #           CREATE TABLE IF NOT EXISTS estatedata (
     #           시군구 VARCHAR(255),
     #           단지명 VARCHAR(255),
     #           계약연월 INT,
     #           전용면적 FLOAT,
     #           매매대금_평균 FLOAT,
     #           전세_평균 FLOAT,
     #           면적당_매매대금평균 FLOAT,
     #           면적당_전세평균 FLOAT,
     #           전세가율 FLOAT,
     #           lat FLOAT,
     #           lng FLOAT
     #           ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
     #      """
     #      self.cursor.execute(create_table_query)
     #      self.conn.commit()

     def search_estate_data(self, keyword):
          search_query = """
               SELECT 시군구, 시군구번지, 계약년월, 면적당보증금, 면적당매매금, 전세가율, lat, lng, timestep, 전세가율90, 전세가율80, 전세가율70, 전세가율60
               FROM kwy2_data
               WHERE 시군구 LIKE %s OR 시군구번지 LIKE %s
          """
          if not self.is_connected():
               self.connect()
          
          self.cursor.execute(search_query, (f"%{keyword}%", f"%{keyword}%"))
          results = self.cursor.fetchall()

          # 결과를 pandas DataFrame으로 반환
          columns = ["시군구", "시군구번지", "계약년월", "면적당보증금", "면적당매매금","timestep", "전세가율", "전세가율90", "전세가율80", "전세가율70","전세가율60","lat","lng"]
          return pd.DataFrame(results, columns=columns)

     def __del__(self):
          # 연결 종료
          if self.is_connected():
               self.conn.close()

db = RealEstateDB()
serch_point = st.text_input('검색하고 싶은 주소를 입력하세요')
result_df = db.search_estate_data(serch_point)


#-----------------------MAP-----------------------#
def create_map(dataframe):
    # Calculate the average latitude and longitude from the data
    avg_lat = dataframe['lat'].mean()
    avg_lng = dataframe['lng'].mean()

    # Create a base map with the average location as the center
    m = folium.Map(location=[avg_lat, avg_lng], zoom_start=11)

    # Function to display detailed information on marker click
    def get_popup_content(row):
         
          content = f"""
               <strong>{row['시군구번지']}</strong><br>
               <strong>{row['계약년월']}</strong><br>
               전용면적: {row['면적당보증금']}<br>
               매매대금 평균: {row['면적당매매금']}<br>
               전세가율: {row['전세가율']}<br>
               전세가율 90%: {row['전세가율90']}<br>
               전세가율 80%: {row['전세가율80']}<br>
               전세가율 70%: {row['전세가율70']}<br>
               전세가율 60%: {row['전세가율60']}<br>
          """
    
          return content
    # Add markers to the map
    for _, row in dataframe.iterrows():
        popup_content = get_popup_content(row)
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=folium.Popup(popup_content, max_width=400)
        ).add_to(m)

    return m

# Assuming result_df is your dataframe with search results:
m = create_map(result_df)
st_data = st_folium(m, width=725)





