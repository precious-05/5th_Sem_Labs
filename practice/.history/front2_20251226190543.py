import streamlit as st 
import requests  # backend ko HTTP request bhejne ke liye


BACKEND_URL = "http://localhost:8000"
# This is backend address bcz backend ko ye nhi pta k Frontend ko yahin pata hota hai backend kahan hai

st.title("MediNomix Connection Test")


if st.button("Test Backend Connection"):
    # User button click kare → andar ka code chale
    response = requests.get(f"{BACKEND_URL}/health")
    # Frontend keh raha: “Backend, mujhe /health ka jawab do”
    # Ye backend ke is code se connect hota hai:
    # @app.get("/health")

    if response.status_code == 200:
        data = response.json()
        # Backend ka JSON data frontend ne receive kar liya
        st.success("Backend Connected Successfully")
        st.balloons()
        st.json(data)
        #Same data UI par show ho gaya
        
    else:
        st.error("Backend Connection Failed")    

