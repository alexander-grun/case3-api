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


st.title("Python Case")
st.text("Case description")
st.write("""You are working in a hedge fund as a data analyst. You are supporting sales managers, who explain investment ideas to potential and existing clients. 

Your manager saw a nice-looking line chart with the ability to select any number of variables and show historical data. He wants you to build the prototype for the case you are working with. He has some plans to improve data visualization and data analytics, which is currently using outdated BI tool. 

Your customers are most interested in investing in big tech stocks and the SP500 index, so you need to analyze the performance of those and also be able to compare other stocks to these benchmarks visually to offer some alternatives.


In this case you will practice data retrieval and manipulation with Python. 
You will:
- retrieve the data from API
- process the data with Pandas
- visualize the results 
- iterate in this process and get the final result customized to the requirements
""")

st.subheader("Preparation")

st.write("""This assignement will not work very well in Jupyter Notebooks or similar notebooks. 
  Both Jupyter Notebooks and IDEs (Integrated Development Environments) like VSCode or PyCharm have their uses in the realm of data science and programming in general. 
  They are tools designed to facilitate coding, but they do so in slightly different ways. For a project such as the one you're working on, you might find an IDE more suitable for a few reasons:
- Project Organization: IDEs make it easy to manage and navigate larger codebases across multiple files and directories, thanks to features like advanced file browsers and project views. This is very useful when your project grows beyond a single script or notebook, which is often the case in real-world applications.
- Code Autocompletion and Linting: IDEs often offer advanced code autocompletion, syntax highlighting, and linting tools out of the box. These features can speed up your coding and help you catch errors before runtime.
- Debugging Tools: Advanced debugging is one of the main benefits of using an IDE. Breakpoints, step-through execution, expression evaluation, etc., are all valuable tools when trying to understand the flow of your program or find bugs.
- Version Control: Most IDEs have integrated support for version control systems like Git. This can make managing versions and collaborating with others easier.
- Testing: IDEs often include tools to facilitate testing your code, such as unit tests and integration tests.
- Integrated Terminal: Most IDEs come with an integrated terminal, which can be extremely handy for running scripts, installing packages, managing environments, etc., without having to switch windows.
- Environment Management: Some IDEs have integrated support for virtual environments, which can help isolate your project's dependencies and maintain reproducibility.

We will not utilize all of these features, but these are good practices that can help you later on in more complex projects. 

For now just install VSCode or Pycharm Community edition and setup your first project with virtual environment: 
- https://www.jetbrains.com/pycharm/download/ Pycharm will prompt the creation of virtual environment for each project by default
- https://code.visualstudio.com/download 
In VSCode follow this guide to setup virtual environment
https://code.visualstudio.com/docs/python/environments
  """)

st.write("""In this project we will need the following libraries:
- plotly
- pandas
- streamlit
- yfinance

Install these in the virtual environment that you will be using for this project and let's begin!

""")

st.code("""
pip install plotly pandas streamlit yfinance
""", language='python')