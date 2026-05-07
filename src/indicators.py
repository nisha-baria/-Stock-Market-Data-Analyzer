import pandas as pd
import sqlite3
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def compute_indicators(db="db/market.db", ticker="AAPL"):
    con = sqlite3.connect(db)
    #To read data from Database
    df = pd.read_sql_query("SELECT date, close FROM candles_daily WHERE ticker=? ORDER BY date", con, params=[ticker])
    
    if df.empty:
        print("No data found in database!")
        return

    s = df["close"]
    
    # To calculate Technical Indicators
    sma20 = SMAIndicator(s, window=20).sma_indicator()
    sma50 = SMAIndicator(s, window=50).sma_indicator()
    rsi14 = RSIIndicator(s, window=14).rsi()
    macd_obj = MACD(s)
    bb = BollingerBands(s, window=20, window_dev=2)

    # To make new DataFrame
    out = pd.DataFrame({
        "date": df["date"],
        "sma20": sma20,
        "sma50": sma50,
        "rsi14": rsi14,
        "macd": macd_obj.macd(),
        "macd_signal": macd_obj.macd_signal(),
        "bb_upper": bb.bollinger_hband(),
        "bb_lower": bb.bollinger_lband()
    }).dropna()

    # To save indicators into database
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS indicators_daily 
                   (ticker TEXT, date TEXT, sma20 REAL, sma50 REAL, rsi14 REAL, 
                    macd REAL, macd_signal REAL, bb_upper REAL, bb_lower REAL,
                    PRIMARY KEY (ticker, date))""")
    
    #To insert Data
    for _, row in out.iterrows():
        cur.execute("""INSERT OR REPLACE INTO indicators_daily 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (ticker, row['date'], row['sma20'], row['sma50'], row['rsi14'], 
                     row['macd'], row['macd_signal'], row['bb_upper'], row['bb_lower']))
    
    con.commit()
    con.close()
    print(f"Indicators for {ticker} computed and saved!")

if __name__ == "__main__":
    compute_indicators()