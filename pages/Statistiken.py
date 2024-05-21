import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read Dataframe for weight
url_weights = 'https://github.com/ratnasha/FirstApp-data/blob/main/mama_weights.csv'
weight_data = pd.read_csv(url_weights, parse_dates=['date'])

# Darstellung der Daten
def plot_line_chart(df):
  df.set_index('date', inplace=True)
  st.title('Weight over Time')
  st.line_chart(df['weight'])

plot_line_chart(weight_data)
