import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Analyzer Dashboard", layout="wide")
st.title("📈 Stock Market Data Analyzer")

ticker = st.sidebar.text_input("Enter Ticker (e.g. AAPL, TSLA)", value="AAPL")

try:
    con = sqlite3.connect("db/market.db")
    df = pd.read_sql_query(f"SELECT * FROM indicators_daily WHERE ticker='{ticker.upper()}'", con)
    con.close()

    if not df.empty:
        df.columns = [c.lower() for c in df.columns]
        
        st.subheader(f"Technical Indicators for {ticker.upper()}")
        
        fig = go.Figure()
        # Price and Moving Averages
        if 'close' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['close'], name='Close Price', line=dict(color='gray', opacity=0.5)))
        if 'sma20' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['sma20'], name='SMA 20', line=dict(color='blue')))
        if 'sma50' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['sma50'], name='SMA 50', line=dict(color='orange')))
        
        fig.update_layout(xaxis_title="Date", yaxis_title="Price", height=500, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### Recent Data Points")
        st.dataframe(df.tail(10), use_container_width=True)
    else:
        st.warning(f"No data found for {ticker}. Please run ingest.py and indicators.py first.")
except Exception as e:
    st.error(f"Display Error: {e}")