import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'market.db')

def calculate_indicators():
    try:
        conn = sqlite3.connect(DB_PATH)
        # 1. Table name 'candles_daily' vapryu che
        df = pd.read_sql("SELECT * FROM candles_daily", conn)
        
        if df.empty:
            print("❌ No data found!")
            return

        # 2. Column names small 'close' kari didha che
        # Jo error aave to check karo ke column nu naam su che
        col = 'close' if 'close' in df.columns else 'Close'
        
        print(f"📊 Calculating indicators for {df['ticker'].iloc[0]} using column: {col}...")

        # SMA calculation
        df['SMA_20'] = df[col].rolling(window=20).mean()
        
        # EMA calculation
        df['EMA_20'] = df[col].ewm(span=20, adjust=False).mean()

        # RSI calculation
        delta = df[col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # 3. Save to Processed Table
        df.to_sql('processed_market_data', conn, if_exists='replace', index=False)
        
        print("✅ Success! Indicators calculated and saved.")
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    calculate_indicators()