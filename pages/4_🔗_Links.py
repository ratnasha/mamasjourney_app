import streamlit as st

st.title("Weiterführende Links :ship:")
tab1, tab2, tab3 = st.tabs(["Ernährung", "Das Recht: als Mutter", "Tipps & Tricks"])

with tab1:
   st.header("Ernährungsberatung")
   st.link_button("Ernährungsguide","https://www.blv.admin.ch/blv/de/home/lebensmittel-und-ernaehrung/ernaehrung/empfehlungen-informationen/lebensphasen-und-ernaehrungsformen/schwangere-und-stillende.html")

with tab2:
   st.header("Mutterschutz")
   st.link_button("Mutterschutz Schweiz","https://www.seco.admin.ch/seco/de/home/Arbeit/Arbeitsbedingungen/faq_arbeitsbedingungen/faq_mutterschutz.html")

with tab3:
   st.header("Tipps für werdende Mütter")
   st.link_button("Swissmom", "https://www.swissmom.ch")
   st.link_button("Pampers Schwangerschaftskalender", "https://www.pampers.ch/de-ch/schwangerschaft/schwangerschaftskalender")

