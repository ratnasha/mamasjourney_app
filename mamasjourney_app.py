import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents
import bcrypt

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")

# Verbindung zu GitHub initialisieren
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

# Load configuration
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Debugging Step: Check the loaded config
st.write("Loaded config:", config)

# Ensure the 'users' field exists
if 'credentials' not in config or 'users' not in config['credentials']:
    config['credentials'] = {'users': []}

# Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Registration function
def register():
    st.title("Register")
    with st.form("register_form"):
        new_username = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.form_submit_button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
                return

            # Check if username already exists
            if any(user['username'] == new_username for user in config['credentials']['users']):
                st.error("Username already exists. Please choose a different one.")
                return

            # Hash the password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode()

            # Add new user to config
            new_user = {
                "username": new_username,
                "email": new_email,
                "password": hashed_password
            }
            config['credentials']['users'].append(new_user)

            # Save updated config to file
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file)

            st.success("Registration successful! You can now log in.")

def main(username):
    st.write(f'Welcome *{username}*')

    def load_last_period_date(file_suffix):
        try:
            data = github.read_json(f"last_period_date_{file_suffix}.json")
            last_period_date = pd.to_datetime(data["last_period_date"])
        except:
            last_period_date = None
        return last_period_date

    def save_last_period_date(date, file_suffix):
        github.write_json(f"last_period_date_{file_suffix}.json", {"last_period_date": date.strftime("%Y-%m-%d")}, "Save last period date")

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

    st.write('Blutwert')
    blutwerte_text = st.text_area("Blutzuckerwerte")
    if st.button("Blutwert speichern"):
        new_row = pd.DataFrame({"Datum": [mama_weight_date], "Blutzuckerwert (in mg/dL)": [blutwerte_text]})
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
    tagebuch_text = st.text_area("Tagebuch")
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame({"Date": [mama_weight_date], "Tagebuch": [tagebuch_text]})
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

# Main application logic
def app():
    page = st.sidebar.selectbox("Choose an action", ["Login", "Register"])
    if page == "Login":
        name, authentication_status, username = authenticator.login()
        if authentication_status:
            authenticator.logout('Logout', 'main')
            main(username)
        elif authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')
    elif page == "Register":
        register()

if __name__ == "__main__":
    app()
