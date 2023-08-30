import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import make_column_transformer
from keras.models import Sequential
from keras.models import load_model
from keras.layers import LSTM, Dropout, Dense
from sklearn.metrics import mean_squared_error, r2_score, precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import mean_absolute_error
import streamlit as st

class RealEstateForecast:
    def __init__(self, data_path, model_num, temp_folder="forecast_pngs"):
        self.data_path = data_path
        self.model_num = model_num
        self.cleaned_data = self.load_data()
        self.temp_folder = temp_folder
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

    def load_data(self):
        # 데이터 불러오기 및 전처리
        df = pd.read_csv(self.data_path)
        # 필요한 전처리 작업을 여기에 추가
        return df
    
    @staticmethod
    def create_dataset(dataset, look_back=3):
        dataX, dataY = [], []
    # dataset이 pandas Series인 경우만 .values를 사용하여 numpy 배열로 변환
        if isinstance(dataset, pd.Series):
           dataset = dataset.values
        for i in range(len(dataset) - look_back - 1):
           a = dataset[i:(i + look_back)]
           dataX.append(a)
           dataY.append(dataset[i + look_back])
        return np.array(dataX), np.array(dataY)

    def save_model(self, model, city_name):
        model_path = os.path.join(self.temp_folder, f"{city_name}_trained_model.h5")
        model.save(model_path)
        return model_path

    def load_saved_model(self, city_name):
        model_path = os.path.join(self.temp_folder, f"{city_name}_trained_model.h5")
        if os.path.exists(model_path):
            model = load_model(model_path)
            return model
        else:
            return None
        
    def train_predict_lstm(self, data_series, epochs=50, batch_size=1):
        # 데이터 스케일링
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data_series = scaler.fit_transform(data_series.values.reshape(-1, 1))
        
        # 데이터를 LSTM에 적합한 형태로 변환
        look_back = 3
        trainX, trainY = self.create_dataset(scaled_data_series, look_back)
        trainX = np.reshape(trainX, (trainX.shape[0], look_back, 1))
    
        # LSTM 모델 구성
        model = Sequential()
        model.add(LSTM(100, input_shape=(look_back, 1), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(25))
        model.add(Dropout(0.2))
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')

    
        # LSTM 모델 학습
        model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, verbose=0)
    
        # 미래 3개월에 대한 예측
        future_predictions = []
        input_data = trainX[-1]  # 마지막 3개월 데이터로 시작
        for _ in range(3):
            prediction = model.predict(input_data.reshape(1, look_back, 1))
            future_predictions.append(prediction[0, 0])
            input_data = np.roll(input_data, -1)
            input_data[-1] = prediction
        
        # 스케일링된 예측값을 원래의 스케일로 변환
        future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
        
        return future_predictions.flatten()


    @staticmethod
    def convert_to_date_format(date_int):
        date_str = str(date_int)
        return date_str[:4] + '-' + date_str[4:]

    def forecast_and_save(self, city_name):
        city_data = self.cleaned_data[self.cleaned_data['시군구-번지'] == city_name]
        
        if city_data.empty:
            raise ValueError(f"{city_name}에 해당하는 데이터가 존재하지 않습니다.")
    
        data_city = city_data[['계약년월', '면적당보증금', '면적당매매금', '전세가율']].groupby('계약년월').mean().reset_index()
        data_city['계약년월'] = data_city['계약년월'].apply(self.convert_to_date_format)
        data_city['timestep'] = range(len(data_city))
        
        if len(data_city) < 4:
            raise ValueError(f"{city_name}에 대한 데이터가 충분하지 않습니다. 최소한 4개월 이상의 데이터가 필요합니다.")
    
        forecasted_매매금 = self.train_predict_lstm(data_city['면적당매매금'])
        forecasted_보증금 = self.train_predict_lstm(data_city['면적당보증금'])
    
        results = []
        for month in range(3):  # 3개월 예측
            if forecasted_보증금[month] > forecasted_매매금[month]:
                results.append({
                    "forecast": f"{month+1}개월 후 {city_name}은(는) 역전세가 의심됩니다.",
                    "보증금": forecasted_보증금[month],
                    "매매금": forecasted_매매금[month]
                })
            else:
                results.append({
                    "forecast": f"{month+1}개월 후 {city_name}은(는) 역전세가 아닙니다.",
                    "보증금": forecasted_보증금[month],
                    "매매금": forecasted_매매금[month]
                })
        return results
    
    def evaluate_performance(self, true_values, predicted_values):
        # 성능 평가 메트릭 계산
        mse = mean_squared_error(true_values, predicted_values)
        mae = mean_absolute_error(true_values, predicted_values)
        return mse, mae

def main():
    forecast_model = RealEstateForecast(data_path="cleaned_data.csv", model_num=1)
    
    partial_city_lot_num = st.text_input("시군구-번지 일부 입력 (예: 강원특별자치도 강릉시): ")
    matching_city_lot_nums = forecast_model.cleaned_data[forecast_model.cleaned_data['시군구-번지'].str.contains(partial_city_lot_num)]['시군구-번지'].unique()

    if len(matching_city_lot_nums) == 0:
        print("일치하는 시군구-번지가 없습니다.")
        return

    for idx, city_lot_num in enumerate(matching_city_lot_nums):
        print(f"{idx + 1}. {city_lot_num}")

    selected_city_lot_num = st.selectbox("원하는 번호를 선택하세요:", options=matching_city_lot_nums)

    results = forecast_model.forecast_and_save(selected_city_lot_num)
    for result in results:
        st.write(result["forecast"])
        st.write(f"매매금 예측값: {round(result['매매금'], 2)}")
        st.write(f"보증금 예측값: {round(result['보증금'], 2)}")
        st.write("------------------------------")

    true_values = forecast_model.cleaned_data[forecast_model.cleaned_data['시군구-번지'] == selected_city_lot_num]['면적당매매금']
    predicted_values = [result['매매금'] for result in results]
    mse, mae = forecast_model.evaluate_performance(true_values[-3:], predicted_values)
    st.write(f"MSE: {mse:.4f}, MAE: {mae:.4f}")

if __name__ == "__main__":
    main()
