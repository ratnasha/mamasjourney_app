import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read Dataframe for weight
def read_df(csv):
  if github.file_exists(csv):
            df = github.read_csv(csv)
            st.write(df)

# Darstellung der Daten
def plot_line_chart(df):
  st.title('Gewichtsentwicklung')
  st.line_chart(df['weight'])

read_df("mama_weights.csv")
plot_line_chart(weight_data)
