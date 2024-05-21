import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read Dataframe for weight
url_weights = 'https://github.com/ratnasha/FirstApp-data/blob/main/mama_weights.csv'
weight_data = pd.read_csv(url_weights, parse_dates=['date'])

# Darstellung der Daten
df.set_index('date', inplace=True)

def plot_line_chart():
  plt.figure(figsize=(10, 6))
  plt.plot(df.index, df['weight'], marker='o', linestyle='-')
  plt.xlabel('Datum')
  plt.ylabel('Gewicht')
  plt.title('Gewichtsentwicklung')
  plt.grid(True)
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.show()

plot_line_chart()
