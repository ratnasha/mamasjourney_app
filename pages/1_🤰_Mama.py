import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents

st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")

# Verbindung zu GitHub initialisieren
github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

def mama_main(username):
    file_suffix = username
    def load_last_period_date(file_suffix):
        try:
            data = github.read_json(f"last_period_date_{file_suffix}.json")
            last_period_date = pd.to_datetime(data["last_period_date"])
        except:
            last_period_date = None
        return last_period_date

    def calculate_due_date(last_period_date):
        gestation_period = timedelta(days=280)
        due_date = last_period_date + gestation_period
        return due_date

    
    last_period_date = load_last_period_date(file_suffix)

    st.markdown("""
    <h1 style="display: flex; align-items: center;">
        Mama
        <img src="https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Schiff.jpg?raw=true" alt="ship" style="height: 1em; margin-left: 10px;">
    </h1>
    """, unsafe_allow_html=True)
    if last_period_date is not None:
        last_period_date = st.date_input('Letzter Menstruationszyklus', value=last_period_date, format="YYYY/MM/DD")
    else:
        last_period_date = st.date_input('Letzter Menstruationszyklus', format="YYYY/MM/DD")

    if last_period_date:
        due_date = calculate_due_date(last_period_date)
        due_date_str = due_date.strftime('%d-%m-%Y')
        st.markdown(f"<div style='font-size: 24px; color: forestgreen;'>Voraussichtlicher Geburtstermin: {due_date_str}</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Schwangerschaftsverlauf.jpg?raw=true" alt="ship" style="height: 25em;">
    </div>
    """, unsafe_allow_html=True)

    st.write('Gewicht')
    mama_weight_date = st.date_input("Gewicht Datum", value=datetime.today(), max_value=datetime.today(), format="YYYY/MM/DD")
    mama_weight = st.number_input("Gewicht (kg)", min_value=0.0)
    if st.button("Gewicht speichern"):
        new_row = pd.DataFrame({"Datum": [mama_weight_date], "Gewicht (kg)": [mama_weight]})
        file_name = f"mama_weights_{file_suffix}.csv"
        if github.file_exists(file_name):
            mama_weights_df = github.read_df(file_name)
            mama_weights_df = pd.concat([mama_weights_df, new_row], ignore_index=True)
        else:
            mama_weights_df = new_row.copy()
        github.write_df(file_name, mama_weights_df, "Speicher Gewicht")

    st.subheader('Gewichtsdaten')
    if github.file_exists(f"mama_weights_{file_suffix}.csv"):
        mama_weights_df = github.read_df(f"mama_weights_{file_suffix}.csv")
        st.write(mama_weights_df)
    else:
        st.write("Noch keine Gewichtsdaten vorhanden.")

    st.write('Blutwerte')
    blutwerte_date = st.date_input("Blutwerte Datum", value=datetime.today(), max_value=datetime.today(), format="YYYY/MM/DD")
    blutwerte_text = st.text_area("Blutzuckerwerte")
    if st.button("Blutwert speichern"):
        new_row = pd.DataFrame({"Datum": [blutwerte_date], "Blutzuckerwert (in mg/dL)": [blutwerte_text]})
        file_name = f"mama_blutwert_{file_suffix}.csv"
        if github.file_exists(file_name):
            mama_blutwert_df = github.read_df(file_name)
            mama_blutwert_df = pd.concat([mama_blutwert_df, new_row], ignore_index=True)
        else:
            mama_blutwert_df = new_row.copy()
        github.write_df(file_name, mama_blutwert_df, "Speicher Blutzuckerwert")

    st.subheader('Blutzuckerwert')
    if github.file_exists(f"mama_blutwert_{file_suffix}.csv"):
        mama_blutwert_df = github.read_df(f"mama_blutwert_{file_suffix}.csv")
        st.write(mama_blutwert_df)
    else:
        st.write("Noch keine Blutzuckerwerte vorhanden.")
                
    st.header('Tagebuch')
    tagebuch_date = st.date_input("Tagebuch Datum", value=datetime.today(), max_value=datetime.today(), format="YYYY/MM/DD")
    tagebuch_text = st.text_area("Tagebuch")
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame({"Date": [tagebuch_date], "Tagebuch": [tagebuch_text]})
        file_name = f"tagebuch_{file_suffix}.csv"
        if github.file_exists(file_name):
            tagebuch_df = github.read_df(file_name)
            tagebuch_df = pd.concat([tagebuch_df, new_row], ignore_index=True)
        else:
            tagebuch_df = new_row.copy()
        github.write_df(file_name, tagebuch_df, "Speicher Tagebucheintrag")

    st.subheader('Tagebuch')
    if github.file_exists(f"tagebuch_{file_suffix}.csv"):
        tagebuch_df = github.read_df(f"tagebuch_{file_suffix}.csv")
        st.write(tagebuch_df)
    else:
        st.write("Noch keine Tagebucheinträge vorhanden.")

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

# Authentication and visualizing the elements
name, authentication_status, username = authenticator.login()
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    mama_main(username)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
