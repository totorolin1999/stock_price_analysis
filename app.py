import streamlit as st
from ma_trading_strategy import show_ma_trading_strategy
from stock_price_prediction import show_stock_price_prediction

st.sidebar.title('股價分析系統')
page = st.sidebar.selectbox("請選擇股價分析方法", ("均線交易策略", "股價預測"))

if page == "均線交易策略":
    show_ma_trading_strategy()
elif page == "股價預測":
    show_stock_price_prediction()
else:
    show_ma_trading_strategy()