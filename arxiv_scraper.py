import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="ArXiv Search", layout="wide")
st.title("🔍 ArXiv Paper Search")

# Text input for custom query
query = st.text_input("Enter a search term:", "")

if query:
    # Format the query string for the URL
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
                "Title": title,
                "Authors": authors,
                "Date": date,
                "Abstract": abstract
            })

        if data:
            df = pd.DataFrame(data)
            st.success(f"✅ Found {len(df)} results for '{query}'")
            st.dataframe(df, use_container_width=True)

            # Optional: download CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download results as CSV", csv, "arxiv_results.csv", "text/csv")

        else:
            st.warning("No results found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please enter a search term above to begin.")
