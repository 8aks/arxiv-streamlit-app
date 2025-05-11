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

            # Extract the breed description from paragraphs
            description = soup.find('div', class_='race-desc')
            if description:
                description_text = description.get_text(strip=True)
                if description_text:
                    st.subheader(f"✨ Détails pour **{race.capitalize()}**")
                    st.write(f"- {description_text}")

            # Extract price and maintenance cost if present
            price_section = soup.find('div', class_='price')
            if price_section:
                price_text = price_section.get_text(strip=True)
                st.write(f"- **Prix d'achat**: {price_text}")

            # Extract breed image
            image = soup.select_one('div.race-img img')
            if image and image.get('src'):
                info["Image"] = f"https://www.woopets.fr{image['src']}"
                st.image(info["Image"], caption=f"Image de {race.capitalize()}", width=300)

            # Extract similar breeds if present
            similar_breeds_section = soup.find('div', class_='similar-breeds')
            if similar_breeds_section:
                similar_breeds = similar_breeds_section.get_text(strip=True)
                st.write(f"- **Races similaires**: {similar_breeds}")

            break

    if not page_found:
        st.error(f"❌ Impossible de trouver une page pour '{race}'. Vérifiez le nom.")
else:
    st.info("Veuillez entrer une race pour afficher les informations.")
