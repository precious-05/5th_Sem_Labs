"""
FRONTEND - Day 2 Simplified Version
Focusing on Backend Communication
"""

import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(
    page_title="MediNomix Frontend",
    page_icon="💊",
    layout="wide"
)

# Backend URL - THIS IS CRITICAL!
BACKEND_URL = "http://localhost:8000"

# Title
st.title("💊 MediNomix - Frontend-Backend Communication")
st.markdown("### Understanding how frontend talks to backend")

# ========== SECTION 1: CONNECTION TEST ==========
st.header("1️⃣ Connection Test")

# Test if backend is reachable
if st.button("Test Backend Connection"):
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ Backend is running! Status: {data['status']}")
            st.json(data)  # Show the JSON response
        else:
            st.error(f"❌ Backend returned error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to backend! Make sure it's running.")
        st.info("""
        **To fix this:**
        1. Open a new terminal
        2. Run: `python backend/day2_backend.py`
        3. Wait for "Starting MediNomix Backend..." message
        4. Then try again
        """)

# ========== SECTION 2: MAKE API CALL ==========
st.header("2️⃣ Make an API Call")

# Drug search input
drug_name = st.text_input("Enter a drug name:", "Metformin")

if st.button("Search Drug"):
    st.info(f"🔄 Sending request to: {BACKEND_URL}/api/search/{drug_name}")
    
    # Show what's happening step by step
    with st.expander("🔍 See the HTTP Request Details"):
        st.code(f"""
        # This is what Streamlit does behind the scenes:
        
        import requests
        
        # 1. Create the URL
        url = "http://localhost:8000/api/search/{drug_name}"
        
        # 2. Send GET request
        response = requests.get(url)
        
        # 3. Check response status
        print(f"Status Code: {{response.status_code}}")
        
        # 4. Parse JSON response
        data = response.json()
        """, language="python")
    
    # Make the actual API call
    try:
        with st.spinner("Calling backend API..."):
            # STEP 1: Send HTTP request
            response = requests.get(f"{BACKEND_URL}/api/search/{drug_name}")
            
            # STEP 2: Check if successful
            if response.status_code == 200:
                # STEP 3: Parse JSON response
                data = response.json()
                
                st.success(f"✅ Received response from backend!")
                
                # Display the raw JSON
                with st.expander("📦 View Raw JSON Response"):
                    st.json(data)
                
                # Display formatted results
                st.subheader("📊 Search Results")
                
                if data["similar_drugs"]:
                    for drug in data["similar_drugs"]:
                        risk_color = "🔴" if drug["risk_category"] == "high" else "🟡" if drug["risk_category"] == "medium" else "🟢"
                        
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**{drug['target_drug']['name']}**")
                        with col2:
                            st.write(f"{risk_color} {drug['risk_category'].upper()}")
                        with col3:
                            st.write(f"Score: {drug['similarity_score']}%")
                        
                        st.progress(drug['similarity_score'] / 100)
                else:
                    st.info("No similar drugs found.")
                    
            else:
                st.error(f"Backend error: {response.status_code}")
                
    except requests.exceptions.ConnectionError as e:
        st.error(f"Cannot connect to backend: {e}")
        st.info("""
        **Common issues:**
        1. Backend not running - run `python backend/day2_backend.py`
        2. Wrong port - check if backend is on port 8000
        3. CORS issue - backend must allow frontend requests
        """)

# ========== SECTION 3: UNDERSTANDING THE FLOW ==========
st.header("3️⃣ Understanding the Communication Flow")

st.markdown("""
### **Step-by-Step Communication:**

1. **User Action** → User clicks "Search Drug" button
2. **Frontend** → Streamlit captures the input value
3. **HTTP Request** → Frontend sends `GET http://localhost:8000/api/search/Metformin`
4. **Backend** → FastAPI receives the request at `/api/search/{drug_name}`
5. **Processing** → Backend searches database, calculates risks
6. **HTTP Response** → Backend sends JSON back to frontend
7. **Frontend Display** → Streamlit renders the JSON as UI components

### **Key Technologies:**
- **HTTP/HTTPS**: Protocol for data transfer
- **JSON**: Format for structured data
- **REST API**: Design pattern for endpoints
- **CORS**: Security feature allowing cross-origin requests
""")

# ========== SECTION 4: PRACTICE EXERCISE ==========
st.header("4️⃣ Practice Exercise")

exercise = st.selectbox("Choose an exercise:", [
    "Modify the backend response",
    "Add a new endpoint",
    "Handle errors gracefully",
    "Test with different drugs"
])

if exercise == "Modify the backend response":
    st.code("""
    # In backend/day2_backend.py, modify the search_drug function:
    
    # Add this to the return dictionary:
    "message": f"Found {len(similar_drugs)} potential confusion risks",
    "analysis_time": "0.5s",  # Add fake timing
    "recommendation": "Consult pharmacist"  # Add safety tip
    """, language="python")
    
elif exercise == "Add a new endpoint":
    st.code("""
    # In backend/day2_backend.py, add this function:
    
    @app.get("/api/stats")
    async def get_stats():
        return {
            "total_drugs": len(fake_drugs_db),
            "average_risk": sum(d["risk"] for d in fake_drugs_db) / len(fake_drugs_db),
            "highest_risk_drug": max(fake_drugs_db, key=lambda x: x["risk"])["name"]
        }
    
    # In frontend, add a button that calls this endpoint
    """, language="python")

# ========== SECTION 5: TROUBLESHOOTING ==========
st.header("5️⃣ Troubleshooting Guide")

issue = st.selectbox("Having issues?", [
    "Select an issue",
    "Backend not connecting",
    "CORS errors in browser",
    "JSON parsing error",
    "Slow response"
])

if issue == "Backend not connecting":
    st.markdown("""
    **Solution:**
    1. Check if backend is running: `python backend/day2_backend.py`
    2. Verify the URL: Should be `http://localhost:8000`
    3. Check port conflicts: Is another app using port 8000?
    4. Try: `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)
    """)

elif issue == "CORS errors in browser":
    st.markdown("""
    **Solution:**
    The backend MUST have CORS middleware configured:
    ```python
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Or ["http://localhost:8500"] for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```
    """)

# Footer
st.markdown("---")
st.caption("MediNomix Learning • Day 2 • Frontend-Backend Communication")