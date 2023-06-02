import matplotlib.pyplot as plt
import yfinance as yf 
import streamlit as st

def show_ma_trading_strategy():

    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

    plt.style.use("dark_background")

    st.title('均線交易策略')

    user_input = st.text_input('輸入股票代號', '2330.TW')
    selected_year = st.slider('選擇期間（年）', 1, 10, 3)
    ma_1 = st.slider('選擇第一條均線周期（日）', 5, 99, 30)
    ma_2 = st.slider('選擇第二條均線周期（日）', 100, 240, 100)

    if st.button('制定均線交易策略'):

        df = yf.download(user_input, period=f'{selected_year}y')
        
        st.subheader(f'至今{selected_year}年期間的股票資料')
        st. write(df.describe())

        st.subheader('收盤價走勢')
        fig = plt.figure(figsize = (12,6))
        plt.plot(df.Close, 'b', label="收盤價")
        plt.legend(loc="upper left")
        st.pyplot(fig)

        # st.subheader(f'收盤價、{ma_1}日均線走勢')
        # ma1 = df.Close.rolling(window=ma_1).mean()
        # fig = plt.figure(figsize = (12,6))
        # plt.plot(ma1, 'r', label=f"{ma_1}日均線")
        # plt.plot(df.Close, 'b', label="收盤價")
        # plt.legend(loc="upper left")
        # st.pyplot(fig)


        st.subheader(f'收盤價、{ma_1}日均線、{ma_2}日均線走勢')
        ma1 = df.Close.rolling(window=ma_1).mean()
        ma2 = df.Close.rolling(window=ma_2).mean()
        fig = plt.figure(figsize = (12,6))
        plt.plot(ma1, 'r', label=f"{ma_1}日均線")
        plt.plot(ma2, 'g', label=f"{ma_2}日均線")
        plt.plot(df.Close, 'b', label="收盤價")
        plt.legend(loc="upper left")
        st.pyplot(fig)


        df[f'SMA_{ma_1}'] = df['Close'].rolling(window=ma_1).mean() # f-string 字串格式化
        df[f'SMA_{ma_2}'] = df['Close'].rolling(window=ma_2).mean()

        data = df.iloc[ma_2:] # iloc[]是用index位置來取我們要的資料。

        buy_signals = [] # 產生一個名叫buy_signals的list
        sell_signals = [] # 產生一個名叫sell_signals的list
        trigger = 0 # trigger先設為0

        for x in range(len(data)): # 參數設為data筆數
            if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1: # 如果data中的SMA_ma_1大於SMA_ma_2且trigger不等於1
                buy_signals.append(data['Close'].iloc[x]) #  buy_signals增加data中該筆資料的Close
                sell_signals.append(float('nan')) #  sell_signals增加一個浮點數為nan
                trigger = 1 # trigger更為1
            elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
                buy_signals.append(float('nan'))
                sell_signals.append(data['Close'].iloc[x])
                trigger = -1 # trigger更為-1
            else:
                buy_signals.append(float('nan'))
                sell_signals.append(float('nan'))

        data['Buy Signals'] = buy_signals
        data['Sell Signals'] = sell_signals

        st.subheader('均線交易策略')
        fig = plt.figure(figsize = (12,6))
        plt.plot(data['Close'], 'b', label="收盤價", alpha=0.5)
        plt.plot(data[f'SMA_{ma_1}'], 'r', label=f"{ma_1}日均線", linestyle="--")
        plt.plot(data[f'SMA_{ma_2}'], 'g', label=f"{ma_2}日均線", linestyle="--")
        plt.scatter(data.index, data['Buy Signals'], label="買進訊號", marker="^", color="#00ff00", lw=3)
        plt.scatter(data.index, data['Sell Signals'], label="賣出訊號", marker="v", color="#ff0000", lw=3)
        plt.legend(loc="upper left")
        st.pyplot(fig)
