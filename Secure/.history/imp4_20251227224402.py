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

# Medical Theme Color Scheme
COLORS = {
    'primary': '#10B981',  # Medical green
    'primary_hover': '#059669',
    'secondary': '#3B82F6',  # Medical blue
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#0EA5E9',
    'purple': '#8B5CF6',
    'yellow': '#FBBF24',
    'pink': '#EC4899',
    'dark': '#1F2937',
    'light': '#FFFFFF',
    'card_bg': '#FFFFFF',
    'sidebar_bg': '#F0FDF4',  # Light medical green
    'border': '#E5E7EB',
    'text_primary': '#111827',
    'text_secondary': '#4B5563',
    'text_muted': '#9CA3AF',
    'shadow': 'rgba(16, 185, 129, 0.15)',
    'shadow_hover': 'rgba(16, 185, 129, 0.25)',
    'gradient_primary': 'linear-gradient(135deg, #10B981 0%, #3B82F6 100%)',
    'gradient_secondary': 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
    'gradient_success': 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
    'gradient_warning': 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)',
    'gradient_danger': 'linear-gradient(135deg, #EF4444 0%, #F87171 100%)',
    'gradient_purple': 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)',
    'gradient_dark': 'linear-gradient(135deg, #1F2937 0%, #374151 100%)',
    'gradient_medical': 'linear-gradient(135deg, #10B981 0%, #0EA5E9 50%, #3B82F6 100%)'
}

# ================================
# PREMIUM CSS STYLING WITH IMPROVEMENTS
# ================================

st.markdown(f"""
<style>
/* ========== GLOBAL STYLES & SCROLLBAR ========== */
.stApp {{
    background: linear-gradient(135deg, #F9FAFB 0%, #F0FDF4 100%);
    color: {COLORS['text_primary']};
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 12px;
    height: 12px;
}}

::-webkit-scrollbar-track {{
    background: #F3F4F6;
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb {{
    background: {COLORS['primary']};
    border-radius: 10px;
    border: 3px solid #F3F4F6;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {COLORS['primary_hover']};
}}

/* ========== INPUT FIELD PLACEHOLDER VISIBILITY ========== */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
.stSelectbox select::placeholder {{
    color: {COLORS['text_muted']} !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}}

/* ========== ALL BUTTON STYLING ========== */
div.stButton > button:first-child {{
    background: {COLORS['gradient_primary']} !important;
    color: white !important;
    border: none !important;
    padding: 14px 32px !important;
    border-radius: 16px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    min-height: 52px !important;
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}}

div.stButton > button:first-child:hover {{
    transform: translateY(-5px) scale(1.05) !important;
    box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4) !important;
}}

/* ========== USER GUIDE TIPS IMPROVEMENT ========== */
.guide-card {{
    background: linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    margin: 20px 0 !important;
    border: 3px solid {COLORS['primary']} !important;
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15) !important;
}}

.guide-step {{
    display: flex !important;
    align-items: center !important;
    gap: 20px !important;
    margin-bottom: 30px !important;
    padding: 24px !important;
    background: white !important;
    border-radius: 20px !important;
    border-left: 6px solid {COLORS['primary']} !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
}}

.step-icon {{
    font-size: 32px !important;
    min-width: 60px !important;
    text-align: center !important;
    background: {COLORS['gradient_primary']} !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}}

.step-content h4 {{
    color: {COLORS['text_primary']} !important;
    margin: 0 0 10px 0 !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}}

.step-content ul {{
    margin: 0 !important;
    padding-left: 20px !important;
    color: {COLORS['text_secondary']} !important;
}}

.step-content li {{
    margin-bottom: 8px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
}}

/* ========== SIDEBAR STYLING ========== */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F0FDF4 100%) !important;
    border-right: 4px solid {COLORS['primary']} !important;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.05) !important;
}}

/* ========== FOOTER STYLING ========== */
.neon-footer {{
    margin-top: 80px;
    padding: 60px 0;
    background: {COLORS['gradient_medical']} !important;
    border-radius: 40px 40px 0 0;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.neon-footer::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50,50 m-20,0 a20,20 0 1,1 40,0 a20,20 0 1,1 -40,0" fill="none" stroke="white" stroke-width="1" opacity="0.1"/></svg>');
}}

.neon-footer h3 {{
    color: white !important;
    font-size: 32px !important;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 2;
}}

.neon-footer p {{
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 18px !important;
    max-width: 800px;
    margin: 20px auto;
    position: relative;
    z-index: 2;
}}

/* ========== CHART CONTAINERS FOR BETTER LAYOUT ========== */
.chart-container {{
    background: white !important;
    border-radius: 20px !important;
    padding: 24px !important;
    margin: 20px 0 !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08) !important;
    border: 2px solid {COLORS['border']} !important;
    height: 100% !important;
}}

/* ========== GLASSMORPHISM CARDS ========== */
.glass-card {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px {COLORS['shadow']};
    padding: 32px;
    margin-bottom: 24px;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}}

.glass-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 40px {COLORS['shadow_hover']};
    border-color: {COLORS['primary']};
}}

.glass-card-header {{
    margin: -32px -32px 24px -32px;
    padding: 32px;
    background: {COLORS['gradient_primary']};
    border-radius: 24px 24px 0 0;
    position: relative;
    overflow: hidden;
}}

.glass-card-header h2 {{
    color: white !important;
    margin: 0 !important;
    font-size: 28px !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}}

/* ========== IMAGE STYLING ========== */
.medical-image {{
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 16px;
    margin: 10px 0;
    border: 3px solid {COLORS['primary']};
    box-shadow: 0 8px 25px {COLORS['shadow']};
    transition: all 0.3s ease;
}}

.medical-image:hover {{
    transform: scale(1.03);
    box-shadow: 0 12px 30px {COLORS['shadow_hover']};
}}

/* ========== STAT CARDS ========== */
.stat-card {{
    background: white;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    border: 3px solid transparent;
    background-clip: padding-box;
    background: linear-gradient(white, white) padding-box,
                {COLORS['gradient_primary']} border-box;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}}

.stat-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 30px {COLORS['shadow_hover']};
}}

/* ========== METRIC BOXES ========== */
.metric-box {{
    background: white;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    border: 2px solid {COLORS['border']};
}}

.metric-box:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border-color: {COLORS['primary']};
}}

/* ========== NAVIGATION TABS ========== */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: white;
    padding: 8px;
    border-radius: 20px;
    border: 2px solid {COLORS['border']};
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}}

/* ========== INPUT FIELDS ========== */
.stTextInput input, .stSelectbox select, .stTextArea textarea {{
    background: white !important;
    color: {COLORS['text_primary']} !important;
    border: 2px solid {COLORS['border']} !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
}}

.stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {{
    border-color: {COLORS['primary']} !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15) !important;
    outline: none !important;
}}

/* ========== EXPANDER STYLING ========== */
.streamlit-expanderHeader {{
    background: {COLORS['gradient_primary']} !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}}

/* ========== SEARCH BOX ========== */
.search-container {{
    background: white;
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    border: 2px solid {COLORS['border']};
    margin: 40px 0;
    position: relative;
    overflow: hidden;
}}

/* ========== RISK BADGES ========== */
.risk-badge {{
    display: inline-flex;
    align-items: center;
    padding: 8px 20px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    gap: 6px;
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

/* ========== DATA FRAME STYLING ========== */
.dataframe {{
    background: white !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
    border: 2px solid {COLORS['border']} !important;
}}

/* ========== ALERTS ========== */
.neon-alert {{
    border-radius: 16px;
    padding: 20px;
    margin: 20px 0;
    border-left: 6px solid;
    background: white;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}}

.alert-success {{
    border-left-color: {COLORS['success']};
    background: linear-gradient(90deg, #F0FDF4 0%, white 100%);
}}

.alert-danger {{
    border-left-color: {COLORS['danger']};
    background: linear-gradient(90deg, #FEF2F2 0%, white 100%);
}}

.alert-info {{
    border-left-color: {COLORS['info']};
    background: linear-gradient(90deg, #F0F9FF 0%, white 100%);
}}

/* ========== HERO SECTION ========== */
.hero-section {{
    background: {COLORS['gradient_medical']};
    border-radius: 32px;
    padding: 60px 40px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    text-align: center;
}}

/* ========== FEATURE CARDS ========== */
.feature-card {{
    background: white;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    border: 2px solid {COLORS['border']};
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    height: 100%;
}}

.feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    border-color: {COLORS['primary']};
}}

/* Responsive adjustments for charts */
@media (max-width: 1200px) {{
    .chart-container {{
        margin-bottom: 20px;
    }}
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
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS['success']],
            [0.25, COLORS['purple']],
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
            titlefont=dict(color=COLORS['text_primary'], size=12),
            tickfont=dict(color=COLORS['text_secondary'], size=10)
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="🎯 Drug Confusion Risk Heatmap",
            font=dict(color=COLORS['text_primary'], size=20),
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
            tickfont=dict(color=COLORS['text_secondary'], size=10),
            gridcolor=COLORS['border']
        ),
        yaxis=dict(
            tickfont=dict(color=COLORS['text_secondary'], size=10),
            gridcolor=COLORS['border']
        ),
        margin=dict(l=80, r=50, t=60, b=80)
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
    colors = [COLORS['danger'], COLORS['warning'], COLORS['purple'], COLORS['success']]
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=counts,
        hole=0.5,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='inside',
        hoverinfo='label+value+percent',
        textfont=dict(color='white', size=12),
        marker_line=dict(color='white', width=2)
    )])
    
    fig.update_layout(
        title=dict(
            text="📊 Risk Distribution",
            font=dict(color=COLORS['text_primary'], size=18),
            x=0.5,
            xanchor="center"
        ),
        height=400,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        legend=dict(
            font=dict(size=12, color=COLORS['text_secondary']),
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
    
    pairs = [f"💊 {item['drug1']} ↔ {item['drug2']}" for item in top_risks]
    scores = [item['risk_score'] for item in top_risks]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color=COLORS['primary'],
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            marker_line_color='white',
            marker_line_width=1,
            textfont=dict(size=12, color=COLORS['text_primary']),
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><extra></extra>"
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="🚨 Top 10 High-Risk Drug Pairs",
            font=dict(color=COLORS['text_primary'], size=18),
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Risk Score (%)",
        yaxis_title="",
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        xaxis=dict(
            gridcolor=COLORS['border'],
            tickfont=dict(color=COLORS['text_secondary'], size=10)
        ),
        yaxis=dict(
            tickfont=dict(color=COLORS['text_secondary'], size=10)
        ),
        margin=dict(l=150, r=50, t=60, b=50)
    )
    
    return fig

# ================================
# UI COMPONENTS
# ================================

def render_neon_alert(message, alert_type="info"):
    """Render a neon styled alert message"""
    
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
            <div style="font-size: 28px; min-width: 32px;">{icon}</div>
            <div>
                <div style="font-weight: 700; font-size: 16px; margin-bottom: 4px; color: {COLORS['text_primary']};">{title}</div>
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
            <div style="font-size: 48px; margin-bottom: 16px; color: {COLORS['primary']};">{icon}</div>
            <div style="font-size: 36px; font-weight: 800; margin-bottom: 8px; color: {COLORS['text_primary']};">{value}</div>
            <div style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

def render_feature_card(icon, title, description, col):
    """Render a feature card"""
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div style="font-size: 48px; margin-bottom: 20px; color: {COLORS['primary']};">{icon}</div>
            <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: {COLORS['text_primary']};">{title}</div>
            <div style="color: {COLORS['text_secondary']}; font-size: 14px; line-height: 1.6;">{description}</div>
        </div>
        """, unsafe_allow_html=True)

def render_metric_box(label, value, col):
    """Render a metric box"""
    with col:
        st.markdown(f"""
        <div class="metric-box">
            <div style="color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">{label}</div>
            <div style="font-size: 28px; font-weight: 800; color: {COLORS['primary']};">{value}</div>
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
    """Render user guide section with improved styling"""
    st.markdown("""
    <div class="guide-card">
        <h2 style="color: #111827 !important; margin-bottom: 30px !important; text-align: center; font-size: 28px !important;">📚 User Guide & Tips</h2>
    """, unsafe_allow_html=True)
    
    # Step 1
    st.markdown("""
    <div class="guide-step">
        <div class="step-icon">🚀</div>
        <div class="step-content">
            <h4>Step 1: Search for a Medication</h4>
            <ul>
                <li>Navigate to the <b>Drug Analysis</b> tab</li>
                <li>Enter any medication name (brand or generic)</li>
                <li>Click <b>Analyze Drug</b> to start the AI analysis</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 2
    st.markdown("""
    <div class="guide-step">
        <div class="step-icon">📊</div>
        <div class="step-content">
            <h4>Step 2: Review Risk Assessment</h4>
            <ul>
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
        <div class="step-icon">🛡️</div>
        <div class="step-content">
            <h4>Step 3: Take Preventive Action</h4>
            <ul>
                <li>Check <b>Analytics</b> tab for overall statistics</li>
                <li>Monitor <b>Real-Time</b> dashboard for live updates</li>
                <li>Use quick examples for demonstration</li>
            </ul>
        </div>
    </div>
    
    <div style="background: linear-gradient(135deg, #F0F9FF 0%, #F0FDF4 100%); padding: 24px; border-radius: 16px; margin-top: 32px; border: 2px solid #D1FAE5;">
        <h4 style="color: #111827 !important; margin-bottom: 16px !important; font-size: 18px !important;">💡 Pro Tips:</h4>
        <ul style="color: #4B5563 !important; font-size: 16px !important; font-weight: 500 !important;">
            <li style="margin-bottom: 10px !important;">Always double-check medication names before administration</li>
            <li style="margin-bottom: 10px !important;">Use Tall Man lettering for look-alike drug names</li>
            <li style="margin-bottom: 10px !important;">Consult the FDA high-alert drug list regularly</li>
            <li>Report any confusion incidents through your institution's safety reporting system</li>
        </ul>
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
        <h1 style="color: white !important; font-size: 48px !important; font-weight: 800 !important; margin-bottom: 16px !important;">💊 MediNomix AI</h1>
        <p style="color: rgba(255, 255, 255, 0.95) !important; font-size: 18px !important; max-width: 800px; margin: 0 auto 32px !important; line-height: 1.6;">
            Advanced AI-powered system that analyzes drug names for potential confusion risks, helping healthcare professionals prevent medication errors and improve patient safety.
        </p>
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
        <div style="font-size: 24px; font-weight: 700; margin-bottom: 12px; color: #111827;">Search Medication</div>
        <div style="color: #4B5563; font-size: 14px; margin-bottom: 24px;">Enter any drug name to analyze potential confusion risks</div>
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
        <h3 style="color: #111827; margin-bottom: 16px; font-weight: 700;">✨ Quick Examples:</h3>
    </div>
    """, unsafe_allow_html=True)
    
    examples = ["Lamictal", "Metformin", "Celebrex", "Clonidine"]
    example_images = [
        "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80"
    ]
    
    cols = st.columns(4)
    for idx, col in enumerate(cols):
        with col:
            # Display image
            st.markdown(f"""
            <img src="{example_images[idx]}" class="medical-image" alt="{examples[idx]}">
            """, unsafe_allow_html=True)
            
            # Display button
            if st.button(f"💊 {examples[idx]}", use_container_width=True, key=f"ex_{idx}"):
                with st.spinner(f"🔬 Analyzing {examples[idx]}..."):
                    result = search_drug(examples[idx])
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
        <div style="margin-top: 40px;">
            <h2 style="color: #111827; margin-bottom: 24px; font-weight: 700;">📊 Analysis Results</h2>
        </div>
        """, unsafe_allow_html=True)
        
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
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 24px; gap: 20px;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0 0 8px 0; color: #111827; font-weight: 700; font-size: 20px;">{result['target_drug']['brand_name']}</h3>
                        {f"<p style='margin: 0 0 12px 0; color: #4B5563; font-size: 14px; font-weight: 500;'>Generic: {result['target_drug']['generic_name']}</p>" if result['target_drug']['generic_name'] else ""}
                    </div>
                    <div style="text-align: center; min-width: 120px;">
                        <div style="font-size: 36px; font-weight: 800; color: {COLORS['primary']}; margin-bottom: 8px;">
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
        
        render_stat_card("💊", metrics.get('total_drugs', 0), "Total Drugs", col1)
        render_stat_card("🔥", metrics.get('critical_risk_pairs', 0), "Critical Pairs", col2)
        render_stat_card("⚠️", metrics.get('high_risk_pairs', 0), "High Risk Pairs", col3)
        render_stat_card("📈", f"{metrics.get('avg_risk_score', 0):.1f}%", "Avg Risk Score", col4)
    
    # Charts Section with better layout
    st.markdown("""
    <div style="margin: 40px 0;">
        <h2 style="color: #111827; margin-bottom: 24px; font-weight: 700;">🎨 Analytics Charts</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # First row: Two charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row: Heatmap full width
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h3 style="color: #111827; margin: 0; font-weight: 700; font-size: 18px;">🎯 Drug Confusion Risk Heatmap</h3>
    </div>
    """, unsafe_allow_html=True)
    
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown(f"""
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px; color: #4B5563; font-size: 14px; font-weight: 600;">
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['success']}; border-radius: 2px;"></div> Low Risk</div>
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['purple']}; border-radius: 2px;"></div> Medium Risk</div>
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['warning']}; border-radius: 2px;"></div> High Risk</div>
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['danger']}; border-radius: 2px;"></div> Critical Risk</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs first.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FDA Alerts Section with images
    render_glass_card("🚨 FDA High Alert Drug Pairs", "Most commonly confused drug pairs according to FDA")
    
    risky_pairs_data = [
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", "Reason": "Epilepsy medication vs Antifungal", "Image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", "Reason": "Arthritis vs Depression medication", "Image": "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", "Reason": "Diabetes vs Antibiotic", "Image": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", "Reason": "Blood Pressure vs Anxiety medication", "Image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", "Reason": "Antipsychotic vs Allergy medication", "Image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    ]
    
    for pair in risky_pairs_data:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f'<img src="{pair["Image"]}" style="width: 100%; border-radius: 12px; margin-bottom: 10px;">', unsafe_allow_html=True)
        with col2:
            risk_color = {
                "Critical": COLORS['danger'],
                "High": COLORS['warning'],
                "Medium": COLORS['purple']
            }.get(pair["Risk Level"], COLORS['text_secondary'])
            
            st.markdown(f"""
            <div style="padding: 16px; background: white; border-radius: 12px; border-left: 4px solid {risk_color}; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-size: 18px; font-weight: 700; color: #111827;">{pair["Drug 1"]} ↔ {pair["Drug 2"]}</div>
                    <div style="padding: 4px 12px; background: {risk_color}; color: white; border-radius: 20px; font-size: 12px; font-weight: 700;">{pair["Risk Level"]}</div>
                </div>
                <div style="color: #4B5563; font-size: 14px;">{pair["Reason"]}</div>
            </div>
            """, unsafe_allow_html=True)

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
        
        render_stat_card("📊", metrics.get('total_drugs', 0), "Live Drugs", col1)
        render_stat_card("🔥", metrics.get('critical_risk_pairs', 0), "Critical Now", col2)
        render_stat_card("📈", f"{metrics.get('avg_risk_score', 0):.1f}%", "Avg Risk", col3)
        render_stat_card("👥", metrics.get('connected_clients', 0), "Connected", col4)
        
        # Recent Activity Section
        render_glass_card("🕒 Recent Activity Timeline", "Latest drug analysis activities")
        
        if metrics.get('recent_searches'):
            for idx, search in enumerate(metrics['recent_searches'][:5]):
                timestamp = search.get('timestamp', '')
                drug_name = search.get('drug_name', 'Unknown')
                similar_drugs = search.get('similar_drugs_found', 0)
                highest_risk = search.get('highest_risk', 0)
                
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown(f'<div style="text-align: center; padding: 12px; background: {COLORS["primary"]}20; border-radius: 12px;"><div style="font-size: 24px; font-weight: 800; color: {COLORS["primary"]};">{idx+1}</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="padding: 12px 0;">
                        <div style="font-weight: 700; color: {COLORS['text_primary']}; font-size: 16px;">💊 {drug_name}</div>
                        <div style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 500;">Found {similar_drugs} similar drugs • Highest risk: {highest_risk:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div style="color: {COLORS["text_muted"]}; font-size: 12px; font-weight: 600; text-align: right; padding-top: 12px;">{timestamp[:19] if timestamp else "Just now"}</div>', unsafe_allow_html=True)
        else:
            st.info("No recent activity data available")
    else:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 60px 40px;">
            <div style="font-size: 64px; margin-bottom: 24px; color: {COLORS['primary']}">⏳</div>
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
        <div style="text-align: center; margin-bottom: 32px; padding: 24px 16px; background: {COLORS['gradient_primary']}; border-radius: 20px; box-shadow: 0 8px 30px rgba(16, 185, 129, 0.2);">
            <div style="font-size: 56px; margin-bottom: 12px; filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));">💊</div>
            <h2 style="margin: 0; color: white !important; font-weight: 800; font-size: 24px;">MediNomix</h2>
            <p style="color: rgba(255, 255, 255, 0.9); margin: 8px 0 0 0; font-size: 14px; font-weight: 600;">AI Medication Safety</p>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Card
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">
            <h3 style="margin: 0 0 16px 0; color: #111827; font-weight: 700; font-size: 16px;">📡 System Status</h3>
        """, unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    st.success("✅ Backend Connected")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("💊 Drugs", data.get('metrics', {}).get('drugs_in_database', 0))
                    with col2:
                        st.metric("📊 Analyses", data.get('metrics', {}).get('total_analyses', 0))
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
        <div style="background: white; border-radius: 16px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">
            <h3 style="margin: 0 0 16px 0; color: #111827; font-weight: 700; font-size: 16px;">🔗 Quick Links</h3>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Documentation", use_container_width=True):
            render_neon_alert("Documentation coming soon!", "info")
        
        if st.button("🐛 Report Bug", use_container_width=True):
            render_neon_alert("Bug reporting coming soon!", "info")
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            render_neon_alert("Cache cleared successfully!", "success")
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Risk Categories Guide
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">
            <h3 style="margin: 0 0 16px 0; color: #111827; font-weight: 700; font-size: 16px;">⚠️ Risk Categories</h3>
        """, unsafe_allow_html=True)
        
        risk_levels = [
            ("Critical", "≥75%", "Immediate attention required", COLORS['danger']),
            ("High", "50-74%", "Review and verify", COLORS['warning']),
            ("Medium", "25-49%", "Monitor closely", COLORS['purple']),
            ("Low", "<25%", "Low priority", COLORS['success'])
        ]
        
        for name, score, desc, color in risk_levels:
            st.markdown(f"""
            <div style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #E5E7EB; last-child: border-bottom: none;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="padding: 4px 12px; background: {color}; color: white; border-radius: 20px; font-size: 11px; font-weight: 700;">{name}</div>
                    <div style="font-weight: 700; color: #111827; font-size: 14px;">{score}</div>
                </div>
                <div style="color: #4B5563; font-size: 12px; font-weight: 500;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ================================
# FOOTER
# ================================

def render_footer():
    """Render footer"""
    
    st.markdown(f"""
    <div class="neon-footer">
        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <div style="margin-bottom: 32px;">
                <div style="font-size: 40px; margin-bottom: 16px;">💊</div>
                <h3 style="color: white !important; margin-bottom: 12px; font-weight: 800;">MediNomix AI</h3>
                <p style="color: rgba(255, 255, 255, 0.95) !important; font-size: 16px; max-width: 600px; margin: 0 auto;">
                    Preventing medication errors with artificial intelligence
                </p>
            </div>
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 24px; color: rgba(255, 255, 255, 0.8) !important; font-size: 14px;">
                <div style="margin-bottom: 12px; font-weight: 600;">© 2024 MediNomix AI. All rights reserved.</div>
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
        <div style="margin: 40px 0;">
            <h2 style="text-align: center; margin-bottom: 32px; color: #111827; font-weight: 800;">✨ How MediNomix Works</h2>
        </div>
        """, unsafe_allow_html=True)
        
        features_cols = st.columns(3)
        features = [
            {"icon": "🔍", "title": "Search Medication", "desc": "Enter any drug name to analyze potential confusion risks"},
            {"icon": "🧠", "title": "AI Analysis", "desc": "Our AI analyzes spelling, phonetic, and therapeutic similarities"},
            {"icon": "🛡️", "title": "Risk Prevention", "desc": "Get detailed risk assessments and prevention recommendations"}
        ]
        
        # Add images for features
        feature_images = [
            "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80"
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
            "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80"
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