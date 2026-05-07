## 🚀 Stock Market Data Analyzer
An automated stock analysis tool built with Python and Streamlit. This project fetches historical stock data, calculates technical indicators (SMA, RSI, MACD), and visualizes the results on an interactive dashboard.

## ✨ Features
Data Ingestion: Automatically fetches daily stock candles for any ticker.

Technical Analysis: Computes moving averages (SMA 20, SMA 50), RSI, and MACD.

Interactive Dashboard: A professional dark-themed UI to visualize price trends and crossover signals.

Database Management: Stores analysis data locally using SQLite.

## 🛠️ Project Structure
Plaintext
Stock Market Data Analyzer/
├── db/               # SQLite database (market.db)
├── src/              # Python source scripts
│   ├── ingest.py     # Fetches data from API
│   └── indicators.py # Computes technical indicators
├── dashboard.py      # Streamlit dashboard UI
├── requirements.txt  # Project dependencies
└── README.md         # Documentation

## 🚀 How to Run

1. **Install Dependencies**: `pip install streamlit pandas ta plotly`
2. **Setup Data**: Run `python src/ingest.py` then `python src/indicators.py`
3. **Start Dashboard**: Run `streamlit run dashboard.py`