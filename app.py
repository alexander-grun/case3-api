import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def plot():
    # Load the gapminder dataset into a DataFrame
    df = pd.DataFrame(px.data.gapminder())

    # Extract the unique countries from the DataFrame
    clist = df["country"].unique().tolist()

    # Allow the user to select multiple countries
    countries = st.multiselect("Select country", clist)

    # Display the selected countries as a header
    st.header("You selected: {}".format(", ".join(countries)))

    # Create a dictionary of DataFrames, with each country as the key
    dfs = {country: df[df["country"] == country] for country in countries}

    # Create an empty figure
    fig = go.Figure()

    # Add a scatter plot for each country to the figure
    for country, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["year"], y=df["gdpPercap"], name=country))

    # Update the layout to include a chart title
    fig.update_layout(
        title="GDP Per Capita Over Time",
        xaxis_title="Year",
        yaxis_title="GDP Per Capita"
    )

    # Display the figure using Plotly in Streamlit
    st.plotly_chart(fig)


plot()
