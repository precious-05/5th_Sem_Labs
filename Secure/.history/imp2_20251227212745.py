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

# ================================
# DUAL THEME SYSTEM
# ================================

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'  # default to light theme

# Dual Theme Color Schemes
THEMES = {
    'light': {
        'primary': '#2563eb',          # Blue 600
        'primary_hover': '#1d4ed8',    # Blue 700
        'secondary': '#7c3aed',        # Purple 600
        'success': '#059669',          # Emerald 600
        'warning': '#d97706',          # Amber 600
        'danger': '#dc2626',           # Red 600
        'info': '#0891b2',             # Cyan 600
        'dark': '#1e293b',             # Slate 800
        'light': '#f8fafc',            # Slate 50
        'card_bg': '#ffffff',
        'sidebar_bg': '#f1f5f9',
        'border': '#e2e8f0',
        'text_primary': '#1e293b',
        'text_secondary': '#64748b',
        'text_muted': '#94a3b8',
        'shadow': 'rgba(0, 0, 0, 0.08)',
        'shadow_hover': 'rgba(0, 0, 0, 0.12)',
        'gradient_primary': 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
        'gradient_success': 'linear-gradient(135deg, #059669 0%, #10b981 100%)',
        'gradient_warning': 'linear-gradient(135deg, #d97706 0%, #f59e0b 100%)',
        'gradient_danger': 'linear-gradient(135deg, #dc2626 0%, #ef4444 100%)',
        'gradient_dark': 'linear-gradient(135deg, #1e293b 0%, #334155 100%)'
    },
    'dark': {
        'primary': '#60a5fa',          # Blue 400
        'primary_hover': '#93c5fd',    # Blue 300
        'secondary': '#a78bfa',        # Purple 400
        'success': '#34d399',          # Emerald 400
        'warning': '#fbbf24',          # Amber 400
        'danger': '#f87171',           # Red 400
        'info': '#22d3ee',             # Cyan 400
        'dark': '#0f172a',             # Slate 900
        'light': '#1e293b',            # Slate 800
        'card_bg': '#334155',
        'sidebar_bg': '#1e293b',
        'border': '#475569',
        'text_primary': '#f1f5f9',
        'text_secondary': '#cbd5e1',
        'text_muted': '#94a3b8',
        'shadow': 'rgba(0, 0, 0, 0.25)',
        'shadow_hover': 'rgba(0, 0, 0, 0.35)',
        'gradient_primary': 'linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%)',
        'gradient_success': 'linear-gradient(135deg, #34d399 0%, #10b981 100%)',
        'gradient_warning': 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)',
        'gradient_danger': 'linear-gradient(135deg, #f87171 0%, #ef4444 100%)',
        'gradient_dark': 'linear-gradient(135deg, #334155 0%, #475569 100%)'
    }
}

# Get current theme colors
def get_theme_colors():
    return THEMES[st.session_state.theme]

# ================================
# PREMIUM CSS STYLING
# ================================

def apply_custom_css():
    """Apply custom CSS with dual theme support"""
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
    /* ========== GLOBAL STYLES ========== */
    .stApp {{
        background-color: {colors['light']};
        color: {colors['text_primary']};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3, h4, h5, h6 {{
        color: {colors['text_primary']} !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }}
    
    p, span, div {{
        color: {colors['text_primary']} !important;
    }}
    
    /* ========== PREMIUM CARDS ========== */
    .premium-card {{
        background: {colors['card_bg']};
        border-radius: 16px;
        border: 1px solid {colors['border']};
        box-shadow: 0 4px 20px {colors['shadow']};
        padding: 24px;
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .premium-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 32px {colors['shadow_hover']};
        border-color: {colors['primary']};
    }}
    
    .premium-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: {colors['gradient_primary']};
    }}
    
    .card-header {{
        margin: -24px -24px 20px -24px;
        padding: 24px;
        background: {colors['gradient_dark']};
        border-radius: 16px 16px 0 0;
    }}
    
    .card-header h2 {{
        color: white !important;
        margin: 0 !important;
    }}
    
    /* ========== GRADIENT BUTTONS ========== */
    .gradient-btn {{
        background: {colors['gradient_primary']};
        color: white !important;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-decoration: none;
        min-height: 44px;
    }}
    
    .gradient-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
        opacity: 0.95;
    }}
    
    .secondary-btn {{
        background: {colors['card_bg']};
        color: {colors['text_primary']} !important;
        border: 2px solid {colors['border']};
        padding: 10px 24px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .secondary-btn:hover {{
        background: {colors['light']};
        border-color: {colors['primary']};
        transform: translateY(-2px);
    }}
    
    .success-btn {{
        background: {colors['gradient_success']};
        color: white !important;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .danger-btn {{
        background: {colors['gradient_danger']};
        color: white !important;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    /* ========== NAVIGATION ========== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {colors['card_bg']};
        padding: 8px;
        border-radius: 12px;
        border: 1px solid {colors['border']};
        margin-bottom: 32px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 44px;
        padding: 0 20px;
        color: {colors['text_secondary']} !important;
        font-weight: 600;
        background: transparent !important;
        border-radius: 8px !important;
        border: none !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {colors['gradient_primary']} !important;
        color: white !important;
    }}
    
    /* ========== STAT CARDS ========== */
    .stat-card {{
        background: {colors['card_bg']};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 1px solid {colors['border']};
        transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px {colors['shadow']};
        border-color: {colors['primary']};
    }}
    
    .stat-icon {{
        font-size: 40px;
        margin-bottom: 16px;
        background: {colors['gradient_primary']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .stat-number {{
        font-size: 36px;
        font-weight: 800;
        margin: 12px 0;
        background: {colors['gradient_primary']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }}
    
    .stat-label {{
        color: {colors['text_secondary']};
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
    
    /* ========== INPUT FIELDS ========== */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {{
        background: {colors['card_bg']} !important;
        color: {colors['text_primary']} !important;
        border: 2px solid {colors['border']} !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }}
    
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {{
        border-color: {colors['primary']} !important;
        box-shadow: 0 0 0 3px {colors['primary']}20 !important;
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
    }}
    
    .badge-critical {{
        background: {colors['gradient_danger']};
        color: white !important;
    }}
    
    .badge-high {{
        background: {colors['gradient_warning']};
        color: white !important;
    }}
    
    .badge-medium {{
        background: {colors['gradient_primary']};
        color: white !important;
    }}
    
    .badge-low {{
        background: {colors['gradient_success']};
        color: white !important;
    }}
    
    /* ========== METRIC BOXES ========== */
    .metric-box {{
        background: {colors['light']};
        border: 2px solid {colors['border']};
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .metric-box:hover {{
        border-color: {colors['primary']};
        transform: translateY(-2px);
    }}
    
    .metric-label {{
        color: {colors['text_secondary']};
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }}
    
    .metric-value {{
        font-size: 28px;
        font-weight: 800;
        background: {colors['gradient_primary']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }}
    
    /* ========== ALERTS & MESSAGES ========== */
    .custom-alert {{
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        border-left: 4px solid;
        background: {colors['card_bg']};
        border-color: {colors['primary']};
        box-shadow: 0 4px 16px {colors['shadow']};
    }}
    
    .alert-success {{
        border-color: {colors['success']};
        background: linear-gradient(90deg, rgba(5, 150, 105, 0.1), {colors['card_bg']});
    }}
    
    .alert-warning {{
        border-color: {colors['warning']};
        background: linear-gradient(90deg, rgba(217, 119, 6, 0.1), {colors['card_bg']});
    }}
    
    .alert-danger {{
        border-color: {colors['danger']};
        background: linear-gradient(90deg, rgba(220, 38, 38, 0.1), {colors['card_bg']});
    }}
    
    .alert-info {{
        border-color: {colors['info']};
        background: linear-gradient(90deg, rgba(8, 145, 178, 0.1), {colors['card_bg']});
    }}
    
    /* ========== TABLES ========== */
    .dataframe {{
        background: {colors['card_bg']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}
    
    .dataframe th {{
        background: {colors['gradient_dark']} !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 16px !important;
    }}
    
    .dataframe td {{
        padding: 14px 16px !important;
        border-bottom: 1px solid {colors['border']} !important;
    }}
    
    .dataframe tr:hover {{
        background: {colors['light']} !important;
    }}
    
    /* ========== SIDEBAR ========== */
    [data-testid="stSidebar"] {{
        background: {colors['sidebar_bg']} !important;
        border-right: 1px solid {colors['border']} !important;
    }}
    
    [data-testid="stSidebar"] .premium-card {{
        background: {colors['card_bg']};
    }}
    
    /* ========== LOADING ANIMATION ========== */
    .loading-spinner {{
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 4px solid {colors['border']};
        border-top: 4px solid {colors['primary']};
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['light']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['primary']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['primary_hover']};
    }}
    
    /* ========== EXPANDERS ========== */
    .streamlit-expanderHeader {{
        background: {colors['light']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-weight: 600 !important;
    }}
    
    .streamlit-expanderContent {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 20px !important;
    }}
    
    /* ========== METRICS ========== */
    [data-testid="stMetricValue"] {{
        font-size: 28px !important;
        font-weight: 800 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {colors['text_secondary']} !important;
        font-weight: 600 !important;
    }}
    
    /* ========== RADIO BUTTONS ========== */
    .stRadio [role="radiogroup"] {{
        background: {colors['card_bg']};
        padding: 12px;
        border-radius: 12px;
        border: 1px solid {colors['border']};
    }}
    
    .stRadio label {{
        color: {colors['text_primary']} !important;
    }}
    
    .stRadio [data-baseweb="radio"] div:first-child {{
        background-color: {colors['card_bg']} !important;
        border-color: {colors['border']} !important;
    }}
    
    /* ========== FOOTER ========== */
    .custom-footer {{
        margin-top: 60px;
        padding: 40px 0;
        background: {colors['gradient_dark']};
        border-radius: 24px 24px 0 0;
        text-align: center;
        color: white !important;
    }}
    
    .custom-footer h3 {{
        color: white !important;
    }}
    
    .custom-footer p {{
        color: rgba(255, 255, 255, 0.8) !important;
    }}
    
    /* ========== THEME TOGGLE ========== */
    .theme-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }}
    
    .theme-btn {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: {colors['gradient_primary']};
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 16px {colors['shadow']};
        transition: all 0.3s ease;
    }}
    
    .theme-btn:hover {{
        transform: rotate(30deg);
        box-shadow: 0 8px 24px {colors['shadow_hover']};
    }}
    </style>
    
    <script>
    // Theme persistence
    document.addEventListener('DOMContentLoaded', function() {{
        const theme = localStorage.getItem('medi_nomix_theme') || 'light';
        document.body.setAttribute('data-theme', theme);
        
        // Add theme toggle button
        const themeToggle = document.createElement('div');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = `
            <button class="theme-btn" onclick="toggleTheme()">
                ${{theme === 'light' ? '🌙' : '☀️'}}
            </button>
        `;
        document.body.appendChild(themeToggle);
    }});
    
    function toggleTheme() {{
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('medi_nomix_theme', newTheme);
        
        // Update button icon
        document.querySelector('.theme-btn').innerHTML = newTheme === 'light' ? '🌙' : '☀️';
        
        // Send message to Streamlit
        window.parent.postMessage({{type: 'set_theme', theme: newTheme}}, '*');
    }}
    </script>
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

# Apply custom CSS
apply_custom_css()

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
    
    colors = get_theme_colors()
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
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['card_bg'],
        font_color=colors['text_primary']
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
    colors = get_theme_colors()
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=counts,
        hole=0.5,
        marker_colors=[colors['danger'], colors['warning'], colors['primary'], colors['success']]
    )])
    
    fig.update_layout(
        title="Risk Distribution",
        height=400,
        showlegend=True,
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['card_bg'],
        font_color=colors['text_primary']
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
    colors = get_theme_colors()
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color=colors['secondary'],
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Top 10 High-Risk Drug Pairs",
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=500,
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['card_bg'],
        font_color=colors['text_primary']
    )
    
    return fig

# ================================
# PREMIUM UI COMPONENTS
# ================================

def render_premium_card(title, content=None, col=None):
    """Render a premium styled card"""
    colors = get_theme_colors()
    
    if col:
        with col:
            st.markdown(f"""
            <div class="premium-card">
                <div class="card-header">
                    <h2>{title}</h2>
                </div>
                <div style="color: {colors['text_primary']};">{content if content else ""}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-header">
                <h2>{title}</h2>
            </div>
            <div style="color: {colors['text_primary']};">{content if content else ""}</div>
        </div>
        """, unsafe_allow_html=True)

def render_stat_card(icon, value, label, col):
    """Render a statistic card"""
    with col:
        colors = get_theme_colors()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-number">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

def render_alert(message, alert_type="info"):
    """Render a styled alert message"""
    colors = get_theme_colors()
    
    if alert_type == "success":
        icon = "✅"
        alert_class = "alert-success"
    elif alert_type == "warning":
        icon = "⚠️"
        alert_class = "alert-warning"
    elif alert_type == "danger":
        icon = "❌"
        alert_class = "alert-danger"
    else:
        icon = "ℹ️"
        alert_class = "alert-info"
    
    st.markdown(f"""
    <div class="custom-alert {alert_class}">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 24px;">{icon}</div>
            <div>
                <div style="font-weight: 600; margin-bottom: 4px;">{message}</div>
                <div style="font-size: 14px; color: {colors['text_secondary']};">Click to dismiss</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_box(label, value, col):
    """Render a metric box"""
    with col:
        colors = get_theme_colors()
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ================================
# HOMEPAGE COMPONENTS
# ================================

def render_hero_section():
    """Render hero/jumbotron section"""
    colors = get_theme_colors()
    
    st.markdown(f"""
    <div class="premium-card" style="background: {colors['gradient_dark']}; color: white; border: none;">
        <div style="text-align: center; padding: 60px 40px;">
            <div style="font-size: 64px; margin-bottom: 24px;">💊</div>
            <h1 style="color: white !important; font-size: 48px; margin-bottom: 20px;">MediNomix AI</h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 20px; max-width: 800px; margin: 0 auto 40px;">
                Advanced AI-powered system that analyzes drug names for potential confusion risks, 
                helping healthcare professionals prevent medication errors and improve patient safety.
            </p>
            <div style="display: flex; gap: 16px; justify-content: center;">
                <button class="gradient-btn" onclick="window.location.href='#analysis'">
                    🚀 Start Analysis
                </button>
                <button class="secondary-btn" style="color: white !important; border-color: rgba(255, 255, 255, 0.3);">
                    📖 Learn More
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# DRUG ANALYSIS TAB
# ================================

def render_drug_analysis_tab():
    """Render Drug Analysis tab with premium styling"""
    colors = get_theme_colors()
    
    render_premium_card(
        "🔍 Drug Confusion Risk Analysis",
        "Search any medication to analyze confusion risks with similar drugs"
    )
    
    # Search Section
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h3 style="color: #2d3748; margin-bottom: 16px;">Search Medication</h3>
    </div>
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
                    render_alert("Examples loaded successfully! Try searching: lamictal, celebrex, metformin", "success")
    
    # Quick Examples
    st.markdown("""
    <div style="margin: 24px 0;">
        <p style="color: #64748b; margin-bottom: 12px; font-weight: 600;">Quick Examples:</p>
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
                        render_alert(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.", "success")
                        st.rerun()
    
    # Handle Search
    if search_clicked and drug_name:
        with st.spinner(f"🧠 Analyzing '{drug_name}'..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                render_alert(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.", "success")
                st.rerun()
            else:
                render_alert("Could not analyze drug. Please check backend connection.", "danger")
    
    # Results Section
    if st.session_state.search_results:
        st.markdown("""
        <div style="margin-top: 40px;">
            <h3 style="color: #2d3748; margin-bottom: 24px;">📊 Analysis Results</h3>
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
        
        # Display Results
        for result in filtered_results[:20]:
            risk_color_class = f"badge-{result['risk_category']}"
            
            st.markdown(f"""
            <div class="premium-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                    <div>
                        <h3 style="margin: 0; color: {colors['text_primary']};">{result['target_drug']['brand_name']}</h3>
                        {f"<p style='margin: 8px 0 0 0; color: {colors['text_secondary']}; font-size: 14px;'>Generic: {result['target_drug']['generic_name']}</p>" if result['target_drug']['generic_name'] else ""}
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
    colors = get_theme_colors()
    
    render_premium_card(
        "📊 Medication Safety Analytics Dashboard",
        "Real-time insights and analytics for medication safety monitoring"
    )
    
    # Load data if needed
    if 'metrics' not in st.session_state.dashboard_data:
        with st.spinner("Loading analytics data..."):
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
    
    # Charts Section
    st.markdown("""
    <div style="margin: 40px 0;">
        <h3 style="color: #2d3748; margin-bottom: 24px;">Analytics Charts</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_premium_card("Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available")
    
    with col2:
        render_premium_card("Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available")
    
    # Heatmap Section
    render_premium_card("Drug Confusion Risk Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px; color: {colors['text_secondary']}; font-size: 14px;">
            🟢 Low Risk &nbsp;&nbsp; 🟡 Medium Risk &nbsp;&nbsp; 🔴 High Risk
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs first.")
    
    # FDA Alerts Section
    render_premium_card("🚨 FDA High Alert Drug Pairs", "Most commonly confused drug pairs according to FDA")
    
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
            "Severity": st.column_config.TextColumn("Severity", width="small")
        }
    )

# ================================
# REAL-TIME DASHBOARD TAB
# ================================

def render_realtime_tab():
    """Render Real-Time Dashboard tab"""
    colors = get_theme_colors()
    
    render_premium_card(
        "⚡ Real-Time Medication Safety Dashboard",
        "Live monitoring and real-time analytics for medication safety"
    )
    
    # Connection Status
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.websocket_connected:
            render_alert("Real-time Connection Active - Live data streaming enabled", "success")
        else:
            render_alert("Connecting to Real-Time Server - Live updates will appear here", "info")
    
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
        render_premium_card("🕒 Recent Activity Timeline", "Latest drug analysis activities")
        
        if metrics.get('recent_searches'):
            for idx, search in enumerate(metrics['recent_searches'][:5]):
                timestamp = search.get('timestamp', '')
                drug_name = search.get('drug_name', 'Unknown')
                similar_drugs = search.get('similar_drugs_found', 0)
                highest_risk = search.get('highest_risk', 0)
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 16px; background: {colors['light']}; border-radius: 12px; margin-bottom: 12px; border: 1px solid {colors['border']}">
                    <div style="margin-right: 16px;">
                        <div style="width: 40px; height: 40px; background: {colors['gradient_primary']}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{idx+1}</div>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 700; color: {colors['text_primary']};">{drug_name}</div>
                        <div style="color: {colors['text_secondary']}; font-size: 14px;">Found {similar_drugs} similar drugs • Highest risk: {highest_risk:.1f}%</div>
                    </div>
                    <div style="color: {colors['text_muted']}; font-size: 12px;">{timestamp[:19] if timestamp else 'Just now'}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity data available")
        
        # System Status
        render_premium_card("⚙️ System Status", "Current system health and status")
        
        status = metrics.get('system_status', 'unknown')
        if status == 'healthy':
            status_color = colors['success']
            status_icon = "✅"
            status_text = "All Systems Operational"
        else:
            status_color = colors['warning']
            status_icon = "⚠️"
            status_text = "System Issues Detected"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background: {colors['light']}; padding: 20px; border-radius: 12px; border: 1px solid {colors['border']}">
                <div style="color: {colors['text_secondary']}; font-size: 14px; margin-bottom: 8px;">Status</div>
                <div style="font-weight: 700; color: {status_color}; font-size: 18px;">{status_icon} {status_text}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: {colors['light']}; padding: 20px; border-radius: 12px; border: 1px solid {colors['border']}">
                <div style="color: {colors['text_secondary']}; font-size: 14px; margin-bottom: 8px;">Last Updated</div>
                <div style="font-weight: 700; color: {colors['text_primary']}; font-size: 18px;">{metrics.get('last_updated', '')[:19]}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 64px; margin-bottom: 24px; color: {colors['text_muted']}">⏳</div>
            <h3 style="color: {colors['text_primary']}; margin-bottom: 16px;">Waiting for Real-Time Data</h3>
            <p style="color: {colors['text_secondary']}; max-width: 500px; margin: 0 auto;">Live updates will appear here once connection is established.</p>
        </div>
        """, unsafe_allow_html=True)

# ================================
# SIDEBAR
# ================================

def render_sidebar():
    """Render sidebar with system status"""
    colors = get_theme_colors()
    
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 32px;">
            <div style="font-size: 48px; margin-bottom: 16px; background: {colors['gradient_primary']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">💊</div>
            <h2 style="margin: 0; color: {colors['text_primary']}; font-weight: 800;">MediNomix</h2>
            <p style="color: {colors['text_secondary']}; margin: 8px 0 24px 0; font-size: 14px;">AI Medication Safety</p>
            <div style="height: 4px; background: {colors['gradient_primary']}; border-radius: 2px; margin: 0 auto 32px auto; width: 60px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Card
        render_premium_card("System Status")
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    render_alert("Backend Connected", "success")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Drugs", data.get('metrics', {}).get('drugs_in_database', 0))
                    with col2:
                        st.metric("Analyses", data.get('metrics', {}).get('total_analyses', 0))
                else:
                    render_alert("Backend Issues", "warning")
            else:
                render_alert("Cannot Connect", "danger")
        except:
            render_alert("Backend Not Running", "danger")
            st.code("python backend.py", language="bash")
        
        # Quick Links
        render_premium_card("Quick Links")
        
        if st.button("📚 Documentation", use_container_width=True):
            render_alert("Documentation coming soon!", "info")
        
        if st.button("🐛 Report Bug", use_container_width=True):
            render_alert("Bug reporting coming soon!", "info")
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            render_alert("Cache cleared successfully!", "success")
            st.rerun()
        
        # Risk Categories Guide
        render_premium_card("Risk Categories")
        
        risk_levels = [
            ("Critical", "≥75%", "Immediate attention required", "badge-critical"),
            ("High", "50-74%", "Review and verify", "badge-high"),
            ("Medium", "25-49%", "Monitor closely", "badge-medium"),
            ("Low", "<25%", "Low priority", "badge-low")
        ]
        
        for name, score, desc, badge_class in risk_levels:
            st.markdown(f"""
            <div style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid {colors['border']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span class="risk-badge {badge_class}" style="font-size: 10px; padding: 4px 12px;">{name}</span>
                    <span style="font-weight: 700; color: {colors['text_primary']};">{score}</span>
                </div>
                <div style="color: {colors['text_secondary']}; font-size: 12px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ================================
# FOOTER
# ================================

def render_footer():
    """Render footer"""
    colors = get_theme_colors()
    
    st.markdown(f"""
    <div class="custom-footer">
        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <div style="margin-bottom: 32px;">
                <div style="font-size: 36px; margin-bottom: 16px;">💊</div>
                <div style="font-weight: 800; color: white !important; margin-bottom: 12px; font-size: 24px;">MediNomix AI</div>
                <div style="color: rgba(255, 255, 255, 0.8) !important; font-size: 16px; max-width: 600px; margin: 0 auto;">
                    Preventing medication errors with artificial intelligence
                </div>
            </div>
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 24px; color: rgba(255, 255, 255, 0.6) !important; font-size: 14px;">
                <div style="margin-bottom: 12px;">© 2024 MediNomix AI. All rights reserved.</div>
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
    
    # Theme Toggle
    st.markdown("""
    <div class="theme-toggle">
        <button class="theme-btn" onclick="toggleTheme()">
            {icon}
        </button>
    </div>
    """.format(icon="🌙" if st.session_state.theme == 'light' else '☀️'), unsafe_allow_html=True)
    
    # JavaScript for theme toggle
    st.markdown("""
    <script>
    function toggleTheme() {{
        const currentTheme = "{theme}";
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        window.parent.postMessage({{type: 'set_theme', theme: newTheme}}, '*');
    }}
    
    // Listen for theme changes
    window.addEventListener('message', function(event) {{
        if (event.data.type === 'set_theme') {{
            // Reload the page to apply new theme
            window.location.reload();
        }}
    }});
    </script>
    """.format(theme=st.session_state.theme), unsafe_allow_html=True)
    
    # Navigation Tabs
    tabs = ["Home", "Drug Analysis", "Analytics", "Real-Time"]
    active_tab = st.session_state.active_tab
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔍 Drug Analysis", "📊 Analytics", "⚡ Real-Time"])
    
    with tab1:
        render_hero_section()
        
        # Stats Counter
        col1, col2, col3, col4 = st.columns(4)
        render_stat_card("👥", "1.5M+", "Patients Protected", col1)
        render_stat_card("💰", "$42B", "Cost Saved", col2)
        render_stat_card("🎯", "99.8%", "Accuracy Rate", col3)
        render_stat_card("💊", "50K+", "Drugs Analyzed", col4)
        
        # Features Section
        st.markdown("""
        <div style="margin: 60px 0;">
            <h2 style="text-align: center; margin-bottom: 40px; color: #2d3748;">How MediNomix Works</h2>
        </div>
        """, unsafe_allow_html=True)
        
        features_cols = st.columns(3)
        features = [
            {"icon": "🔍", "title": "Search Medication", "desc": "Enter any drug name to analyze potential confusion risks"},
            {"icon": "🧠", "title": "AI Analysis", "desc": "Our AI analyzes spelling, phonetic, and therapeutic similarities"},
            {"icon": "🛡️", "title": "Risk Prevention", "desc": "Get detailed risk assessments and prevention recommendations"}
        ]
        
        for idx, col in enumerate(features_cols):
            with col:
                feature = features[idx]
                render_premium_card(
                    f"{feature['icon']} {feature['title']}",
                    feature['desc'],
                    col
                )
        
        # User Guide
        render_premium_card("📚 User Guide & Quick Start")
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