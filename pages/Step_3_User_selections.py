import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
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

st.header("Step 3. User selections and final touches")
st.write("""Almost there, the result starts to look presentable. But your know that you manager will be asking for period selection and the ability to compare more stocks. 

1. Data :white_check_mark:
2. Chart :white_check_mark:
3. Ability to display selected values (interactivity) :white_check_mark:
4. Ability to add new values dynamically :white_check_mark:
5. Ability to select time periods :white_check_mark:

Let's focus on the remaining components and also polish the solution as we go.
""")

st.header("Adding the remaining components")
st.write("Note that at this stage you should use the code from previous steps and add to it")

st.header("1. Select Date Range")
st.code("""
# get today's date
today = datetime.today().date()  
# calculate the date 20 years ago
twenty_years_ago = today - timedelta(days=20*365)  
# create an input widget for the date range, preset with a 20 year range from today
date_range = st.date_input("Date range", [twenty_years_ago, today])  
""", language='python')
st.markdown("We've used Streamlit's date_input function to select a range for which to fetch stock data.")
today = datetime.today().date()
twenty_years_ago = today - timedelta(days=20*365)
date_range = st.date_input("Date range", [twenty_years_ago, today])

df = get_stock_data(stocks, date_range[0], date_range[1])


st.header("2. Normalize the data")
st.write("We can spot that if we compare SP500 index and any stock on the same chart the proportions of Y-axis are not allowing us to see the details. This happens beacuse the index is measured in points which are for SP500 in thousands range and stocks are usually traded in 1-1000$ range to be accessible for the wider audience. ")
st.write("""In simple terms, normalization of stock prices is a way of adjusting the prices so that they start from the same point, which is typically 100, and show the percentage change from that starting point.

This is useful when comparing multiple stocks over time. If you were to simply plot the stock prices of multiple companies on a graph, the one with the higher price would always appear to have more variation. By normalizing, you're putting all stocks on a level playing field.

Consider an example where you have two stocks, one starts from 100 USD and another from 10 USD. After a year, the first stock might have risen to 120, and the second stock to 20. If you plot the raw prices, the first stock appears to have risen more because it went from 100 to 120.

But if you normalize, you would consider the starting price as 100 for both stocks. After a year, the first stock has risen to 120 (20% increase), and the second stock to 200 (a 100% increase). So now when you plot the prices, it is clear that the second stock has increased more in percentage terms despite having a lower raw price.

That's why we normalize data: to make fair comparisons between different stocks.
 """)
st.code("""df["Close"] = (df["Close"] / df.groupby("Symbol")["Close"].transform('first')) * 100
""", language='python')

st.markdown("Let's add a checkbox to allow the user to choose whether to normalize the data or not.")

st.code("""
normalize_data = st.checkbox('Normalize data', value=False)
if normalize_data:
    df["Close"] = (df["Close"] / df.groupby("Symbol")["Close"].transform('first')) * 100  # Normalize to percentage change from first date
""", language='python')

normalize_data = st.checkbox('Normalize data', value=False)
if normalize_data:
    df["Close"] = (df["Close"] / df.groupby("Symbol")["Close"].transform('first')) * 100  # Normalize to percentage change from first date

st.header("3.: Add Ticker Input")
st.code("""
new_stock = st.text_input('Enter a new stock ticker')
stocks[new_stock] = new_stock
""", language='python')
st.markdown("We've added an input for users to enter new stock tickers. ")
new_stock = st.text_input('Enter a new stock ticker')
if new_stock:
    try:
        stocks[new_stock] = new_stock
    except Exception as e:
        st.warning(f"Failed to fetch data for {new_stock}. Please make sure it's a valid ticker symbol.")
        st.write("Error details:", str(e))

df = pd.DataFrame()
for stock in stocks.values():
    df = pd.concat([df, fetch_data(stock, date_range[0], date_range[1])])

clist = list(stocks.keys())
stocks_selected = st.multiselect("Select stock", clist)
st.header("You selected: {}".format(", ".join(stocks_selected)))


dfs = {stock: df[df["Symbol"] == stocks[stock]] for stock in stocks_selected}
draw_plot(dfs)

st.header("Full Code")
st.code("""
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
    stock_data = stock_data.resample('M').last() # Resample data to get the last price of each month
    stock_data = stock_data.reset_index()
    stock_data["Symbol"] = stock
    return stock_data

# Add the ability to write a stock ticker
new_stock = st.text_input('Enter a new stock ticker')

stocks[new_stock] = new_stock

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
normalize_data = st.checkbox('Normalize data', value=False)

if normalize_data:
    df["Close"] = (df["Close"] / df.groupby("Symbol")["Close"].transform('first')) * 100  # Normalize to percentage change from first date

st.header("You selected: {}".format(", ".join(stocks_selected)))

dfs = {stock: df[df["Symbol"] == stocks[stock]] for stock in stocks_selected}

fig = go.Figure()
for stock, df in dfs.items():
    fig = fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name=stock))

st.plotly_chart(fig)

""", language='python')
