import streamlit as st

st.title("Links")

# Einfügen des Swissmom-Links
link = '[Besuche Swissmom](https://www.swissmom.ch)'
st.markdown(link, unsafe_allow_html=True)

st.write("Dies ist eine einfache Streamlit-App mit einem Link zu Swissmom.")

