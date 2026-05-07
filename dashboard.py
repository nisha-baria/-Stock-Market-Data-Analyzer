import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Stock Analyzer Dashboard", layout="wide")
st.title("📈 Stock Market Data Analyzer")

ticker = st.sidebar.text_input("Enter Ticker (e.g. AAPL, TSLA)", value="AAPL")

# Database path check karva mate (Safe side)
db_path = "db/market.db"
if not os.path.exists(db_path):
    db_path = "market.db"

try:
    con = sqlite3.connect(db_path)
    # Ticker capital ma hovo joie query mate
    df = pd.read_sql(f"SELECT * FROM processed_market_data WHERE ticker='{ticker.upper()}'", con)
    con.close()

    if not df.empty:
        # Badha column names small kari nakhiye jethi handle karvu saral rahe
        df.columns = [c.lower() for c in df.columns]
        
        st.subheader(f"Technical Indicators for {ticker.upper()}")
        
        fig = go.Figure()

        # 1. Close Price (Opacity kadhi nakhyu che error dur karva)
        if 'close' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['close'], name='Close Price', line=dict(color='gray', width=1)))

        # 2. SMA 20 (Check karo 'sma_20' che ke 'sma20')
        if 'sma_20' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['sma_20'], name='SMA 20', line=dict(color='blue')))
        elif 'sma20' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['sma20'], name='SMA 20', line=dict(color='blue')))

        # 3. EMA 20 (Optional)
        if 'ema_20' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['ema_20'], name='EMA 20', line=dict(color='orange')))

        fig.update_layout(xaxis_title="Date", yaxis_title="Price", height=500, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### Recent Data Points")
        st.dataframe(df.tail(10), use_container_width=True)
    else:
        st.warning(f"No data found for {ticker}. Please run ingest.py and indicators.py first.")
except Exception as e:
    st.error(f"Display Error: {e}")