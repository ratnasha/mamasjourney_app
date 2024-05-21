import streamlit as st
import pandas as pd
import numpy as np
from github_contents import GithubContents

github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

# Read Dataframe
def read_df(csv):
  if github.file_exists(csv):
            df = github.read_df(csv)
            st.write(df)

# Darstellung der Daten
weights_mama = read_df("mama_weights.csv")
st.line_chart(data = weights_mama)
