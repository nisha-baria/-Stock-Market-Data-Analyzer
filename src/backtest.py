import pandas as pd
import numpy as np
import sqlite3

def run_backtest(db="db/market.db", ticker="AAPL"):
    con = sqlite3.connect(db)
    query = """
    SELECT c.date, c.close, i.sma20, i.sma50 
    FROM candles_daily c 
    JOIN indicators_daily i ON c.date = i.date AND c.ticker = i.ticker
    WHERE c.ticker = ? ORDER BY c.date
    """
    df = pd.read_sql_query(query, con, params=[ticker])
    con.close()

    if df.empty:
        print("No data found for backtesting!")
        return

    df['signal'] = np.where(df['sma20'] > df['sma50'], 1, 0)
    df['position'] = df['signal'].shift(1) # Agla divas na signal par trade
    
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['position'] * df['returns']
    
    # Cumulative Profit
    df['cum_profit'] = (1 + df['strategy_returns'].fillna(0)).cumprod()
    
    final_profit = (df['cum_profit'].iloc[-1] - 1) * 100
    print(f"Backtest Complete for {ticker}!")
    print(f"Total Return: {final_profit:.2f}%")
    
    return df

if __name__ == "__main__":
    run_backtest()