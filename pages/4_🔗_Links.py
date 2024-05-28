import streamlit as st

st.title("Weiterführende Links :ship:")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Allgemein","Ernährung", "Rechtsschutz", "Entwicklung", "Beschwerden"])

with tab1:
   st.header("Allgemeine Informationen")
   st.link_button("Swissmom", "https://www.swissmom.ch")
   
with tab2:
   st.header("Ernährungsberatung")
   st.link_button("Ernährungsguide BLV","https://www.blv.admin.ch/blv/de/home/lebensmittel-und-ernaehrung/ernaehrung/empfehlungen-informationen/lebensphasen-und-ernaehrungsformen/schwangere-und-stillende.html")
   
with tab3:
   st.header("Mutterschutz")
   st.link_button("Mutterschutz Schweiz","https://www.seco.admin.ch/seco/de/home/Arbeit/Arbeitsbedingungen/faq_arbeitsbedingungen/faq_mutterschutz.html")

with tab4:
   st.header("Entwicklung in der Schwangerschaft")
   st.link_button("Pampers Schwangerschaftskalender", "https://www.pampers.ch/de-ch/schwangerschaft/schwangerschaftskalender")

with tab5:
   st.header("Beschwerden in der Schwangerschaft")
   st.link_button("9monate.de", "https://www.9monate.de/schwangerschaft-geburt/beschwerden-erkrankungen/")

