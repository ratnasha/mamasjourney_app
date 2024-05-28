import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from github_contents import GithubContents

st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")

# Initialize GithubContents object
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Read DataFrame and column names from GitHub
def read_df(csv):
    if github.file_exists(csv):
        df = github.read_df(csv)
        xaxis = df.columns[0]
        yaxis = df.columns[1]
        return df, xaxis, yaxis
    else:
        return None, None, None

# Function to plot the graph
def plot_graph(csv, title, y_label):
    df, xaxis, yaxis = read_df(csv)
    if df is not None and xaxis is not None and yaxis is not None:
        st.write(f"### {title}:")
        st.write(f"X-Achse: {xaxis}, Y-Achse: {yaxis}")
        st.line_chart(df.set_index(xaxis)[yaxis], color='#77ddaa', height=0, width=0)  # Plot the line chart
    else:
        st.warning(f"Es wurden keine Daten erfasst für {title}.")

# Load configuration
def load_config():
    try:
        data = github.read_json("config.json")
        return data
    except Exception as e:
        st.error(f"Fehler beim Laden der Konfigurationsdatei: {e}")
        return {}

def save_config(config):
    try:
        github.write_json("config.json", config, "Update config")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Konfigurationsdatei: {e}")

# Laden der Konfigurationsdaten
config = load_config()

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Authentication and visualizing the charts
name, authentication_status, username = authenticator.login()
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.markdown("""
    <h1 style="display: flex; align-items: center;">
        Statistiken
        <img src="https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Schiff.jpg?raw=true" alt="ship" style="height: 1em; margin-left: 10px;">
    </h1>
    """, unsafe_allow_html=True)
    plot_graph(f'mama_weights_{username}.csv', 'Gewichtsverlauf', 'kg')
    plot_graph(f'mama_blutwert_{username}.csv', 'Blutzuckerwerte Verlauf', 'mg/dL')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
