import streamlit as st

st.set_page_config(layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("""In this case you will practice data retrieval and manipulation with Python. 
You will:
- retrieve the data from API
- process the data with Pandas
- visualize the results 
- iterate in this process and get the final result customized to the requirements
""")

st.subheader("Preparation")

st.write("""In this project we will need the following libraries:
- plotly
- pandas
- streamlit

""")

st.code("""
pip install ADD LIBRARIES HERE
""", language='python')