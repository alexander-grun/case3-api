import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta


st.header("Step 3. User selections anf final touches")
st.write("""Almost there, the result starts to look presentable. But your know that you manager will be asking for period selection and the ability to compare more stocks. 

1. Data :white_check_mark:
2. Chart :white_check_mark:
3. Ability to display selected values (interactivity) :white_check_mark:
4. Ability to add new values dynamically
5. Ability to select time periods

Let's focus on the remaining components and also polish the solution as we go.
""")

