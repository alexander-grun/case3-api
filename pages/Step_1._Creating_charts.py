import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.header("Step 1. Creating Charts")
st.write("""Your manager saw a nice-looking line chart with the ability to select any number of variables and show historical data. He wants you to build the prototype for the case you are working with. Your customers are mostly interested in investing in big tech stocks and the SP500 index, so you need to analyze the performance of those and also be able to compare other stocks to these benchmarks visually. 

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
st.write("For now we are leaving the question 'Where should I take the data from?' out and utilizing built-in datasets that Plotly has. We will practice on world's demographics and economics data from Gapminder. Read more about built-in datasets in Plotly documentation https://plotly.com/python-api-reference/generated/plotly.data.html#module-plotly.data")
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

st.markdown("## 1. Add you chart to webpage")
st.code("""
    import streamlit as st
    import plotly.express as px

    def main():
        df = px.data.gapminder()
        df_india = df[df['country'] == 'India']
        fig = px.line(df_india, x='year', y='lifeExp', title='Life Expectancy in India Over the Years')
        st.plotly_chart(fig)

    main()
    """, language='python')
st.write("Remember to run the Streamlit app, save it into a Python file (e.g., streamlit_app.py), and then in your terminal, run:")
st.code("streamlit run streamlit_app.py", language="python")
st.write("This will start the Streamlit server and open a new tab in your web browser displaying your web app.")

st.markdown("## 2. Select multiple countries")
st.code("""
# Retrieve unique values from the "country" column of the DataFrame and convert them into a list
clist = df["country"].unique().tolist()

# Create a multiselect widget using Streamlit
# Prompt the user to select countries from the list of available options
# The selected options will be stored in the 'countries' variable
countries = st.multiselect("Select country", clist)

# Display Selected country in the header for the user
st.header("You selected: {}".format(", ".join(countries)))

""", language='python')
st.write("End result should look like this:")
st.divider()
clist = df["country"].unique().tolist()
countries = st.multiselect("Select countries", clist)
st.header("You selected: {}".format(", ".join(countries)))
st.divider()

st.markdown("## 3. Filter the data for the selected countries and create an empty figure")
st.code("""
dfs = {country: df[df["country"] == country] for country in countries}
fig = go.Figure()
""", language='python')

st.markdown("## 4. Add a scatter plot for each country to the figure")
st.code("""
for country, df in dfs.items():
    fig = fig.add_trace(go.Scatter(x=df["year"], y=df["gdpPercap"], name=country))

fig.update_layout(
        title="GDP Per Capita Over Time",
        xaxis_title="Year",
        yaxis_title="GDP Per Capita"
    ) #Update the layout to include a chart title

st.plotly_chart(fig) #Display the figure using Plotly in Streamlit
""", language='python')

st.markdown("## Full Code:")
st.code("""
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def main():
    df = pd.DataFrame(px.data.gapminder())
    clist = df["country"].unique().tolist()
    countries = st.multiselect("Select country", clist)
    st.header("You selected: {}".format(", ".join(countries)))
    dfs = {country: df[df["country"] == country] for country in countries}
    fig = go.Figure()
    for country, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["year"], y=df["gdpPercap"], name=country))
    fig.update_layout(
        title="GDP Per Capita Over Time",
        xaxis_title="Year",
        yaxis_title="GDP Per Capita"
    )
    st.plotly_chart(fig)

main() """, language='python')
st.divider()
st.subheader("Demo:")
def main():
    df = pd.DataFrame(px.data.gapminder())
    clist = df["country"].unique().tolist()
    countries = st.multiselect("Select country", clist)
    st.header("You selected: {}".format(", ".join(countries)))
    dfs = {country: df[df["country"] == country] for country in countries}
    fig = go.Figure()
    for country, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["year"], y=df["gdpPercap"], name=country))
    fig.update_layout(
        title="GDP Per Capita Over Time",
        xaxis_title="Year",
        yaxis_title="GDP Per Capita"
    )
    st.plotly_chart(fig)

main()







