import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_arxiv(query, max_results=50):
    base_url = "https://arxiv.org/search/"
    params = {
        "query": query,
        "searchtype": "all",
        "abstracts": "show",
        "order": "-announced_date_first",
        "size": max_results
    }

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('li', class_='arxiv-result')

    papers = []
    for result in results:
        title = result.find('p', class_='title is-5 mathjax').text.strip()
        abstract = result.find('span', class_='abstract-full has-text-grey-dark mathjax').text.strip()
        authors = result.find('p', class_='authors').text.replace('Authors:', '').strip()
        date_tag = result.find('p', class_='is-size-7')
        date = date_tag.text.strip().split(';')[0].replace('Submitted ', '') if date_tag else 'N/A'

        papers.append({
            'Title': title,
            'Abstract': abstract,
            'Authors': authors,
            'Date': date
        })

    return pd.DataFrame(papers)

# Streamlit UI
st.set_page_config(page_title="ArXiv Scraper", layout="wide")

st.title("📄 ArXiv Paper Scraper")
query = st.text_input("Enter your search query", "machine learning")

if st.button("Scrape"):
    with st.spinner("Scraping arXiv... Please wait..."):
        df = scrape_arxiv(query)
        if df.empty:
            st.warning("No results found.")
        else:
            st.success(f"Found {len(df)} papers!")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "arxiv_results.csv", "text/csv")

