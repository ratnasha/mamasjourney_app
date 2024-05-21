import streamlit as st
import pandas as pd
import numpy as np

# Read Dataframe for weight
weight_data = pd.read_df("mama_weights.csv")


st.line_chart(data = weight_data, x=None, y=None, color=None, width=0, height=0)
