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

# Base64 encoded images
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Medical icon as base64
medical_icon_base64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFiSURBVHic1ZO9SgNBFIVPymAENbYGX8FWtPIlLCwsLCwsLCwsrCx8hdhZ2FhYCLYxP2JjZ2FhIQgTCoXodY2fDnBdb8hFcevJHO7MfHNmuW+Mf5QA1sliEbgCHoE34H2Q8yvghPwQyf3qM5FqwB1wC1wAh0AX2AVawCqwAqwB+0AfOAEegE8X5AqYagJIAFNgAlz4tJ8B58AH8AW8JnzUAyaBYRNAtJ8DXoBnYK7m1VwBq3+mhMGAwzzmz9V8HAvI23xUeRl4iQUcRcL0Yz4eC+gqAGZVvwl0FIAO0IuE9YB2ckACkAD2gP1IwL6KxyYQwVXgFNgFOjYB1Q3gEXgD3oG9mo9HQdfe8vI5h2q13n6AR2DAc6Y08CQDdMFuSbg0e2rnrJkq32ZP7Zz15vtK7s2e2jlv+v+dg8xX9d+u4lVcBSwDe5Usf6YlK8Y3B7fL9Px7dGkAAAAASUVORK5CYII="

# ================================
# MEDICAL PROFESSIONAL COLOR SCHEME
# ================================

# Clean Medical Blue Theme
COLORS = {
    'primary': '#2A7DE1',           # Professional Medical Blue
    'primary_hover': '#1E6BC8',     # Darker Blue
    'secondary': '#34C759',         # Medical Green
    'success': '#30B67E',           # Success Green
    'warning': '#FF9500',           # Warning Orange
    'danger': '#FF3B30',            # Alert Red
    'info': '#5AC8FA',              # Info Light Blue
    'purple': '#AF52DE',            # Medical Purple
    'teal': '#5AC8FA',              # Teal
    'dark': '#1C1C1E',              # Dark Gray
    'light': '#F8F9FA',             # Light Gray
    'card_bg': '#FFFFFF',
    'sidebar_bg': '#2A7DE1',        # Blue Sidebar
    'border': '#E5E5EA',
    'text_primary': '#1C1C1E',
    'text_secondary': '#3C3C43',
    'text_muted': '#8E8E93',
    'shadow': 'rgba(42, 125, 225, 0.1)',
    'shadow_hover': 'rgba(42, 125, 225, 0.2)',
    'gradient_primary': 'linear-gradient(135deg, #2A7DE1 0%, #34C759 100%)',
    'gradient_secondary': 'linear-gradient(135deg, #34C759 0%, #5AC8FA 100%)',
    'gradient_success': 'linear-gradient(135deg, #30B67E 0%, #34C759 100%)',
    'gradient_warning': 'linear-gradient(135deg, #FF9500 0%, #FFD60A 100%)',
    'gradient_danger': 'linear-gradient(135deg, #FF3B30 0%, #FF9500 100%)',
    'gradient_purple': 'linear-gradient(135deg, #AF52DE 0%, #5AC8FA 100%)',
    'gradient_dark': 'linear-gradient(135deg, #1C1C1E 0%, #3C3C43 100%)',
    'gradient_sidebar': 'linear-gradient(180deg, #2A7DE1 0%, #1E6BC8 100%)'
}

# ================================
# PREMIUM CSS STYLING
# ================================

st.markdown(f"""
<style>
/* ========== CUSTOM SCROLLBAR ========== */
::-webkit-scrollbar {{
    width: 12px !important;
    height: 12px !important;
}}

::-webkit-scrollbar-track {{
    background: #F8F9FA !important;
    border-radius: 8px !important;
    margin: 4px !important;
}}

::-webkit-scrollbar-thumb {{
    background: {COLORS['primary']} !important;
    border-radius: 8px !important;
    border: 3px solid #F8F9FA !important;
    min-height: 40px !important;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {COLORS['primary_hover']} !important;
}}

/* For Firefox */
* {{
    scrollbar-width: thin !important;
    scrollbar-color: {COLORS['primary']} #F8F9FA !important;
}}

/* ========== GLOBAL STYLES ========== */
.stApp {{
    background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
    color: {COLORS['text_primary']};
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    scroll-behavior: smooth;
}}

/* ========== PLACEHOLDER TEXT VISIBLE ========== */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {{
    color: {COLORS['text_muted']} !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 400 !important;
}}

/* ========== ALL BUTTON STYLING ========== */
div.stButton > button:first-child {{
    background: {COLORS['gradient_primary']} !important;
    color: white !important;
    border: none !important;
    padding: 12px 28px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    min-height: 48px !important;
    box-shadow: 0 2px 8px {COLORS['shadow']} !important;
    position: relative !important;
    overflow: hidden !important;
}}

div.stButton > button:first-child:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px {COLORS['shadow_hover']} !important;
}}

/* Secondary Button Style */
div.stButton > button[kind="secondary"] {{
    background: white !important;
    color: {COLORS['primary']} !important;
    border: 2px solid {COLORS['primary']} !important;
    box-shadow: 0 2px 8px rgba(42, 125, 225, 0.1) !important;
}}

div.stButton > button[kind="secondary"]:hover {{
    background: {COLORS['primary']}10 !important;
}}

/* Small Button Style */
div.stButton > button[data-testid="baseButton-secondary"] {{
    background: white !important;
    color: {COLORS['purple']} !important;
    border: 2px solid {COLORS['purple']} !important;
}}

/* ========== GLASSMORPHISM CARDS ========== */
.glass-card {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid {COLORS['border']};
    box-shadow: 0 4px 20px {COLORS['shadow']};
    padding: 24px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}

.glass-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 30px {COLORS['shadow_hover']};
    border-color: {COLORS['primary']};
}}

.glass-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: {COLORS['gradient_primary']};
}}

.glass-card-header {{
    margin: -24px -24px 20px -24px;
    padding: 24px;
    background: {COLORS['gradient_primary']};
    border-radius: 16px 16px 0 0;
    position: relative;
    overflow: hidden;
}}

.glass-card-header h2 {{
    color: white !important;
    margin: 0 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}}

/* ========== USER GUIDE STYLING ========== */
.guide-container {{
    background: linear-gradient(135deg, #FFFFFF 0%, #F0F7FF 100%);
    border-radius: 20px;
    padding: 32px;
    margin: 24px 0;
    border: 2px solid {COLORS['primary']}20;
    box-shadow: 0 8px 30px rgba(42, 125, 225, 0.1);
}}

.guide-title {{
    text-align: center;
    color: {COLORS['primary']} !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    margin-bottom: 32px !important;
}}

.guide-step {{
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    border-left: 4px solid {COLORS['primary']};
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}}

.guide-step:hover {{
    transform: translateX(5px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}}

.step-header {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
}}

.step-icon {{
    font-size: 32px;
    color: {COLORS['primary']};
}}

.step-title {{
    color: {COLORS['text_primary']} !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    margin: 0 !important;
}}

.step-content {{
    color: {COLORS['text_secondary']} !important;
    font-size: 16px !important;
    line-height: 1.6;
    margin-left: 48px;
}}

.step-list {{
    margin: 12px 0 !important;
    padding-left: 20px !important;
}}

.step-list li {{
    margin-bottom: 8px !important;
    color: {COLORS['text_secondary']} !important;
    font-size: 16px !important;
}}

/* ========== IMAGE STYLING ========== */
.medical-image {{
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 12px;
    margin: 12px 0;
    border: 2px solid {COLORS['border']};
    box-shadow: 0 4px 15px {COLORS['shadow']};
    transition: all 0.3s ease;
}}

.medical-image:hover {{
    transform: scale(1.02);
    box-shadow: 0 8px 25px {COLORS['shadow_hover']};
    border-color: {COLORS['primary']};
}}

.drug-image {{
    width: 100%;
    height: 180px;
    object-fit: contain;
    background: #F8F9FA;
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
    border: 2px solid {COLORS['border']};
    box-shadow: 0 4px 15px {COLORS['shadow']};
}}

/* ========== STAT CARDS ========== */
.stat-card {{
    background: white;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    border: 2px solid {COLORS['border']};
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}

.stat-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 30px {COLORS['shadow_hover']};
    border-color: {COLORS['primary']};
}}

.stat-icon {{
    font-size: 40px;
    margin-bottom: 16px;
    color: {COLORS['primary']};
}}

.stat-number {{
    font-size: 36px;
    font-weight: 800;
    margin: 12px 0;
    color: {COLORS['primary']};
    line-height: 1;
}}

.stat-label {{
    color: {COLORS['text_secondary']};
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}}

/* ========== RISK BADGES ========== */
.risk-badge {{
    display: inline-flex;
    align-items: center;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    gap: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}}

.badge-critical {{
    background: {COLORS['gradient_danger']};
    color: white !important;
}}

.badge-high {{
    background: {COLORS['gradient_warning']};
    color: white !important;
}}

.badge-medium {{
    background: {COLORS['gradient_purple']};
    color: white !important;
}}

.badge-low {{
    background: {COLORS['gradient_success']};
    color: white !important;
}}

/* ========== METRIC BOXES ========== */
.metric-box {{
    background: white;
    border: 2px solid {COLORS['border']};
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px {COLORS['shadow']};
}}

.metric-box:hover {{
    border-color: {COLORS['primary']};
    transform: translateY(-2px);
}}

.metric-label {{
    color: {COLORS['text_secondary']};
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}}

.metric-value {{
    font-size: 24px;
    font-weight: 700;
    color: {COLORS['primary']};
    line-height: 1;
}}

/* ========== ALERTS ========== */
.neon-alert {{
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
    border-left: 4px solid;
    background: white;
    border-color: {COLORS['primary']};
    box-shadow: 0 4px 16px {COLORS['shadow']};
}}

.alert-success {{
    border-color: {COLORS['success']};
    background: linear-gradient(90deg, rgba(48, 182, 126, 0.1), white);
}}

.alert-danger {{
    border-color: {COLORS['danger']};
    background: linear-gradient(90deg, rgba(255, 59, 48, 0.1), white);
}}

.alert-info {{
    border-color: {COLORS['info']};
    background: linear-gradient(90deg, rgba(90, 200, 250, 0.1), white);
}}

/* ========== CHART CONTAINERS ========== */
.chart-section {{
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin: 24px 0;
    border: 1px solid {COLORS['border']};
    box-shadow: 0 4px 20px {COLORS['shadow']};
}}

.chart-title {{
    color: {COLORS['text_primary']} !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    margin-bottom: 20px !important;
}}

/* ========== PROFESSIONAL FOOTER ========== */
.professional-footer {{
    margin-top: 60px;
    padding: 40px 0;
    background: {COLORS['gradient_dark']};
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.footer-content {{
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
    color: white !important;
}}

.footer-logo {{
    font-size: 36px;
    margin-bottom: 16px;
    color: white;
}}

.footer-title {{
    color: white !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
}}

.footer-subtitle {{
    color: rgba(255, 255, 255, 0.8) !important;
    font-size: 16px !important;
    max-width: 600px;
    margin: 0 auto 24px !important;
    line-height: 1.6;
}}

.footer-disclaimer {{
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 20px;
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 14px !important;
}}

/* ========== HERO SECTION ========== */
.hero-section {{
    background: {COLORS['gradient_primary']};
    border-radius: 24px;
    padding: 60px 40px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    text-align: center;
    box-shadow: 0 8px 40px {COLORS['shadow_hover']};
}}

.hero-title {{
    color: white !important;
    font-size: 48px !important;
    font-weight: 800 !important;
    margin-bottom: 20px !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}}

.hero-subtitle {{
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 20px !important;
    max-width: 800px;
    margin: 0 auto 40px !important;
    line-height: 1.6;
}}

/* ========== FEATURE CARDS ========== */
.feature-card {{
    background: white;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    border: 2px solid {COLORS['border']};
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px {COLORS['shadow']};
    height: 100%;
}}

.feature-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 12px 30px {COLORS['shadow_hover']};
    border-color: {COLORS['primary']};
}}

.feature-icon {{
    font-size: 48px;
    margin-bottom: 20px;
    color: {COLORS['primary']};
}}

.feature-title {{
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
    color: {COLORS['text_primary']};
}}

.feature-desc {{
    color: {COLORS['text_secondary']};
    font-size: 14px;
    line-height: 1.6;
}}

/* ========== SEARCH BOX ========== */
.search-container {{
    background: white;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 8px 30px {COLORS['shadow']};
    border: 2px solid {COLORS['border']};
    margin: 32px 0;
    position: relative;
    overflow: hidden;
}}

.search-title {{
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 16px;
    color: {COLORS['text_primary']};
}}

.search-subtitle {{
    color: {COLORS['text_secondary']};
    font-size: 14px;
    margin-bottom: 24px;
}}

/* ========== PROFESSIONAL SIDEBAR ========== */
[data-testid="stSidebar"] {{
    background: {COLORS['gradient_sidebar']} !important;
    border-right: 2px solid rgba(255, 255, 255, 0.1) !important;
}}

.sidebar-header {{
    text-align: center;
    margin-bottom: 32px;
    padding: 32px 20px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

.sidebar-logo {{
    font-size: 48px;
    margin-bottom: 16px;
    color: white;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}}

.sidebar-title {{
    margin: 0 !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 24px !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}}

.sidebar-subtitle {{
    color: rgba(255, 255, 255, 0.9) !important;
    margin: 8px 0 0 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}}

/* ========== NAVIGATION TABS ========== */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: white;
    padding: 8px;
    border-radius: 12px;
    border: 1px solid {COLORS['border']};
    margin-bottom: 32px;
    box-shadow: 0 2px 8px {COLORS['shadow']};
}}

.stTabs [data-baseweb="tab"] {{
    height: 44px;
    padding: 0 20px;
    color: {COLORS['text_secondary']} !important;
    font-weight: 600;
    background: transparent !important;
    border-radius: 8px !important;
    border: none !important;
    transition: all 0.3s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: {COLORS['primary']}10 !important;
    transform: translateY(-1px);
}}

.stTabs [aria-selected="true"] {{
    background: {COLORS['gradient_primary']} !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(42, 125, 225, 0.3) !important;
    transform: translateY(-1px);
}}

/* ========== INPUT FIELDS ========== */
.stTextInput input, .stSelectbox select, .stTextArea textarea {{
    background: white !important;
    color: {COLORS['text_primary']} !important;
    border: 2px solid {COLORS['border']} !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    transition: all 0.3s ease !important;
}}

.stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {{
    border-color: {COLORS['primary']} !important;
    box-shadow: 0 0 0 3px {COLORS['primary']}20 !important;
    outline: none !important;
}}

/* ========== DATA FRAME STYLING ========== */
.dataframe {{
    background: white !important;
    color: {COLORS['text_primary']} !important;
    border: 1px solid {COLORS['border']} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 15px {COLORS['shadow']} !important;
}}

.dataframe th {{
    background: {COLORS['gradient_primary']} !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 16px !important;
    font-size: 14px !important;
}}

.dataframe td {{
    padding: 14px 16px !important;
    border-bottom: 1px solid {COLORS['border']} !important;
    font-weight: 400 !important;
}}

/* ========== EXPANDER STYLING ========== */
.streamlit-expanderHeader {{
    background: {COLORS['gradient_primary']} !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    margin-bottom: 8px !important;
    box-shadow: 0 2px 8px {COLORS['shadow']} !important;
}}

.streamlit-expanderHeader:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 15px {COLORS['shadow_hover']} !important;
}}

.streamlit-expanderContent {{
    background: white !important;
    border: 2px solid {COLORS['gradient_primary']} !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 15px {COLORS['shadow']} !important;
}}

/* ========== RADIO BUTTONS ========== */
.stRadio [role="radiogroup"] {{
    background: white;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid {COLORS['border']};
    box-shadow: 0 2px 8px {COLORS['shadow']};
}}

.stRadio label {{
    color: {COLORS['text_primary']} !important;
    font-weight: 500 !important;
}}

.stRadio [aria-checked="true"] + div label {{
    color: {COLORS['primary']} !important;
    font-weight: 600 !important;
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
            st.error(f"WebSocket connection error: {e}")
    
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
    """Create interactive drug confusion heatmap with annotations"""
    if 'heatmap' not in st.session_state.dashboard_data:
        return None
    
    heatmap_data = st.session_state.dashboard_data['heatmap']
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Create annotations for high-risk cells
    annotations = []
    for i, row in enumerate(risk_matrix):
        for j, value in enumerate(row):
            if value > 70:  # High risk values
                annotations.append(
                    dict(
                        x=j,
                        y=i,
                        text=f"<b>{value:.0f}%</b>",
                        showarrow=False,
                        font=dict(color="white", size=10, family="Inter"),
                        bgcolor="rgba(255, 59, 48, 0.8)",
                        bordercolor="white",
                        borderwidth=1,
                        borderpad=4
                    )
                )
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS['success']],
            [0.25, COLORS['secondary']],
            [0.5, COLORS['warning']],
            [0.75, COLORS['danger']],
            [1, COLORS['primary']]
        ],
        zmin=0,
        zmax=100,
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>Risk: <b>%{z:.1f}%</b><extra></extra>",
        colorbar=dict(
            title="Risk %",
            titleside="right",
            titlefont=dict(color=COLORS['text_primary'], size=12, family="Inter"),
            tickfont=dict(color=COLORS['text_primary'], size=10, family="Inter"),
            bgcolor="white",
            bordercolor=COLORS['border'],
            borderwidth=1
        ),
        text=[[f"{val:.1f}%" for val in row] for row in risk_matrix],
        texttemplate="%{text}",
        textfont=dict(color="white", size=9, family="Inter")
    ))
    
    fig.update_layout(
        title=dict(
            text="Drug Confusion Risk Heatmap",
            font=dict(color=COLORS['text_primary'], size=18, family="Inter"),
            x=0.5,
            xanchor="center"
        ),
        height=500,
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        xaxis=dict(
            tickfont=dict(color=COLORS['text_primary'], size=10, family="Inter"),
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            linewidth=1
        ),
        yaxis=dict(
            tickfont=dict(color=COLORS['text_primary'], size=10, family="Inter"),
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            linewidth=1
        ),
        margin=dict(l=100, r=50, t=60, b=100),
        annotations=annotations
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
        marker_colors=[COLORS['danger'], COLORS['warning'], COLORS['purple'], COLORS['success']],
        textinfo='label+percent',
        textposition='inside',
        hoverinfo='label+value+percent',
        textfont=dict(color='white', size=12, family='Inter'),
        marker_line=dict(color='white', width=1),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        title=dict(
            text="Risk Distribution",
            font=dict(color=COLORS['text_primary'], size=16, family="Inter"),
            x=0.5,
            xanchor="center"
        ),
        height=400,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        legend=dict(
            font=dict(size=12, color=COLORS['text_primary'], family="Inter"),
            bgcolor='white',
            bordercolor=COLORS['border'],
            borderwidth=1
        )
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
            marker_color=COLORS['primary'],
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            marker_line_color=COLORS['border'],
            marker_line_width=1,
            textfont=dict(size=11, color=COLORS['text_primary'], family="Inter"),
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><extra></extra>"
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Top 10 High-Risk Drug Pairs",
            font=dict(color=COLORS['text_primary'], size=16, family="Inter"),
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        xaxis=dict(
            gridcolor=COLORS['border'],
            gridwidth=1,
            tickfont=dict(color=COLORS['text_primary'], size=10, family="Inter"),
            linecolor=COLORS['border'],
            linewidth=1
        ),
        yaxis=dict(
            gridcolor=COLORS['border'],
            gridwidth=1,
            tickfont=dict(color=COLORS['text_primary'], size=10, family="Inter"),
            linecolor=COLORS['border'],
            linewidth=1
        ),
        margin=dict(l=150, r=50, t=60, b=50)
    )
    
    return fig

# ================================
# UI COMPONENTS
# ================================

def render_neon_alert(message, alert_type="info"):
    """Render a styled alert message"""
    
    if alert_type == "success":
        icon = "✅"
        alert_class = "alert-success"
        title = "Success!"
    elif alert_type == "warning":
        icon = "⚠️"
        alert_class = "alert-warning"
        title = "Warning!"
    elif alert_type == "danger":
        icon = "❌"
        alert_class = "alert-danger"
        title = "Error!"
    else:
        icon = "ℹ️"
        alert_class = "alert-info"
        title = "Info"
    
    st.markdown(f"""
    <div class="neon-alert {alert_class}">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="font-size: 24px; min-width: 32px;">{icon}</div>
            <div>
                <div style="font-weight: 700; font-size: 16px; margin-bottom: 4px;">{title}</div>
                <div style="color: {COLORS['text_secondary']}; font-size: 14px;">{message}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_stat_card(icon, value, label, col):
    """Render a statistic card"""
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-number">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

def render_feature_card(icon, title, description, col):
    """Render a feature card"""
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{description}</div>
        </div>
        """, unsafe_allow_html=True)

def render_metric_box(label, value, col):
    """Render a metric box"""
    with col:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

def render_glass_card(title, content=None):
    """Render a glassmorphism card"""
    st.markdown(f"""
    <div class="glass-card">
        <div class="glass-card-header">
            <h2>{title}</h2>
        </div>
        <div style="color: {COLORS['text_primary']};">{content if content else ""}</div>
    </div>
    """, unsafe_allow_html=True)

def render_guide_section():
    """Render user guide section"""
    st.markdown("""
    <div class="guide-container">
        <h2 class="guide-title">📚 User Guide</h2>
    """, unsafe_allow_html=True)
    
    # Step 1
    st.markdown("""
    <div class="guide-step">
        <div class="step-header">
            <div class="step-icon">🚀</div>
            <h3 class="step-title">Step 1: Search for a Medication</h3>
        </div>
        <div class="step-content">
            <p><strong>How to Search:</strong></p>
            <ul class="step-list">
                <li>Navigate to the <strong>Drug Analysis</strong> tab</li>
                <li>Enter any medication name (brand or generic)</li>
                <li>Click <strong>Analyze Drug</strong> to start the AI analysis</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 2
    st.markdown("""
    <div class="guide-step">
        <div class="step-header">
            <div class="step-icon">📊</div>
            <h3 class="step-title">Step 2: Review Risk Assessment</h3>
        </div>
        <div class="step-content">
            <p><strong>Understanding Results:</strong></p>
            <ul class="step-list">
                <li>View all similar drugs with confusion risks</li>
                <li>Filter by risk level (Critical, High, Medium, Low)</li>
                <li>Examine detailed similarity metrics</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 3
    st.markdown("""
    <div class="guide-step">
        <div class="step-header">
            <div class="step-icon">🛡️</div>
            <h3 class="step-title">Step 3: Take Preventive Action</h3>
        </div>
        <div class="step-content">
            <p><strong>Preventive Measures:</strong></p>
            <ul class="step-list">
                <li>Check <strong>Analytics</strong> tab for overall statistics</li>
                <li>Monitor <strong>Real-Time</strong> dashboard for live updates</li>
                <li>Use quick examples for demonstration</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================================
# HOMEPAGE
# ================================

def render_hero_section():
    """Render hero section"""
    
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">💊 MediNomix AI</h1>
        <p class="hero-subtitle">Advanced AI-powered system that analyzes drug names for potential confusion risks, helping healthcare professionals prevent medication errors and improve patient safety.</p>
        <div style="display: flex; gap: 16px; justify-content: center; margin-top: 32px;">
            <div class="stButton">
                <button data-testid="baseButton-primary">🚀 Start Analysis</button>
            </div>
            <div class="stButton">
                <button data-testid="baseButton-secondary">📖 View Documentation</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# DRUG ANALYSIS TAB
# ================================

def render_drug_analysis_tab():
    """Render Drug Analysis tab"""
    
    render_glass_card(
        "🔍 Drug Confusion Risk Analysis",
        "Search any medication to analyze confusion risks with similar drugs"
    )
    
    # Search Section
    st.markdown("""
    <div class="search-container">
        <div class="search-title">Search Medication</div>
        <div class="search-subtitle">Enter any drug name to analyze potential confusion risks</div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        drug_name = st.text_input(
            "",
            placeholder="Enter drug name (e.g., metformin, lamictal, celebrex...)",
            key="search_input",
            label_visibility="collapsed"
        )
    
    with col2:
        search_clicked = st.button("🔍 Analyze Drug", type="primary", use_container_width=True)
    
    with col3:
        if st.button("📚 Load Examples", type="secondary", use_container_width=True):
            with st.spinner("Loading examples..."):
                if load_examples():
                    render_neon_alert("Examples loaded successfully! Try searching: lamictal, celebrex, metformin", "success")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Examples with Images
    st.markdown("""
    <div style="margin: 24px 0;">
        <h3 style="color: {COLORS['text_primary']}; margin-bottom: 16px; font-weight: 700;">✨ Quick Examples:</h3>
    </div>
    """.format(COLORS=COLORS), unsafe_allow_html=True)
    
    examples = [
        {"name": "Lamictal", "image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
        {"name": "Metformin", "image": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
        {"name": "Celebrex", "image": "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
        {"name": "Clonidine", "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"}
    ]
    
    cols = st.columns(4)
    for idx, col in enumerate(cols):
        with col:
            # Display drug image
            st.markdown(f"""
            <img src="{examples[idx]['image']}" class="medical-image" alt="{examples[idx]['name']}">
            """, unsafe_allow_html=True)
            
            # Display button
            if st.button(f"💊 {examples[idx]['name']}", use_container_width=True, key=f"ex_{idx}"):
                with st.spinner(f"🔬 Analyzing {examples[idx]['name']}..."):
                    result = search_drug(examples[idx]['name'])
                    if result:
                        st.session_state.search_results = result.get('similar_drugs', [])
                        render_neon_alert(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.", "success")
                        st.rerun()
    
    # Handle Search
    if search_clicked and drug_name:
        with st.spinner(f"🧠 Analyzing '{drug_name}'..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                render_neon_alert(f"✅ Analysis complete! Found {len(st.session_state.search_results)} similar drugs.", "success")
                st.rerun()
            else:
                render_neon_alert("❌ Could not analyze drug. Please check backend connection.", "danger")
    
    # Results Section
    if st.session_state.search_results:
        st.markdown("""
        <div style="margin-top: 32px;">
            <h2 style="color: {COLORS['text_primary']}; margin-bottom: 20px; font-weight: 700;">📊 Analysis Results</h2>
        </div>
        """.format(COLORS=COLORS), unsafe_allow_html=True)
        
        # Risk Filters
        risk_filters = st.radio(
            "🎯 Filter by risk level:",
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
        
        # Display Results
        for result in filtered_results[:20]:
            risk_color_class = f"badge-{result['risk_category']}"
            
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <div>
                        <h3 style="margin: 0; color: {COLORS['text_primary']}; font-weight: 700;">{result['target_drug']['brand_name']}</h3>
                        {f"<p style='margin: 8px 0 0 0; color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 500;'>Generic: {result['target_drug']['generic_name']}</p>" if result['target_drug']['generic_name'] else ""}
                    </div>
                    <div style="text-align: center;">
                        <div class="metric-value" style="font-size: 36px;">
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
                    render_metric_box(label, value, col)
            
            st.markdown("</div>")

# ================================
# ANALYTICS DASHBOARD TAB
# ================================

def render_analytics_tab():
    """Render Analytics Dashboard tab"""
    
    render_glass_card(
        "📊 Medication Safety Analytics Dashboard",
        "Real-time insights and analytics for medication safety monitoring"
    )
    
    # Load data if needed
    if 'metrics' not in st.session_state.dashboard_data:
        with st.spinner("📡 Loading analytics data..."):
            load_dashboard_data()
    
    # KPI Cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_stat_card("💊", metrics.get('total_drugs', 0), "Total Drugs", col1)
        
        with col2:
            render_stat_card("🔥", metrics.get('critical_risk_pairs', 0), "Critical Pairs", col2)
        
        with col3:
            render_stat_card("⚠️", metrics.get('high_risk_pairs', 0), "High Risk Pairs", col3)
        
        with col4:
            avg_score = metrics.get('avg_risk_score', 0)
            render_stat_card("📈", f"{avg_score:.1f}%", "Avg Risk Score", col4)
    
    # Charts Section - Each chart in separate row
    st.markdown("""
    <div style="margin: 32px 0;">
        <h2 style="color: {COLORS['text_primary']}; margin-bottom: 24px; font-weight: 700;">📈 Analytics Charts</h2>
    </div>
    """.format(COLORS=COLORS), unsafe_allow_html=True)
    
    # Chart 1: Risk Distribution
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Risk Distribution</h3>', unsafe_allow_html=True)
    breakdown_chart = create_risk_breakdown_chart()
    if breakdown_chart:
        st.plotly_chart(breakdown_chart, use_container_width=True)
    else:
        st.info("No risk breakdown data available")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 2: Top Risk Pairs
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Top 10 High-Risk Drug Pairs</h3>', unsafe_allow_html=True)
    risks_chart = create_top_risks_chart()
    if risks_chart:
        st.plotly_chart(risks_chart, use_container_width=True)
    else:
        st.info("No top risk data available")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 3: Heatmap
    st.markdown('<div class="chart-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Drug Confusion Risk Heatmap</h3>', unsafe_allow_html=True)
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown(f"""
        <div style="text-align: center; margin-top: 16px; color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600;">
            🟢 Low Risk &nbsp;&nbsp; 🟢 Medium Risk &nbsp;&nbsp; 🟡 High Risk &nbsp;&nbsp; 🔴 Critical Risk
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs first.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FDA Alerts Section
    render_glass_card("🚨 FDA High Alert Drug Pairs", "Most commonly confused drug pairs according to FDA")
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", "Reason": "Epilepsy medication vs Antifungal", "Severity": "🔴"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", "Reason": "Arthritis vs Depression medication", "Severity": "🔴"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", "Reason": "Diabetes vs Antibiotic", "Severity": "🟠"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", "Reason": "Blood Pressure vs Anxiety medication", "Severity": "🟠"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", "Reason": "Antipsychotic vs Allergy medication", "Severity": "🟡"},
    ])
    
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Severity": st.column_config.TextColumn("⚠️ Severity", width="small")
        }
    )

# ================================
# REAL-TIME DASHBOARD TAB
# ================================

def render_realtime_tab():
    """Render Real-Time Dashboard tab"""
    
    render_glass_card(
        "⚡ Real-Time Medication Safety Dashboard",
        "Live monitoring and real-time analytics for medication safety"
    )
    
    # Connection Status
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.websocket_connected:
            render_neon_alert("✅ Real-time Connection Active - Live data streaming enabled", "success")
        else:
            render_neon_alert("🔌 Connecting to Real-Time Server - Live updates will appear here", "info")
    
    with col2:
        if st.button("🔄 Refresh Connection", type="primary", use_container_width=True):
            websocket_manager.start_connection()
            st.rerun()
    
    # Auto-start WebSocket if not connected
    if not st.session_state.websocket_connected:
        websocket_manager.start_connection()
    
    # Display Real-time Metrics
    metrics = st.session_state.realtime_metrics or {}
    
    if metrics:
        # Real-time KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_stat_card("📊", metrics.get('total_drugs', 0), "Live Drugs", col1)
        
        with col2:
            render_stat_card("🔥", metrics.get('critical_risk_pairs', 0), "Critical Now", col2)
        
        with col3:
            avg_score = metrics.get('avg_risk_score', 0)
            render_stat_card("📈", f"{avg_score:.1f}%", "Avg Risk", col3)
        
        with col4:
            clients = metrics.get('connected_clients', 0)
            render_stat_card("👥", clients, "Connected", col4)
        
        # Recent Activity Section
        render_glass_card("🕒 Recent Activity Timeline", "Latest drug analysis activities")
        
        if metrics.get('recent_searches'):
            for idx, search in enumerate(metrics['recent_searches'][:5]):
                timestamp = search.get('timestamp', '')
                drug_name = search.get('drug_name', 'Unknown')
                similar_drugs = search.get('similar_drugs_found', 0)
                highest_risk = search.get('highest_risk', 0)
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 16px; background: linear-gradient(135deg, {COLORS['primary']}10, transparent); border-radius: 12px; margin-bottom: 12px; border: 1px solid {COLORS['border']}">
                    <div style="margin-right: 16px;">
                        <div style="width: 40px; height: 40px; background: {COLORS['primary']}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 16px;">{idx+1}</div>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 700; color: {COLORS['text_primary']}; font-size: 16px;">💊 {drug_name}</div>
                        <div style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 500;">Found {similar_drugs} similar drugs • Highest risk: {highest_risk:.1f}%</div>
                    </div>
                    <div style="color: {COLORS['text_muted']}; font-size: 12px; font-weight: 600;">{timestamp[:19] if timestamp else 'Just now'}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity data available")
        
        # System Status
        render_glass_card("⚙️ System Status", "Current system health and status")
        
        status = metrics.get('system_status', 'unknown')
        if status == 'healthy':
            status_color = COLORS['success']
            status_icon = "✅"
            status_text = "All Systems Operational"
        else:
            status_color = COLORS['warning']
            status_icon = "⚠️"
            status_text = "System Issues Detected"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="glass-card">
                <div style="text-align: center;">
                    <div style="font-size: 40px; margin-bottom: 12px; color: {status_color};">{status_icon}</div>
                    <div style="font-weight: 700; color: {COLORS['text_primary']}; font-size: 18px;">{status_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="glass-card">
                <div style="text-align: center;">
                    <div style="font-size: 40px; margin-bottom: 12px; color: {COLORS['info']};">🕐</div>
                    <div style="font-weight: 700; color: {COLORS['text_primary']}; font-size: 18px;">{metrics.get('last_updated', '')[:19]}</div>
                    <div style="color: {COLORS['text_secondary']}; margin-top: 8px;">Last Updated</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 60px 32px;">
            <div style="font-size: 72px; margin-bottom: 24px; color: {COLORS['primary']}">⏳</div>
            <h2 style="color: {COLORS['text_primary']}; margin-bottom: 16px; font-weight: 700;">Waiting for Real-Time Data</h2>
            <p style="color: {COLORS['text_secondary']}; max-width: 500px; margin: 0 auto; font-size: 16px; font-weight: 500;">Live updates will appear here once connection is established.</p>
        </div>
        """, unsafe_allow_html=True)

# ================================
# SIDEBAR
# ================================

def render_sidebar():
    """Render sidebar with system status"""
    
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-header">
            <div class="sidebar-logo">💊</div>
            <h2 class="sidebar-title">MediNomix</h2>
            <p class="sidebar-subtitle">AI Medication Safety</p>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Card
        render_glass_card("📡 System Status")
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    render_neon_alert("✅ Backend Connected", "success")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("💊 Drugs", data.get('metrics', {}).get('drugs_in_database', 0))
                    with col2:
                        st.metric("📊 Analyses", data.get('metrics', {}).get('total_analyses', 0))
                else:
                    render_neon_alert("⚠️ Backend Issues", "warning")
            else:
                render_neon_alert("❌ Cannot Connect", "danger")
        except:
            render_neon_alert("🔌 Backend Not Running", "danger")
            st.code("python backend.py", language="bash")
        
        # Quick Links with Premium Buttons
        render_glass_card("🔗 Quick Links")
        
        if st.button("📚 Documentation", use_container_width=True):
            render_neon_alert("Documentation coming soon!", "info")
        
        if st.button("🐛 Report Bug", use_container_width=True):
            render_neon_alert("Bug reporting coming soon!", "info")
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            render_neon_alert("Cache cleared successfully!", "success")
            st.rerun()
        
        # Risk Categories Guide
        render_glass_card("⚠️ Risk Categories")
        
        risk_levels = [
            ("Critical", "≥75%", "Immediate attention required", "badge-critical"),
            ("High", "50-74%", "Review and verify", "badge-high"),
            ("Medium", "25-49%", "Monitor closely", "badge-medium"),
            ("Low", "<25%", "Low priority", "badge-low")
        ]
        
        for name, score, desc, badge_class in risk_levels:
            st.markdown(f"""
            <div style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid {COLORS['border']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span class="risk-badge {badge_class}" style="font-size: 11px; padding: 6px 12px;">{name}</span>
                    <span style="font-weight: 700; color: {COLORS['text_primary']}; font-size: 14px;">{score}</span>
                </div>
                <div style="color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 500;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ================================
# PROFESSIONAL FOOTER
# ================================

def render_footer():
    """Render professional footer"""
    
    st.markdown(f"""
    <div class="professional-footer">
        <div class="footer-content">
            <div class="footer-logo">💊</div>
            <h3 class="footer-title">MediNomix AI</h3>
            <p class="footer-subtitle">Preventing medication errors with artificial intelligence</p>
            <div class="footer-disclaimer">
                <div style="margin-bottom: 8px; font-weight: 600;">© 2024 MediNomix AI. All rights reserved.</div>
                <div>Disclaimer: This tool is for educational purposes and should not replace professional medical advice.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# MAIN APPLICATION
# ================================

def main():
    """Main application renderer"""
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔍 Drug Analysis", "📊 Analytics", "⚡ Real-Time"])
    
    with tab1:
        render_hero_section()
        
        # Stats Counter
        col1, col2, col3, col4 = st.columns(4)
        render_stat_card("👥", "1.5M+", "Patients Protected", col1)
        render_stat_card("💰", "$42B", "Cost Saved", col2)
        render_stat_card("🎯", "99.8%", "Accuracy Rate", col3)
        render_stat_card("💊", "50K+", "Drugs Analyzed", col4)
        
        # Features Section with Images
        st.markdown("""
        <div style="margin: 48px 0;">
            <h2 style="text-align: center; margin-bottom: 32px; color: {COLORS['text_primary']}; font-weight: 700;">✨ How MediNomix Works</h2>
        </div>
        """.format(COLORS=COLORS), unsafe_allow_html=True)
        
        features_cols = st.columns(3)
        features = [
            {"icon": "🔍", "title": "Search Medication", "desc": "Enter any drug name to analyze potential confusion risks"},
            {"icon": "🧠", "title": "AI Analysis", "desc": "Our AI analyzes spelling, phonetic, and therapeutic similarities"},
            {"icon": "🛡️", "title": "Risk Prevention", "desc": "Get detailed risk assessments and prevention recommendations"}
        ]
        
        # Add images for features
        feature_images = [
            "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80"
        ]
        
        for idx, col in enumerate(features_cols):
            with col:
                # Display image
                st.markdown(f"""
                <img src="{feature_images[idx]}" class="medical-image" alt="{features[idx]['title']}">
                """, unsafe_allow_html=True)
                
                # Display feature card
                feature = features[idx]
                render_feature_card(feature['icon'], feature['title'], feature['desc'], col)
        
        # User Guide Section
        render_guide_section()
        
        # Trust Section with Images
        render_glass_card("🏥 Trusted by Healthcare Professionals")
        
        # Medical images grid
        medical_images = [
            "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w-300&q=80",
            "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
            "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
            "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"
        ]
        
        cols = st.columns(4)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <img src="{medical_images[idx]}" class="medical-image" alt="Medical Facility {idx+1}">
                """, unsafe_allow_html=True)
    
    with tab2:
        render_drug_analysis_tab()
    
    with tab3:
        render_analytics_tab()
    
    with tab4:
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