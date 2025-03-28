import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from modules.stock_analysis import get_stock_data, plot_stock_price
from modules.portfolio import calculate_portfolio_metrics
from modules.technical_indicators import calculate_technical_indicators
from modules.risk_metrics import calculate_risk_metrics
from modules.financial_metrics import get_financial_metrics, get_all_stocks_comparison

# Top 10 Saudi Stocks (Tadawul Market)
SAUDI_STOCKS = {
    '2222.SR': 'Saudi Aramco - أرامكو السعودية',
    '1180.SR': 'Al Rajhi Bank - مصرف الراجحي',
    '2350.SR': 'Saudi Telecom Co - الاتصالات السعودية',
    '1010.SR': 'SABIC - سابك',
    '1150.SR': 'Alinma Bank - مصرف الإنماء',
    '2310.SR': 'Zain KSA - زين السعودية',
    '2380.SR': 'Mobily - موبايلي',
    '1050.SR': 'Saudi National Bank - البنك الأهلي السعودي',
    '2001.SR': 'ACWA Power - أكوا باور',
    '2330.SR': 'Advanced - المتقدمة'
}

st.set_page_config(page_title="Saudi Stock Market Analysis Dashboard", layout="wide")

st.title("Saudi Stock Market Analysis Dashboard")
st.markdown("Analyze top companies from the Saudi Stock Exchange (Tadawul) to make informed investment decisions.")

# Market Overview Section
st.header("Market Overview - Top 10 Saudi Stocks Comparison")
with st.spinner("Fetching market data..."):
    comparison_df = get_all_stocks_comparison(SAUDI_STOCKS)
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Symbol": st.column_config.TextColumn("Symbol", width="medium"),
            "Company": st.column_config.TextColumn("Company", width="large"),
            "P/E Ratio": st.column_config.NumberColumn("P/E Ratio", format="%.2f"),
            "ROE (%)": st.column_config.NumberColumn("ROE (%)", format="%.2f%%"),
            "ROA (%)": st.column_config.NumberColumn("ROA (%)", format="%.2f%%"),
            "Dividend Score": st.column_config.NumberColumn("Dividend Score", format="%.1f"),
            "Dividend Yield (%)": st.column_config.NumberColumn("Dividend Yield (%)", format="%.2f%%"),
            "Payout Ratio (%)": st.column_config.NumberColumn("Payout Ratio (%)", format="%.2f%%")
        }
    )

# Sidebar inputs
st.sidebar.header("Analysis Parameters")

# Stock symbol selection
symbol = st.sidebar.selectbox(
    "Select Saudi Stock",
    options=list(SAUDI_STOCKS.keys()),
    format_func=lambda x: f"{SAUDI_STOCKS[x]}",
    index=0
)

# Date range selection
date_range = st.sidebar.selectbox(
    "Select Time Period",
    ["1M", "3M", "6M", "1Y", "2Y", "5Y"],
    index=2
)

# Convert date range to actual dates
end_date = datetime.now()
date_ranges = {
    "1M": 30, "3M": 90, "6M": 180,
    "1Y": 365, "2Y": 730, "5Y": 1825
}
start_date = end_date - timedelta(days=date_ranges[date_range])

try:
    # Fetch stock data
    df = get_stock_data(symbol, start_date, end_date)

    # Get financial metrics
    financial_metrics = get_financial_metrics(symbol)

    # Display company name and basic info
    company_name = SAUDI_STOCKS[symbol]
    st.header(f"{company_name}")
    st.markdown(f"Symbol: {symbol}")

    # Financial Metrics Section
    st.subheader("Key Financial Metrics")
    fin_cols = st.columns(6)

    with fin_cols[0]:
        pe_value = financial_metrics['pe_ratio']
        st.metric("P/E Ratio", f"{pe_value:.2f}" if pe_value else "N/A")

    with fin_cols[1]:
        roe_value = financial_metrics['roe']
        st.metric("ROE", f"{roe_value:.2f}%" if roe_value else "N/A")

    with fin_cols[2]:
        roa_value = financial_metrics['roa']
        st.metric("ROA", f"{roa_value:.2f}%" if roa_value else "N/A")

    with fin_cols[3]:
        div_score = financial_metrics['dividend_score']
        st.metric("Dividend Score", f"{div_score:.1f}/100" if div_score else "N/A")

    with fin_cols[4]:
        div_yield = financial_metrics['dividend_yield']
        st.metric("Dividend Yield", f"{div_yield:.2f}%" if div_yield else "N/A")

    with fin_cols[5]:
        payout = financial_metrics['payout_ratio']
        st.metric("Payout Ratio", f"{payout:.2f}%" if payout else "N/A")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stock Price Chart")
        fig = plot_stock_price(df)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Technical Indicators")
        indicators = calculate_technical_indicators(df)
        st.dataframe(indicators)

    with col2:
        st.subheader("Risk Metrics")
        risk_metrics = calculate_risk_metrics(df)

        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.metric("Beta", f"{risk_metrics['beta']:.2f}")
            st.metric("Volatility", f"{risk_metrics['volatility']:.2%}")
        with metrics_col2:
            st.metric("Sharpe Ratio", f"{risk_metrics['sharpe_ratio']:.2f}")
            st.metric("Max Drawdown", f"{risk_metrics['max_drawdown']:.2%}")

    # Portfolio Analysis Section
    st.subheader("Portfolio Analysis")
    portfolio_metrics = calculate_portfolio_metrics(df)

    metrics_cols = st.columns(4)
    with metrics_cols[0]:
        st.metric("Return (Annualized)", f"{portfolio_metrics['annual_return']:.2%}")
    with metrics_cols[1]:
        st.metric("Alpha", f"{portfolio_metrics['alpha']:.2%}")
    with metrics_cols[2]:
        st.metric("Information Ratio", f"{portfolio_metrics['info_ratio']:.2f}")
    with metrics_cols[3]:
        st.metric("Tracking Error", f"{portfolio_metrics['tracking_error']:.2%}")

except Exception as e:
    st.error(f"Error: {str(e)}")