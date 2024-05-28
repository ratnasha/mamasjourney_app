import streamlit as st

st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide")

st.markdown("""
    <h1 style="display: flex; align-items: center;">
        Weiterführende Links
        <img src="https://github.com/ratnasha/mamasjourney_app/blob/main/Bilder/Schiff.jpg?raw=true" alt="ship" style="height: 1em; margin-left: 10px;">
    </h1>
    """, unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Allgemein","Ernährung", "Rechtsschutz", "Entwicklung", "Beschwerden"])

with tab1:
   st.header("Allgemeine Informationen")
   st.link_button("Swissmom", "https://www.swissmom.ch")
   st.link_button("Elternbildung", "https://www.elternbildung.ch")
   st.link_button("Kinderspital Zürich", "https://kispi.uzh.ch") 
   
with tab2:
   st.header("Ernährungsberatung")
   st.link_button("Ernährungsguide BLV","https://www.blv.admin.ch/blv/de/home/lebensmittel-und-ernaehrung/ernaehrung/empfehlungen-informationen/lebensphasen-und-ernaehrungsformen/schwangere-und-stillende.html")
   st.link_button("Ernährungsguide DGE", "https://www.dge.de/gesunde-ernaehrung/gezielte-ernaehrung/ernaehrung-in-schwangerschaft-und-stillzeit/handlungsempfehlungen-ernaehrung-in-der-schwangerschaft/")
   
with tab3:
   st.header("Mutterschutz")
   st.link_button("Mutterschutz Schweiz","https://www.seco.admin.ch/seco/de/home/Arbeit/Arbeitsbedingungen/faq_arbeitsbedingungen/faq_mutterschutz.html")

with tab4:
   st.header("Entwicklung in der Schwangerschaft")
   st.link_button("Pampers Schwangerschaftskalender", "https://www.pampers.ch/de-ch/schwangerschaft/schwangerschaftskalender")

with tab5:
   st.header("Beschwerden in der Schwangerschaft")
   st.link_button("9monate.de", "https://www.9monate.de/schwangerschaft-geburt/beschwerden-erkrankungen/")

