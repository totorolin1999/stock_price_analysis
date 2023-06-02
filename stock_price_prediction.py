import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf 
from keras.models import load_model
import streamlit as st

def show_stock_price_prediction():

    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

    plt.style.use("dark_background")

    st.title('股價預測')

    user_input = st.text_input('輸入股票代號', '2330.TW')
    selected_year = st.slider('選擇期間（年）', 1, 10, 3)

    if st.button('預測股價'):

        df = yf.download(user_input, period=f'{selected_year}y')

        st.subheader(f'至今{selected_year}年期間的股票資料')
        st. write(df.describe())

        st.subheader('收盤價走勢')
        fig = plt.figure(figsize = (12,6))
        plt.plot(df.Close, 'b', label="收盤價")
        plt.legend(loc="upper left")
        st.pyplot(fig)


        # Splitting Data into Training and Testing

        data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
        data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(0,1))

        data_training_array = scaler.fit_transform(data_training)



        #Load my model
        model = load_model('lstm_model_2330.h5', compile = False)

        #Testing Part

        past_100_days = data_training.tail(100)
        # final_df = past_100_days.append(data_testing, ignore_index=True)
        final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data = scaler.fit_transform(final_df)

        x_test = [] # 產生一個名叫x_test的list
        y_test = [] # 產生一個名叫y_test的list

        for i in range(100, data_training_array.shape[0]):
            x_test.append(data_training_array[i-100: i])
            y_test.append(data_training_array[i, 0])

        x_test, y_test = np.array(x_test), np.array(y_test)
        y_predicted = model.predict(x_test)
        scaler = scaler.scale_

        scaler_factor = 1/scaler[0]
        y_predicted = y_predicted * scaler_factor
        y_test = y_test * scaler_factor


        #Final Graph

        st.subheader('使用LSTM模型預測收盤價走勢')
        fig2 = plt.figure(figsize=(12,6))
        plt.plot(y_test, 'b', label = '原收盤價')
        plt.plot(y_predicted, 'r', label = '預測收盤價')
        plt.xlabel('時間')
        plt.ylabel('收盤價')
        plt.legend()
        st.pyplot(fig2)