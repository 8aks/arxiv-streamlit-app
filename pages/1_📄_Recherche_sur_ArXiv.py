import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Recherche ArXiv", layout="wide")
st.title("🔍 Recherche d'articles sur ArXiv")

query = st.text_input("Entrez un mot-clé de recherche :", "")

if query:
    formatted_query = query.replace(" ", "+")
    url = f"https://arxiv.org/search/?query={formatted_query}&searchtype=all&abstracts=show&order=-announced_date_first&size=100"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("li", class_="arxiv-result")

        data = []
        for result in results:
            title = result.find("p", class_="title").get_text(strip=True)
            abstract = result.find("span", class_="abstract-full").get_text(strip=True).replace("Abstract: ", "")
            authors = result.find("p", class_="authors").get_text(strip=True).replace("Authors:", "")
            date = result.find("p", class_="is-size-7").get_text(strip=True).split(";")[0].replace("Submitted ", "")

            data.append({
                "Titre": title,
                "Auteurs": authors,
                "Date": date,
                "Résumé": abstract
            })

        if data:
            df = pd.DataFrame(data)
            st.success(f"✅ {len(df)} résultats trouvés pour '{query}'")
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Télécharger les résultats au format CSV", csv, "resultats_arxiv.csv", "text/csv")
        else:
            st.warning("Aucun résultat trouvé.")

    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
else:
    st.info("Veuillez entrer un terme de recherche ci-dessus.")
