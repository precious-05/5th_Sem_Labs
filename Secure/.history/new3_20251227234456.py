import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import time
import json
import threading
import websocket

# Page configuration - Clean Professional
st.set_page_config(
    page_title="MediNomix | Medication Safety",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/dashboard"

# Clean Color Scheme
COLORS = {
    "primary": "#2563EB",
    "secondary": "#7C3AED", 
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "dark": "#1F2937",
    "light": "#F8FAFC",
    "gray": "#6B7280",
}

# Initialize session state
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
# REAL-TIME WEBSOCKET MANAGER
# ================================

class RealTimeWebSocketManager:
    def __init__(self):
        self.connected = False
        self.ws = None
        
    def start_connection(self):
        try:
            self.ws = websocket.WebSocketApp(
                WS_URL,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            threading.Thread(target=self.ws.run_forever, daemon=True).start()
        except Exception as e:
            print(f"WebSocket error: {e}")
    
    def _on_open(self, ws):
        self.connected = True
        st.session_state.websocket_connected = True
    
    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            if data.get('type') in ['initial', 'update']:
                st.session_state.realtime_metrics = data.get('data', {})
        except:
            pass
    
    def _on_error(self, ws, error):
        self.connected = False
        st.session_state.websocket_connected = False
    
    def _on_close(self, ws, close_status_code, close_msg):
        self.connected = False
        st.session_state.websocket_connected = False

websocket_manager = RealTimeWebSocketManager()

# ================================
# CORE FUNCTIONS
# ================================

def search_drug(drug_name):
    """Search for drug and analyze confusion risks"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/search/{drug_name}", timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Cannot connect to backend. Make sure backend is running.")
        return None

def load_examples():
    """Load example drugs for demonstration"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/seed-database", timeout=30)
        if response.status_code == 200:
            return True
        else:
            st.error("Failed to load examples")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def load_dashboard_data():
    """Load dashboard analytics data"""
    try:
        # Load metrics
        metrics_response = requests.get(f"{BACKEND_URL}/api/metrics")
        if metrics_response.status_code == 200:
            st.session_state.dashboard_data['metrics'] = metrics_response.json()
        
        # Load top risks
        risks_response = requests.get(f"{BACKEND_URL}/api/top-risks?limit=10")
        if risks_response.status_code == 200:
            st.session_state.dashboard_data['top_risks'] = risks_response.json()
        
        # Load risk breakdown
        breakdown_response = requests.get(f"{BACKEND_URL}/api/risk-breakdown")
        if breakdown_response.status_code == 200:
            st.session_state.dashboard_data['breakdown'] = breakdown_response.json()
        
        # Load heatmap data
        heatmap_response = requests.get(f"{BACKEND_URL}/api/heatmap?limit=15")
        if heatmap_response.status_code == 200:
            st.session_state.dashboard_data['heatmap'] = heatmap_response.json()
            
        return True
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")
        return False

def create_heatmap_chart():
    """Create interactive drug confusion heatmap"""
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
        colorscale='RdYlGn_r',
        zmin=0,
        zmax=100,
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>Risk: %{z:.1f}%<extra></extra>",
    ))
    
    fig.update_layout(
        title="Drug Confusion Risk Matrix",
        height=600,
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        plot_bgcolor='white'
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
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=counts,
        hole=0.5,
        marker_colors=['#EF4444', '#F59E0B', '#10B981', '#3B82F6']
    )])
    
    fig.update_layout(
        title="Risk Distribution",
        height=400,
        showlegend=True
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
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color='#7C3AED',
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Top 10 High-Risk Drug Pairs",
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=500,
        plot_bgcolor='white'
    )
    
    return fig

# ================================
# MAIN APPLICATION
# ================================

# Header
st.title("💊 MediNomix")
st.subheader("Medication Safety Platform")

# Welcome Section
st.markdown("""
<div style='background-color: #f0f9ff; padding: 20px; border-radius: 10px; border-left: 4px solid #2563EB; margin-bottom: 30px;'>
<h4 style='margin-top: 0; color: #1e40af;'>Welcome to MediNomix</h4>
<p style='margin-bottom: 0; color: #4b5563;'>Search any medication to analyze confusion risks with similar drugs. 
First search may take 5-10 seconds as we fetch live FDA data.</p>
</div>
""", unsafe_allow_html=True)

# Quick Actions
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📚 Load Examples", use_container_width=True, type="secondary"):
        with st.spinner("Loading example drugs..."):
            if load_examples():
                load_dashboard_data()
                st.success("Examples loaded! Try searching: lamictal, celebrex, metformin")
                st.rerun()

with col2:
    if st.button(" Try Lamictal", use_container_width=True, type="primary"):
        with st.spinner("Analyzing Lamictal..."):
            result = search_drug("lamictal")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()

with col3:
    if st.button("Refresh Dashboard", use_container_width=True, type="secondary"):
        with st.spinner("Refreshing data..."):
            load_dashboard_data()
            st.rerun()

st.divider()

# ================================
# MAIN TABS
# ================================

tab1, tab2, tab3 = st.tabs([
    "Drug Analysis", 
    "Analytics Dashboard",
    "Real-Time Dashboard"
])

# TAB 1: DRUG ANALYSIS
with tab1:
    st.header("Drug Confusion Risk Analysis")
    
    # Search Section
    col1, col2 = st.columns([3, 1])
    with col1:
        drug_name = st.text_input(
            "Enter drug name:",
            placeholder="e.g., metformin, lamictal, celebrex...",
            key="search_input"
        )
    with col2:
        st.write("")
        st.write("")
        search_clicked = st.button("Analyze Drug", use_container_width=True, type="primary")
    
    if search_clicked and drug_name:
        with st.spinner(f"Analyzing '{drug_name}'..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.")
                st.rerun()
    
    # Results Section
    if st.session_state.search_results:
        st.divider()
        st.subheader("Analysis Results")
        
        # Risk Filters
        risk_filters = st.radio(
            "Filter by risk level:",
            ["All Risks", "Critical (≥75%)", "High (50-74%)", "Medium (25-49%)", "Low (<25%)"],
            horizontal=True
        )
        
        # Filter results
        if risk_filters == "All Risks":
            filtered_results = st.session_state.search_results
        else:
            risk_map = {
                "Critical (≥75%)": "critical",
                "High (50-74%)": "high",
                "Medium (25-49%)": "medium",
                "Low (<25%)": "low"
            }
            risk_level = risk_map[risk_filters]
            filtered_results = [
                r for r in st.session_state.search_results 
                if r['risk_category'] == risk_level
            ]
        
        # Display Results
        for result in filtered_results:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{result['target_drug']['brand_name']}**")
                    if result['target_drug']['generic_name']:
                        st.caption(f"Generic: {result['target_drug']['generic_name']}")
                with col2:
                    risk_color = {
                        "critical": "#EF4444",
                        "high": "#F59E0B",
                        "medium": "#3B82F6",
                        "low": "#10B981"
                    }.get(result['risk_category'], "#6B7280")
                    
                    st.markdown(f"""
                    <div style='text-align: center;'>
                        <div style='font-size: 24px; font-weight: bold; color: {risk_color};'>
                            {result['combined_risk']:.0f}%
                        </div>
                        <div style='color: {risk_color}; font-weight: 500;'>
                            {result['risk_category'].upper()}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Metrics
                cols = st.columns(4)
                metrics = [
                    ("Spelling", f"{result['spelling_similarity']:.1f}%"),
                    ("Phonetic", f"{result['phonetic_similarity']:.1f}%"),
                    ("Context", f"{result['therapeutic_context_risk']:.1f}%"),
                    ("Overall", f"{result['combined_risk']:.1f}%")
                ]
                
                for col, (label, value) in zip(cols, metrics):
                    with col:
                        st.metric(label, value)
                
                st.divider()

# TAB 2: ANALYTICS DASHBOARD
with tab2:
    st.header("Medication Safety Analytics")
    
    # Load data if needed
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Metrics Cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Drugs", metrics.get('total_drugs', 0))
        with col2:
            st.metric("Critical Pairs", metrics.get('critical_risk_pairs', 0))
        with col3:
            st.metric("High Risk Pairs", metrics.get('high_risk_pairs', 0))
        with col4:
            st.metric("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available")
    
    with col2:
        st.subheader("Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available")
    
    # Heatmap
    st.divider()
    st.subheader("Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.caption("Green = Low risk, Yellow = Medium risk, Red = High risk")
    else:
        st.info("No heatmap data available. Search for drugs first.")
    
    # FDA Alert Table
    st.divider()
    st.subheader("FDA High Alert Drug Pairs")
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk": "Critical", "Reason": "Epilepsy vs Fungal"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk": "Critical", "Reason": "Arthritis vs Depression"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk": "High", "Reason": "Diabetes vs Antibiotic"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk": "High", "Reason": "BP vs Anxiety"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk": "Medium", "Reason": "Antipsychotic vs Allergy"},
    ])
    
    st.dataframe(risky_pairs, use_container_width=True, hide_index=True)

# TAB 3: REAL-TIME DASHBOARD
with tab3:
    st.header("Real-Time Dashboard")
    
    # Connection status
    if st.session_state.websocket_connected:
        st.success("✅ Real-time connection active")
    else:
        st.info("Real-time dashboard - connect to see live updates")
    
    # Auto-start WebSocket
    if not st.session_state.websocket_connected:
        websocket_manager.start_connection()
    
    # Display metrics
    metrics = st.session_state.realtime_metrics or {}
    
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Drugs", metrics.get('total_drugs', 0))
        with col2:
            st.metric("Critical Pairs", metrics.get('critical_risk_pairs', 0))
        with col3:
            st.metric("Avg Risk", f"{metrics.get('avg_risk_score', 0):.1f}%")
        with col4:
            st.metric("Connected", metrics.get('connected_clients', 0))
        
        # Recent activity
        if metrics.get('recent_searches'):
            st.subheader("Recent Activity")
            for search in metrics['recent_searches'][:5]:
                with st.container():
                    st.write(f"**{search.get('drug_name', 'Unknown')}** - Found {search.get('similar_drugs_found', 0)} similar drugs")
    else:
        st.info("Waiting for real-time data...")

# ================================
# SIDEBAR
# ================================

with st.sidebar:
    st.title("MediNomix")
    st.caption("Medication Safety Platform")
    
    st.divider()
    
    st.subheader("Quick Examples")
    example_col1, example_col2 = st.columns(2)
    with example_col1:
        if st.button("Lamictal", use_container_width=True):
            with st.spinner("Loading..."):
                result = search_drug("lamictal")
                if result:
                    st.session_state.search_results = result.get('similar_drugs', [])
                    st.rerun()
    
    with example_col2:
        if st.button("Metformin", use_container_width=True):
            with st.spinner("Loading..."):
                result = search_drug("metformin")
                if result:
                    st.session_state.search_results = result.get('similar_drugs', [])
                    st.rerun()
    
    st.divider()
    
    st.subheader("System Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.success("✅ Backend Connected")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Drugs", data.get('metrics', {}).get('drugs_in_database', 0))
                with col2:
                    st.metric("Analyses", data.get('metrics', {}).get('total_analyses', 0))
            else:
                st.warning("⚠️ Backend Issues")
        else:
            st.error("❌ Cannot Connect")
    except:
        st.error("🔌 Backend Not Running")
        st.code("python backend.py", language="bash")
    
    st.divider()
    
    st.subheader("Risk Categories")
    risk_info = [
        ("Critical", "≥75%", "Immediate attention required"),
        ("High", "50-74%", "Review and verify"),
        ("Medium", "25-49%", "Monitor closely"),
        ("Low", "<25%", "Low priority"),
    ]
    
    for name, score, desc in risk_info:
        with st.expander(f"{name} ({score})"):
            st.caption(desc)

# Auto-start WebSocket
if not st.session_state.get('websocket_started', False):
    websocket_manager.start_connection()
    st.session_state.websocket_started = True