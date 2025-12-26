import streamlit as st 
import requests  # backend ko HTTP request bhejne ke liye


BACKEND_URL = "http://localhost:8000"

st.title("MediNomix Connection Test")


if st.button("Test Backend Connection"):
    response = requests.get(f"{BACKEND_URL}/health")
    
    
    if response.status_code == 200:
        data = response.json()
        

