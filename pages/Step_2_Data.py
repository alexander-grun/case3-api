import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta


st.header("Step 2. Data")
st.write("""We did a lot of things, let's come back to our initial plan and check what should we figure out next.

1. Data
2. Chart :white_check_mark:
3. Ability to display selected values (interactivity) :white_check_mark:
4. Ability to add new values dynamically
5. Ability to select time periods

Now that we can create charts with interactivity, let's focus on the stock market data that we need.
""")

st.write("""Luckily there some APIs that offer stock market data. To make things even easier there are libraries written to interract with these APIs in Python. We will use 'yfinance' which is an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. https://pypi.org/project/yfinance/

Please remember that the yfinance package may not always be able to retrieve data due to changes in Yahoo Finance's website. It's recommended to use official APIs (like Alpha Vantage or IEX Cloud) for commercial applications. These generally require an API key but provide more stable and reliable service. """)

# Set the title of the app
st.header('Apple Stock Data Visualization Tutorial')

st.markdown("## 1. Import necessary libraries")
st.code("""
import streamlit as st
import plotly.express as px
import yfinance as yf
""", language='python')

st.markdown("## 2. Define the ticker symbol")
st.code("""
tickerSymbol = 'AAPL'
""", language='python')

tickerSymbol = 'AAPL'

st.code("""# Get data on the specified ticker

tickerDf = yf.download(tickerSymbol, start='2010-5-31', end='2023-5-31') 
""", language='python')

st.markdown("## 3. Show entire historical data in a table")
st.code("""
   st.write("## Complete historical data")
   st.dataframe(tickerDf)
   """, language='python')

tickerDf = yf.download(tickerSymbol, start='2010-5-31', end='2023-5-31')

st.subheader("Complete historical data")
st.dataframe(tickerDf.head())

st.markdown("## 4. Plotting data using Plotly")
st.code("""
fig = px.line(tickerDf, x=tickerDf.index, y="Close", title='Apple Close Price Over Time')
st.plotly_chart(fig)
""", language='python')

# Plotting data using plotly
fig = px.line(tickerDf, x=tickerDf.index, y="Close", title='Apple Close Price Over Time')
st.plotly_chart(fig)

st.markdown("## Full Code:")
st.code("""
import streamlit as st
import plotly.express as px
import yfinance as yf

def main():
    tickerSymbol = 'AAPL'
    tickerDf = yf.download(tickerSymbol, start='2010-5-31', end='2023-5-31')
    st.write("## Complete historical data")
    st.dataframe(tickerDf)
    fig = px.line(tickerDf, x=tickerDf.index, y="Close", title='Apple Close Price Over Time')
    st.plotly_chart(fig)


main()
""", language='python')

st.divider()

st.write("""Let's think, now we can fetch stock data and we also know how to build a chart with multiple selections:

- let's combine these components together and build a chart with the ability to select stocks.
- we can see that the data is too granular showing daily figures, we can smooth the chart by showing the last value of each month. We need to do a bit of data preparation here. 
- we also see that each time the page refreshes we fetch the data from API again, this is not a very good pattern as it put the load on API, so let's try to save the data to cache, it will be fetched once when the app is first opened.
""")

st.header('Combining the results and building chart for multiple stocks')

st.markdown("## 1. Define the stocks dictionary")
st.code("""
stocks = {
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "S&P 500": "^GSPC"
}
""", language='python')

stocks = {
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "S&P 500": "^GSPC"
}

st.markdown("## 2. Select a stock ticker")
st.code("""
clist = list(stocks.keys())
selected_stocks = st.multiselect("Select stock", clist)
""", language='python')

clist = list(stocks.keys())
selected_stocks = st.multiselect("Select stock", clist)

st.markdown("## 3. Download and cache data")
st.code("""
    from datetime import datetime, timedelta # add this library to imports
    
@st.cache_data
def fetch_data(stock, start_date, end_date):
    stock_data = yf.download(stock, start=start_date, end=end_date)["Close"]  # Adjust the date range as needed
    stock_data = stock_data.resample('M').last() # Resample data to get the last price of each month
    stock_data = stock_data.reset_index()
    stock_data["Symbol"] = stock
    return stock_data

today = datetime.today().date()
twenty_years_ago = today - timedelta(days=20*365)
date_range = [twenty_years_ago, today]

df = pd.DataFrame()
for stock in stocks.values():
    df = pd.concat([df, fetch_data(stock, date_range[0], date_range[1])])

st.dataframe(df.head(20))
   """, language='python')

@st.cache_data
def fetch_data(stock, start_date, end_date):
    stock_data = yf.download(stock, start=start_date, end=end_date)["Close"]  # Adjust the date range as needed
    stock_data = stock_data.resample('M').last() # Resample data to get the last price of each month
    stock_data = stock_data.reset_index()
    stock_data["Symbol"] = stock
    return stock_data

today = datetime.today().date()
twenty_years_ago = today - timedelta(days=20*365)
date_range = [twenty_years_ago, today]

df = pd.DataFrame()
for stock in stocks.values():
    df = pd.concat([df, fetch_data(stock, date_range[0], date_range[1])])

st.dataframe(df.head(20))

st.markdown("## 4. Plotting data using Plotly")
st.code("""
def draw_plot(dfs):
    fig = go.Figure()
    for stock, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name=stock))
    st.plotly_chart(fig)

clist = list(stocks.keys())
stocks_selected = st.multiselect("Select stocks", clist)
st.header("You selected: {}".format(", ".join(stocks_selected)))
dfs = {stock: df[df["Symbol"] == stocks[stock]] for stock in stocks_selected}
draw_plot(dfs)
""", language='python')

def draw_plot(dfs):
    fig = go.Figure()
    for stock, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name=stock))
    st.plotly_chart(fig)

clist = list(stocks.keys())
stocks_selected = st.multiselect("Select stocks", clist)
st.header("You selected: {}".format(", ".join(stocks_selected)))
dfs = {stock: df[df["Symbol"] == stocks[stock]] for stock in stocks_selected}
draw_plot(dfs)


st.markdown("## Full Code:")
st.code("""
    import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Create a dictionary with stock symbols as keys
stocks = {
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "S&P 500": "^GSPC"
}

@st.cache_data
def fetch_data(stock, start_date, end_date):
    stock_data = yf.download(stock, start=start_date, end=end_date)["Close"]
    stock_data = stock_data.resample('M').last()
    stock_data = stock_data.reset_index()
    stock_data["Symbol"] = stock
    return stock_data

def get_stock_data(stocks, start_date, end_date):
    df = pd.DataFrame()
    for stock in stocks.values():
        df = pd.concat([df, fetch_data(stock, start_date, end_date)])
    return df

def draw_plot(dfs):
    fig = go.Figure()
    for stock, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name=stock))
    st.plotly_chart(fig)

def main():
    today = datetime.today().date()
    twenty_years_ago = today - timedelta(days=20*365)
    date_range = [twenty_years_ago, today]

    df = get_stock_data(stocks, date_range[0], date_range[1])

    clist = list(stocks.keys())
    stocks_selected = st.multiselect("Select stock", clist)
    st.header("You selected: {}".format(", ".join(stocks_selected)))

    dfs = {stock: df[df["Symbol"] == stocks[stock]] for stock in stocks_selected}
    draw_plot(dfs)


main()
    """, language='python')

