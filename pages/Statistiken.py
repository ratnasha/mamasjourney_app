import streamlit as st
import pandas as pd
from github_contents import GithubContents

# Initialize GithubContents object
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
    )

# Read DataFrame and column names
def read_df(csv):
    if github.file_exists(csv):
        df = github.read_df(csv)
        xaxis = df.columns[0]
        yaxis = df.columns[1]
        return df, xaxis, yaxis
    else:
        st.error(f"File {csv} does not exist.")
        return None, None, None

# Function to plot the graph
def plot_graph(csv):
    df, xaxis, yaxis = read_df(csv)
    if df is not None and xaxis is not None and yaxis is not None:
        st.write("### DataFrame:")
        st.write(df)  # Display the DataFrame
        st.write(f"X-axis: {xaxis}, Y-axis: {yaxis}")
        st.line_chart(df[[xaxis, yaxis]].set_index(xaxis))  # Plot the line chart
    else:
        st.error("Error in loading DataFrame or column names.")

# Plot the graph for the specific file
if authentication_status:
    authenticator.logout('Logout', 'main')
    if username == 'mama1':
        st.write(f'Welcome *{name}*')
        plot_graph('mama_weights.csv')
elif username == 'mama2':
        st.write(f'Welcome *{name}*')
        plot_graph('mama_weights_mama2.csv')
