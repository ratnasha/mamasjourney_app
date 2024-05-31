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

# Liste der Fruchtgrössen
fruchtgroessen = [
    ("4 Wochen", "Mohnsamen.jpg"),
    ("5 Wochen", "Sonnenblumenkern.jpg"),
    ("6 Wochen", "Linsenkorn.jpg"),
    ("7 Wochen", "Heidelbeere.jpg"),
    ("8 Wochen", "Himbeere.jpg"),
    ("9 Wochen", "Kirsche.jpg"),
    ("10 Wochen", "Erdbeere.jpg"),
    ("11 Wochen", "Feige.jpg"),
    ("12 Wochen", "Limette.jpg"),
    ("13 Wochen", "Pflaume.jpg"),
    ("14 Wochen", "Zitrone.jpg"),
    ("15 Wochen", "Apfel.jpg"),
    ("16 Wochen", "Avocado.jpg"),
    ("17 Wochen", "Kartoffel.jpg"),
    ("18 Wochen", "Paprika.jpg"),
    ("19 Wochen", "Mango.jpg"),
    ("20 Wochen", "Banane.jpg"),
    ("21 Wochen", "Karotte.jpg"),
    ("22 Wochen", "Papaya.jpg"),
    ("23 Wochen", "Grapefruit.jpg"),
    ("24 Wochen", "Maiskolben.jpg"),
    ("25 Wochen", "Aubergine.jpg"),
    ("26 Wochen", "Zucchini.jpg"),
    ("27 Wochen", "Blumenkohl.jpg"),
    ("28 Wochen", "Kopfsalat.jpg"),
    ("29 Wochen", "Butternusskürbis.jpg"),
    ("30 Wochen", "Kohlkopf.jpg"),
    ("31 Wochen", "Kokosnuss.jpg"),
    ("32 Wochen", "Jicama.jpg"),
    ("33 Wochen", "Ananas.jpg"),
    ("34 Wochen", "Cantaloupe.jpg"),
    ("35 Wochen", "Honigmelone.jpg"),
    ("36 Wochen", "Romana-Salat.jpg"),
    ("37 Wochen", "Lauch.jpg"),
    ("38 Wochen", "Rhabarber.jpg"),
    ("39 Wochen", "Wassermelone.jpg"),
    ("40 Wochen", "Kürbis.jpg"),
]

base_url = "https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/"

# Main definieren mit allen gewünschten Funktionen
def baby_main(username):
    file_suffix = username
    st.markdown("""
    <h1 style="display: flex; align-items: center;">
        Baby
        <img src="https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Schiff.jpg?raw=true" alt="ship" style="height: 1em; margin-left: 10px;">
    </h1>
    """, unsafe_allow_html=True)
    # Tabs erstellen
    tab1, tab2 = st.tabs(["Entwicklung Baby", "Babynamen"])
    # Visualisierung der Grössenentwicklung des Babys
    with tab1:
        st.subheader('Entwicklung Baby')
        df = pd.DataFrame(fruchtgroessen, columns=["Schwangerschaftswoche", "Grösse"])
        def path_to_image_html(image_name):
            if image_name:  
                return f'<img src="{base_url}{image_name}?raw=true" width="150" >'
            return "" 
        df['Grösse'] = df['Grösse'].apply(path_to_image_html)
        mid_index = len(df) // 2
        df1 = df.iloc[:mid_index]
        df2 = df.iloc[mid_index:]
        html1 = df1.to_html(escape=False, index=False, justify='center', border=0)
        html2 = df2.to_html(escape=False, index=False, justify='center', border=0)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(html1, unsafe_allow_html=True)
        with col2:
            st.markdown(html2, unsafe_allow_html=True)
    # Babyname Ideen
    with tab2:
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

# Konfiguration laden
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

config = load_config()

# Authenticator initialisieren
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Authentication und Darstellung der Elemente
name, authentication_status, username = authenticator.login()
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    baby_main(username)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
