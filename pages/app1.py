import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

# Create a dictionary with stock symbols as keys and their corresponding data sources as values
stocks = {
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "S&P 500": "^GSPC"
}

@st.cache_data
def fetch_data(stock, start_date, end_date):
    stock_data = yf.download(stock, start=start_date, end=end_date)["Close"]  # Adjust the date range as needed
    stock_data = stock_data.resample('Q').last() # Resample data to get the last price of each quarter
    stock_data = stock_data.reset_index()
    stock_data["Symbol"] = stock
    return stock_data

# Add the ability to write a stock ticker
new_stock = st.text_input('Enter a new stock ticker')

if new_stock:
    try:
        stocks[new_stock] = new_stock
    except Exception as e:
        st.warning(f"Failed to fetch data for {new_stock}. Please make sure it's a valid ticker symbol.")
        st.write("Error details:", str(e))

# Add a slider for the time period selection
today = datetime.today().date()
twenty_years_ago = today - timedelta(days=20*365)
date_range = st.date_input("Date range", [twenty_years_ago, today])

# Fetch stock prices using the yfinance library
df = pd.DataFrame()
for stock in stocks.values():
    df = pd.concat([df, fetch_data(stock, date_range[0], date_range[1])])

clist = list(stocks.keys())
stocks_selected = st.multiselect("Select stock", clist)

# Add checkbox to toggle normalization
normalize_data = st.checkbox('Normalize data', value=True)

if len(stocks_selected) > 1 and normalize_data:
    df["Close"] = (df["Close"] / df.groupby("Symbol")["Close"].transform('first')) * 100  # Normalize to percentage change from first date

st.header("You selected: {}".format(", ".join(stocks_selected)))

dfs = {stock: df[df["Symbol"] == stocks[stock]] for stock in stocks_selected}

fig = go.Figure()
for stock, df in dfs.items():
    fig = fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name=stock))

st.plotly_chart(fig)
