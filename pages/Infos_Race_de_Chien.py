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

            # Extraire tous les éléments texte disponibles
            all_texts = soup.find_all(text=True)

            # Afficher uniquement les textes visibles
            visible_texts = [t.strip() for t in all_texts if t.strip() and not t.parent.name in ['style', 'script']]
            if visible_texts:
                st.subheader(f"✨ Détails pour **{race.capitalize()}**")
                for text in visible_texts:
                    st.write(f"- {text}")

            # Récupérer l'image de la race
            image = soup.select_one('div.race-img img')
            if image and image.get('src'):
                info["Image"] = f"https://www.woopets.fr{image['src']}"
                st.image(info["Image"], width=300)

            break

    if not page_found:
        st.error(f"❌ Impossible de trouver une page pour '{race}'. Vérifiez le nom.")
else:
    st.info("Veuillez entrer une race pour afficher les informations.")
