"""
MediNomix - Advanced Medication Safety Platform
SIMPLE VERSION WITH USER GUIDE
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import threading
import websocket
import time

# Page configuration
st.set_page_config(
    page_title="MediNomix | Medication Safety",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/dashboard"

# Initialize session state
if 'user_onboarding_complete' not in st.session_state:
    st.session_state.user_onboarding_complete = False
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'dashboard_data' not in st.session_state:
    st.session_state.dashboard_data = {}
if 'selected_risk' not in st.session_state:
    st.session_state.selected_risk = "all"
if 'realtime_metrics' not in st.session_state:
    st.session_state.realtime_metrics = {}
if 'websocket_connected' not in st.session_state:
    st.session_state.websocket_connected = False

# ================================
# USER GUIDE SECTION
# ================================

def show_user_guide():
    """Show step-by-step user guide"""
    
    st.markdown("## 🚀 Welcome to MediNomix!")
    st.markdown("### A Step-by-Step Guide to Get Started")
    
    guide_cols = st.columns(3)
    
    with guide_cols[0]:
        st.markdown("""
        ### **Step 1: Setup**
        📊 **Load Sample Database**
        
        Click the button below to load sample medications into the system.
        
        This will add common drugs like:
        • Metformin (Diabetes)
        • Lamictal (Epilepsy)
        • Celebrex (Arthritis)
        """)
        
        if st.button("📥 **Load Sample Database**", 
                     type="primary",
                     use_container_width=True,
                     key="guide_load_db"):
            with st.spinner("Loading sample medications..."):
                if seed_database():
                    st.session_state.user_onboarding_complete = True
                    st.success("✅ Database loaded! Now proceed to Step 2")
                    st.rerun()
    
    with guide_cols[1]:
        st.markdown("""
        ### **Step 2: Try a Search**
        🔍 **Search for a Medication**
        
        After loading database, try searching for:
        
        **Examples to try:**
        • `metformin` (diabetes medication)
        • `lamictal` (epilepsy medication)
        • `celebrex` (arthritis medication)
        
        The system will show similar drugs and confusion risks.
        """)
        
        if st.button("🔍 **Try: Search 'metformin'**",
                     disabled=not st.session_state.user_onboarding_complete,
                     use_container_width=True,
                     key="guide_example"):
            if st.session_state.user_onboarding_complete:
                with st.spinner("Analyzing Metformin..."):
                    result = search_drug("metformin")
                    if result:
                        st.session_state.search_results = result.get('similar_drugs', [])
                        st.success(f"✅ Found {len(st.session_state.search_results)} similar drugs!")
                        st.rerun()
            else:
                st.warning("Please complete Step 1 first")
    
    with guide_cols[2]:
        st.markdown("""
        ### **Step 3: Explore Analytics**
        📈 **View Dashboard & Analytics**
        
        After searching, explore:
        
        • **Drug Confusion Heatmap**
        • **Risk Distribution Charts**
        • **Real-time Analytics**
        • **FDA Alert Pairs**
        
        Use the tabs above to navigate.
        """)
        
        if st.button("📊 **View Analytics Dashboard**",
                     disabled=not st.session_state.user_onboarding_complete,
                     use_container_width=True,
                     key="guide_analytics"):
            if st.session_state.user_onboarding_complete:
                load_dashboard_data()
                st.success("✅ Analytics loaded! Switch to 'Analytics Dashboard' tab")
                st.rerun()
            else:
                st.warning("Please complete Step 1 first")
    
    st.divider()
    
    # Quick Tips Section
    st.markdown("### 💡 Quick Tips")
    
    tip_cols = st.columns(4)
    
    with tip_cols[0]:
        st.info("""
        **Search Tips:**
        • Use generic names
        • Try brand names
        • Partial names work too
        """)
    
    with tip_cols[1]:
        st.info("""
        **Risk Colors:**
        • 🔴 Critical: ≥75%
        • 🟠 High: 50-74%
        • 🟡 Medium: 25-49%
        • 🟢 Low: <25%
        """)
    
    with tip_cols[2]:
        st.info("""
        **Common Errors:**
        • Lamictal ↔ Lamisil
        • Celebrex ↔ Celexa
        • Metformin ↔ Metronidazole
        """)
    
    with tip_cols[3]:
        st.info("""
        **Need Help?**
        1. Load database first
        2. Try example searches
        3. Check analytics
        """)

# ================================
# HELPER FUNCTIONS
# ================================

def check_backend_connection():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data
        return False, {}
    except:
        return False, {}

def search_drug(drug_name):
    """Search for drug and analyze confusion risks"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/search/{drug_name}", timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Search error: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"❌ Cannot connect to backend server")
        return None

def seed_database():
    """Seed database with common drugs"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/seed-database", timeout=10)
        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ Success! Added {data.get('drugs_added', 0)} medications to database.")
            return True
        else:
            st.error(f"Failed: {response.text}")
            return False
    except Exception as e:
        st.error(f"""
        ❌ **Backend Connection Failed**
        
        **To fix this:**
        1. Open a new terminal
        2. Navigate to your project folder
        3. Run: `python backend.py`
        4. Wait for "Server started" message
        5. Refresh this page
        """)
        return False

def load_dashboard_data():
    """Load ALL dashboard data"""
    try:
        # Check connection first
        connected, health_data = check_backend_connection()
        if not connected:
            st.warning("⚠️ Backend not connected. Please start backend server first.")
            return
        
        # Load metrics
        metrics_response = requests.get(f"{BACKEND_URL}/api/metrics", timeout=10)
        if metrics_response.status_code == 200:
            st.session_state.dashboard_data['metrics'] = metrics_response.json()
            st.session_state.dashboard_data['last_update'] = datetime.now().strftime("%H:%M:%S")
        
        # Load top risks
        risks_response = requests.get(f"{BACKEND_URL}/api/top-risks?limit=10", timeout=10)
        if risks_response.status_code == 200:
            st.session_state.dashboard_data['top_risks'] = risks_response.json()
        
        # Load risk breakdown
        breakdown_response = requests.get(f"{BACKEND_URL}/api/risk-breakdown", timeout=10)
        if breakdown_response.status_code == 200:
            st.session_state.dashboard_data['breakdown'] = breakdown_response.json()
        
        # Load heatmap data
        heatmap_response = requests.get(f"{BACKEND_URL}/api/heatmap?limit=15", timeout=10)
        if heatmap_response.status_code == 200:
            st.session_state.dashboard_data['heatmap'] = heatmap_response.json()
            
        st.success("✅ Dashboard data loaded successfully!")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

def create_heatmap_chart():
    """Create drug confusion heatmap"""
    if 'heatmap' not in st.session_state.dashboard_data:
        return None
    
    heatmap_data = st.session_state.dashboard_data['heatmap']
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, "#10B981"],    # Green
            [0.25, "#F59E0B"], # Yellow
            [0.5, "#ff9a00"],  # Orange
            [0.75, "#EF4444"], # Red
            [1, "#b5179e"]     # Purple
        ],
        zmin=0,
        zmax=100,
        hoverongaps=False,
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>Risk Score: %{z:.1f}%<extra></extra>",
    ))
    
    fig.update_layout(
        title="Drug Confusion Risk Heatmap",
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        height=500,
        xaxis=dict(tickangle=45),
    )
    
    return fig

def create_risk_breakdown_chart():
    """Create risk breakdown chart"""
    if 'breakdown' not in st.session_state.dashboard_data:
        return None
    
    breakdown = st.session_state.dashboard_data['breakdown']
    if not breakdown:
        return None
    
    categories = [item['category'].title() for item in breakdown]
    counts = [item['count'] for item in breakdown]
    
    color_map = {
        "Critical": "#b5179e",
        "High": "#EF4444",
        "Medium": "#F59E0B",
        "Low": "#10B981"
    }
    colors = [color_map.get(cat, "#F59E0B") for cat in categories]
    
    fig = px.pie(
        values=counts, 
        names=categories, 
        color=categories,
        color_discrete_map=color_map,
        hole=0.5
    )
    
    fig.update_layout(
        title="Risk Level Distribution",
        height=400,
        showlegend=True,
    )
    
    return fig

def create_top_risks_chart():
    """Create top risks chart"""
    if 'top_risks' not in st.session_state.dashboard_data:
        return None
    
    top_risks = st.session_state.dashboard_data['top_risks']
    if not top_risks:
        return None
    
    pairs = [f"{item['drug1']} ↔ {item['drug2']}" for item in top_risks]
    scores = [item['risk_score'] for item in top_risks]
    categories = [item['risk_category'] for item in top_risks]
    
    color_map = {
        "critical": "#b5179e",
        "high": "#EF4444",
        "medium": "#F59E0B",
        "low": "#10B981"
    }
    colors = [color_map.get(cat.lower(), "#F59E0B") for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color=colors,
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Risk Score: %{x:.1f}%<extra></extra>",
        )
    ])
    
    fig.update_layout(
        title="Top 10 High-Risk Drug Pairs",
        xaxis_title="Risk Score (%)",
        yaxis_title="",
        height=500,
        xaxis=dict(range=[0, 105]),
        yaxis=dict(categoryorder='total ascending')
    )
    
    return fig

# ================================
# MAIN APPLICATION
# ================================

# Title
st.title("💊 MediNomix - Medication Safety Platform")
st.markdown("AI-powered system to prevent medication confusion errors")

# Check backend connection
connected, health_data = check_backend_connection()

if not connected:
    st.error("""
    ## ⚠️ Backend Server Not Running
    
    **To start the application:**
    
    1. **Open a new terminal/command prompt**
    2. **Navigate to your project folder**
    3. **Run this command:**
    ```
    python backend.py
    ```
    4. **Wait for the message:** `Server started on http://localhost:8000`
    5. **Refresh this page**
    
    *If you don't have backend.py, please check your project files.*
    """)
    st.stop()

# Show user guide if not completed
if not st.session_state.user_onboarding_complete:
    show_user_guide()
    st.stop()

# Main interface for users who completed onboarding
st.success(f"✅ Connected to backend | Drugs in database: {health_data.get('drugs_in_database', 0)}")

# Quick Actions
st.markdown("### Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 **Refresh All Data**", 
                 use_container_width=True,
                 help="Reload all dashboard data and analytics"):
        with st.spinner("Refreshing..."):
            load_dashboard_data()
            st.rerun()

with col2:
    if st.button("➕ **Add More Drugs**", 
                 use_container_width=True,
                 help="Add additional sample medications to database"):
        with st.spinner("Adding more medications..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()

with col3:
    if st.button("📋 **View Database Info**",
                 use_container_width=True,
                 help="Check current database status"):
        connected, data = check_backend_connection()
        if connected:
            st.info(f"""
            **Database Status:**
            • Total Drugs: {data.get('drugs_in_database', 0)}
            • Risk Assessments: {data.get('risk_assessments', 0)}
            • Status: {data.get('status', 'Unknown')}
            • Last Updated: {st.session_state.dashboard_data.get('last_update', 'Never')}
            """)

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Drug Search", "📊 Analytics", "⚡ Live Dashboard", "📖 Guide"])

# TAB 1: DRUG SEARCH
with tab1:
    st.header("Search Medication Confusion Risks")
    
    # Search section
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        drug_name = st.text_input(
            "Enter medication name:",
            placeholder="e.g., metformin, lamictal, celebrex...",
            help="Enter brand or generic name of medication"
        )
    
    with search_col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        search_clicked = st.button("🔍 **Analyze**", use_container_width=True)
    
    # Quick search buttons
    st.markdown("**Quick examples:**")
    example_cols = st.columns(5)
    examples = ["metformin", "lamictal", "celebrex", "clonidine", "zyprexa"]
    
    for col, example in zip(example_cols, examples):
        with col:
            if st.button(f"**{example}**", use_container_width=True):
                drug_name = example
                search_clicked = True
    
    if search_clicked and drug_name:
        with st.spinner(f"Analyzing '{drug_name}' for confusion risks..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"✅ Found {len(st.session_state.search_results)} potentially confusing medications")
                st.rerun()
    
    # Display results
    if st.session_state.search_results:
        st.divider()
        st.subheader(f"Analysis Results: {len(st.session_state.search_results)} Similar Drugs Found")
        
        # Risk filter
        risk_levels = ["All", "Critical (≥75%)", "High (50-74%)", "Medium (25-49%)", "Low (<25%)"]
        selected_risk = st.radio("Filter by risk level:", risk_levels, horizontal=True)
        
        # Map selection
        risk_map = {
            "All": "all",
            "Critical (≥75%)": "critical",
            "High (50-74%)": "high",
            "Medium (25-49%)": "medium",
            "Low (<25%)": "low"
        }
        
        filtered_risk = risk_map[selected_risk]
        
        # Filter results
        if filtered_risk == "all":
            filtered_results = st.session_state.search_results
        else:
            filtered_results = [
                r for r in st.session_state.search_results 
                if r['risk_category'] == filtered_risk
            ]
        
        st.info(f"Showing {len(filtered_results)} results ({selected_risk})")
        
        # Display each result
        for result in filtered_results:
            risk_color = {
                "critical": "#b5179e",
                "high": "#EF4444", 
                "medium": "#F59E0B",
                "low": "#10B981"
            }.get(result['risk_category'], "#F59E0B")
            
            with st.container():
                st.markdown(f"""
                <div style='padding: 15px; border-left: 5px solid {risk_color}; 
                     background-color: #f8f9fa; border-radius: 5px; margin: 10px 0;'>
                    <h4 style='margin: 0;'>{result['target_drug']['brand_name']} 
                    <span style='color: {risk_color}; font-size: 0.9em;'>
                    ({result['risk_category'].upper()} - {result['combined_risk']:.0f}%)
                    </span></h4>
                    <p style='margin: 5px 0; color: #666;'>
                    Generic: {result['target_drug'].get('generic_name', 'N/A')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics in columns
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Spelling", f"{result['spelling_similarity']:.1f}%")
                with m2:
                    st.metric("Pronunciation", f"{result['phonetic_similarity']:.1f}%")
                with m3:
                    st.metric("Context", f"{result['therapeutic_context_risk']:.1f}%")
                with m4:
                    st.metric("Overall Risk", f"{result['combined_risk']:.1f}%")
                
                st.divider()

# TAB 2: ANALYTICS
with tab2:
    st.header("Analytics Dashboard")
    
    # Load data button
    if 'metrics' not in st.session_state.dashboard_data or not st.session_state.dashboard_data.get('metrics'):
        st.info("📊 **Analytics data not loaded yet.** Click below to load dashboard data.")
        if st.button("📥 **Load Analytics Data**", type="primary"):
            load_dashboard_data()
            st.rerun()
    else:
        metrics = st.session_state.dashboard_data['metrics']
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Drugs", metrics.get('total_drugs', 0))
        with col2:
            st.metric("Critical Pairs", metrics.get('critical_risk_pairs', 0))
        with col3:
            st.metric("High Pairs", metrics.get('high_risk_pairs', 0))
        with col4:
            st.metric("Avg Risk", f"{metrics.get('avg_risk_score', 0):.1f}%")
        
        st.divider()
        
        # Heatmap
        st.subheader("Drug Confusion Heatmap")
        heatmap_chart = create_heatmap_chart()
        if heatmap_chart:
            st.plotly_chart(heatmap_chart, use_container_width=True)
        else:
            st.info("No heatmap data available. Try searching for drugs first.")
        
        st.divider()
        
        # Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("Risk Distribution")
            breakdown_chart = create_risk_breakdown_chart()
            if breakdown_chart:
                st.plotly_chart(breakdown_chart, use_container_width=True)
        
        with chart_col2:
            st.subheader("Top Risk Pairs")
            risks_chart = create_top_risks_chart()
            if risks_chart:
                st.plotly_chart(risks_chart, use_container_width=True)
        
        st.divider()
        
        # FDA Alerts
        st.subheader("⚠️ FDA High Alert Drug Pairs")
        
        alert_data = pd.DataFrame([
            {"Drug Pair": "Lamictal ↔ Lamisil", "Risk": "Critical", "Issue": "Spelling similarity", "Medical Impact": "Epilepsy vs Fungal infection"},
            {"Drug Pair": "Celebrex ↔ Celexa", "Risk": "Critical", "Issue": "Spelling similarity", "Medical Impact": "Arthritis vs Depression"},
            {"Drug Pair": "Metformin ↔ Metronidazole", "Risk": "High", "Issue": "Spelling similarity", "Medical Impact": "Diabetes vs Antibiotic"},
            {"Drug Pair": "Clonidine ↔ Klonopin", "Risk": "High", "Issue": "Sound-alike", "Medical Impact": "Blood pressure vs Anxiety"},
            {"Drug Pair": "Zyprexa ↔ Zyrtec", "Risk": "Medium", "Issue": "Spelling similarity", "Medical Impact": "Antipsychotic vs Allergy"},
        ])
        
        st.dataframe(alert_data, use_container_width=True, hide_index=True)

# TAB 3: LIVE DASHBOARD
with tab3:
    st.header("Live Dashboard")
    
    st.info("""
    **Real-time Features:**
    • Live search monitoring
    • Real-time risk updates
    • System health tracking
    """)
    
    # Simple metrics display
    connected, health_data = check_backend_connection()
    
    if connected:
        st.success(f"✅ Backend Connected | Drugs: {health_data.get('drugs_in_database', 0)}")
        
        # Display current stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Database Status", "Healthy" if health_data.get('status') == 'healthy' else "Warning")
        with col2:
            st.metric("Total Drugs", health_data.get('drugs_in_database', 0))
        with col3:
            st.metric("Risk Assessments", health_data.get('risk_assessments', 0))
    else:
        st.warning("⚠️ Backend not connected")

# TAB 4: USER GUIDE
with tab4:
    st.header("📖 User Guide & Help")
    
    st.markdown("""
    ## How to Use MediNomix
    
    ### **Step 1: Setup**
    1. Make sure backend server is running (should show ✅ Connected)
    2. If "Drugs in database: 0" appears, click "Load Sample Database"
    3. Wait for success message
    
    ### **Step 2: Search Medications**
    • Go to **"Drug Search"** tab
    • Enter medication name (e.g., `metformin`)
    • Or click quick examples like `lamictal`, `celebrex`
    • View confusion risk analysis
    
    ### **Step 3: Analyze Results**
    • **Risk Levels:**
      - 🔴 **Critical (≥75%)**: Immediate attention needed
      - 🟠 **High (50-74%)**: Review required
      - 🟡 **Medium (25-49%)**: Monitor closely
      - 🟢 **Low (<25%)**: Low priority
    
    ### **Step 4: View Analytics**
    • Go to **"Analytics"** tab
    • See overall statistics
    • View heatmap of drug confusion
    • Check risk distribution
    
    ### **Common Issues & Solutions**
    
    **Problem: "Backend not connected"**
    ```
    Solution: Run `python backend.py` in terminal
    ```
    
    **Problem: "No drugs in database"**
    ```
    Solution: Click "Load Sample Database" button
    ```
    
    **Problem: "Search not working"**
    ```
    Solution: 
    1. Check backend is running
    2. Load sample database first
    3. Try example searches
    ```
    
    ### **Quick Reference**
    
    | Action | Button | Result |
    |--------|--------|--------|
    | First-time setup | Load Sample Database | Adds 50+ medications |
    | Test search | Quick examples | Try metformin, lamictal |
    | View stats | Analytics tab | Charts & heatmaps |
    | Check status | Sidebar | Database health |
    
    ### **Need More Help?**
    • Check that backend.py is running
    • Ensure you loaded sample database
    • Try the example searches first
    • Refresh page if issues persist
    """)

# ================================
# SIDEBAR
# ================================

with st.sidebar:
    st.title("💊 MediNomix")
    st.caption("Medication Safety System")
    
    st.divider()
    
    # Database Status
    st.subheader("Database Status")
    connected, health_data = check_backend_connection()
    
    if connected:
        status_color = "🟢" if health_data.get('status') == 'healthy' else "🟡"
        st.success(f"{status_color} **Connected**")
        
        # Display database info
        st.metric("Drugs in Database", health_data.get('drugs_in_database', 0))
        
        if health_data.get('drugs_in_database', 0) == 0:
            st.warning("⚠️ Database is empty")
            if st.button("📥 **Load Sample Data**", use_container_width=True):
                if seed_database():
                    st.rerun()
    else:
        st.error("🔴 **Not Connected**")
        st.code("Run: python backend.py", language="bash")
    
    st.divider()
    
    # Quick Actions
    st.subheader("Quick Actions")
    
    if st.button("🔄 **Refresh Status**", use_container_width=True):
        st.rerun()
    
    if st.button("📊 **Load Analytics**", use_container_width=True):
        load_dashboard_data()
        st.success("Data loaded!")
        st.rerun()
    
    if st.button("🔍 **Search Example**", use_container_width=True):
        result = search_drug("metformin")
        if result:
            st.session_state.search_results = result.get('similar_drugs', [])
            st.rerun()
    
    st.divider()
    
    # Help Section
    st.subheader("Need Help?")
    
    if st.button("📖 **Show User Guide**", use_container_width=True):
        st.session_state.user_onboarding_complete = False
        st.rerun()
    
    st.info("""
    **First time?**
    1. Load sample database
    2. Try example search
    3. View analytics
    """)

# ================================
# FOOTER
# ================================

st.divider()
st.caption(f"MediNomix v1.0 • Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')} • Backend: {'✅ Connected' if connected else '❌ Disconnected'}")