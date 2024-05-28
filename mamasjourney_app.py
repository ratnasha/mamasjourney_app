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

            # Check if username already exists
            if new_username in config['credentials']['usernames']:
                st.error("Username already exists. Please choose a different one.")
                return

            # Hash the password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode()

            # Add new user to config
            new_user = {
                "email": new_email,
                "name": new_username,
                "password": hashed_password
            }
            config['credentials']['usernames'][new_username] = new_user

            # Save updated config to file
            with open('./config.yaml', 'w') as file:
                yaml.dump(config, file)

            st.success("Registration successful! You can now log in.")
            
def about_mamasjourney():
    st.subheader("Willkommen bei deiner persönlichen Schwangerschafts-App")
    st.markdown('Diese App soll dir dabei helfen, blababalabal')

def main(username):
    st.write(f'Willkommen *{username}*')
    st.title("mamasjourney :ship:")
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
            st.write(f"Debug: token - {token if 'token' in locals() else 'Token not available'}")
            st.write(f"Debug: config['credentials'] - {config['credentials']}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    elif page == "Register":
        register()

if __name__ == "__main__":
    app()
