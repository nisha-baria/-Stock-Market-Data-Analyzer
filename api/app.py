from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Stock Analyzer API is Live!"}

@app.get("/chart/{ticker}")
def get_chart_data(ticker: str):
    con = sqlite3.connect("db/market.db")
    con.row_factory = sqlite3.Row
    rows = con.execute("SELECT * FROM indicators_daily WHERE ticker=? LIMIT 100", [ticker]).fetchall()
    con.close()
    return [dict(r) for r in rows]