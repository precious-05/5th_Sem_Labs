import streamlit as st 
import requests  # backend ko HTTP request bhejne ke liye


BACKEND_URL = "http://localhost:8000"
# This is backend address bcz backend ko ye nhi pta k Frontend ko yahin pata hota hai backend kahan hai

st.title("MediNomix Connection Test")


if st.button("Test Backend Connection"):
    # User button click kare → andar ka code chale
    response = requests.get(f"{BACKEND_URL}/health")
    
    
    if response.status_code == 200:
        data = response.json()
        st.success("Backend Connected Successfully")
        st.balloons()
        st.json(data)
        
    else:
        st.error("Backend Connection Failed")    

