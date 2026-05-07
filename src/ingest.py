import yfinance as yf
import pandas as pd
import sqlite3

def fetch_and_save(ticker="AAPL"):
    # To Fetch Data
    df = yf.download(ticker, start="2020-01-01", auto_adjust=False)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df = df.reset_index()
    
    df.columns = [str(c).lower() for c in df.columns]
    
    df['ticker'] = ticker
    
    # To store SQLite
    con = sqlite3.connect("db/market.db")
    df.to_sql("candles_daily", con, if_exists="replace", index=False)
    con.close()
    print(f"Data for {ticker} saved successfully with ticker column!")

if __name__ == "__main__":
    fetch_and_save()