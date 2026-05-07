import yfinance as yf
import sqlite3
import os

# Database setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'market.db')

def fetch_and_save():
    # Banve tickers ek list ma
    tickers = ["AAPL", "TSLA"]
    
    conn = sqlite3.connect(DB_PATH)
    
    for ticker in tickers:
        print(f"📥 Fetching data for {ticker}...")
        data = yf.download(ticker, period="2y", interval="1d")
        
        if not data.empty:
            data['ticker'] = ticker
            # Column names ne simple banavva (Dashboard mate)
            data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
            
            # Save to candles_daily table
            # Pehla ticker mate 'replace' ane pachi na mate 'append'
            mode = 'replace' if ticker == tickers[0] else 'append'
            data.to_sql("candles_daily", conn, if_exists=mode, index=True)
            print(f"✅ {ticker} saved successfully!")
            
    conn.close()

if __name__ == "__main__":
    fetch_and_save()