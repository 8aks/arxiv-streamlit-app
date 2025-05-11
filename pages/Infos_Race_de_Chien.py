import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Race de Chien", layout="centered")
st.title("🐶 Informations sur une race de chien")

race = st.text_input("Entrez le nom de la race (ex : ariegeois, berger allemand, bichon frisé) :").strip()

if race:
    # Nettoyer l'entrée pour l'URL
    url_friendly = race.lower().replace(" ", "-") \
        .replace("é", "e").replace("è", "e").replace("ê", "e") \
        .replace("à", "a").replace("â", "a").replace("î", "i") \
        .replace("ç", "c").replace("ô", "o").replace("ù", "u")

    url = f"https://www.woopets.fr/chien/races/{url_friendly}/"
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
        st.error(f"❌ Impossible de trouver des données pour '{race}'. Vérifiez le nom ou essayez une autre orthographe.")
else:
    st.info("Veuillez entrer une race pour afficher les informations.")
