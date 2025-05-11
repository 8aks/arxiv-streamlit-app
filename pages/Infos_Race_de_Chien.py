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

            # Tenter de récupérer tous les paragraphes et informations présentes sur la page
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text:
                    info["Texte extrait"] = text

            # Récupérer des informations possibles sur l'image
            image = soup.select_one('div.race-img img')
            if image and image.get('src'):
                info["Image"] = f"https://www.woopets.fr{image['src']}"

            # Recherche des autres informations dans la page
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
