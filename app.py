import pandas as pd
import pymysql
import folium
import streamlit as st
from streamlit_folium import st_folium

class RealEstateDB:
     def __init__(self):
          self.conn = None
          self.cursor = None
          self.connect()
          self.create_table()

     def connect(self):
          # MariaDB 연결
          self.conn = pymysql.connect(host='khrpa.com', user='joyunseo77', password='WhgkdbsWhdbstj77', charset='utf8', database='joyunseo77')
          self.cursor = self.conn.cursor()

     def is_connected(self):
          # 연결 상태 확인
          return self.conn and self.conn.open

     def create_table(self):
          create_table_query = """
               CREATE TABLE IF NOT EXISTS estatedata (
               시군구 VARCHAR(255),
               단지명 VARCHAR(255),
               계약연월 INT,
               전용면적 FLOAT,
               매매대금_평균 FLOAT,
               전세_평균 FLOAT,
               면적당_매매대금평균 FLOAT,
               면적당_전세평균 FLOAT,
               전세가율 FLOAT,
               lat FLOAT,
               lng FLOAT
               ) CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
          """
          self.cursor.execute(create_table_query)
          self.conn.commit()

     def search_estate_data(self, keyword):
          search_query = """
               SELECT 시군구, 단지명, 계약연월, 전용면적, 매매대금_평균, 전세_평균, 면적당_매매대금평균, 면적당_전세평균, 전세가율,lat,lng 
               FROM estate_data
               WHERE 시군구 LIKE %s OR 단지명 LIKE %s
          """
          if not self.is_connected():
               self.connect()
          
          self.cursor.execute(search_query, (f"%{keyword}%", f"%{keyword}%"))
          results = self.cursor.fetchall()

          # 결과를 pandas DataFrame으로 반환
          columns = ["시군구", "단지명", "계약연월", "전용면적", "매매대금_평균", "전세_평균", "면적당_매매대금평균", "면적당_전세평균", "전세가율","lat","lng"]
          return pd.DataFrame(results, columns=columns)

     def __del__(self):
          # 연결 종료
          if self.is_connected():
               self.conn.close()

db = RealEstateDB()
serch_point = st.text_input('검색하고 싶은 주소를 입력하세요')
result_df = db.search_estate_data(serch_point)

#------------------MAP------------------#
import streamlit as st
import folium
import pandas as pd

def create_map(dataframe, search_location):
    # Calculate the center of the search results
    center_lat = dataframe['lat'].mean()
    center_lng = dataframe['lng'].mean()

    # Create a base map using the center of the search results
    m = folium.Map(location=[center_lat, center_lng], zoom_start=11)

    def get_popup_content(row):
        content = f"""
        <strong>{row['시군구']}</strong><br>
        <strong>{row['단지명']}</strong><br>
        계약연월: {row['계약연월']}<br>
        전용면적: {row['전용면적']}<br>
        매매대금 평균: {row['매매대금_평균']}<br>
        전세 평균: {row['전세_평균']}<br>
        면적당 매매대금평균: {row['면적당_매매대금평균']}<br>
        면적당 전세평균: {row['면적당_전세평균']}<br>
        전세가율: {row['전세가율']}
        """
        return content

    for _, row in dataframe.iterrows():
        popup_content = get_popup_content(row)
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=folium.Popup(popup_content, max_width=400)
        ).add_to(m)

    return m

# Streamlit app
def main():
    st.title("Search Map by Location")

    # Input for search location
    search_location = st.text_input('Enter location to search:')

    # If the button is clicked, filter the dataframe by the searched location
    if st.button('Search'):
        # Dummy: Filter your data based on the search_location
        # result_df = original_df[original_df['시군구'] == search_location] 
        result_df = pd.DataFrame({
            '시군구': ['Example'],
            '단지명': ['Example Name'],
            '계약연월': ['2023-08'],
            '전용면적': [30],
            '매매대금_평균': [1000],
            '전세_평균': [500],
            '면적당_매매대금평균': [33333],
            '면적당_전세평균': [16666],
            '전세가율': [0.5],
            'lat': [37.5665],
            'lng': [126.9780]
        }) # This is dummy data, replace it with actual filtering

        m = create_map(result_df, search_location)
        st_folium(m, width=725)

if __name__ == '__main__':
    main()
