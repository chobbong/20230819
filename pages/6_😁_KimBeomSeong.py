import joblib 
import warnings
import pymysql
import streamlit as st
import pandas as pd
import numpy as np

# 경고 무시
warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn')
warnings.filterwarnings(action='ignore', module='xgboost')

class Model:
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        # target: 사용할 target
        self.model1 = joblib.load('./kbs/save/apt_target60.joblib')
        self.model2 = joblib.load('./kbs/save/apt_target70.joblib')
        self.model3 = joblib.load('./kbs/save/apt_target80.joblib')
        self.model4 = joblib.load('./kbs/save/apt_target90.joblib')

    def connect(self):
        # MariaDB 연결
        # user = st.secrets["db_user"]
        # password = st.secrets["db_password"]
        self.conn = pymysql.connect(host="khrpa.com", user='joyunseo77', password='WhgkdbsWhdbstj77', charset='utf8', database="joyunseo77")
        self.cursor = self.conn.cursor()

    def is_connected(self):
        return self.conn and self.conn.open

    def search_estate_data(self, keyword, date_input):
        search_query = """
            SELECT 시군구, 계약년월, 면적당보증금, 조정대상지역, 투기과열지구, 광역, target60, target70, target80, target90
            FROM kbs_data
            WHERE 시군구 LIKE %s and 계약년월 = %s
        """
        if not self.is_connected():
            self.connect()

        self.cursor.execute(search_query, (f"%{keyword}%", date_input))
        results = self.cursor.fetchall()

        # 결과를 pandas DataFrame으로 반환
        columns = ["시군구", "계약년월", "면적당보증금", "조정대상지역", "투기과열지구", "광역", "target60","target70", "target80", "target90"]
        df = pd.DataFrame(results, columns=columns)
        
        return df

    def __del__(self):
          # 연결 종료
          if self.is_connected():
               self.conn.close()


    def predict_all(self, city_num):
        """
        각 모델 예측 결과를 기반으로 message를 return함

        Arg:
            city_num: 입력 데이터

        Return:
            역전세 위험도 관련 메세지
        """


        #-------------------------- 입력데이터 전처리 시작------------------
        # 광역, 시군구 encoding
        le1 = joblib.load('./kbs/save/sigungu.joblib')
        le2 = joblib.load('./kbs/save/gwangyeok.joblib')
        city_num.at['시군구'] = le1.transform([city_num['시군구']])[0]
        city_num.at['광역'] = le2.transform([city_num['광역']])[0]

        # 자료형 변환할 때 Series는 불편해서 DataFrame 변환해서 진행
        city_num = city_num.to_frame().T  # Series를 DataFrame으로 변환

        # target 특성들이 들어가있어서 제거
        drop_columns = ['target60', 'target70', 'target80', 'target90']
        city_num.drop(columns=drop_columns, inplace=True)

        # 자료형 바꾸기
        # int로 변환할 열들
        int_columns = ['시군구', '계약년월', '조정대상지역', '투기과열지구', '광역']
        for col in int_columns:
            city_num[col] = city_num[col].astype(int)

        # 면적당보증금 특성 자료형 float로 바꾸기
        city_num['면적당보증금'] = city_num['면적당보증금'].astype(float)

        # target70, target80 모델은 data의 면적당보증금을 log변환해야함
        city_num_log = city_num.copy()
        
        # log변환
        city_num_log['log_면적당보증금'] = np.log(city_num['면적당보증금'])
        city_num_log.drop(columns = '면적당보증금', inplace= True)    
        #-------------------------- 입력데이터 전처리 끝 ---------------------
        # 모델 각각 선언
        model60 = self.model1
        model70 = self.model2
        model80 = self.model3
        model90 = self.model4

        # 예측 결과 crit에 저장
        crit1 = model60.predict(city_num)
        crit4 = model90.predict(city_num)
        
        # 70, 80 모델은 면적당보증금 log변환하고 예측해야함
        crit2 = model70.predict(city_num_log)
        crit3 = model80.predict(city_num_log)

        result_message = ''
        if crit1[0] == 0:
            result_message = '역전세 위험에서 매우 안전합니다'

        elif (crit1[0] == 1) & (crit2[0] == 0):
            result_message = '역전세 가능성이 낮습니다'

        elif (crit2[0] == 1) & (crit3[0] == 0):
            result_message = '역전세 가능성을 경계해야 합니다'

        elif (crit3[0] == 1) & (crit4[0] == 0):
            result_message = '역전세 위험이 높습니다'        

        elif crit4[0]== 1:
            result_message = '역전세 위험이 매우 높습니다'

        else:
            result_message = '해당 데이터에 대해 검토가 필요합니다'
            
        return result_message
   
def main():
    model_instance = Model()  # Model 인스턴스 생성
     
    keyword = st.text_input("검색할 지역을 입력하세요 (예 : 강릉시, 강남구): ")
    date_input = st.text_input("계약년월을 입력하세요 (예 : 201908~202307): ")
     
    matching_city_lot_nums = model_instance.search_estate_data(keyword, date_input)
    city_selection_list = matching_city_lot_nums["시군구"].tolist()
    
    selected_city = st.selectbox("원하는 지역을 선택하세요:", options=city_selection_list)
    filtered_data = matching_city_lot_nums[matching_city_lot_nums["시군구"] == selected_city]
    
    if not filtered_data.empty:
        selected_city_data = filtered_data.iloc[0]
        result_message = model_instance.predict_all(selected_city_data)
        st.write(result_message)
    else:
        st.write("선택한 지역의 데이터를 찾을 수 없습니다.")
    
if __name__ == "__main__":
    main()
