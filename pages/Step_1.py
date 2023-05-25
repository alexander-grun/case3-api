import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.header("Step 1")
st.write("""Your manager saw a nice-looking line chart with the ability to select any number of variables and show historical data. He wants you to build the prototype for the case you are working with. Your customers are mostly interested to invest in big tech stocks and the SP500 index, so you need to analyze the performance of those and also be able to compare other stocks to these benchmarks visually. 

To solve this complex problem, we need to break it down into smaller pieces and then assemble the final solution. Here are some components which we need to figure out:

1. Data
2. Chart
3. Ability to display selected values (interactivity)
4. Ability to add new values dynamically
5. Ability to select time periods

In Step 1 we will focus on points 2 and 3. Solving Chart and interactivity of user selection.  

""")


st.header('Building chart with Plotly')

st.markdown("## 1. Import necessary libraries")
st.code("""
import plotly.express as px # we will need this for plotting the chart
""", language='python')

st.markdown("## 2. Load the Gapminder dataset")
st.write("For now we are leaving the question 'Where should I take the data from?' out and utilizing built-in datasets that Plotly has. We will practice on world's demographics and economics data from Gapminder. Read more about in plotly documentation https://plotly.com/python-api-reference/generated/plotly.data.html#module-plotly.data")
st.code("""
df = px.data.gapminder() # load the gapminder data into the dataframe 
""", language='python')

df = px.data.gapminder()
st.dataframe(df.head())

st.markdown("## 3. Filter the data for a specific country, e.g., 'India'")
st.code("""
df_india = df[df['country'] == 'India']
""", language='python')

df_india = df[df['country'] == 'India']
st.dataframe(df_india.head())

st.markdown("## 4. Create the line chart")
st.code("""
fig = px.line(df_india, x='year', y='lifeExp', title='Life Expectancy in India Over the Years')
""", language='python')

fig = px.line(df_india, x='year', y='lifeExp', title='Life Expectancy in India Over the Years')

st.markdown("## 5. Display the chart")
st.code("""
fig.show()
""", language='python')

st.plotly_chart(fig)

st.markdown("## Full Code:")
st.code("""
import plotly.express as px

df = px.data.gapminder()
df_india = df[df['country'] == 'India']
fig = px.line(df_india, x='year', y='lifeExp', title='Life Expectancy in India Over the Years')
fig.show()
""", language='python')



st.divider()

st.header('Adding selections to the chart')

st.write("Working with single chart is easy, but once you start to have components and other charts it starts to get hard with layout. To solve this complexity let's bring one more library into this and integrate our plotly chart on the website")

st.markdown("## 1. Select multiple countries")

st.markdown("## 2. Select multiple countries")
st.code("""
# Retrieve unique values from the "country" column of the DataFrame and convert them into a list
clist = df["country"].unique().tolist()

# Create a multiselect widget using Streamlit
# Prompt the user to select countries from the list of available options
# The selected options will be stored in the 'countries' variable
countries = st.multiselect("Select country", clist)

""", language='python')

clist = df["country"].unique().tolist()
countries = st.multiselect("Select country", clist)
st.header("You selected: {}".format(", ".join(countries)))



