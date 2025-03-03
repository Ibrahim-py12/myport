
import streamlit as st
import matplotlib as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


url = st.text_input("Enter the URL ")
if url:
    responce = requests.get(url)
    st.write(responce.status_code)
    soup =BeautifulSoup(responce.text,'html.parser')
    data = []

    for h2 in soup.find_all("h2"):
        # Find the closest <p> tag that follows the <h2>
        p = h2.find_next("p")

        if p:
            data.append({"Title": h2.text.strip(), "Content": p.text.strip()})
        else:
            data.append({"Title": h2.text.strip(), "Content": "No content available"})

    # st.write("Number of headings:", len(headings))
    # st.write("Number of contents:", len(contents))
    # # Ensure both lists have the same length
    # if len(contents) < len(headings):
    #     contents.extend(["No content available"] * (len(headings) - len(contents)))
    # elif len(contents) > len(headings):
    #     contents = contents[:len(headings)]  # Trim extra content
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Streamlit UI
    st.title("Web Scraper with Keyword Search")

    # **🔎 Search Bar**
    search_query = st.text_input("Enter keyword to search:", "")

    # **🔹 Filter Data Based on Search Query**
    if search_query:
        df = df[df.apply(lambda rows: search_query.lower() in rows["Title"].lower() or search_query.lower() in rows["Content"].lower(), axis=1)]

    # **📋 Display Filtered Results**
    if not df.empty:
        for index, row in df.iterrows():
            with st.expander(row["Title"]):
                st.write(row["Content"])
    else:
        st.write("❌ No results found for your search.")

    # **📋 Display Filtered Results**
    if not df.empty:
        for index, row in df.iterrows():
            with st.expander(row["Title"]):
                st.write(row["Content"])

        # **📊 Use Streamlit's Built-in Bar Chart**
        st.subheader("Filtered Articles Overview")
        st.bar_chart(df.set_index("Title"))  # Streamlit handles the visualization automatically
    else:
        st.write("❌ No results found for your search.")
else:  st.write("Enter URL ")

#  streamlit run webscrap.py