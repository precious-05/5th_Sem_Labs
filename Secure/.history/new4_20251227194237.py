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
import base64

# Page configuration
st.set_page_config(
    page_title="MediNomix | AI Medication Safety",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/dashboard"

# Base64 encoded images for Streamlit compatibility
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Medical icon as base64
medical_icon_base64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFiSURBVHic1ZO9SgNBFIVPymAENbYGX8FWtPIlLCwsLCwsLCwsrCx8hdhZ2FhYCLYxP2JjZ2FhIQgTCoXodY2fDnBdb8hFcevJHO7MfHNmuW+Mf5QA1sliEbgCHoE34H2Q8yvghPwQyf3qM5FqwB1wC1wAh0AX2AVawCqwAqwB+0AfOAEegE8X5AqYagJIAFNgAlz4tJ8B58AH8AW8JnzUAyaBYRPAtJ8DXoBnYK7m1VwBq3+mhMGAwzzmz9V8HAvI23xUeRl4iQUcRcL0Yz4eC+gqAGZVvwl0FIAO0IuE9YB2ckACkAD2gP1IwL6KxyYQwVXgFNgFOjYB1Q3gEXgD3oG9mo9HQdfe8vI5h2q13n6AR2DAc6Y08CQDdMFuSbg0e2rnrJkq32ZP7Zz15vtK7s2e2jlv+v+dg8xX9d+u4lVcBSwDe5Usf6YlK8Y3B7fL9Px7dGkAAAAASUVORK5CYII="

# Premium Color Scheme with gradients
COLORS = {
    "primary_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "secondary_gradient": "linear-gradient(to right, #4776E6, #8E54E9)",
    "success_gradient": "linear-gradient(to right, #00b09b, #96c93d)",
    "warning_gradient": "linear-gradient(to right, #f7971e, #ffd200)",
    "danger_gradient": "linear-gradient(to right, #ff416c, #ff4b2b)",
    "light_gradient": "linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%)",
    "card_bg": "#ffffff",
    "sidebar_bg": "#f8f9fa",
    "text_dark": "#2d3748",
    "text_light": "#718096",
    "border": "#e2e8f0"
}

# Custom CSS for Bootstrap-like styling
st.markdown(f"""
<style>
/* Global Styles */
.stApp {{
    background-color: #f7fafc;
}}

/* Premium Card Design */
.custom-card {{
    background: {COLORS['card_bg']};
    border-radius: 15px;
    border: 1px solid {COLORS['border']};
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    padding: 25px;
    transition: all 0.3s ease;
    margin-bottom: 20px;
}}

.custom-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.12);
}}

.card-header {{
    background: {COLORS['light_gradient']};
    border-radius: 10px 10px 0 0;
    padding: 20px;
    margin: -25px -25px 25px -25px;
    border-bottom: 1px solid {COLORS['border']};
}}

/* Gradient Buttons */
.gradient-btn {{
    background: {COLORS['secondary_gradient']};
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-block;
    text-align: center;
}}

.gradient-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(71, 118, 230, 0.3);
}}

.secondary-btn {{
    background: white;
    color: {COLORS['text_dark']};
    border: 2px solid {COLORS['border']};
    padding: 10px 25px;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.secondary-btn:hover {{
    background: #f8f9fa;
    transform: translateY(-2px);
}}

/* Custom Navigation */
.custom-nav {{
    background: white;
    padding: 15px 0;
    box-shadow: 0 2px 15px rgba(0,0,0,0.05);
    margin-bottom: 30px;
    border-radius: 0 0 15px 15px;
}}

.nav-item {{
    padding: 10px 20px;
    color: {COLORS['text_light']};
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 10px;
    margin: 0 5px;
}}

.nav-item:hover {{
    color: #667eea;
    background: #f7fafc;
}}

.nav-item.active {{
    background: {COLORS['primary_gradient']};
    color: white !important;
}}

/* Stat Cards */
.stat-card {{
    background: white;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}}

.stat-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}}

.stat-icon {{
    font-size: 40px;
    margin-bottom: 15px;
    color: #667eea;
}}

.stat-number {{
    font-size: 32px;
    font-weight: 700;
    background: {COLORS['primary_gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 10px 0;
}}

.stat-label {{
    color: {COLORS['text_light']};
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* Feature Cards */
.feature-card {{
    background: white;
    border-radius: 15px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    height: 100%;
}}

.feature-card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}}

.feature-icon {{
    font-size: 50px;
    margin-bottom: 20px;
    color: #667eea;
}}

/* Risk Badges */
.risk-badge {{
    display: inline-block;
    padding: 6px 20px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.badge-critical {{
    background: {COLORS['danger_gradient']};
    color: white;
}}

.badge-high {{
    background: {COLORS['warning_gradient']};
    color: white;
}}

.badge-medium {{
    background: linear-gradient(to right, #4facfe, #00f2fe);
    color: white;
}}

.badge-low {{
    background: {COLORS['success_gradient']};
    color: white;
}}

/* Custom Loader */
.loader {{
    display: inline-block;
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

/* Hero Section */
.hero-section {{
    background: {COLORS['primary_gradient']};
    padding: 80px 0;
    border-radius: 20px;
    margin-bottom: 40px;
    color: white;
    text-align: center;
}}

.hero-title {{
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 20px;
}}

.hero-subtitle {{
    font-size: 20px;
    opacity: 0.9;
    max-width: 700px;
    margin: 0 auto 30px;
}}

/* Footer */
.custom-footer {{
    background: {COLORS['sidebar_bg']};
    padding: 30px 0;
    margin-top: 50px;
    border-radius: 15px 15px 0 0;
    text-align: center;
    color: {COLORS['text_light']};
}}

/* Metric Value Styling */
.metric-value {{
    font-size: 28px;
    font-weight: 700;
    background: {COLORS['primary_gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

/* Hover Effects for Charts */
.plotly-chart {{
    transition: all 0.3s ease;
}}

.plotly-chart:hover {{
    transform: scale(1.02);
}}

/* Custom Expander */
.custom-expander {{
    background: white;
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    margin-bottom: 10px;
    overflow: hidden;
}}

.expander-header {{
    padding: 15px 20px;
    background: #f8f9fa;
    cursor: pointer;
    font-weight: 600;
    color: {COLORS['text_dark']};
}}

.expander-content {{
    padding: 20px;
    background: white;
}}
</style>
""", unsafe_allow_html=True)

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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Home"

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
# CORE FUNCTIONS (UNCHANGED)
# ================================

def search_drug(drug_name):
    """Search for drug and analyze confusion risks"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/search/{drug_name}", timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

def load_examples():
    """Load example drugs for demonstration"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/seed-database", timeout=30)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
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
# CUSTOM NAVIGATION BAR
# ================================

def render_navigation():
    """Render custom Bootstrap-style navigation bar"""
    st.markdown("""
    <div class="custom-nav">
        <div style="display: flex; justify-content: center; align-items: center;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
    
    tabs = ["Home", "Drug Analysis", "Analytics", "Real-Time"]
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.active_tab = "Home"
            st.rerun()
    
    with col2:
        if st.button("🔍 Analysis", use_container_width=True):
            st.session_state.active_tab = "Drug Analysis"
            st.rerun()
    
    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.active_tab = "Analytics"
            st.rerun()
    
    with col4:
        if st.button("⚡ Real-Time", use_container_width=True):
            st.session_state.active_tab = "Real-Time"
            st.rerun()
    
    with col5:
        st.markdown(f"<div style='text-align: right; font-weight: 600; color: #667eea; font-size: 24px;'>💊 MediNomix</div>", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ================================
# HOMEPAGE COMPONENTS
# ================================

def render_hero_section():
    """Render hero/jumbotron section"""
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">Prevent Medication Errors with AI</h1>
        <p class="hero-subtitle">Advanced AI-powered system that analyzes drug names for potential confusion risks, helping healthcare professionals prevent medication errors and improve patient safety.</p>
        <button class="gradient-btn" onclick="window.location.href='#analysis'">Start Analysis</button>
    </div>
    """, unsafe_allow_html=True)

def render_stats_counter():
    """Render animated stats counter"""
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px;">
    """, unsafe_allow_html=True)
    
    stats = [
        {"icon": "👥", "value": "1.5M+", "label": "Patients Protected"},
        {"icon": "💰", "value": "$42B", "label": "Cost Saved"},
        {"icon": "🎯", "value": "99.8%", "label": "Accuracy Rate"},
        {"icon": "💊", "value": "50K+", "label": "Drugs Analyzed"}
    ]
    
    cols = st.columns(4)
    for idx, (col, stat) in enumerate(zip(cols, stats)):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{stat['icon']}</div>
                <div class="stat-number">{stat['value']}</div>
                <div class="stat-label">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)

def render_features_section():
    """Render how it works feature cards"""
    st.markdown("""
    <div style="margin: 40px 0;">
        <h2 style="text-align: center; margin-bottom: 30px; color: #2d3748;">How MediNomix Works</h2>
    </div>
    """, unsafe_allow_html=True)
    
    features = [
        {"icon": "🔍", "title": "Search Medication", "desc": "Enter any drug name to analyze potential confusion risks"},
        {"icon": "🧠", "title": "AI Analysis", "desc": "Our AI analyzes spelling, phonetic, and therapeutic similarities"},
        {"icon": "🛡️", "title": "Risk Prevention", "desc": "Get detailed risk assessments and prevention recommendations"}
    ]
    
    cols = st.columns(3)
    for idx, (col, feature) in enumerate(zip(cols, features)):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <h3 style="margin-bottom: 15px; color: #2d3748;">{feature['title']}</h3>
                <p style="color: #718096; line-height: 1.6;">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def render_user_guide():
    """Render user guide accordion"""
    st.markdown("""
    <div class="custom-card" style="margin: 40px 0;">
        <div class="card-header">
            <h2 style="margin: 0; color: #2d3748;">📚 User Guide & Quick Start</h2>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Step 1: Search for a Medication", expanded=True):
        st.markdown("""
        1. Navigate to the **Drug Analysis** tab
        2. Enter any medication name (brand or generic)
        3. Click **Analyze Drug** to start the AI analysis
        """)
    
    with st.expander("Step 2: Review Risk Assessment"):
        st.markdown("""
        1. View all similar drugs with confusion risks
        2. Filter by risk level (Critical, High, Medium, Low)
        3. Examine detailed similarity metrics
        """)
    
    with st.expander("Step 3: Take Preventive Action"):
        st.markdown("""
        1. Check **Analytics** tab for overall statistics
        2. Monitor **Real-Time** dashboard for live updates
        3. Use quick examples for demonstration
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_trust_section():
    """Render trust/evidence section with images"""
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <h2 style="margin: 0; color: #2d3748;">🏥 Trusted by Healthcare Professionals</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Medical images from Unsplash (placeholder URLs)
    images = [
        "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80",
        "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80"
    ]
    
    cols = st.columns(4)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div style="border-radius: 10px; overflow: hidden; height: 200px; background: url('{images[idx]}'); 
                    background-size: cover; background-position: center; margin: 10px;">
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# DRUG ANALYSIS TAB
# ================================

def render_drug_analysis_tab():
    """Render Drug Analysis tab with premium styling"""
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <h2 style="margin: 0; color: #2d3748;">🔍 Drug Confusion Risk Analysis</h2>
            <p style="margin: 10px 0 0 0; color: #718096;">Search any medication to analyze confusion risks with similar drugs</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Search Section in Card
    st.markdown("""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        drug_name = st.text_input(
            "",
            placeholder="Enter drug name (e.g., metformin, lamictal, celebrex...)",
            key="search_input",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")
        search_clicked = st.button("🔍 Analyze Drug", type="primary", use_container_width=True)
    
    with col3:
        st.write("")
        if st.button("📚 Load Examples", type="secondary", use_container_width=True):
            with st.spinner("Loading examples..."):
                if load_examples():
                    st.success("Examples loaded! Try searching: lamictal, celebrex, metformin")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("""
    <div style="margin: 20px 0;">
        <p style="color: #718096; margin-bottom: 10px;">Quick Examples:</p>
    </div>
    """, unsafe_allow_html=True)
    
    examples = ["Lamictal", "Metformin", "Celebrex", "Clonidine"]
    cols = st.columns(4)
    for idx, (col, example) in enumerate(zip(cols, examples)):
        with col:
            if st.button(f"{example}", use_container_width=True, key=f"ex_{idx}"):
                with st.spinner(f"Analyzing {example}..."):
                    result = search_drug(example)
                    if result:
                        st.session_state.search_results = result.get('similar_drugs', [])
                        st.rerun()
    
    # Handle Search
    if search_clicked and drug_name:
        with st.spinner(f"🧠 Analyzing '{drug_name}'..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"✅ Analysis complete! Found {len(st.session_state.search_results)} similar drugs.")
                st.rerun()
            else:
                st.error("❌ Could not analyze drug. Please check backend connection.")
    
    # Results Section
    if st.session_state.search_results:
        st.markdown("""
        <div style="margin-top: 30px;">
            <h3 style="color: #2d3748; margin-bottom: 20px;">📊 Analysis Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Filters
        risk_filters = st.radio(
            "Filter by risk level:",
            ["All Risks", "Critical (≥75%)", "High (50-74%)", "Medium (25-49%)", "Low (<25%)"],
            horizontal=True,
            key="risk_filter"
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
        
        # Display Results in Cards
        for result in filtered_results[:20]:  # Limit to 20 results
            risk_color_class = f"badge-{result['risk_category']}"
            
            st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <div>
                        <h3 style="margin: 0; color: #2d3748;">{result['target_drug']['brand_name']}</h3>
                        {f"<p style='margin: 5px 0 0 0; color: #718096; font-size: 14px;'>Generic: {result['target_drug']['generic_name']}</p>" if result['target_drug']['generic_name'] else ""}
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 32px; font-weight: 700; background: {COLORS['primary_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                            {result['combined_risk']:.0f}%
                        </div>
                        <span class="risk-badge {risk_color_class}">{result['risk_category'].upper()}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Metrics Grid
            cols = st.columns(4)
            metrics = [
                ("Spelling Similarity", f"{result['spelling_similarity']:.1f}%"),
                ("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%"),
                ("Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%"),
                ("Overall Risk", f"{result['combined_risk']:.1f}%")
            ]
            
            for col, (label, value) in zip(cols, metrics):
                with col:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                        <div style="font-size: 12px; color: #718096; margin-bottom: 5px;">{label}</div>
                        <div style="font-size: 24px; font-weight: 700; color: #2d3748;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>")
    
    st.markdown("</div>")

# ================================
# ANALYTICS DASHBOARD TAB
# ================================

def render_analytics_tab():
    """Render Analytics Dashboard tab"""
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <h2 style="margin: 0; color: #2d3748;">📊 Medication Safety Analytics Dashboard</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data if needed
    if 'metrics' not in st.session_state.dashboard_data:
        with st.spinner("Loading analytics data..."):
            load_dashboard_data()
    
    # Row 1: KPI Cards
    st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">💊</div>
                <div class="stat-number">{metrics.get('total_drugs', 0)}</div>
                <div class="stat-label">Total Drugs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-number">{metrics.get('critical_risk_pairs', 0)}</div>
                <div class="stat-label">Critical Pairs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">⚠️</div>
                <div class="stat-number">{metrics.get('high_risk_pairs', 0)}</div>
                <div class="stat-label">High Risk Pairs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_score = metrics.get('avg_risk_score', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-number">{avg_score:.1f}%</div>
                <div class="stat-label">Avg Risk Score</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 2: Charts
    st.markdown("<div style='margin: 30px 0;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #2d3748; margin-bottom: 20px;">Risk Distribution</h3>
        """, unsafe_allow_html=True)
        
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #2d3748; margin-bottom: 20px;">Top Risk Pairs</h3>
        """, unsafe_allow_html=True)
        
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 3: Heatmap
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #2d3748; margin-bottom: 20px;">Drug Confusion Risk Heatmap</h3>
    """, unsafe_allow_html=True)
    
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; color: #718096; font-size: 14px;">
            🟢 Low Risk &nbsp;&nbsp; 🟡 Medium Risk &nbsp;&nbsp; 🔴 High Risk
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs first.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 4: FDA Alerts
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #2d3748; margin-bottom: 20px;">🚨 FDA High Alert Drug Pairs</h3>
    """, unsafe_allow_html=True)
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", "Reason": "Epilepsy medication vs Antifungal", "Severity": "🔴"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", "Reason": "Arthritis vs Depression medication", "Severity": "🔴"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", "Reason": "Diabetes vs Antibiotic", "Severity": "🟠"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", "Reason": "Blood Pressure vs Anxiety medication", "Severity": "🟠"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", "Reason": "Antipsychotic vs Allergy medication", "Severity": "🟡"},
    ])
    
    # Style the dataframe
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Severity": st.column_config.TextColumn("Severity", width="small")
        }
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>")

# ================================
# REAL-TIME DASHBOARD TAB
# ================================

def render_realtime_tab():
    """Render Real-Time Dashboard tab"""
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <h2 style="margin: 0; color: #2d3748;">⚡ Real-Time Medication Safety Dashboard</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Connection Status
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.websocket_connected:
            st.markdown("""
            <div style="background: linear-gradient(to right, #00b09b, #96c93d); color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 24px; margin-right: 10px;">✅</div>
                    <div>
                        <div style="font-weight: 600; font-size: 18px;">Real-time Connection Active</div>
                        <div style="font-size: 14px; opacity: 0.9;">Live data streaming enabled</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 24px; margin-right: 10px;">🔌</div>
                    <div>
                        <div style="font-weight: 600; color: #2d3748;">Connecting to Real-Time Server</div>
                        <div style="color: #718096; font-size: 14px;">Live updates will appear here</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Refresh Connection", use_container_width=True):
            websocket_manager.start_connection()
            st.rerun()
    
    # Auto-start WebSocket if not connected
    if not st.session_state.websocket_connected:
        websocket_manager.start_connection()
    
    # Display Real-time Metrics
    metrics = st.session_state.realtime_metrics or {}
    
    if metrics:
        # Real-time KPI Cards
        st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-number">{metrics.get('total_drugs', 0)}</div>
                <div class="stat-label">Live Drugs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-number">{metrics.get('critical_risk_pairs', 0)}</div>
                <div class="stat-label">Critical Now</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_score = metrics.get('avg_risk_score', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-number">{avg_score:.1f}%</div>
                <div class="stat-label">Avg Risk</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            clients = metrics.get('connected_clients', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-number">{clients}</div>
                <div class="stat-label">Connected</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Recent Activity Section
        st.markdown("""
        <div class="custom-card" style="margin-top: 30px;">
            <h3 style="color: #2d3748; margin-bottom: 20px;">🕒 Recent Activity Timeline</h3>
        """, unsafe_allow_html=True)
        
        if metrics.get('recent_searches'):
            for idx, search in enumerate(metrics['recent_searches'][:5]):
                timestamp = search.get('timestamp', '')
                drug_name = search.get('drug_name', 'Unknown')
                similar_drugs = search.get('similar_drugs_found', 0)
                highest_risk = search.get('highest_risk', 0)
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 15px; background: {'#f8f9fa' if idx % 2 == 0 else 'white'}; border-radius: 10px; margin-bottom: 10px;">
                    <div style="margin-right: 15px;">
                        <div style="width: 40px; height: 40px; background: {COLORS['primary_gradient']}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{idx+1}</div>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600; color: #2d3748;">{drug_name}</div>
                        <div style="color: #718096; font-size: 14px;">Found {similar_drugs} similar drugs • Highest risk: {highest_risk:.1f}%</div>
                    </div>
                    <div style="color: #718096; font-size: 12px;">{timestamp[:19] if timestamp else 'Just now'}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity data available")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # System Status
        st.markdown("""
        <div class="custom-card" style="margin-top: 20px;">
            <h3 style="color: #2d3748; margin-bottom: 20px;">⚙️ System Status</h3>
            <div style="display: flex; justify-content: space-between; align-items: center;">
        """, unsafe_allow_html=True)
        
        status = metrics.get('system_status', 'unknown')
        if status == 'healthy':
            status_color = "#10B981"
            status_icon = "✅"
            status_text = "All Systems Operational"
        else:
            status_color = "#F59E0B"
            status_icon = "⚠️"
            status_text = "System Issues Detected"
        
        st.markdown(f"""
                <div>
                    <div style="font-size: 14px; color: #718096;">Status</div>
                    <div style="font-weight: 600; color: {status_color};">{status_icon} {status_text}</div>
                </div>
                <div>
                    <div style="font-size: 14px; color: #718096;">Last Updated</div>
                    <div style="font-weight: 600; color: #2d3748;">{metrics.get('last_updated', '')[:19]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px;">
            <div style="font-size: 48px; margin-bottom: 20px;">⏳</div>
            <h3 style="color: #2d3748; margin-bottom: 10px;">Waiting for Real-Time Data</h3>
            <p style="color: #718096;">Live updates will appear here once connection is established.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>")

# ================================
# SIDEBAR
# ================================

def render_sidebar():
    """Render sidebar with system status"""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 36px; margin-bottom: 10px;">💊</div>
            <h2 style="margin: 0; color: #2d3748;">MediNomix</h2>
            <p style="color: #718096; margin: 5px 0 20px 0;">AI Medication Safety</p>
            <div style="height: 4px; background: {COLORS['primary_gradient']}; border-radius: 2px; margin: 0 auto 30px auto; width: 50px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Card
        st.markdown("""
        <div class="custom-card" style="margin-bottom: 20px;">
            <h3 style="color: #2d3748; margin-bottom: 15px;">System Status</h3>
        """, unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    st.markdown("""
                    <div style="background: linear-gradient(to right, #00b09b, #96c93d); color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                        <div style="font-size: 20px; margin-bottom: 5px;">✅</div>
                        <div style="font-weight: 600;">Backend Connected</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
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
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick Links
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #2d3748; margin-bottom: 15px;">Quick Links</h3>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Documentation", use_container_width=True):
            st.info("Documentation coming soon!")
        
        if st.button("🐛 Report Bug", use_container_width=True):
            st.info("Bug reporting coming soon!")
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            st.success("Cache cleared!")
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Risk Categories Guide
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #2d3748; margin-bottom: 15px;">Risk Categories</h3>
        """, unsafe_allow_html=True)
        
        risk_levels = [
            ("Critical", "≥75%", "Immediate attention required", "badge-critical"),
            ("High", "50-74%", "Review and verify", "badge-high"),
            ("Medium", "25-49%", "Monitor closely", "badge-medium"),
            ("Low", "<25%", "Low priority", "badge-low")
        ]
        
        for name, score, desc, badge_class in risk_levels:
            st.markdown(f"""
            <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #f0f0f0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span class="risk-badge {badge_class}" style="font-size: 10px; padding: 3px 10px;">{name}</span>
                    <span style="font-weight: 600; color: #2d3748;">{score}</span>
                </div>
                <div style="color: #718096; font-size: 12px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ================================
# FOOTER
# ================================

def render_footer():
    """Render footer"""
    st.markdown(f"""
    <div class="custom-footer">
        <div style="max-width: 800px; margin: 0 auto;">
            <div style="margin-bottom: 20px;">
                <div style="font-size: 24px; margin-bottom: 10px;">💊</div>
                <div style="font-weight: 600; color: #2d3748; margin-bottom: 10px;">MediNomix AI</div>
                <div style="color: #718096; font-size: 14px;">Preventing medication errors with artificial intelligence</div>
            </div>
            <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; color: #a0aec0; font-size: 12px;">
                <div style="margin-bottom: 10px;">© 2024 MediNomix AI. All rights reserved.</div>
                <div>Disclaimer: This tool is for educational purposes and should not replace professional medical advice.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# MAIN APPLICATION RENDERER
# ================================

def main():
    """Main application renderer"""
    
    # Render Navigation Bar
    render_navigation()
    
    # Render based on active tab
    if st.session_state.active_tab == "Home":
        render_hero_section()
        render_stats_counter()
        render_features_section()
        render_user_guide()
        render_trust_section()
        
    elif st.session_state.active_tab == "Drug Analysis":
        render_drug_analysis_tab()
        
    elif st.session_state.active_tab == "Analytics":
        render_analytics_tab()
        
    elif st.session_state.active_tab == "Real-Time":
        render_realtime_tab()
    
    # Render Sidebar
    render_sidebar()
    
    # Render Footer
    render_footer()

# ================================
# START APPLICATION
# ================================

if __name__ == "__main__":
    main()