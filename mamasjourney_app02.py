import streamlit as st
from streamlit_timeline import st_timeline
import pandas as pd
from datetime import datetime, timedelta, date

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide",)

# Titel-Darstellung
st.title("mamasjourney :ship:")


# Funktion zur Berechnung des Geburtstermins
def calculate_due_date(last_period_date):
    gestation_period = timedelta(days=280)
    due_date = last_period_date + gestation_period
    return due_date

# Timeline Darstellung und Berechnung der SSW
last_period_date = st.date_input('Letzter Menstruationszyklus' , format="YYYY/MM/DD")
if last_period_date:
    due_date = calculate_due_date(last_period_date)
    st.write("Voraussichtlicher Geburtstermin:", due_date)
    
if isinstance(last_period_date, date):
    week = timedelta(days=7)
    weeks = []
    for i in range(1, 43):
        weeks.append(last_period_date + (i * week))
else:
    st.write("Bitte wählen Sie ein Datum aus.")

items = [
    {
        "id": "a",
        "content": "1.Trimester",
        "start": str(last_period_date),
        "end": str(weeks[12]),
        "type": "background"
    }
]

for i, week_date in enumerate(weeks):
    items.append({"id": i + 1, "content": f"SSW{i+1}", "start": str(week_date)})

timeline = st_timeline(items, groups=[], options={}, height='250px')
st.subheader('Ausgewählte Woche')
st.write(timeline)


# Dummy-Daten für den DataFrame
data = {
    'Bauelement': ['Baby', 'Mama', 'Notizen'],
    'Gewicht': [57, 60, 62],
    'Blutwerte': ['Normal', 'Erhöht', 'Normal']
}

# DataFrame erstellen
df = pd.DataFrame(data)

# Eingabefeld für das Datum des letzten Menstruationszyklus
last_period_date = st.date_input("Datum des letzten Menstruationszyklus:")

# Übersicht über Bauelemente, Gewicht und Blutwerte
st.header('Übersicht')
st.write('Schwangerschaftsbauelemente, Gewicht und Blutwerte')
st.write(df)


st.subheader('Mamas Tagebuch')
st.text_area('Notieren Sie ihre Erkenntnisse', value='Hier tippen')

# Container
st.sidebar.subheader('Zusätzliche Informationen')
with st.sidebar.expander("mamasjourney :ship:"):
    st.write('"Mamasjourney" ist ein digitales Schwangerschaftstagebuch für werdende Mütter. Mit dieser App können sie jederzeit auf ihre persönlichen Daten zugreifen und wichtige Informationen wie aktuelle Schwangerschaftswoche, Blutwerte und Gewicht verflogen kann. Nur die Mutter selbst hat Zugriff auf diese Daten über ihren eigenen Benutzer-Login. Sie kann ihre Informationen manuell hinzufügen. Die App erfasst die gesamten 40 Schwangerschaftswochen und bietet außerdem die Möglichkeit, Gefühle und Gedanken schriftlich festzuhalten. Zusätzlich können alle Daten zu ihren Babys, sei es Kind 1, Kind 2 usw., dokumentiert und miteinander verglichen werden..')


# Sathurnas Code

def add_bloodtests():
    st.title("Blutwerte")

    # Eingabefeld für Blutwerte 
    st.subheader("Blutwerte eingeben")

    # Button zum Speichern der Blutwerte 
    if st.button("Blutwerte eingeben"):
        # Code, um Blutwerte einzugeben
        pass

    # Button zum Speichern der Blutwerte
    if st.button("Blutwerte speichern"):
        # Hier könntest du den Code einfügen, der die eingegebenen Blutwerte speichert
        st.success("Blutwerte gespeichert!")

def add_weight():
    st.title("Gewicht")
    
    # Eingabefeld für Gewicht 
    st.subheader("Gewicht eingeben")

    # Button zum Speichern der Gewichte
    if st.button("Gewicht eingeben"):
        pass

    # Button zum Speichern der Gewichte
    if st.button("Gewicht speichern"):
        st.success("Gewicht gespeichert!")
def main():
    add_bloodtests()
    add_weight()


if __name__ == "__main__":
    main()

# Titel


# Titel
def main():
    st.title("Notizen")

# Eingabefeld für Notizen
st.subheader("Notizen eingeben")
notes = st.text_area("Notizen eingeben")

# Button zum Speichern der Notizen
if st.button("Notizen speichern"):
    # Hier könntest du den Code einfügen, der die eingegebenen Notizen speichert
    st.success("Notizen gespeichert!")