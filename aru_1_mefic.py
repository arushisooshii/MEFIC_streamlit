import streamlit as st
import pandas as pd
import yfinance as yf

# Function to fetch stock data
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1y')
        return data, stock
    except Exception as e:
        return None, None

# Function to fetch financial metrics
def get_financial_metrics(stock):
    try:
        info = stock.info
        metrics = {
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "Return on Equity (ROE)": info.get("returnOnEquity", "N/A"),
            "Return on Assets (ROA)": info.get("returnOnAssets", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Payout Ratio": info.get("payoutRatio", "N/A"),
            "Dividend Score": "High" if info.get("dividendYield", 0) > 0.04 else "Low"
        }
        return metrics
    except Exception as e:
        return None

# Investment decision function (example using simple moving average)
def investment_decision(data):
    if data is None or data.empty:
        return "No Data Available"
    
    sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
    sma_200 = data['Close'].rolling(window=200).mean().iloc[-1]
    latest_price = data['Close'].iloc[-1]
    
    if latest_price > sma_50 > sma_200:
        return "Buy - Strong Uptrend"
    elif latest_price < sma_50 < sma_200:
        return "Sell - Strong Downtrend"
    else:
        return "Hold - Unclear Trend"

# Streamlit UI
st.title("Saudi Stock Exchange Investment Calculator")

# User input for company ticker
ticker = st.text_input("Enter Company Ticker (e.g., 2222.SR for Saudi Aramco)")

if ticker:
    data, stock = get_stock_data(ticker)
    decision = investment_decision(data)
    metrics = get_financial_metrics(stock) if stock else None
    
    if data is not None:
        st.line_chart(data['Close'])
    
    st.subheader("Investment Decision:")
    st.write(decision)
    
    if metrics:
        st.subheader("Financial Metrics:")
        for key, value in metrics.items():
            st.write(f"{key}: {value}")
