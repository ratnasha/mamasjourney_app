import streamlit as st
import pandas as pd
import numpy as np
from github_contents import GithubContents

github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

# Read Dataframe and Names for Line Graph
def read_df(csv):
  if github.file_exists(csv):
            df = github.read_df(csv)
            xaxis = pd.read_csv(csv).columns[0]
            yaxis = pd.read_csv(csv).columns[1]

# Darstellung der Daten
def plot_graph(csv):
  data = read_df(csv)
  '''Darstellung eines Linegraph'''
  st.line_chart(data, x=xaxis, y=yaxis, color='#94c871', width=0, height=0)

# Gewicht Mama1
plot_graph('mama_weights.csv')
