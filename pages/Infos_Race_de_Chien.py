import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Race de Chien", layout="centered")
st.title("🐶 Informations sur une race de chien")

race = st.text_input("Entrez le nom de la race (ex : ariegeois) :").lower().strip()

if race:
    url = f"https://www.woopets.fr/chien/races/{race}/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        info = {}
        labels = soup.select("div.race-details .race-details__label")
        values = soup.select("div.race-details .race-details__value")

        for label, value in zip(labels, values):
            info[label.get_text(strip=True)] = value.get_text(strip=True)

        st.subheader(f"✨ Détails pour **{race.capitalize()}**")
        for key, val in info.items():
            st.write(f"**{key}** : {val}")
    else:
        st.error(f"Impossible de trouver des données pour '{race}'. Vérifiez le nom.")
else:
    st.info("Veuillez entrer une race pour afficher les informations.")
