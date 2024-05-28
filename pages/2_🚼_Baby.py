import yaml
import streamlit as st
from yaml.loader import SafeLoader
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

# Liste der Fruchtgrössen
fruchtgroessen = [
    ("4 Wochen", "Mohnsamen", "https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Mohnsamen.jpg"),
    ("5 Wochen", "Sonnenblumenkern", "https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Sonnenblumenkern.jpg"),
    ("6 Wochen", "Linsenkorn"),
    ("7 Wochen", "Blaubeere"),
    ("8 Wochen", "Kidneybohne"),
    ("9 Wochen", "Traube"),
    ("10 Wochen", "Kirsche"),
    ("11 Wochen", "Erdbeere"),
    ("12 Wochen", "Limette"),
    ("13 Wochen", "Erbsenschote"),
    ("14 Wochen", "Zitrone"),
    ("15 Wochen", "Apfel"),
    ("16 Wochen", "Avocado"),
    ("17 Wochen", "Rübe"),
    ("18 Wochen", "Paprika"),
    ("19 Wochen", "Mango"),
    ("20 Wochen", "Banane"),
    ("21 Wochen", "Karotte"),
    ("22 Wochen", "Papaya"),
    ("23 Wochen", "Grapefruit"),
    ("24 Wochen", "Maiskolben"),
    ("25 Wochen", "Aubergine"),
    ("26 Wochen", "Zucchini"),
    ("27 Wochen", "Blumenkohl"),
    ("28 Wochen", "Aubergine"),
    ("29 Wochen", "Butternusskürbis"),
    ("30 Wochen", "Kohlkopf"),
    ("31 Wochen", "Kokosnuss"),
    ("32 Wochen", "Jicama (Yam Bean)"),
    ("33 Wochen", "Ananas"),
    ("34 Wochen", "Melone"),
    ("35 Wochen", "Honigmelone"),
    ("36 Wochen", "Romanesco"),
    ("37 Wochen", "Lauch"),
    ("38 Wochen", "Rhabarber"),
    ("39 Wochen", "Wassermelone"),
    ("40 Wochen", "Kürbis"),
]

# Main definieren mit allen gewünschten Funktionen
def baby_main(username):
    file_suffix = username
    st.header('Baby :ship:')
    st.subheader('Ideen Babyname')
    baby_name_date = st.date_input("Babyname Datum", value=datetime.today(), max_value=datetime.today(), format="YYYY/MM/DD")
    baby_name_text = st.text_area("Babyname")
    if st.button("Name speichern"):
        new_row = pd.DataFrame({"Datum": [baby_name_date], "Babyname": [baby_name_text]})
        file_name = f"baby_name_{file_suffix}.csv"
        if github.file_exists(file_name):
            mama_babyname_df = github.read_df(file_name)
            mama_babyname_df = pd.concat([mama_babyname_df, new_row], ignore_index=True)
        else:
            mama_babyname_df = new_row.copy()
        github.write_df(file_name, mama_babyname_df, "Speicher Babyname")
    if github.file_exists(f"baby_name_{file_suffix}.csv"):
        mama_babyname_df = github.read_df(f"baby_name_{file_suffix}.csv")
        st.write(mama_babyname_df)
    else:
        st.write("Noch keine Babynamen vorhanden.")
    st.subheader('Entwicklung Baby')
    df = pd.DataFrame(fruchtgroessen, columns=['Weeks', 'Fruit', 'Image URL'])
    column_config = {
        "Image URL": st.data_editor.ImageColumn("Image")
    }
    st.data_editor(df, column_config=column_config)

# Load the configuration file
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

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
    baby_main(username)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
