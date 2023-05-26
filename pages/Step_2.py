import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go


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
st.header('Apple Stock Data Visualization')

# Define the ticker symbol
tickerSymbol = 'AAPL'

# Get data on the specified ticker
tickerDf = yf.download(tickerSymbol, start='2010-5-31', end='2023-5-31')

# Show entire historical data in a table
st.write("""
## Complete historical data
""")
st.dataframe(tickerDf)

# Plotting data using plotly
fig = px.line(tickerDf, x=tickerDf.index, y="Close", title='Apple Close Price Over Time')
st.plotly_chart(fig)


