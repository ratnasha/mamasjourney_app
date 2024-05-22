import streamlit as st
import pandas as pd

# Liste der Fruchtgrößen
fruchtgroessen = [
    ("4 Wochen", "Mohnsamen"),
    ("5 Wochen", "Sesamsamen"),
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

# Titel der Seite
st.title("Baby-Timeline: Fruchtgrössen")

# Tabelle mit Streamlit DataFrame
df = pd.DataFrame(fruchtgroessen, columns=["Schwangerschaftswoche", "Fruchtgröße"])
st.dataframe(df)
# Link zu einer externen Ressource
st.write("Weitere Informationen finden Sie auf [babycenter.com](https://www.babycenter.com/pregnancy-week-by-week).")
