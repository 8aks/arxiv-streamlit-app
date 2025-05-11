import streamlit as st

st.set_page_config(page_title="Centre d'information", layout="centered")

st.title("📚🐶 Centre d'information")
st.write("Bienvenue ! Choisissez ce que vous souhaitez explorer :")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_📄_Recherche_sur_ArXiv.py", label="🔍 Rechercher des articles scientifiques", icon="📄")

with col2:
    st.page_link("pages/2_🐶_Infos_Race_de_Chien.py", label="🐶 Informations sur une race de chien", icon="🐶")
