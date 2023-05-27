import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.header("Final assignement")
if st.button('Celebrate!'):
    st.balloons()
st.write("""Well done! 
         
1. Data :white_check_mark:
2. Chart :white_check_mark:
3. Ability to display selected values (interactivity) :white_check_mark:
4. Ability to add new values dynamically :white_check_mark:
5. Ability to select time periods :white_check_mark:         
           
You have just created an interactive dashboard using real API data in Python, this is awesome! Don't stop here, think about how can you use these skills in your own projects or how can it help at work. """)

st.write("To complete these assignement add ")
st.write("""
1. Make it so that the data is shown Quarterly instead of monthly
2. While the closing price simply refers to the cost of shares at the end of the day, the adjusted closing price takes dividends, stock splits, and new stock offerings into account. Change Close price to Adjusted close price.
3. Add error handling to avoid errors when wrong ticker is provided by user or when data is not found from API

You can see these implemented below
""")

st.divider()


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
    stock_data = yf.download(stock, start=start_date, end=end_date)["Adj Close"]  # Adjust the date range as needed
    stock_data = stock_data.resample('Q').last() # Resample data to get the last price of each month
    stock_data = stock_data.reset_index()
    stock_data["Symbol"] = stock
    return stock_data

# Add a slider for the time period selection
today = datetime.today().date()
twenty_years_ago = today - timedelta(days=20*365)
date_range = st.date_input("Date range", [twenty_years_ago, today])

# Add the ability to write a stock ticker
new_stock = st.text_input('Enter a new stock ticker')

# Test if new_stock is valid
try:
    # Try to download data for the new_stock from yfinance.
    # If new_stock is not a valid ticker, an error will occur here.
    test_data = yf.download(new_stock, start=date_range[0], end=date_range[1])

    # If the downloaded data is empty, it indicates that new_stock may not be a valid ticker
    # or there's no available data for the given date range. Show a warning message in this case.
    if test_data.empty:
        st.warning(f"Failed to fetch data for {new_stock}. Please make sure it's a valid ticker symbol.")
    else:
        # If the downloaded data is not empty, it means new_stock is a valid ticker.
        # Add new_stock to the stocks dictionary.
        stocks[new_stock] = new_stock
except:
    # If an error occurred while downloading data for new_stock, silently ignore it.
    # Note: It's generally a good idea to at least log the error message or show it to the user,
    # rather than ignoring it entirely.
    pass

# Fetch stock prices using the yfinance library
df = pd.DataFrame()
for stock in stocks.values():
    df = pd.concat([df, fetch_data(stock, date_range[0], date_range[1])])

clist = list(stocks.keys())
stocks_selected = st.multiselect("Select stock", clist)

# Add checkbox to toggle normalization
normalize_data = st.checkbox('Normalize data', value=False)

if normalize_data:
    df["Adj Close"] = (df["Adj Close"] / df.groupby("Symbol")["Adj Close"].transform('first')) * 100  # Normalize to percentage change from first date

st.header("You selected: {}".format(", ".join(stocks_selected)))

dfs = {stock: df[df["Symbol"] == stocks[stock]] for stock in stocks_selected}

fig = go.Figure()
for stock, df in dfs.items():
    fig = fig.add_trace(go.Scatter(x=df["Date"], y=df["Adj Close"], name=stock))

st.plotly_chart(fig)
