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
medical_icon_base64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFiSURBVHic1ZO9SgNBFIVPymAENbYGX8FWtPIlLCwsLCwsLCwsrCx8hdhZ2FhYCLYxP2JjZ2FhIQgTCoXodY2fDnBdb8hFcevJHO7MfHNmuW+Mf5QA1sliEbgCHoE34H2Q8yvghPwQyf3qM5FqwB1wC1wAB8AB0APawBqwAqwB60AP2AUOgWdg4gJ5B6b+AKJISsA4MAd+m5+AHwAzzO+CqQWJIgB3gB7D/AtgGcC8w7wNwDUwbwMYA5oDwM2HTVkDDvNNLAswbzBvYwFy7WB6AXJg3gYy87FdIO1IPQbQj+QdZOWi60iuYmBbDrE2YEXIhqPBdKQCfBNoC/Z1IF0D2Am0DfunSAmgFiFBnQB6QLsAfAHsBPomgA6Q/CclzL+U8DwK0Iz0aYySBIl4Lf4rIiJ4T4F0IE9D3gpgvwdSd/A5SMNBFgFJHOxpIBUHOzE3YQc7AqTgYI8T6TjYowDKDvZQRBnACICUfjuYrwG8H3Uj+X6kHUjfwy0LeyxCz+8F9sycm/cnE2kAAAAASUVORK5CYII="

# Premium Color Scheme with improved contrast
COLORS = {
    "primary_gradient": "linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)",
    "secondary_gradient": "linear-gradient(to right, #3b82f6, #8b5cf6)",
    "success_gradient": "linear-gradient(to right, #10b981, #34d399)",
    "warning_gradient": "linear-gradient(to right, #f59e0b, #fbbf24)",
    "danger_gradient": "linear-gradient(to right, #ef4444, #f87171)",
    "light_gradient": "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
    "dark_gradient": "linear-gradient(135deg, #1e293b 0%, #334155 100%)",
    "card_bg": "#ffffff",
    "sidebar_bg": "#f1f5f9",
    "text_dark": "#0f172a",
    "text_medium": "#475569",
    "text_light": "#64748b",
    "border": "#e2e8f0",
    "hover_bg": "#f8fafc"
}

# Custom CSS for Bootstrap-like styling with improved readability
st.markdown(f"""
<style>
/* Import Google Fonts for premium typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

/* Global Styles */
* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: #f8fafc;
    font-family: 'Inter', sans-serif;
}}

/* Premium Card Design */
.custom-card {{
    background: {COLORS['card_bg']};
    border-radius: 16px;
    border: 1px solid {COLORS['border']};
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    padding: 28px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 24px;
    color: {COLORS['text_dark']};
}}

.custom-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.12);
    border-color: #c7d2fe;
}}

.card-header {{
    background: {COLORS['light_gradient']};
    border-radius: 12px 12px 0 0;
    padding: 24px;
    margin: -28px -28px 28px -28px;
    border-bottom: 1px solid {COLORS['border']};
    color: {COLORS['text_dark']};
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
}}

.card-header h2 {{
    margin: 0;
    color: {COLORS['text_dark']};
    font-size: 1.5rem;
    font-weight: 700;
    font-family: 'Poppins', sans-serif;
}}

.card-header p {{
    margin: 8px 0 0 0;
    color: {COLORS['text_medium']};
    font-size: 0.95rem;
    font-weight: 400;
}}

/* Gradient Buttons with better contrast */
.gradient-btn {{
    background: {COLORS['secondary_gradient']};
    color: white !important;
    border: none;
    padding: 14px 36px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: inline-block;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    letter-spacing: 0.3px;
}}

.gradient-btn:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 24px rgba(59, 130, 246, 0.25);
    color: white !important;
}}

.secondary-btn {{
    background: white;
    color: {COLORS['text_dark']} !important;
    border: 2px solid {COLORS['border']};
    padding: 12px 28px;
    border-radius: 50px;
    font-weight: 500;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
}}

.secondary-btn:hover {{
    background: #f8fafc;
    transform: translateY(-2px);
    border-color: #c7d2fe;
    color: {COLORS['text_dark']} !important;
}}

/* Custom Navigation */
.custom-nav {{
    background: white;
    padding: 0;
    box-shadow: 0 2px 20px rgba(0,0,0,0.06);
    margin-bottom: 36px;
    border-radius: 0 0 16px 16px;
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.95);
}}

.nav-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
}}

.nav-logo {{
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 28px;
    background: {COLORS['primary_gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.nav-items {{
    display: flex;
    gap: 8px;
}}

.nav-item {{
    padding: 12px 24px;
    color: {COLORS['text_medium']};
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 12px;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    text-decoration: none;
}}

.nav-item:hover {{
    color: #4f46e5;
    background: {COLORS['hover_bg']};
    transform: translateY(-1px);
}}

.nav-item.active {{
    background: {COLORS['primary_gradient']};
    color: white !important;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}}

/* Stat Cards */
.stat-card {{
    background: white;
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(0,0,0,0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: {COLORS['text_dark']};
    height: 100%;
}}

.stat-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 16px 36px rgba(0,0,0,0.1);
}}

.stat-icon {{
    font-size: 48px;
    margin-bottom: 20px;
    color: #4f46e5;
}}

.stat-number {{
    font-size: 40px;
    font-weight: 700;
    background: {COLORS['primary_gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 16px 0;
    font-family: 'Poppins', sans-serif;
}}

.stat-label {{
    color: {COLORS['text_medium']};
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}}

/* Feature Cards */
.feature-card {{
    background: white;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    box-shadow: 0 8px 28px rgba(0,0,0,0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    color: {COLORS['text_dark']};
}}

.feature-card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 20px 48px rgba(0,0,0,0.12);
}}

.feature-icon {{
    font-size: 56px;
    margin-bottom: 24px;
    color: #4f46e5;
}}

.feature-card h3 {{
    margin-bottom: 16px;
    color: {COLORS['text_dark']};
    font-size: 1.25rem;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
}}

.feature-card p {{
    color: {COLORS['text_medium']};
    line-height: 1.7;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
}}

/* Risk Badges with better contrast */
.risk-badge {{
    display: inline-block;
    padding: 8px 24px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'Inter', sans-serif;
}}

.badge-critical {{
    background: {COLORS['danger_gradient']};
    color: white;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}}

.badge-high {{
    background: {COLORS['warning_gradient']};
    color: #0f172a;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
}}

.badge-medium {{
    background: linear-gradient(to right, #3b82f6, #06b6d4);
    color: white;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}}

.badge-low {{
    background: {COLORS['success_gradient']};
    color: white;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}}

/* Hero Section */
.hero-section {{
    background: {COLORS['primary_gradient']};
    padding: 100px 0;
    border-radius: 24px;
    margin-bottom: 48px;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.hero-section::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
}}

.hero-title {{
    font-size: 56px;
    font-weight: 700;
    margin-bottom: 24px;
    font-family: 'Poppins', sans-serif;
    position: relative;
    line-height: 1.2;
}}

.hero-subtitle {{
    font-size: 20px;
    opacity: 0.95;
    max-width: 700px;
    margin: 0 auto 40px;
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    position: relative;
    font-weight: 400;
}}

/* Footer */
.custom-footer {{
    background: {COLORS['sidebar_bg']};
    padding: 40px 0;
    margin-top: 60px;
    border-radius: 16px 16px 0 0;
    text-align: center;
    color: {COLORS['text_medium']};
    font-family: 'Inter', sans-serif;
}}

/* Input Fields - LARGER and BETTER */
.stTextInput > div > div > input {{
    font-family: 'Inter', sans-serif;
    font-size: 16px !important;
    padding: 16px 20px !important;
    border-radius: 12px !important;
    border: 2px solid {COLORS['border']} !important;
    background: white !important;
    color: {COLORS['text_dark']} !important;
    height: auto !important;
    min-height: 56px !important;
    transition: all 0.3s ease !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
    outline: none !important;
}}

.stTextInput > div > div > input::placeholder {{
    color: {COLORS['text_light']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
}}

/* Selectbox, Radio, Checkbox - LARGER */
.stRadio > div {{
    font-family: 'Inter', sans-serif !important;
    color: {COLORS['text_dark']} !important;
    font-size: 16px !important;
}}

.stRadio > div > label {{
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    color: {COLORS['text_dark']} !important;
    padding: 12px 20px !important;
    margin: 8px 0 !important;
    border-radius: 12px !important;
    border: 2px solid {COLORS['border']} !important;
    background: white !important;
    transition: all 0.3s ease !important;
}}

.stRadio > div > label:hover {{
    background: {COLORS['hover_bg']} !important;
    border-color: #c7d2fe !important;
}}

.stRadio > div > label[data-baseweb="radio"] > div:first-child {{
    width: 24px !important;
    height: 24px !important;
}}

/* Button Styling */
.stButton > button {{
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    padding: 14px 32px !important;
    border-radius: 50px !important;
    min-height: 56px !important;
    transition: all 0.3s ease !important;
    border: none !important;
}}

/* Metric Cards */
.stMetric {{
    font-family: 'Inter', sans-serif !important;
    color: {COLORS['text_dark']} !important;
}}

.stMetric > div {{
    padding: 20px !important;
    border-radius: 16px !important;
    background: white !important;
    border: 1px solid {COLORS['border']} !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}}

.stMetric > div > div[data-testid="stMetricValue"] {{
    font-size: 36px !important;
    font-weight: 700 !important;
    font-family: 'Poppins', sans-serif !important;
    color: {COLORS['text_dark']} !important;
}}

.stMetric > div > div[data-testid="stMetricLabel"] {{
    font-size: 14px !important;
    color: {COLORS['text_medium']} !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}}

/* Dataframe Styling */
.stDataFrame {{
    font-family: 'Inter', sans-serif !important;
}}

.dataframe {{
    font-family: 'Inter', sans-serif !important;
    color: {COLORS['text_dark']} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}

/* Scrollbar Styling - VISIBLE AND BEAUTIFUL */
::-webkit-scrollbar {{
    width: 12px !important;
    height: 12px !important;
}}

::-webkit-scrollbar-track {{
    background: {COLORS['sidebar_bg']} !important;
    border-radius: 6px !important;
}}

::-webkit-scrollbar-thumb {{
    background: linear-gradient(135deg, #c7d2fe 0%, #a5b4fc 100%) !important;
    border-radius: 6px !important;
    border: 2px solid {COLORS['sidebar_bg']} !important;
}}

::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 100%) !important;
}}

/* Sidebar Styling */
[data-testid="stSidebar"] {{
    background: {COLORS['sidebar_bg']} !important;
    font-family: 'Inter', sans-serif !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important;
    margin: 8px 0 !important;
    background: white !important;
    color: {COLORS['text_dark']} !important;
    border: 2px solid {COLORS['border']} !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: {COLORS['hover_bg']} !important;
    border-color: #c7d2fe !important;
    transform: translateY(-2px) !important;
}}

/* Image Slider */
.image-slider {{
    display: flex;
    overflow-x: auto;
    gap: 20px;
    padding: 20px 0;
    scroll-behavior: smooth;
}}

.image-slider::-webkit-scrollbar {{
    height: 8px;
}}

.image-slider::-webkit-scrollbar-track {{
    background: {COLORS['border']};
    border-radius: 4px;
}}

.image-slider::-webkit-scrollbar-thumb {{
    background: {COLORS['primary_gradient']};
    border-radius: 4px;
}}

.slider-image {{
    flex: 0 0 auto;
    width: 300px;
    height: 200px;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}}

.slider-image:hover {{
    transform: scale(1.05);
    box-shadow: 0 12px 32px rgba(0,0,0,0.15);
}}

/* Tab Content Styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
}}

.stTabs [data-baseweb="tab"] {{
    height: 60px;
    padding: 0 24px;
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    color: {COLORS['text_medium']} !important;
    border-radius: 12px !important;
    border: 2px solid {COLORS['border']} !important;
    background: white !important;
}}

.stTabs [aria-selected="true"] {{
    background: {COLORS['primary_gradient']} !important;
    color: white !important;
    border-color: transparent !important;
    font-weight: 600 !important;
}}

/* Plotly Charts */
.js-plotly-plot .plotly {{
    font-family: 'Inter', sans-serif !important;
}}

/* Custom Expander */
.custom-expander {{
    background: white;
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    margin-bottom: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
}}

.custom-expander:hover {{
    border-color: #c7d2fe;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

.expander-header {{
    padding: 20px;
    background: #f8fafc;
    cursor: pointer;
    font-weight: 600;
    color: {COLORS['text_dark']};
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.expander-content {{
    padding: 24px;
    background: white;
    color: {COLORS['text_medium']};
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    font-size: 15px;
}}

/* Typography Improvements */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Poppins', sans-serif !important;
    color: {COLORS['text_dark']} !important;
    font-weight: 600 !important;
}}

p, span, div, li {{
    font-family: 'Inter', sans-serif !important;
    color: {COLORS['text_medium']} !important;
}}

strong, b {{
    font-weight: 600 !important;
    color: {COLORS['text_dark']} !important;
}}

/* Alert/Info Boxes */
.stAlert {{
    font-family: 'Inter', sans-serif !important;
    border-radius: 12px !important;
    border: 1px solid !important;
}}

/* Code blocks */
.stCode {{
    font-family: 'Monaco', 'Courier New', monospace !important;
    color: {COLORS['text_dark']} !important;
}}

/* Loading spinner */
.stSpinner {{
    color: #4f46e5 !important;
}}

/* Slider controls */
.stSlider {{
    font-family: 'Inter', sans-serif !important;
}}

/* Better contrast for all text elements */
.element-container {{
    color: {COLORS['text_dark']} !important;
}}

/* Remove Streamlit default branding */
#MainMenu {{
    visibility: hidden;
}}
footer {{
    visibility: hidden;
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
if 'image_slider_pos' not in st.session_state:
    st.session_state.image_slider_pos = 0

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
        title=dict(text="Drug Confusion Risk Matrix", font=dict(size=20, family='Poppins')),
        height=600,
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        plot_bgcolor='white',
        font=dict(family='Inter', size=14, color=COLORS['text_dark'])
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
        marker_colors=['#ef4444', '#f59e0b', '#10b981', '#3b82f6'],
        textfont=dict(family='Inter', size=14, color=COLORS['text_dark'])
    )])
    
    fig.update_layout(
        title=dict(text="Risk Distribution", font=dict(size=20, family='Poppins')),
        height=400,
        showlegend=True,
        font=dict(family='Inter', size=14, color=COLORS['text_dark'])
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
            marker_color='#7c3aed',
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            textfont=dict(family='Inter', size=14, color=COLORS['text_dark'])
        )
    ])
    
    fig.update_layout(
        title=dict(text="Top 10 High-Risk Drug Pairs", font=dict(size=20, family='Poppins')),
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=500,
        plot_bgcolor='white',
        font=dict(family='Inter', size=14, color=COLORS['text_dark'])
    )
    
    return fig

# ================================
# IMAGE SLIDER FUNCTIONALITY
# ================================

def create_image_slider():
    """Create interactive image slider"""
    # Medical images from Unsplash
    images = [
        "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
    ]
    
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <h2 style="margin: 0; color: #0f172a;">🏥 Trusted by Healthcare Professionals Worldwide</h2>
            <p style="margin: 10px 0 0 0; color: #475569;">See how leading hospitals and clinics use MediNomix to prevent medication errors</p>
        </div>
        
        <div class="image-slider" id="imageSlider">
    """, unsafe_allow_html=True)
    
    # Display images
    for idx, img_url in enumerate(images):
        st.markdown(f"""
        <div class="slider-image">
            <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" alt="Healthcare facility {idx+1}">
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Slider controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous", use_container_width=True):
            st.session_state.image_slider_pos = max(0, st.session_state.image_slider_pos - 1)
            st.rerun()
    
    with col3:
        if st.button("Next ➡️", use_container_width=True):
            st.session_state.image_slider_pos = min(len(images) - 1, st.session_state.image_slider_pos + 1)
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; color: #64748b; font-family: 'Inter', sans-serif;">
            Image {st.session_state.image_slider_pos + 1} of {len(images)}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # JavaScript for smooth scrolling
    st.markdown("""
    <script>
    // Auto-scroll the image slider
    const slider = document.getElementById('imageSlider');
    if (slider) {{
        slider.scrollLeft = %d * 320; // Scroll to current position
    }}
    </script>
    """ % st.session_state.image_slider_pos, unsafe_allow_html=True)

# ================================
# CUSTOM NAVIGATION BAR
# ================================

def render_navigation():
    """Render custom Bootstrap-style navigation bar"""
    st.markdown("""
    <div class="custom-nav">
        <div class="nav-container">
            <div class="nav-logo">
                💊 MediNomix
            </div>
            <div class="nav-items">
    """, unsafe_allow_html=True)
    
    tabs = ["Home", "Drug Analysis", "Analytics", "Real-Time"]
    
    for tab in tabs:
        active_class = "active" if st.session_state.active_tab == tab else ""
        if st.button(tab, key=f"nav_{tab}", use_container_width=False):
            st.session_state.active_tab = tab
            st.rerun()
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# HOMEPAGE COMPONENTS
# ================================

def render_hero_section():
    """Render hero/jumbotron section"""
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">Prevent Medication Errors with AI</h1>
        <p class="hero-subtitle">Advanced AI-powered system that analyzes drug names for potential confusion risks, helping healthcare professionals prevent medication errors and improve patient safety worldwide.</p>
        <button class="gradient-btn" style="margin-top: 20px; padding: 16px 40px; font-size: 18px;" onclick="window.location.href='#analysis'">Start Free Analysis</button>
    </div>
    """, unsafe_allow_html=True)

def render_stats_counter():
    """Render animated stats counter"""
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 48px;">
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
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_features_section():
    """Render how it works feature cards"""
    st.markdown("""
    <div style="margin: 48px 0;">
        <h2 style="text-align: center; margin-bottom: 36px; color: #0f172a; font-family: 'Poppins', sans-serif; font-size: 32px;">How MediNomix Works</h2>
    </div>
    """, unsafe_allow_html=True)
    
    features = [
        {"icon": "🔍", "title": "Search Medication", "desc": "Enter any drug name to analyze potential confusion risks with similar medications"},
        {"icon": "🧠", "title": "AI Risk Analysis", "desc": "Our advanced AI analyzes spelling, phonetic, and therapeutic similarities in real-time"},
        {"icon": "🛡️", "title": "Prevent Errors", "desc": "Get detailed risk assessments and actionable recommendations to prevent medication errors"}
    ]
    
    cols = st.columns(3)
    for idx, (col, feature) in enumerate(zip(cols, features)):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <h3 style="margin-bottom: 16px; color: #0f172a; font-family: 'Poppins', sans-serif;">{feature['title']}</h3>
                <p style="color: #475569; line-height: 1.7; font-size: 16px; font-family: 'Inter', sans-serif;">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def render_user_guide():
    """Render user guide accordion"""
    st.markdown("""
    <div class="custom-card" style="margin: 48px 0;">
        <div class="card-header">
            <h2 style="margin: 0; color: #0f172a;">📚 User Guide & Quick Start</h2>
            <p style="margin: 10px 0 0 0; color: #475569;">Follow these simple steps to get started with MediNomix</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Step 1: Search for a Medication", expanded=True):
        st.markdown("""
        <div style="padding: 20px; font-family: 'Inter', sans-serif; color: #475569;">
        <ol style="line-height: 1.8;">
            <li><strong>Navigate to the Drug Analysis tab</strong> using the top navigation menu</li>
            <li><strong>Enter any medication name</strong> (brand or generic) in the search box</li>
            <li><strong>Click "Analyze Drug"</strong> to start the AI-powered analysis</li>
            <li><strong>Try our quick examples:</strong> Lamictal, Metformin, or Celebrex</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Step 2: Review Risk Assessment"):
        st.markdown("""
        <div style="padding: 20px; font-family: 'Inter', sans-serif; color: #475569;">
        <ol style="line-height: 1.8;">
            <li><strong>View all similar drugs</strong> with confusion risk scores</li>
            <li><strong>Filter by risk level:</strong> Critical, High, Medium, or Low</li>
            <li><strong>Examine detailed similarity metrics:</strong> Spelling, Phonetic, Therapeutic Context</li>
            <li><strong>Check risk badges</strong> for quick visual identification</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Step 3: Take Preventive Action"):
        st.markdown("""
        <div style="padding: 20px; font-family: 'Inter', sans-serif; color: #475569;">
        <ol style="line-height: 1.8;">
            <li><strong>Check the Analytics tab</strong> for overall system statistics</li>
            <li><strong>Monitor the Real-Time dashboard</strong> for live updates and alerts</li>
            <li><strong>Use the heatmap visualization</strong> to identify high-risk drug pairs</li>
            <li><strong>Review FDA alerts</strong> for known high-risk medication combinations</li>
        </ol>
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
            <h2 style="margin: 0; color: #0f172a;">🔍 Drug Confusion Risk Analysis</h2>
            <p style="margin: 10px 0 0 0; color: #475569;">Search any medication to analyze confusion risks with similar drugs. First search may take 5-10 seconds as we fetch live FDA data.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Search Section in Card
    st.markdown("""
    <div style="background: #f8fafc; padding: 28px; border-radius: 16px; margin: 24px 0;">
        <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">Enter Medication Name</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        drug_name = st.text_input(
            "",
            placeholder="Type drug name here (e.g., metformin, lamictal, celebrex, clonidine...)",
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
                    st.success("✅ Examples loaded! Try searching: lamictal, celebrex, metformin")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("""
    <div style="margin: 24px 0;">
        <h4 style="color: #475569; margin-bottom: 16px; font-family: 'Inter', sans-serif; font-weight: 500;">💡 Quick Examples:</h4>
    </div>
    """, unsafe_allow_html=True)
    
    examples = ["Lamictal", "Metformin", "Celebrex", "Clonidine"]
    cols = st.columns(4)
    for idx, (col, example) in enumerate(zip(cols, examples)):
        with col:
            if st.button(f"{example}", use_container_width=True, key=f"ex_{idx}"):
                with st.spinner(f"🧠 Analyzing {example}..."):
                    result = search_drug(example)
                    if result:
                        st.session_state.search_results = result.get('similar_drugs', [])
                        st.success(f"✅ Analysis complete! Found {len(st.session_state.search_results)} similar drugs.")
                        st.rerun()
                    else:
                        st.error("❌ Could not analyze drug. Please check backend connection.")
    
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
        <div style="margin-top: 36px;">
            <h3 style="color: #0f172a; margin-bottom: 24px; font-family: 'Poppins', sans-serif; font-size: 24px;">📊 Analysis Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Filters
        st.markdown("<div style='margin-bottom: 24px;'>", unsafe_allow_html=True)
        risk_filters = st.radio(
            "Filter by risk level:",
            ["All Risks", "Critical (≥75%)", "High (50-74%)", "Medium (25-49%)", "Low (<25%)"],
            horizontal=True,
            key="risk_filter"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
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
            risk_percentage = result['combined_risk']
            
            st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0 0 8px 0; color: #0f172a; font-family: 'Poppins', sans-serif; font-size: 20px;">{result['target_drug']['brand_name']}</h3>
                        {f"<p style='margin: 0 0 16px 0; color: #475569; font-family: Inter, sans-serif; font-size: 15px;'><strong>Generic:</strong> {result['target_drug']['generic_name']}</p>" if result['target_drug']['generic_name'] else ""}
                        {f"<p style='margin: 0 0 16px 0; color: #475569; font-family: Inter, sans-serif; font-size: 14px;'><strong>Manufacturer:</strong> {result['target_drug']['manufacturer']}</p>" if result['target_drug']['manufacturer'] else ""}
                    </div>
                    <div style="text-align: center; min-width: 120px;">
                        <div style="font-size: 40px; font-weight: 700; font-family: 'Poppins', sans-serif; background: {COLORS['primary_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px;">
                            {risk_percentage:.0f}%
                        </div>
                        <span class="risk-badge {risk_color_class}" style="display: inline-block; margin-top: 4px;">{result['risk_category'].upper()}</span>
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
                    <div style="text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px; margin: 8px 0;">
                        <div style="font-size: 14px; color: #64748b; margin-bottom: 8px; font-family: 'Inter', sans-serif; font-weight: 500;">{label}</div>
                        <div style="font-size: 28px; font-weight: 700; color: #0f172a; font-family: 'Poppins', sans-serif;">{value}</div>
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
            <h2 style="margin: 0; color: #0f172a;">📊 Medication Safety Analytics Dashboard</h2>
            <p style="margin: 10px 0 0 0; color: #475569;">Comprehensive analytics and insights into medication confusion risks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data if needed
    if 'metrics' not in st.session_state.dashboard_data:
        with st.spinner("📊 Loading analytics data..."):
            load_dashboard_data()
    
    # Row 1: KPI Cards
    st.markdown("<div style='margin: 24px 0;'>", unsafe_allow_html=True)
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Drugs",
                value=f"{metrics.get('total_drugs', 0):,}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="Critical Pairs",
                value=f"{metrics.get('critical_risk_pairs', 0):,}",
                delta=None,
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                label="High Risk Pairs",
                value=f"{metrics.get('high_risk_pairs', 0):,}",
                delta=None,
                delta_color="inverse"
            )
        
        with col4:
            avg_score = metrics.get('avg_risk_score', 0)
            st.metric(
                label="Avg Risk Score",
                value=f"{avg_score:.1f}%",
                delta=None
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 2: Charts
    st.markdown("<div style='margin: 36px 0;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">Risk Distribution</h3>
        """, unsafe_allow_html=True)
        
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available. Try loading examples first.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">Top Risk Pairs</h3>
        """, unsafe_allow_html=True)
        
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available. Try loading examples first.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 3: Heatmap
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">Drug Confusion Risk Heatmap</h3>
    """, unsafe_allow_html=True)
    
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown("""
        <div style="text-align: center; margin-top: 24px; color: #64748b; font-size: 15px; font-family: 'Inter', sans-serif;">
            🟢 Low Risk &nbsp;&nbsp; 🟡 Medium Risk &nbsp;&nbsp; 🔴 High Risk
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs or load examples first.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 4: FDA Alerts
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">🚨 FDA High Alert Drug Pairs</h3>
        <p style="color: #64748b; margin-bottom: 24px; font-family: 'Inter', sans-serif; font-size: 15px;">Known high-risk medication pairs identified by FDA</p>
    """, unsafe_allow_html=True)
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", "Reason": "Epilepsy medication vs Antifungal", "Severity": "🔴"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", "Reason": "Arthritis vs Depression medication", "Severity": "🔴"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", "Reason": "Diabetes vs Antibiotic", "Severity": "🟠"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", "Reason": "Blood Pressure vs Anxiety medication", "Severity": "🟠"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", "Reason": "Antipsychotic vs Allergy medication", "Severity": "🟡"},
        {"Drug 1": "Hydralazine", "Drug 2": "Hydroxyzine", "Risk Level": "High", "Reason": "Blood Pressure vs Allergy medication", "Severity": "🟠"},
        {"Drug 1": "Risperidone", "Drug 2": "Ropinirole", "Risk Level": "Medium", "Reason": "Antipsychotic vs Parkinson's medication", "Severity": "🟡"},
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
            <h2 style="margin: 0; color: #0f172a;">⚡ Real-Time Medication Safety Dashboard</h2>
            <p style="margin: 10px 0 0 0; color: #475569;">Live monitoring and real-time updates of medication confusion risks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Connection Status
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.websocket_connected:
            st.markdown("""
            <div style="background: linear-gradient(to right, #10b981, #34d399); color: white; padding: 20px; border-radius: 16px; margin-bottom: 24px;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 32px; margin-right: 16px;">✅</div>
                    <div>
                        <div style="font-weight: 600; font-size: 20px; font-family: 'Poppins', sans-serif;">Real-time Connection Active</div>
                        <div style="font-size: 15px; opacity: 0.95; font-family: 'Inter', sans-serif;">Live data streaming enabled - Updates every 10 seconds</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f8fafc; padding: 20px; border-radius: 16px; margin-bottom: 24px; border: 2px dashed #cbd5e1;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 32px; margin-right: 16px;">🔌</div>
                    <div>
                        <div style="font-weight: 600; color: #0f172a; font-size: 20px; font-family: 'Poppins', sans-serif;">Connecting to Real-Time Server</div>
                        <div style="color: #64748b; font-size: 15px; font-family: 'Inter', sans-serif;">Live updates will appear here once connection is established</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Refresh Connection", use_container_width=True, type="secondary"):
            websocket_manager.start_connection()
            st.rerun()
    
    # Auto-start WebSocket if not connected
    if not st.session_state.websocket_connected:
        websocket_manager.start_connection()
    
    # Display Real-time Metrics
    metrics = st.session_state.realtime_metrics or {}
    
    if metrics:
        # Real-time KPI Cards
        st.markdown("<div style='margin: 24px 0;'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Live Drugs",
                value=f"{metrics.get('total_drugs', 0):,}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="Critical Now",
                value=f"{metrics.get('critical_risk_pairs', 0):,}",
                delta=None,
                delta_color="inverse"
            )
        
        with col3:
            avg_score = metrics.get('avg_risk_score', 0)
            st.metric(
                label="Avg Risk",
                value=f"{avg_score:.1f}%",
                delta=None
            )
        
        with col4:
            clients = metrics.get('connected_clients', 0)
            st.metric(
                label="Connected",
                value=f"{clients}",
                delta=None
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Recent Activity Section
        st.markdown("""
        <div class="custom-card" style="margin-top: 36px;">
            <h3 style="color: #0f172a; margin-bottom: 24px; font-family: 'Poppins', sans-serif;">🕒 Recent Activity Timeline</h3>
        """, unsafe_allow_html=True)
        
        if metrics.get('recent_searches'):
            for idx, search in enumerate(metrics['recent_searches'][:5]):
                timestamp = search.get('timestamp', '')
                drug_name = search.get('drug_name', 'Unknown')
                similar_drugs = search.get('similar_drugs_found', 0)
                highest_risk = search.get('highest_risk', 0)
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 20px; background: {'#f8fafc' if idx % 2 == 0 else 'white'}; border-radius: 12px; margin-bottom: 12px; transition: all 0.3s ease;">
                    <div style="margin-right: 20px;">
                        <div style="width: 48px; height: 48px; background: {COLORS['primary_gradient']}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-family: 'Poppins', sans-serif; font-size: 18px;">{idx+1}</div>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600; color: #0f172a; font-family: 'Poppins', sans-serif; font-size: 16px;">{drug_name}</div>
                        <div style="color: #64748b; font-family: 'Inter', sans-serif; font-size: 14px; margin-top: 4px;">Found {similar_drugs} similar drugs • Highest risk: {highest_risk:.1f}%</div>
                    </div>
                    <div style="color: #94a3b8; font-family: 'Inter', sans-serif; font-size: 13px; white-space: nowrap;">{timestamp[:19] if timestamp else 'Just now'}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity data available. Try searching for drugs first.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # System Status
        st.markdown("""
        <div class="custom-card" style="margin-top: 24px;">
            <h3 style="color: #0f172a; margin-bottom: 24px; font-family: 'Poppins', sans-serif;">⚙️ System Status</h3>
            <div style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; padding: 24px; border-radius: 12px;">
        """, unsafe_allow_html=True)
        
        status = metrics.get('system_status', 'unknown')
        if status == 'healthy':
            status_color = "#10b981"
            status_icon = "✅"
            status_text = "All Systems Operational"
        else:
            status_color = "#f59e0b"
            status_icon = "⚠️"
            status_text = "System Issues Detected"
        
        last_updated = metrics.get('last_updated', '')
        if last_updated:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                formatted_time = dt.strftime("%H:%M:%S")
            except:
                formatted_time = last_updated[:19]
        else:
            formatted_time = "N/A"
        
        st.markdown(f"""
                <div>
                    <div style="font-size: 14px; color: #64748b; font-family: 'Inter', sans-serif; margin-bottom: 4px;">Status</div>
                    <div style="font-weight: 600; color: {status_color}; font-family: 'Poppins', sans-serif; font-size: 18px;">{status_icon} {status_text}</div>
                </div>
                <div>
                    <div style="font-size: 14px; color: #64748b; font-family: 'Inter', sans-serif; margin-bottom: 4px;">Last Updated</div>
                    <div style="font-weight: 600; color: #0f172a; font-family: 'Poppins', sans-serif; font-size: 18px;">{formatted_time}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 64px; margin-bottom: 24px;">⏳</div>
            <h3 style="color: #0f172a; margin-bottom: 16px; font-family: 'Poppins', sans-serif;">Waiting for Real-Time Data</h3>
            <p style="color: #64748b; font-family: 'Inter', sans-serif; font-size: 16px; max-width: 500px; margin: 0 auto;">Live updates will appear here once connection is established.</p>
            <button class="gradient-btn" style="margin-top: 24px;" onclick="window.location.reload()">Refresh Page</button>
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
        <div style="text-align: center; margin-bottom: 32px;">
            <div style="font-size: 48px; margin-bottom: 16px; color: #4f46e5;">💊</div>
            <h2 style="margin: 0; color: #0f172a; font-family: 'Poppins', sans-serif;">MediNomix</h2>
            <p style="color: #64748b; margin: 8px 0 24px 0; font-family: 'Inter', sans-serif;">AI Medication Safety</p>
            <div style="height: 4px; background: {COLORS['primary_gradient']}; border-radius: 2px; margin: 0 auto 32px auto; width: 60px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Card
        st.markdown("""
        <div class="custom-card" style="margin-bottom: 24px;">
            <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">System Status</h3>
        """, unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    st.markdown("""
                    <div style="background: linear-gradient(to right, #10b981, #34d399); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                        <div style="font-size: 24px; margin-bottom: 8px;">✅</div>
                        <div style="font-weight: 600; font-size: 18px; font-family: 'Poppins', sans-serif;">Backend Connected</div>
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
            <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">Quick Links</h3>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Documentation", use_container_width=True, type="secondary"):
            st.info("Documentation coming soon!")
        
        if st.button("🐛 Report Bug", use_container_width=True, type="secondary"):
            st.info("Bug reporting coming soon!")
        
        if st.button("🔄 Clear Cache", use_container_width=True, type="secondary"):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            st.success("✅ Cache cleared!")
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Risk Categories Guide
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #0f172a; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">Risk Categories</h3>
        """, unsafe_allow_html=True)
        
        risk_levels = [
            ("Critical", "≥75%", "Immediate attention required", "badge-critical"),
            ("High", "50-74%", "Review and verify", "badge-high"),
            ("Medium", "25-49%", "Monitor closely", "badge-medium"),
            ("Low", "<25%", "Low priority", "badge-low")
        ]
        
        for name, score, desc, badge_class in risk_levels:
            st.markdown(f"""
            <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #f0f0f0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span class="risk-badge {badge_class}" style="font-size: 11px; padding: 6px 16px;">{name}</span>
                    <span style="font-weight: 600; color: #0f172a; font-family: 'Poppins', sans-serif;">{score}</span>
                </div>
                <div style="color: #64748b; font-family: 'Inter', sans-serif; font-size: 13px; line-height: 1.5;">{desc}</div>
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
            <div style="margin-bottom: 24px;">
                <div style="font-size: 32px; margin-bottom: 16px; color: #4f46e5;">💊</div>
                <div style="font-weight: 600; color: #0f172a; margin-bottom: 12px; font-family: 'Poppins', sans-serif; font-size: 24px;">MediNomix AI</div>
                <div style="color: #64748b; font-family: 'Inter', sans-serif; font-size: 16px;">Preventing medication errors with artificial intelligence</div>
            </div>
            <div style="border-top: 1px solid #e2e8f0; padding-top: 24px; color: #94a3b8; font-family: 'Inter', sans-serif; font-size: 14px;">
                <div style="margin-bottom: 12px;">© 2024 MediNomix AI. All rights reserved.</div>
                <div style="font-size: 13px; line-height: 1.6;">Disclaimer: This tool is for educational purposes and should not replace professional medical advice. Always consult healthcare professionals for medical decisions.</div>
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
        create_image_slider()  # Interactive image slider
        
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