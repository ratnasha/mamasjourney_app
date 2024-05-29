import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime, timedelta
from github_contents import GithubContents
import bcrypt

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")
st.sidebar.image('https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Logo2.jpg?raw=true', use_column_width=True)

# Verbindung zu GitHub initialisieren
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"]
)

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

# Ensure the 'usernames' field exists in 'credentials'
if 'credentials' not in config:
    config['credentials'] = {'usernames': {}}
if 'usernames' not in config['credentials']:
    config['credentials']['usernames'] = {}

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

            # Überprüfen, ob der Benutzername bereits existiert
            if new_username in config['credentials']['usernames']:
                st.error("Username already exists. Please choose a different one.")
                return

            # Passwort hashen
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode()

            # Neuen Benutzer zur Konfiguration hinzufügen
            new_user = {
                "email": new_email,
                "name": new_username,
                "password": hashed_password
            }
            config['credentials']['usernames'][new_username] = new_user

            # Aktualisierte Konfiguration speichern
            save_config(config)

            st.success("Registration successful! You can now log in.")

def about_mamasjourney():
    st.subheader("Willkommen bei deiner persönlichen Schwangerschafts-App")
    st.markdown('"Mamasjourney" ist ein digitales Schwangerschaftstagebuch für werdende Mütter. Mit dieser App können sie jederzeit auf ihre persönlichen Daten zugreifen und wichtige Informationen wie aktuelle Schwangerschaftswoche, Blutwerte und Gewicht verflogen kann. Nur die Mutter selbst hat Zugriff auf diese Daten über ihren eigenen Benutzer-Login. Sie kann ihre Informationen manuell hinzufügen. Die App erfasst die gesamten 40 Schwangerschaftswochen und bietet außerdem die Möglichkeit, Gefühle und Gedanken schriftlich festzuhalten.')

def main(username):
    st.write(f'Willkommen *{username}*')
    st.markdown("""
    <div style="text-align: left;">
        <img src="https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Logo.jpg?raw=true" alt="ship" style="height: 5em;">
    </div>
    """, unsafe_allow_html=True)
    about_mamasjourney()



# Main application logic
def app():
    page = st.sidebar.selectbox("Choose an action", ["Login", "Register"])
    if page == "Login":
        try:
            name, authentication_status, username = authenticator.login()
            if authentication_status:
                authenticator.logout('Logout', 'main')
                main(username)
            elif authentication_status == False:
                st.error('Username/password is incorrect')
            elif authentication_status == None:
                st.warning('Please enter your username and password')
        except KeyError as e:
            st.error(f"KeyError: {e}. This may be due to a missing username in the credentials.")
            st.write(f"Debug: Please check the token and credentials structure.")
            st.write(f"Debug: config['credentials'] - {config['credentials']}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    elif page == "Register":
        register()

if __name__ == "__main__":
    app()
