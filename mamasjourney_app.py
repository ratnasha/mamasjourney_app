##############################################################################################################
# Title: Multi-User Login and Registration Example
# Author: Samuel Wehrli, Dominik Kunz
# Date: 05.05.2024
# Institution: ZHAW - Institute for Computational Health
#
# Description: 
# A Streamlit app that allows multiple users to login and register. 
# The app uses a CSV file to store user credentials and pushes it to a separate Github repository. 
# The bcrypt library hashes the passwords and the binascii library to convert the hashed password to 
# a hexadecimal string. The app uses the GithubContents class from the github_contents.py file to 
# interact with the Github data repository. The st.secrets object stores the Github owner, repository, 
# and token which are used to authenticate the Github data repository.
#
# To run the app, install the required libraries using: pip install bcrypt binascii
##############################################################################################################

import binascii
import streamlit as st
import pandas as pd
from github_contents import GithubContents
import bcrypt
from datetime import datetime, timedelta

# Set constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def login_page():
    """ Login an existing user. """
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def register_page():
    """ Register a new user. """
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()) # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode() # Convert hash to hexadecimal string
            
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """ 
    Initialize the authentication status.

    Parameters:
    username (str): The username to authenticate.
    password (str): The password to authenticate.    
    """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password) # convert hex to bytes
        
        # Check the input password
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        print("github initialized")
    
def init_credentials():
    """Initialize or load the dataframe."""
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def main_app(username):
    st.write(f'Welcome *{username}*')
    
    def load_last_period_date(file_suffix):
        try:
            data = GithubContents.read_json(f"last_period_date_{file_suffix}.json")
            last_period_date = pd.to_datetime(data["last_period_date"])
        except:
            last_period_date = None
        return last_period_date

    def save_last_period_date(date, file_suffix):
        GithubContents.write_json(f"last_period_date_{file_suffix}.json", {"last_period_date": date.strftime("%Y-%m-%d")}, "Save last period date")

    def calculate_due_date(last_period_date):
        gestation_period = timedelta(days=280)
        due_date = last_period_date + gestation_period
        return due_date

    calendar_weeks_data = {
        'Kalenderwoche': list(range(1, 41)),
        'Ereignis': ['Ultraschall', 'Arztbesuch', 'Ernährungsberatung', 'Geburtsvorbereitungskurs', 'Ruhestunde'] * 8
    } 

    st.title("mamasjourney :ship:")

    file_suffix = username
    last_period_date = load_last_period_date(file_suffix)

    st.header('Mama')
    if last_period_date is not None:
        last_period_date = st.date_input('Letzter Menstruationszyklus', value=last_period_date, format="YYYY/MM/DD")
    else:
        last_period_date = st.date_input('Letzter Menstruationszyklus', format="YYYY/MM/DD")

    if last_period_date:
        due_date = calculate_due_date(last_period_date)
        st.write("Voraussichtlicher Geburtstermin:", due_date)
        st.subheader('Schwangerschafts-Timeline')
        df_calendar_weeks = pd.DataFrame(calendar_weeks_data)
        st.write(df_calendar_weeks)

    st.write('Gewicht')
    mama_weight_date = st.date_input("Datum", value=datetime.today(), min_value=last_period_date, max_value=datetime.today(), format="YYYY/MM/DD")
    mama_weight = st.number_input("Gewicht (kg)", min_value=0.0)
    if st.button("Gewicht speichern"):
        new_row = pd.DataFrame({"Datum": [mama_weight_date], "Gewicht (kg)": [mama_weight]})
        file_name = f"mama_weights_{file_suffix}.csv"
        if GithubContents.file_exists(file_name):
            mama_weights_df = GithubContents.read_df(file_name)
            mama_weights_df = pd.concat([mama_weights_df, new_row], ignore_index=True)
        else:
            mama_weights_df = new_row.copy()
        GithubContents.write_df(file_name, mama_weights_df, "Speicher Gewicht")

    st.subheader('Gewichtsdaten')
    if GithubContents.file_exists(f"mama_weights_{file_suffix}.csv"):
        mama_weights_df = GithubContents.read_df(f"mama_weights_{file_suffix}.csv")
        st.write(mama_weights_df)
    else:
        st.write("Noch keine Gewichtsdaten vorhanden.")

    st.write('Blutwert')
    blutwerte_text = st.text_area("Blutzuckerwerte")
    if st.button("Blutwert speichern"):
        new_row = pd.DataFrame({"Datum": [mama_weight_date], "Blutzuckerwert (in mg/dL)": [blutwerte_text]})
        file_name = f"mama_blutwert_{file_suffix}.csv"
        if GithubContents.file_exists(file_name):
            mama_blutwert_df = GithubContents.read_df(file_name)
            mama_blutwert_df = pd.concat([mama_blutwert_df, new_row], ignore_index=True)
        else:
            mama_blutwert_df = new_row.copy()
        GithubContents.write_df(file_name, mama_blutwert_df, "Speicher Blutzuckerwert")

    st.subheader('Blutzuckerwert')
    if GithubContents.file_exists(f"mama_blutwert_{file_suffix}.csv"):
        mama_blutwert_df = GithubContents.read_df(f"mama_blutwert_{file_suffix}.csv")
        st.write(mama_blutwert_df)
    else:
        st.write("Noch keine Blutzuckerwerte vorhanden.")
                    
    st.header('Tagebuch')
    tagebuch_text = st
