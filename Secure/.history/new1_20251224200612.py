"""
MediNomix - Advanced Medication Safety Platform
ULTRA MODERN PROFESSIONAL UI with premium healthcare theme
FUNCTIONALITY: 100% preserved, with REAL-TIME dashboard analytics integration
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import base64
import time
import json
import threading
import queue

# Page configuration - Premium Medical Theme
st.set_page_config(
    page_title="MediNomix | AI-Powered Medication Safety",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/precious-05/MediNomix',
        'Report a bug': "https://github.com/precious-05/MediNomix/issues",
        'About': "### MediNomix AI v3.0\nAdvanced Medication Safety Platform"
    }
)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Modern Gradient Color Scheme for Dark Theme
COLORS = {
    "background": "#0a0e17",           # Deep navy blue background
    "surface": "#1a1f2e",              # Dark surface for cards
    "surface_light": "#222738",        # Lighter surface
    "primary": "#6366f1",              # Indigo - primary accent
    "primary_gradient": "#8b5cf6",     # Purple for gradients
    "secondary": "#06b6d4",            # Cyan
    "accent": "#10b981",               # Emerald green
    "warning": "#f59e0b",              # Amber
    "danger": "#ef4444",               # Red
    "text_primary": "#f8fafc",         # Light text
    "text_secondary": "#94a3b8",       # Gray text
    "text_muted": "#64748b",           # Muted text
    "border": "#334155",               # Border color
    "success": "#22c55e",              # Bright green
    "info": "#3b82f6",                 # Blue
}

# Initialize session state
for key in ['search_results', 'dashboard_data', 'selected_risk', 'heatmap_data', 
            'realtime_metrics', 'realtime_events', 'last_update', 'ws_connected']:
    if key not in st.session_state:
        st.session_state[key] = None if key in ['heatmap_data', 'realtime_metrics', 'realtime_events'] else (
            [] if key == 'search_results' else {} if key in ['dashboard_data'] else "all" if key == 'selected_risk' else 
            datetime.now() if key == 'last_update' else False
        )

# Base64 encoded SVG Icons for Dark Theme
def get_icon_svg(icon_name, color="#6366f1", size=24):
    """Generate base64 encoded SVG icons optimized for dark theme"""
    icon_map = {
        "pill": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="8" y="2" width="8" height="4" rx="1"/>
            <rect x="3" y="6" width="18" height="12" rx="3"/>
            <path d="M10 10h4"/>
            <path d="M12 10v4"/>
        </svg>
        """,
        "search": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
        </svg>
        """,
        "dashboard": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="9" rx="1"/>
            <rect x="14" y="3" width="7" height="5" rx="1"/>
            <rect x="14" y="12" width="7" height="9" rx="1"/>
            <rect x="3" y="16" width="7" height="5" rx="1"/>
        </svg>
        """,
        "analytics": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v16a2 2 0 0 0 2 2h16"/>
            <path d="M7 16l4-4 4 4 6-6"/>
            <path d="M17 11V7"/>
        </svg>
        """,
        "alert": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        """,
        "safety": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <path d="m9 12 2 2 4-4"/>
        </svg>
        """,
        "brain": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-2.5 2.5h-2A2.5 2.5 0 0 1 5 19.5v-15A2.5 2.5 0 0 1 7.5 2z"/>
            <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 2.5 2.5h2A2.5 2.5 0 0 0 19 19.5v-15A2.5 2.5 0 0 0 16.5 2z"/>
        </svg>
        """,
        "database": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <ellipse cx="12" cy="5" rx="9" ry="3"/>
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
        </svg>
        """,
        "refresh": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
        </svg>
        """,
        "heartbeat": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 17H2l4-8 5 5 7-7"/>
            <path d="M2 12h6"/>
            <path d="M16 12h6"/>
        </svg>
        """,
        "chart-line": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v16a2 2 0 0 0 2 2h16"/>
            <path d="m7 16 4-4 4 4 6-6"/>
        </svg>
        """,
        "activity": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
        """,
        "bell": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        """,
        "users": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        """,
        "clock": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
        </svg>
        """,
        "server": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
            <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
            <line x1="6" y1="6" x2="6.01" y2="6"/>
            <line x1="6" y1="18" x2="6.01" y2="18"/>
        </svg>
        """,
        "bolt": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
        </svg>
        """,
        "chart-pie": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>
            <path d="M22 12A10 10 0 0 0 12 2v10z"/>
        </svg>
        """,
        "chart-bar": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="20" x2="12" y2="10"/>
            <line x1="18" y1="20" x2="18" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="16"/>
        </svg>
        """,
        "eye": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
            <circle cx="12" cy="12" r="3"/>
        </svg>
        """,
        "download": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        """,
        "info": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
        </svg>
        """,
        "settings": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
        """,
        "trending-up": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
            <polyline points="17 6 23 6 23 12"/>
        </svg>
        """,
        "calendar": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        """,
        "filter": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
        </svg>
        """,
        "external-link": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15 3 21 3 21 9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
        """,
        "chevron-up": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="18 15 12 9 6 15"/>
        </svg>
        """,
        "chevron-down": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"/>
        </svg>
        """,
        "check-circle": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
        """,
        "x-circle": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
        </svg>
        """,
        "wifi": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12.55a11 11 0 0 1 14.08 0"/>
            <path d="M1.42 9a16 16 0 0 1 21.16 0"/>
            <path d="M8.53 16.11a6 6 0 0 1 6.95 0"/>
            <line x1="12" y1="20" x2="12.01" y2="20"/>
        </svg>
        """,
        "wifi-off": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="1" y1="1" x2="23" y2="23"/>
            <path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/>
            <path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"/>
            <path d="M10.71 5.05A16 16 0 0 1 22.58 9"/>
            <path d="M1.42 9a15.91 15.91 0 0 1 4.7-2.88"/>
            <path d="M8.53 16.11a6 6 0 0 1 6.95 0"/>
            <line x1="12" y1="20" x2="12.01" y2="20"/>
        </svg>
        """,
        "cpu": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="4" y="4" width="16" height="16" rx="2" ry="2"/>
            <rect x="9" y="9" width="6" height="6"/>
            <line x1="9" y1="1" x2="9" y2="4"/>
            <line x1="15" y1="1" x2="15" y2="4"/>
            <line x1="9" y1="20" x2="9" y2="23"/>
            <line x1="15" y1="20" x2="15" y2="23"/>
            <line x1="20" y1="9" x2="23" y2="9"/>
            <line x1="20" y1="14" x2="23" y2="14"/>
            <line x1="1" y1="9" x2="4" y2="9"/>
            <line x1="1" y1="14" x2="4" y2="14"/>
        </svg>
        """,
        "layers": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 2 7 12 12 22 7 12 2"/>
            <polyline points="2 17 12 22 22 17"/>
            <polyline points="2 12 12 17 22 12"/>
        </svg>
        """,
    }
    
    if icon_name in icon_map:
        svg = icon_map[icon_name]
        b64 = base64.b64encode(svg.encode('utf-8')).decode()
        return f"data:image/svg+xml;base64,{b64}"
    return ""

# ============================================
# REAL-TIME DASHBOARD FUNCTIONS
# ============================================

def fetch_realtime_metrics():
    """Fetch real-time metrics from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/realtime-metrics")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def fetch_realtime_events(limit=10):
    """Fetch real-time events from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/realtime-events?limit={limit}")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def update_realtime_data():
    """Update real-time data in background"""
    metrics = fetch_realtime_metrics()
    if metrics:
        st.session_state.realtime_metrics = metrics
        st.session_state.last_update = datetime.now()
    
    events = fetch_realtime_events()
    if events:
        st.session_state.realtime_events = events

def check_websocket_connection():
    """Check if WebSocket connection is available"""
    try:
        # Try to make a simple request to check connection
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        st.session_state.ws_connected = response.status_code == 200
        return st.session_state.ws_connected
    except:
        st.session_state.ws_connected = False
        return False

# ============================================
# ORIGINAL HELPER FUNCTIONS (100% SAME)
# ============================================

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
        st.error(f"Cannot connect to backend: {str(e)}\n\nMake sure backend is running: `python backend.py`")
        return None

def seed_database():
    """Seed database with common drugs"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/seed-database")
        if response.status_code == 200:
            st.success("Database seeded successfully!")
            return True
        else:
            st.error("Failed to seed database")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def load_dashboard_data():
    """Load ALL dashboard data including heatmap"""
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
            st.session_state.heatmap_data = heatmap_response.json()
            
        # Update real-time data as well
        update_realtime_data()
            
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")

def create_heatmap_chart():
    """Create interactive drug confusion heatmap - Modern Dark Design"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Dark theme heatmap with gradient colors
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS["success"]],
            [0.3, COLORS["accent"]],
            [0.6, COLORS["warning"]],
            [0.8, COLORS["danger"]],
            [1, "#be185d"]
        ],
        zmin=0,
        zmax=100,
        text=[[f"{val:.0f}%" if val > 0 else "" for val in row] for row in risk_matrix],
        texttemplate="%{text}",
        textfont={"size": 11, "color": "#FFFFFF"},
        hoverongaps=False,
        hoverinfo="text",
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br><b>Risk Score: %{z:.1f}%</b><br><extra></extra>",
        colorbar=dict(
            title="Risk Score %",
            titleside="right",
            titlefont=dict(size=14, color=COLORS["text_secondary"]),
            tickfont=dict(size=12, color=COLORS["text_secondary"]),
            thickness=15,
            len=0.75,
            y=0.5,
            yanchor="middle"
        )
    ))
    
    fig.update_layout(
        title={
            "text": "Drug Confusion Risk Matrix",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 24, "color": COLORS["text_primary"], "family": "'Inter', sans-serif"}
        },
        xaxis_title="<b>Drug Names</b>",
        yaxis_title="<b>Drug Names</b>",
        height=650,
        margin={"t": 100, "b": 100, "l": 120, "r": 50},
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="'Inter', sans-serif", size=12, color=COLORS["text_secondary"]),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10, color=COLORS["text_secondary"]),
            gridcolor=COLORS["border"],
            showgrid=True,
            linecolor=COLORS["border"],
            zerolinecolor=COLORS["border"]
        ),
        yaxis=dict(
            tickfont=dict(size=10, color=COLORS["text_secondary"]),
            gridcolor=COLORS["border"],
            showgrid=True,
            linecolor=COLORS["border"],
            zerolinecolor=COLORS["border"]
        )
    )
    
    return fig

def create_risk_breakdown_chart():
    """Create modern risk breakdown donut chart for dark theme"""
    if 'breakdown' not in st.session_state.dashboard_data:
        return None
    
    breakdown = st.session_state.dashboard_data['breakdown']
    if not breakdown:
        return None
    
    categories = [item['category'].title() for item in breakdown]
    counts = [item['count'] for item in breakdown]
    
    color_map = {
        "Critical": "#be185d",
        "High": COLORS["danger"],
        "Medium": COLORS["warning"],
        "Low": COLORS["success"]
    }
    colors = [color_map.get(cat, COLORS["warning"]) for cat in categories]
    
    # Create donut chart
    fig = go.Figure(data=[
        go.Pie(
            labels=categories,
            values=counts,
            hole=0.6,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial',
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            textfont=dict(size=13, color=COLORS["text_primary"], family="'Inter', sans-serif"),
            marker=dict(line=dict(color=COLORS["background"], width=2))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Risk Distribution",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": COLORS["text_primary"], "family": "'Inter', sans-serif"}
        },
        height=450,
        margin=dict(t=80, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05,
            font=dict(size=12, color=COLORS["text_secondary"], family="'Inter', sans-serif"),
            bgcolor=COLORS["surface"],
            bordercolor=COLORS["border"],
            borderwidth=1
        ),
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="'Inter', sans-serif", size=12, color=COLORS["text_secondary"]),
    )
    
    # Add center text
    fig.add_annotation(
        text=f"<b>Total</b><br>{sum(counts)}",
        x=0.5, y=0.5,
        font=dict(size=16, color=COLORS["text_primary"], family="'Inter', sans-serif"),
        showarrow=False
    )
    
    return fig

def create_top_risks_chart():
    """Create modern top risks horizontal bar chart for dark theme"""
    if 'top_risks' not in st.session_state.dashboard_data:
        return None
    
    top_risks = st.session_state.dashboard_data['top_risks']
    if not top_risks:
        return None
    
    pairs = [f"{item['drug1']} ↔ {item['drug2']}" for item in top_risks]
    scores = [item['risk_score'] for item in top_risks]
    categories = [item['risk_category'] for item in top_risks]
    reasons = [item['reason'] for item in top_risks]
    
    color_map = {
        "critical": "#be185d",
        "high": COLORS["danger"],
        "medium": COLORS["warning"],
        "low": COLORS["success"]
    }
    colors = [color_map.get(cat.lower(), COLORS["warning"]) for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color=colors,
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            textfont=dict(size=11, color=COLORS["text_primary"], family="'Inter', sans-serif"),
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><br>Category: %{customdata[0]}<br>%{customdata[1]}<extra></extra>",
            customdata=list(zip(categories, reasons)),
            marker=dict(line=dict(color=COLORS["background"], width=1))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Top 10 High-Risk Drug Pairs",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor" : "top",
            "font": {"size": 22, "color": COLORS["text_primary"], "family": "'Inter', sans-serif"}
        },
        xaxis_title="<b>Risk Score (%)</b>",
        yaxis_title="<b>Drug Pairs</b>",
        height=500,
        margin=dict(t=80, b=50, l=220, r=50),
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="'Inter', sans-serif", size=12, color=COLORS["text_secondary"]),
        xaxis=dict(
            gridcolor=COLORS["border"],
            range=[0, 105],
            showgrid=True,
            linecolor=COLORS["border"],
            zerolinecolor=COLORS["border"]
        ),
        yaxis=dict(
            tickfont=dict(size=11, family="'Inter', sans-serif", color=COLORS["text_secondary"]),
            categoryorder='total ascending',
            linecolor=COLORS["border"]
        )
    )
    
    # Add threshold lines
    fig.add_vline(x=75, line_dash="dash", line_color="#be185d", opacity=0.3)
    fig.add_vline(x=50, line_dash="dash", line_color=COLORS["danger"], opacity=0.3)
    fig.add_vline(x=25, line_dash="dash", line_color=COLORS["warning"], opacity=0.3)
    
    return fig

# ============================================
# DARK THEME CSS
# ============================================

st.markdown(f"""
<style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Base Reset */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    /* Modern Dark Theme */
    .stApp {{
        background: {COLORS["background"]};
        font-family: 'Inter', sans-serif;
        color: {COLORS["text_primary"]};
        background-attachment: fixed;
    }}
    
    /* Animated Background Elements */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.03) 0%, transparent 40%);
        z-index: -1;
        pointer-events: none;
    }}
    
    /* Animations */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Modern Header */
    .main-header {{
        font-size: 3.5rem;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_gradient"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-family: 'Inter', sans-serif;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }}
    
    .sub-header {{
        color: {COLORS["text_secondary"]};
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }}
    
    /* Modern Cards */
    .metric-card {{
        background: linear-gradient(135deg, 
            rgba(99, 102, 241, 0.1) 0%, 
            rgba(30, 41, 59, 0.4) 50%,
            rgba(15, 23, 42, 0.6) 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid {COLORS["border"]};
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
        border-color: {COLORS["primary"]};
    }}
    
    .metric-card .value {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_gradient"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }}
    
    .metric-card .label {{
        color: {COLORS["text_secondary"]};
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }}
    
    /* Risk Cards */
    .risk-card {{
        background: linear-gradient(135deg, 
            rgba(30, 41, 59, 0.8) 0%, 
            rgba(15, 23, 42, 0.6) 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border-left: 4px solid;
        transition: all 0.3s ease;
        border: 1px solid {COLORS["border"]};
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }}
    
    .risk-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }}
    
    .risk-card.critical {{ 
        border-left-color: #be185d;
        background: linear-gradient(135deg, 
            rgba(190, 24, 93, 0.1) 0%, 
            rgba(30, 41, 59, 0.8) 100%);
    }}
    
    .risk-card.high {{ 
        border-left-color: {COLORS["danger"]};
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.1) 0%, 
            rgba(30, 41, 59, 0.8) 100%);
    }}
    
    .risk-card.medium {{ 
        border-left-color: {COLORS["warning"]};
        background: linear-gradient(135deg, 
            rgba(245, 158, 11, 0.1) 0%, 
            rgba(30, 41, 59, 0.8) 100%);
    }}
    
    .risk-card.low {{ 
        border-left-color: {COLORS["success"]};
        background: linear-gradient(135deg, 
            rgba(34, 197, 94, 0.1) 0%, 
            rgba(30, 41, 59, 0.8) 100%);
    }}
    
    /* Modern Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_gradient"]} 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4) !important;
    }}
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {COLORS["surface"]};
        padding: 8px;
        border-radius: 12px;
        border: 1px solid {COLORS["border"]};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        padding: 0 24px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        color: {COLORS["text_secondary"]};
        background: transparent;
        border: 1px solid transparent;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(99, 102, 241, 0.1) !important;
        color: {COLORS["primary"]} !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_gradient"]} 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        border-color: {COLORS["primary"]} !important;
    }}
    
    /* Modern Sidebar */
    [data-testid="stSidebar"] {{
        background: {COLORS["surface"]};
        border-right: 1px solid {COLORS["border"]};
    }}
    
    /* Modern Inputs */
    .stTextInput > div > div > input {{
        background: {COLORS["surface"]} !important;
        color: {COLORS["text_primary"]} !important;
        border: 1px solid {COLORS["border"]} !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS["primary"]} !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }}
    
    /* Divider */
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            {COLORS["border"]} 50%, 
            transparent);
        margin: 2rem 0;
    }}
    
    /* Status Indicators */
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid;
    }}
    
    .status-healthy {{
        background: rgba(34, 197, 94, 0.1);
        color: {COLORS["success"]};
        border-color: rgba(34, 197, 94, 0.3);
    }}
    
    .status-warning {{
        background: rgba(245, 158, 11, 0.1);
        color: {COLORS["warning"]};
        border-color: rgba(245, 158, 11, 0.3);
    }}
    
    .status-critical {{
        background: rgba(239, 68, 68, 0.1);
        color: {COLORS["danger"]};
        border-color: rgba(239, 68, 68, 0.3);
    }}
    
    /* Real-time Badge */
    .realtime-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        animation: pulse 2s infinite;
    }}
    
    .realtime-on {{
        background: rgba(34, 197, 94, 0.2);
        color: {COLORS["success"]};
        border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    
    .realtime-off {{
        background: rgba(239, 68, 68, 0.2);
        color: {COLORS["danger"]};
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    
    /* Event Card */
    .event-card {{
        background: {COLORS["surface"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }}
    
    .event-card:hover {{
        border-color: {COLORS["primary"]};
        transform: translateX(5px);
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS["surface"]};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS["border"]};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS["primary"]};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# MAIN APP LAYOUT
# ============================================

# Title and Icons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown(f"<div style='text-align: right;'><img src='{get_icon_svg('pill', COLORS['primary'], 80)}' style='animation: float 3s ease-in-out infinite;'></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 class='main-header'>MediNomix</h1>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='text-align: left;'><img src='{get_icon_svg('brain', COLORS['primary_gradient'], 80)}' style='animation: float 3s ease-in-out infinite 0.5s;'></div>", unsafe_allow_html=True)

# Sub-header with real-time status
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<div class='sub-header'>AI-Powered Medication Safety Intelligence Platform</div>", unsafe_allow_html=True)
with col2:
    # Real-time status badge
    is_connected = check_websocket_connection()
    badge_class = "realtime-badge realtime-on" if is_connected else "realtime-badge realtime-off"
    badge_text = "● REAL-TIME" if is_connected else "● OFFLINE"
    badge_icon = "wifi" if is_connected else "wifi-off"
    st.markdown(f"""
    <div style='text-align: right;'>
        <span class='{badge_class}'>
            <img src='{get_icon_svg(badge_icon, COLORS["success"] if is_connected else COLORS["danger"], 16)}'>
            {badge_text}
        </span>
    </div>
    """, unsafe_allow_html=True)

# Status Indicators
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
status_cols = st.columns(4)

with status_cols[0]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("safety", COLORS["success"], 20)}'>
        Patient Safety First
    </span>
    """, unsafe_allow_html=True)

with status_cols[1]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("cpu", COLORS["primary"], 20)}'>
        AI-Powered Analysis
    </span>
    """, unsafe_allow_html=True)

with status_cols[2]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("layers", COLORS["secondary"], 20)}'>
        Multi-Layer Detection
    </span>
    """, unsafe_allow_html=True)

with status_cols[3]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("bolt", COLORS["accent"], 20)}'>
        Real-time Alerts
    </span>
    """, unsafe_allow_html=True)

# Action Buttons
st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

action_cols = st.columns([1, 1, 1, 1])
with action_cols[0]:
    if st.button(f"**Seed Database**", use_container_width=True, type="secondary"):
        with st.spinner("Seeding database with sample drugs..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()
with action_cols[1]:
    if st.button(f"**Refresh Data**", use_container_width=True, type="secondary"):
        with st.spinner("Refreshing dashboard data..."):
            load_dashboard_data()
            st.rerun()
with action_cols[2]:
    if st.button(f"**Quick Demo**", use_container_width=True):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
with action_cols[3]:
    if st.button(f"**Update Live Data**", use_container_width=True, type="secondary"):
        with st.spinner("Fetching real-time data..."):
            update_realtime_data()
            st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Modern Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    f"**Drug Analysis**", 
    f"**Analytics Dashboard**", 
    f"**Real-time Monitor**",
    f"**About & Resources**"
])

with tab1:
    # Drug Analysis Tab
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <img src='{get_icon_svg("search", COLORS["primary"], 80)}' style='margin-bottom: 20px; animation: pulse 2s infinite;'>
            <h2 style='color: {COLORS["text_primary"]}; font-size: 2.5rem; margin-bottom: 1rem;'>Drug Confusion Risk Analysis</h2>
            <p style='color: {COLORS["text_secondary"]}; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                Enter a drug name to analyze potential confusion risks with similar medications
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Search Section
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        drug_name = st.text_input(
            "Enter drug name:",
            placeholder="e.g., metformin, lamictal, celebrex...",
            label_visibility="visible",
            key="search_input"
        )
        
        search_cols = st.columns([1, 1])
        with search_cols[0]:
            search_clicked = st.button(f"**Analyze Drug**", use_container_width=True, type="primary")
        with search_cols[1]:
            if st.button(f"**Show Examples**", use_container_width=True, type="secondary"):
                examples = ["metformin", "lamictal", "celebrex", "clonidine", "zyprexa"]
                st.info(f"**Try these drugs:** {', '.join(examples)}")
    
    if search_clicked and drug_name:
        with st.spinner(f"Analyzing '{drug_name}' for confusion risks..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.")
                st.rerun()
    
    # Results Section
    if st.session_state.search_results:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Risk Filter Buttons
        st.markdown("### Filter Results")
        risk_filters = {
            "All Risks": "all",
            "Critical (≥75%)": "critical",
            "High (50-74%)": "high",
            "Medium (25-49%)": "medium",
            "Low (<25%)": "low"
        }
        
        filter_cols = st.columns(5)
        for i, (label, value) in enumerate(risk_filters.items()):
            btn_type = "primary" if st.session_state.selected_risk == value else "secondary"
            if filter_cols[i].button(label, use_container_width=True, type=btn_type):
                st.session_state.selected_risk = value
                st.rerun()
        
        # Filter results
        if st.session_state.selected_risk == "all":
            filtered_results = st.session_state.search_results
        else:
            filtered_results = [
                r for r in st.session_state.search_results 
                if r['risk_category'] == st.session_state.selected_risk
            ]
        
        # Results Header
        st.markdown(f"""
        <div style='background: {COLORS["surface"]}; padding: 1.5rem; border-radius: 16px; border: 1px solid {COLORS["border"]}; margin-bottom: 2rem;'>
            <h3 style='color: {COLORS["text_primary"]}; margin: 0; font-size: 1.6rem; display: flex; align-items: center; gap: 15px;'>
                <img src='{get_icon_svg("chart-network", COLORS["primary"], 24)}'>
                Found {len(filtered_results)} Similar Drugs
            </h3>
            <p style='color: {COLORS["text_secondary"]}; margin: 10px 0 0 0; display: flex; align-items: center; gap: 10px;'>
                <img src='{get_icon_svg("filter", COLORS["text_secondary"], 18)}'>
                Displaying {'all' if st.session_state.selected_risk == 'all' else st.session_state.selected_risk} risk levels
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Drug Cards
        for idx, result in enumerate(filtered_results):
            risk_class = result['risk_category']
            risk_color = {
                "critical": "#be185d",
                "high": COLORS["danger"],
                "medium": COLORS["warning"],
                "low": COLORS["success"]
            }.get(risk_class, COLORS["warning"])
            
            with st.container():
                st.markdown(f"""
                <div class='risk-card {risk_class}'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem;'>
                        <div>
                            <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 5px; font-size: 1.4rem; display: flex; align-items: center; gap: 10px;'>
                                <img src='{get_icon_svg("pill", risk_color, 24)}'>
                                {result['target_drug']['brand_name']}
                            </h3>
                            <p style='color: {COLORS["text_secondary"]}; margin: 0; font-style: italic; display: flex; align-items: center; gap: 8px;'>
                                <img src='{get_icon_svg("info", COLORS["text_secondary"], 16)}'>
                                {result['target_drug']['generic_name'] if result['target_drug']['generic_name'] else 'Generic name not available'}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <div style='background: {risk_color}20; color: {risk_color}; padding: 6px 16px; border-radius: 20px; 
                                 display: inline-block; font-weight: 700; font-size: 0.9rem; border: 1px solid {risk_color}40;'>
                                {risk_class.upper()}
                            </div>
                            <div style='margin-top: 10px; font-size: 2rem; font-weight: 800; color: {risk_color};'>
                                {result['combined_risk']:.0f}%
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Metrics Grid
                cols = st.columns(4)
                metrics = [
                    ("Spelling Similarity", f"{result['spelling_similarity']:.1f}%", "activity"),
                    ("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%", "trending-up"),
                    ("Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%", "layers"),
                    ("Overall Risk", f"{result['combined_risk']:.1f}%", "chart-line")
                ]
                
                for col, (label, value, icon) in zip(cols, metrics):
                    with col:
                        st.markdown(f"""
                        <div style='background: rgba(30, 41, 59, 0.5); padding: 1rem; border-radius: 12px; border: 1px solid {COLORS["border"]};'>
                            <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]}; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;'>
                                <img src='{get_icon_svg(icon, COLORS["primary"], 16)}'>
                                {label}
                            </div>
                            <div style='font-size: 1.5rem; font-weight: 700; color: {COLORS["text_primary"]};'>{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Additional Details
                with st.expander(f"View Drug Details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        if result['target_drug']['purpose']:
                            st.markdown(f"**Purpose:**")
                            st.info(result['target_drug']['purpose'][:200] + "..." if len(result['target_drug']['purpose']) > 200 else result['target_drug']['purpose'])
                    with col2:
                        if result['target_drug']['manufacturer']:
                            st.markdown(f"**Manufacturer:**")
                            st.text(result['target_drug']['manufacturer'])
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

with tab2:
    # Analytics Dashboard Tab
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <img src='{get_icon_svg("dashboard", COLORS["primary"], 80)}' style='margin-bottom: 20px; animation: pulse 2s infinite;'>
        <h2 style='color: {COLORS["text_primary"]}; font-size: 2.5rem; margin-bottom: 1rem;'>Medication Safety Analytics</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
            Advanced analytics and insights into drug confusion risks and safety patterns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Metrics Cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        metric_cols = st.columns(4)
        
        metric_data = [
            ("Total Drugs", metrics.get('total_drugs', 0), COLORS["primary"], "database"),
            ("High Risk Pairs", metrics.get('high_risk_pairs', 0), COLORS["danger"], "alert"),
            ("Critical Pairs", metrics.get('critical_risk_pairs', 0), "#be185d", "x-circle"),
            ("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%", COLORS["secondary"], "chart-line")
        ]
        
        for col, (title, value, color, icon) in zip(metric_cols, metric_data):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 1rem; color: {COLORS["text_secondary"]}; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 10px;'>
                        <img src='{get_icon_svg(icon, color, 24)}'>
                        <span>{title}</span>
                    </div>
                    <div class='value'>{value}</div>
                    <div class='label'>
                        {metric_data[metric_cols.index(col)][0].replace('Avg Risk Score', 'Average confusion risk')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Heatmap Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 15px;'>
            <img src='{get_icon_svg("chart-network", COLORS["primary"], 24)}'>
            Drug Confusion Heatmap
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown(f"""
        <div style='background: {COLORS["surface"]}; padding: 1.5rem; border-radius: 16px; border: 1px solid {COLORS["border"]}; margin-top: 2rem;'>
            <p style='margin: 0; display: flex; align-items: flex-start; gap: 15px; color: {COLORS["text_secondary"]};'>
                <img src='{get_icon_svg("info", COLORS["primary"], 20)}'>
                <span><b>How to read this heatmap:</b> Each cell shows confusion risk between two drugs. 
                Colors range from green (low risk) to pink (critical risk). 
                Hover over any cell for detailed information.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs or seed the database first.")
    
    # Charts Section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 2rem; display: flex; align-items: center; gap: 15px;'>
        <img src='{get_icon_svg("chart-pie", COLORS["primary"], 24)}'>
        Risk Analytics
    </h3>
    """, unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown(f"#### Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available.")
    
    with chart_col2:
        st.markdown(f"#### Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available.")
    
    # FDA Alert Table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 15px;'>
        <img src='{get_icon_svg("alert", COLORS["danger"], 24)}'>
        FDA High Alert Drug Pairs
    </h3>
    """, unsafe_allow_html=True)
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", 
         "Medical Use": "Epilepsy vs Fungal infection", "Alert Type": "FDA Safety Warning", "Year": "2023"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", 
         "Medical Use": "Arthritis vs Depression", "Alert Type": "ISMP High Alert", "Year": "2023"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", 
         "Medical Use": "Diabetes vs Antibiotic", "Alert Type": "Common Error", "Year": "2022"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", 
         "Medical Use": "Blood pressure vs Anxiety", "Alert Type": "Sound-alike", "Year": "2022"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", 
         "Medical Use": "Antipsychotic vs Allergy", "Alert Type": "Look-alike", "Year": "2021"},
        {"Drug 1": "Hydrocodone", "Drug 2": "Oxycodone", "Risk Level": "Critical", 
         "Medical Use": "Pain medication", "Alert Type": "FDA Black Box", "Year": "2023"},
    ])
    
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Drug 1": st.column_config.TextColumn("Drug 1", width="medium"),
            "Drug 2": st.column_config.TextColumn("Drug 2", width="medium"),
            "Risk Level": st.column_config.TextColumn("Risk", width="small"),
            "Alert Type": st.column_config.TextColumn("Alert", width="medium"),
            "Year": st.column_config.NumberColumn("Year", width="small")
        }
    )

with tab3:
    # REAL-TIME DASHBOARD TAB - NEW FEATURE
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <img src='{get_icon_svg("activity", COLORS["primary"], 80)}' style='margin-bottom: 20px; animation: pulse 1s infinite;'>
        <h2 style='color: {COLORS["text_primary"]}; font-size: 2.5rem; margin-bottom: 1rem;'>Real-time Safety Monitor</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
            Live monitoring of medication safety metrics and system events
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Connection Status
    is_connected = check_websocket_connection()
    status_cols = st.columns(3)
    
    with status_cols[0]:
        status_class = "status-indicator status-healthy" if is_connected else "status-indicator status-critical"
        status_icon = "check-circle" if is_connected else "x-circle"
        status_text = "Connected" if is_connected else "Disconnected"
        st.markdown(f"""
        <div style='text-align: center;'>
            <span class='{status_class}' style='margin-bottom: 10px; display: inline-block;'>
                <img src='{get_icon_svg(status_icon, COLORS["success"] if is_connected else COLORS["danger"], 20)}'>
                {status_text}
            </span>
            <div style='color: {COLORS["text_secondary"]}; font-size: 0.9rem;'>WebSocket Status</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_cols[1]:
        last_update = st.session_state.last_update.strftime("%H:%M:%S") if st.session_state.last_update else "Never"
        st.markdown(f"""
        <div style='text-align: center;'>
            <div style='font-size: 1.8rem; font-weight: 700; color: {COLORS["primary"]}; margin-bottom: 5px;'>{last_update}</div>
            <div style='color: {COLORS["text_secondary"]}; font-size: 0.9rem;'>Last Update</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_cols[2]:
        event_count = len(st.session_state.realtime_events.get('events', [])) if st.session_state.realtime_events else 0
        st.markdown(f"""
        <div style='text-align: center;'>
            <div style='font-size: 1.8rem; font-weight: 700; color: {COLORS["secondary"]}; margin-bottom: 5px;'>{event_count}</div>
            <div style='color: {COLORS["text_secondary"]}; font-size: 0.9rem;'>Recent Events</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Real-time Metrics
    st.markdown(f"""
    <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 15px;'>
        <img src='{get_icon_svg("cpu", COLORS["primary"], 24)}'>
        Live System Metrics
    </h3>
    """, unsafe_allow_html=True)
    
    if st.session_state.realtime_metrics:
        metrics = st.session_state.realtime_metrics
        rt_cols = st.columns(4)
        
        rt_metric_data = [
            ("Connected Clients", metrics.get('connected_clients', 0), COLORS["primary"], "users"),
            ("System Status", metrics.get('system_status', 'unknown').title(), 
             COLORS["success"] if metrics.get('system_status') == 'healthy' else COLORS["warning"], "server"),
            ("Total Analyses", metrics.get('total_analyses', 0), COLORS["secondary"], "activity"),
            ("Active Drugs", metrics.get('total_drugs', 0), COLORS["accent"], "database")
        ]
        
        for col, (title, value, color, icon) in zip(rt_cols, rt_metric_data):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 1rem; color: {COLORS["text_secondary"]}; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 10px;'>
                        <img src='{get_icon_svg(icon, color, 20)}'>
                        <span>{title}</span>
                    </div>
                    <div style='font-size: 2.5rem; font-weight: 800; color: {color}; margin-bottom: 8px;'>{value}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Additional metrics in 2 columns
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        metric_cols = st.columns(2)
        
        with metric_cols[0]:
            # Recent Searches
            st.markdown(f"""
            <div style='background: {COLORS["surface"]}; padding: 1.5rem; border-radius: 16px; border: 1px solid {COLORS["border"]};'>
                <h4 style='color: {COLORS["text_primary"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
                    <img src='{get_icon_svg("search", COLORS["primary"], 20)}'>
                    Recent Searches
                </h4>
            """, unsafe_allow_html=True)
            
            recent_searches = metrics.get('recent_searches', [])
            if recent_searches:
                for search in recent_searches[:5]:
                    st.markdown(f"""
                    <div class='event-card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <div style='font-weight: 600; color: {COLORS["text_primary"]};'>{search.get('drug_name', 'Unknown')}</div>
                                <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]};'>{search.get('timestamp', '')}</div>
                            </div>
                            <div style='text-align: right;'>
                                <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]};'>{search.get('risks_found', 0)} risks</div>
                                <div style='font-size: 1.2rem; font-weight: 700; color: {COLORS["primary"]};'>{search.get('highest_risk', 0):.0f}%</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<p style="color: {COLORS["text_secondary"]}; text-align: center;">No recent searches</p>',
                    unsafe_allow_html=True
                )

            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with metric_cols[1]:
            # Risk Statistics
            st.markdown(f"""
            <div style='background: {COLORS["surface"]}; padding: 1.5rem; border-radius: 16px; border: 1px solid {COLORS["border"]};'>
                <h4 style='color: {COLORS["text_primary"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
                    <img src='{get_icon_svg("chart-bar", COLORS["danger"], 20)}'>
                    Risk Statistics
                </h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                    <div style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: 800; color: {COLORS["danger"]};'>{metrics.get('critical_risk_pairs', 0)}</div>
                        <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]};'>Critical Pairs</div>
                    </div>
                    <div style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: 800; color: {COLORS["warning"]};'>{metrics.get('high_risk_pairs', 0)}</div>
                        <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]};'>High Risk Pairs</div>
                    </div>
                    <div style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: 800; color: {COLORS["secondary"]};'>{metrics.get('avg_risk_score', 0):.1f}%</div>
                        <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]};'>Avg Risk</div>
                    </div>
                    <div style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: 800; color: {COLORS["accent"]};'>{metrics.get('total_analyses', 0)}</div>
                        <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]};'>Total Analyses</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("No real-time data available. Make sure the backend is running and click 'Update Live Data'.")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Real-time Events
    st.markdown(f"""
    <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 15px;'>
        <img src='{get_icon_svg("bell", COLORS["secondary"], 24)}'>
        System Events Stream
    </h3>
    """, unsafe_allow_html=True)
    
    if st.session_state.realtime_events and st.session_state.realtime_events.get('events'):
        events = st.session_state.realtime_events['events']
        
        for event in events[:10]:  # Show last 10 events
            event_type = event.get('type', 'unknown')
            severity = event.get('severity', 'info')
            event_data = event.get('data', {})
            timestamp = event.get('timestamp', '')
            
            # Determine color based on severity
            severity_color = {
                'critical': COLORS["danger"],
                'error': COLORS["danger"],
                'warning': COLORS["warning"],
                'info': COLORS["secondary"],
                'success': COLORS["success"]
            }.get(severity, COLORS["text_secondary"])
            
            # Determine icon based on event type
            event_icon = {
                'drug_searched': 'search',
                'new_drug_added': 'database',
                'error': 'x-circle',
                'warning': 'alert',
                'database_seeded': 'check-circle'
            }.get(event_type, 'info')
            
            st.markdown(f"""
            <div class='event-card'>
                <div style='display: flex; align-items: flex-start; gap: 15px;'>
                    <div style='flex-shrink: 0;'>
                        <img src='{get_icon_svg(event_icon, severity_color, 20)}'>
                    </div>
                    <div style='flex: 1;'>
                        <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                            <div>
                                <div style='font-weight: 600; color: {COLORS["text_primary"]}; text-transform: capitalize;'>
                                    {event_type.replace('_', ' ')}
                                </div>
                                <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]}; margin-top: 4px;'>
                                    {timestamp.split('T')[1][:8] if 'T' in timestamp else timestamp}
                                </div>
                            </div>
                            <div style='background: {severity_color}20; color: {severity_color}; padding: 4px 12px; 
                                 border-radius: 12px; font-size: 0.8rem; font-weight: 600; border: 1px solid {severity_color}40;'>
                                {severity}
                            </div>
                        </div>
                        {f"<div style='margin-top: 10px; color: {COLORS[\"text_secondary\"]}; font-size: 0.9rem;'>" + 
                         (json.dumps(event_data, indent=2) if isinstance(event_data, dict) else str(event_data)) + 
                         "</div>" if event_data else ""}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No events to display. System events will appear here as they occur.")
    
    # Refresh button for real-time data
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    if st.button(f"**Refresh Live Data**", use_container_width=True, type="primary"):
        with st.spinner("Fetching latest real-time data..."):
            update_realtime_data()
            st.rerun()

with tab4:
    # About Tab
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <img src='{get_icon_svg("safety", COLORS["primary"], 80)}' style='margin-bottom: 20px;'>
        <h2 style='color: {COLORS["text_primary"]}; font-size: 2.5rem; margin-bottom: 1rem;'>About MediNomix</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6;'>
            A next-generation healthcare safety platform designed to prevent medication errors through advanced AI analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Medication Errors", "25%", "involve name confusion", delta_color="inverse",
                  help="FDA Statistics")
    with col2:
        st.metric("Annual Harm", "1.5M", "Americans affected", delta_color="inverse",
                  help="National Impact")
    with col3:
        st.metric("Annual Cost", "$42B", "preventable expenses", delta_color="inverse",
                  help="Economic Burden")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Problem & Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left; border-left-color: {COLORS["danger"]};'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <img src='{get_icon_svg("alert", COLORS["danger"], 32)}' style='margin-right: 20px;'>
                <h3 style='color: {COLORS["danger"]}; margin: 0;'>The Challenge</h3>
            </div>
            <div style='color: {COLORS["text_secondary"]}; line-height: 1.7;'>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("warning", COLORS["danger"], 18)}'>
                    <span><b>25% of medication errors</b> involve name confusion</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("users", COLORS["danger"], 18)}'>
                    <span><b>1.5 million Americans</b> harmed annually</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px;'>
                    <img src='{get_icon_svg("x-circle", COLORS["danger"], 18)}'>
                    <span>Common pairs: <b>Lamictal↔Lamisil</b>, <b>Celebrex↔Celexa</b></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left; border-left-color: {COLORS["success"]};'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <img src='{get_icon_svg("check-circle", COLORS["success"], 32)}' style='margin-right: 20px;'>
                <h3 style='color: {COLORS["success"]}; margin: 0;'>Our Solution</h3>
            </div>
            <div style='color: {COLORS["text_secondary"]}; line-height: 1.7;'>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("brain", COLORS["success"], 18)}'>
                    <span><b>Multi-algorithm AI</b> risk assessment</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("activity", COLORS["success"], 18)}'>
                    <span><b>Real-time monitoring</b> and alerts</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px;'>
                    <img src='{get_icon_svg("bolt", COLORS["success"], 18)}'>
                    <span><b>Instant prevention</b> guidance</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    # Logo and Title
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <div style='display: inline-flex; align-items: center; justify-content: center; width: 80px; height: 80px; 
             background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_gradient"]}); 
             border-radius: 20px; margin-bottom: 15px;'>
            <img src='{get_icon_svg("pill", "#ffffff", 40)}'>
        </div>
        <h3 style='color: {COLORS["text_primary"]}; margin: 10px 0 5px 0; font-weight: 800;'>MediNomix</h3>
        <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; font-weight: 500;'>AI-Powered Medication Safety</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown(f"""
    <h4 style='color: {COLORS["text_primary"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <img src='{get_icon_svg("bolt", COLORS["primary"], 20)}'>
        Quick Actions
    </h4>
    """, unsafe_allow_html=True)
    
    if st.button(f"**Test with Metformin**", use_container_width=True, type="primary"):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
    
    if st.button(f"**Load Sample Data**", use_container_width=True, type="secondary"):
        if seed_database():
            load_dashboard_data()
            st.rerun()
    
    if st.button(f"**Update Live Feed**", use_container_width=True, type="secondary"):
        update_realtime_data()
        st.rerun()
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # System Status
    st.markdown(f"""
    <h4 style='color: {COLORS["text_primary"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <img src='{get_icon_svg('server', COLORS["primary"], 20)}'>
        System Status
    </h4>
    """, unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.markdown('<div class="status-indicator status-healthy">✅ Backend Connected</div>', unsafe_allow_html=True)
                status_cols = st.columns(2)
                with status_cols[0]:
                    st.metric("Drugs", data.get('drugs_in_database', 0), 
                             delta_color="normal", help="Drugs in database")
                with status_cols[1]:
                    st.metric("Risks", data.get('risk_assessments', 0),
                             delta_color="normal", help="Risk assessments")
            else:
                st.markdown('<div class="status-indicator status-warning">⚠️ Backend Error</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-critical">❌ Cannot Connect</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="status-indicator status-critical">🔌 Backend Not Running</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: rgba(239,68,68,0.1); padding: 15px; border-radius: 12px; margin-top: 10px; border: 1px solid rgba(239,68,68,0.2);'>
            <p style='margin: 0; font-size: 0.9rem; color: {COLORS["text_secondary"]}; line-height: 1.5;'>
            <b>Fix:</b> Run in terminal:<br>
            <code style='background: {COLORS["surface"]}; padding: 8px 12px; border-radius: 8px; 
                   font-size: 0.85rem; display: block; margin-top: 8px; font-family: monospace; color: {COLORS["text_primary"]};'>
            python backend.py</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Risk Categories Guide
    st.markdown(f"""
    <h4 style='color: {COLORS["text_primary"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <img src='{get_icon_svg('alert', COLORS["primary"], 20)}'>
        Risk Categories
    </h4>
    """, unsafe_allow_html=True)
    
    risk_categories = [
        ("Critical", "≥75%", "Immediate intervention", "#be185d"),
        ("High", "50-74%", "Review required", COLORS["danger"]),
        ("Medium", "25-49%", "Monitor closely", COLORS["warning"]),
        ("Low", "<25%", "Low priority", COLORS["success"])
    ]
    
    for name, range_, desc, color in risk_categories:
        st.markdown(f"""
        <div style='display: flex; align-items: flex-start; gap: 15px; margin-bottom: 15px; padding: 12px; 
             background: rgba(30, 41, 59, 0.5); border-radius: 10px; border: 1px solid {COLORS["border"]};'>
            <div style='width: 12px; height: 12px; background-color: {color}; border-radius: 50%; margin-top: 5px;'></div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; color: {COLORS["text_primary"]};'>{name} {range_}</div>
                <div style='font-size: 0.85rem; color: {COLORS["text_secondary"]}; margin-top: 4px;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# AUTO-REFRESH FOR REAL-TIME DATA
# ============================================

# Auto-refresh real-time data every 30 seconds
if st.session_state.get('auto_refresh', True):
    time_diff = (datetime.now() - st.session_state.last_update).seconds if st.session_state.last_update else 999
    if time_diff > 30:  # Refresh every 30 seconds
        update_realtime_data()

# Footer
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; padding: 2rem 0; color: {COLORS["text_secondary"]}; font-size: 0.9rem; 
     border-top: 1px solid {COLORS["border"]};'>
    <div style='margin-bottom: 10px;'>
        © 2024 MediNomix • Version 3.0 • Advanced Medication Safety Platform
    </div>
    <div style='opacity: 0.7;'>
        Real-time Dashboard Analytics • AI-Powered Risk Detection
    </div>
</div>
""", unsafe_allow_html=True)