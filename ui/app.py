import streamlit as st
import requests
import os
st.write("STREAMLIT KEY:", os.getenv("TAVILY_API_KEY"))

API_URL = "http://127.0.0.1:8000/research"

st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Autonomous Logistics Research Agent")

query = st.text_input("Enter research query")

if st.button("Run Research"):

    if query.strip() == "":
        st.warning("Please enter a query")
    else:
        with st.spinner("Running research pipeline..."):

            response = requests.post(
                API_URL,
                json={"query": query}
            )

            if response.status_code == 200:
                data = response.json()

                st.success("Research completed")

                st.subheader("Report")
                st.write(data["report"])

            else:
                st.error("API request failed")