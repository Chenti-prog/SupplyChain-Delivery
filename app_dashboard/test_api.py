import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

st.title("API Health Test")

try:
    resp = requests.get(f"{API_BASE_URL}/health", timeout=5)
    st.write("Status code:", resp.status_code)
    st.write("Response JSON:", resp.json())
except Exception as e:
    st.error(f"Error calling API: {e}")
