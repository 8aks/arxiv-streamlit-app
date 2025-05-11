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
            labels = soup.select("div.race-details .race-details__label")
            values = soup.select("div.race-details .race-details__value")

            if labels and values:
                st.subheader(f"✨ Détails pour **{race.capitalize()}**")
                for label, value in zip(labels, values):
                    st.write(f"**{label.get_text(strip=True)}** : {value.get_text(strip=True)}")
            else:
                st.warning("Page trouvée, mais les détails sont introuvables.")
            break

    if not page_found:
        st.error(f"❌ Impossible de trouver une page pour '{race}'. Vérifiez le nom.")
else:
    st.info("Veuillez entrer une race pour afficher les informations.")
