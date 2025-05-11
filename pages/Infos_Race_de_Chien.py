import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Race de Chien", layout="centered")
st.title("🐶 Informations sur une race de chien")

race = st.text_input("Entrez le nom de la race (ex : ariegeois, berger allemand, bichon frisé) :").strip()

def slugify(text):
    return text.lower().replace(" ", "-") \
        .replace("é", "e").replace("è", "e").replace("ê", "e") \
        .replace("à", "a").replace("â", "a").replace("î", "i") \
        .replace("ç", "c").replace("ô", "o").replace("ù", "u")

if race:
    slug = slugify(race)
    urls = [
        f"https://www.woopets.fr/chien/races/{slug}/",
        f"https://www.woopets.fr/chien/race/{slug}/"
    ]

    page_found = False
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            page_found = True
            soup = BeautifulSoup(response.content, "html.parser")
            info = {}

            # Tentons de récupérer d'autres informations possibles
            description = soup.select_one('div.description p')
            if description:
                info["Description"] = description.get_text(strip=True)

            # Récupération de l'image de la race
            image = soup.select_one('div.race-img img')
            if image and image.get('src'):
                info["Image"] = f"https://www.woopets.fr{image['src']}"

            # Recherche des caractéristiques
            labels = soup.select("div.race-details .race-details__label")
            values = soup.select("div.race-details .race-details__value")

            for label, value in zip(labels, values):
                info[label.get_text(strip=True)] = value.get_text(strip=True)

            if info:
                st.subheader(f"✨ Détails pour **{race.capitalize()}**")
                for key, val in info.items():
                    st.write(f"**{key}** : {val}")
            else:
                st.warning("Page trouvée, mais aucune information détaillée n'a pu être extraite.")

            break

    if not page_found:
        st.error(f"❌ Impossible de trouver une page pour '{race}'. Vérifiez le nom.")
else:
    st.info("Veuillez entrer une race pour afficher les informations.")
