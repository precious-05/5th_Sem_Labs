"""
MediNomix - Advanced Medication Safety Platform
ULTRA MODERN PROFESSIONAL UI with premium healthcare theme
FUNCTIONALITY: 100% preserved, only UI enhanced
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import base64

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

COLORS = {
    "primary": "#D946EF",
    "primary_light": "#E879F9",
    "primary_dark": "#C026D3",
    "secondary": "#8B5CF6",
    "accent": "#0EA5E9",
    "accent_pink": "#F472B6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "dark": "#1E1B4B",
    "light": "#FDF4FF",
    "surface": "#FFB7F5",
    "gray": "#A78BFA",
    "gray_light": "#FAF5FF",
    "border": "#F5D0FE",
}

# Base64 encoded SVG Icons for FontAwesome-like appearance
def get_icon_svg(icon_name, color="#4361ee", size=24):
    """Generate base64 encoded SVG icons"""
    icon_map = {
        "pill": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.5 20H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v6.5"/>
            <rect x="8" y="12" width="8" height="8" rx="2"/>
            <path d="m18.5 9.5-1 1"/>
            <path d="m15.5 9.5-1 1"/>
        </svg>
        """,
        "search": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
            <path d="M11 8v6"/>
            <path d="M8 11h6"/>
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
        "hospital": f"""
        <svg xmlns="http://www.w3.org2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 22h18"/>
            <path d="M6 18v-6"/>
            <path d="M10 18v-6"/>
            <path d="M14 18v-6"/>
            <path d="M18 18v-6"/>
            <path d="M12 6V2"/>
            <path d="M8 6h8"/>
            <rect x="4" y="6" width="16" height="12" rx="2"/>
        </svg>
        """,
        "brain": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-2.5 2.5h-2A2.5 2.5 0 0 1 5 19.5v-15A2.5 2.5 0 0 1 7.5 2z"/>
            <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 2.5 2.5h2A2.5 2.5 0 0 0 19 19.5v-15A2.5 2.5 0 0 0 16.5 2z"/>
            <path d="M12 8v4"/>
            <path d="M12 16v2"/>
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
            <path d="M21 2v6h-6"/>
            <path d="M3 12a9 9 0 0 1 15-6.7L21 8"/>
            <path d="M3 22v-6h6"/>
            <path d="M21 12a9 9 0 0 1-15 6.7L3 16"/>
        </svg>
        """,
        "info": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
        </svg>
        """,
        "stats": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"/>
            <line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="14"/>
        </svg>
        """,
        "heartbeat": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 17H2l4-8 5 5 7-7"/>
            <path d="M2 12h6"/>
            <path d="M16 12h6"/>
        </svg>
        """,
        "capsules": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 2v6"/>
            <path d="M14 2v6"/>
            <path d="M16 8a4 4 0 0 1-8 0"/>
            <rect x="4" y="10" width="16" height="10" rx="2"/>
        </svg>
        """,
        "chart-network": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="2"/>
            <circle cx="6" cy="6" r="2"/>
            <circle cx="18" cy="6" r="2"/>
            <circle cx="6" cy="18" r="2"/>
            <circle cx="18" cy="18" r="2"/>
            <line x1="6" y1="8" x2="6" y2="16"/>
            <line x1="12" y1="10" x2="12" y2="14"/>
            <line x1="18" y1="8" x2="18" y2="16"/>
            <line x1="8" y1="6" x2="16" y2="6"/>
            <line x1="8" y1="18" x2="16" y2="18"/>
            <line x1="10" y1="12" x2="14" y2="12"/>
        </svg>
        """,
        "shield": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        """,
        "bell": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        """,
        "check": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 6 9 17l-5-5"/>
        </svg>
        """,
        "chevron-right": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"/>
        </svg>
        """,
        "filter": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
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
        "trash": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 6h18"/>
            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
            <line x1="10" y1="11" x2="10" y2="17"/>
            <line x1="14" y1="11" x2="14" y2="17"/>
        </svg>
        """,
        "lightbulb": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>
            <path d="M9 18h6"/>
            <path d="M10 22h4"/>
        </svg>
        """,
        "rocket": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>
            <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>
            <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>
            <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>
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
        "tools": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
        </svg>
        """,
        "book": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        </svg>
        """,
        "chevron-up": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="18 15 12 9 6 15"/>
        </svg>
        """,
        "bug": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="6" height="6" rx="1"/>
            <path d="M12 3v2"/>
            <path d="M19 12h2"/>
            <path d="M12 19v2"/>
            <path d="M3 12h2"/>
            <path d="M17.66 6.34l1.41-1.41"/>
            <path d="M6.34 17.66l-1.41-1.41"/>
            <path d="M17.66 17.66l1.41 1.41"/>
            <path d="M6.34 6.34l-1.41 1.41"/>
        </svg>
        """,
        "flask": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 2v6"/>
            <path d="M14 2v6"/>
            <path d="M16 8a4 4 0 0 1-8 0"/>
            <path d="M5 10h14l1 10H4L5 10z"/>
        </svg>
        """,
        "wave-square": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 12h4v8H2z"/>
            <path d="M10 4h4v16h-4z"/>
            <path d="M18 8h4v12h-4z"/>
        </svg>
        """,
        "stethoscope": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4.5 3h15v5a7.5 7.5 0 0 1-7.5 7.5A7.5 7.5 0 0 1 4.5 8V3z"/>
            <path d="M8.5 18a4.5 4.5 0 1 0 9 0v-3"/>
            <circle cx="18" cy="11" r="2"/>
        </svg>
        """,
        "tachometer": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v10"/>
            <path d="m19.07 19.07-1.41-1.41"/>
            <path d="M5 12a7 7 0 1 0 14 0"/>
            <circle cx="12" cy="12" r="3"/>
        </svg>
        """,
        "industry": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22V8"/>
            <path d="M2 12h4l2-4 2 4h4l2-4 2 4h4l2-4 2 4h4"/>
            <rect x="2" y="16" width="20" height="6" rx="2"/>
        </svg>
        """,
        "cogs": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
        """,
        "bolt": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
            <polyline points="12.5 22 12.5 12 20 8"/>
            <polyline points="11.5 2 11.5 12 4 8"/>
        </svg>
        """,
        "dollar": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="1" x2="12" y2="23"/>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
        """,
        "microchip": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="4" y="4" width="16" height="16" rx="2"/>
            <rect x="9" y="9" width="6" height="6"/>
            <path d="M15 2v2"/>
            <path d="M15 20v2"/>
            <path d="M2 15h2"/>
            <path d="M2 9h2"/>
            <path d="M20 15h2"/>
            <path d="M20 9h2"/>
            <path d="M9 2v2"/>
            <path d="M9 20v2"/>
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
        "vial": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 2v4"/>
            <path d="M16 2v4"/>
            <rect x="4" y="6" width="16" height="16" rx="2"/>
            <path d="M9 13h6"/>
        </svg>
        """,
        "book-medical": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            <path d="M12 8v4"/>
            <path d="M10 12h4"/>
        </svg>
        """,
        "exclamation": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        """,
        "triangle": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
        </svg>
        """,
        "spell-check": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m6 16 6-12 6 12"/>
            <path d="M8 12h8"/>
            <path d="M4 21c1.1 0 1.1-1 2.3-1s1.1 1 2.3 1c1.1 0 1.1-1 2.3-1 1.1 0 1.1 1 2.3 1 1.1 0 1.1-1 2.3-1 1.1 0 1.1 1 2.3 1 1.1 0 1.1-1 2.3-1"/>
        </svg>
        """,
        "thermometer": f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0z"/>
        </svg>
        """,
    }
    
    if icon_name in icon_map:
        svg = icon_map[icon_name]
        b64 = base64.b64encode(svg.encode('utf-8')).decode()
        return f"data:image/svg+xml;base64,{b64}"
    return ""

# Initialize session state
for key in ['search_results', 'dashboard_data', 'selected_risk', 'heatmap_data']:
    if key not in st.session_state:
        st.session_state[key] = None if key == 'heatmap_data' else ([] if key == 'search_results' else {} if key == 'dashboard_data' else "all")

# Helper functions - 100% SAME FUNCTIONALITY
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
            
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")

def create_heatmap_chart():
    """Create interactive drug confusion heatmap - Modern Design"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Modern heatmap with gradient colors
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS["success"]],
            [0.25, COLORS["warning"]],
            [0.5, "#ff9a00"],  # Orange
            [0.75, COLORS["danger"]],
            [1, "#b5179e"]     # Dark Pink
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
            titlefont=dict(size=14),
            tickfont=dict(size=12),
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
            "font": {"size": 24, "color": COLORS["dark"], "family": "'Poppins', sans-serif"}
        },
        xaxis_title="<b>Drug Names</b>",
        yaxis_title="<b>Drug Names</b>",
        height=650,
        margin={"t": 100, "b": 100, "l": 120, "r": 50},
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["light"],
        font=dict(family="'Poppins', sans-serif", size=12, color=COLORS["dark"]),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10),
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True
        )
    )
    
    return fig

def create_risk_breakdown_chart():
    """Create modern risk breakdown donut chart"""
    if 'breakdown' not in st.session_state.dashboard_data:
        return None
    
    breakdown = st.session_state.dashboard_data['breakdown']
    if not breakdown:
        return None
    
    categories = [item['category'].title() for item in breakdown]
    counts = [item['count'] for item in breakdown]
    
    color_map = {
        "Critical": "#b5179e",  # Dark Pink
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
            textfont=dict(size=13, color="white", family="'Poppins', sans-serif"),
            marker=dict(line=dict(color=COLORS["surface"], width=2))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Risk Distribution",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": COLORS["dark"], "family": "'Poppins', sans-serif"}
        },
        height=450,
        margin=dict(t=80, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05,
            font=dict(size=12, family="'Poppins', sans-serif")
        ),
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["light"],
        font=dict(family="'Poppins', sans-serif", size=12, color=COLORS["dark"]),
    )
    
    # Add center text
    fig.add_annotation(
        text=f"<b>Total</b><br>{sum(counts)}",
        x=0.5, y=0.5,
        font=dict(size=16, color=COLORS["dark"], family="'Poppins', sans-serif"),
        showarrow=False
    )
    
    return fig

def create_top_risks_chart():
    """Create modern top risks horizontal bar chart"""
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
        "critical": "#b5179e",
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
            textfont=dict(size=11, color=COLORS["dark"], family="'Poppins', sans-serif"),
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><br>Category: %{customdata[0]}<br>%{customdata[1]}<extra></extra>",
            customdata=list(zip(categories, reasons)),
            marker=dict(line=dict(color=COLORS["surface"], width=1))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Top 10 High-Risk Drug Pairs",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 22, "color": COLORS["dark"], "family": "'Poppins', sans-serif"}
        },
        xaxis_title="<b>Risk Score (%)</b>",
        yaxis_title="<b>Drug Pairs</b>",
        height=500,
        margin=dict(t=80, b=50, l=220, r=50),
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["light"],
        font=dict(family="'Poppins', sans-serif", size=12, color=COLORS["dark"]),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            range=[0, 105],
            showgrid=True
        ),
        yaxis=dict(
            tickfont=dict(size=11, family="'Poppins', sans-serif"),
            categoryorder='total ascending'
        )
    )
    
    # Add threshold lines
    fig.add_vline(x=75, line_dash="dash", line_color="#b5179e", opacity=0.3)
    fig.add_vline(x=50, line_dash="dash", line_color=COLORS["danger"], opacity=0.3)
    fig.add_vline(x=25, line_dash="dash", line_color=COLORS["warning"], opacity=0.3)
    
    return fig

# Ultra Modern CSS Styling with Animations
st.markdown(f"""
<style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Montserrat:wght@700;800;900&display=swap');
    
    /* Base Reset */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    /* Modern Medical Theme */
    .stApp {{
        background: linear-gradient(135deg, {COLORS["light"]} 0%, #ffffff 100%);
        font-family: 'Poppins', sans-serif;
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
            radial-gradient(circle at 10% 20%, rgba(67, 97, 238, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(76, 201, 240, 0.03) 0%, transparent 40%);
        z-index: -1;
        pointer-events: none;
    }}
    
    /* Floating Animation */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(180deg); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.05); opacity: 0.8; }}
    }}
    
    @keyframes slideInLeft {{
        from {{ transform: translateX(-30px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    @keyframes slideInRight {{
        from {{ transform: translateX(30px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    @keyframes fadeInUp {{
        from {{ transform: translateY(20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
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
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        text-shadow: 0 4px 20px rgba(67, 97, 238, 0.1);
        animation: fadeInUp 0.8s ease-out;
    }}
    
    .sub-header {{
        color: {COLORS["gray"]};
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
        animation: fadeInUp 0.8s ease-out 0.2s both;
        opacity: 0;
    }}
    
    /* Modern Card Design */
    .metric-card {{
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, rgba(255, 255, 255, 0.95) 100%);
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.06),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.4);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.6s ease-out;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-left: 4px solid {COLORS["primary"]};
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }}
    
    .metric-card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(67, 97, 238, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        border-color: {COLORS["primary"]};
    }}
    
    .metric-card:hover::before {{
        left: 100%;
    }}
    
    /* Modern Risk Cards */
    .risk-card {{
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, rgba(255, 255, 255, 0.95) 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        border-left: 6px solid;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease-out;
    }}
    
    .risk-card::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }}
    
    .risk-card:hover::after {{
        transform: translateX(100%);
    }}
    
    .risk-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }}
    
    .risk-card.critical {{ 
        border-left-color: #b5179e;
        background: linear-gradient(135deg, rgba(181, 23, 158, 0.05) 0%, {COLORS["surface"]} 100%);
    }}
    .risk-card.high {{ 
        border-left-color: {COLORS["danger"]};
        background: linear-gradient(135deg, rgba(239, 71, 111, 0.05) 0%, {COLORS["surface"]} 100%);
    }}
    .risk-card.medium {{ 
        border-left-color: {COLORS["warning"]};
        background: linear-gradient(135deg, rgba(255, 209, 102, 0.05) 0%, {COLORS["surface"]} 100%);
    }}
    .risk-card.low {{ 
        border-left-color: {COLORS["success"]};
        background: linear-gradient(135deg, rgba(6, 214, 160, 0.05) 0%, {COLORS["surface"]} 100%);
    }}
    
    /* Modern Button System */
    .stButton > button {{
        position: relative !important;
        padding: 16px 32px !important;
        border: none !important;
        border-radius: 15px !important;
        cursor: pointer !important;
        overflow: hidden !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 56px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 12px !important;
        letter-spacing: 0.3px !important;
        text-transform: uppercase !important;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
        color: white !important;
        background-size: 200% auto !important;
        box-shadow: 
            0 8px 25px rgba(67, 97, 238, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-5px) !important;
        box-shadow: 
            0 15px 35px rgba(67, 97, 238, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        background-position: right center !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(-2px) !important;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    /* Secondary Button */
    .stButton > button[kind="secondary"] {{
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, rgba(248, 249, 250, 0.95) 100%) !important;
        color: {COLORS["primary"]} !important;
        border: 2px solid {COLORS["primary"]} !important;
        box-shadow: 0 4px 15px rgba(67, 97, 238, 0.1) !important;
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
        color: white !important;
        border-color: transparent !important;
        transform: translateY(-5px) !important;
    }}
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, rgba(255, 255, 255, 0.95) 100%);
        padding: 12px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 60px;
        padding: 0 28px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Poppins', sans-serif;
        color: {COLORS["gray"]};
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: linear-gradient(135deg, rgba(67, 97, 238, 0.1) 0%, rgba(114, 9, 183, 0.05) 100%) !important;
        color: {COLORS["primary"]} !important;
        transform: translateY(-2px);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
        color: white !important;
        box-shadow: 0 6px 20px rgba(67, 97, 238, 0.25);
        transform: translateY(-2px);
    }}
    
    /* Modern Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, rgba(255, 255, 255, 0.98) 100%);
        font-family: 'Poppins', sans-serif;
        border-right: 1px solid rgba(67, 97, 238, 0.1);
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.05);
    }}
    
    /* Modern Inputs */
    .stTextInput > div > div > input {{
        border-radius: 12px;
        border: 2px solid rgba(67, 97, 238, 0.15);
        padding: 16px 20px;
        font-size: 16px;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, rgba(255, 255, 255, 0.95) 100%);
        backdrop-filter: blur(10px);
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 0 0 4px rgba(67, 97, 238, 0.1);
        transform: translateY(-2px);
    }}
    
    /* Modern Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        font-family: 'Montserrat', sans-serif !important;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;
        color: transparent !important;
        letter-spacing: -1px !important;
    }}
    
    /* Animated Divider */
    .divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent, {COLORS["primary"]} 50%, transparent);
        margin: 3rem 0;
        position: relative;
        overflow: hidden;
    }}
    
    .divider::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
        animation: shimmer 3s infinite;
    }}
    
    /* Modern Badges */
    .risk-badge {{
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-family: 'Poppins', sans-serif;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        backdrop-filter: blur(10px);
        border: 2px solid;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .risk-badge:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }}
    
    /* Info Box */
    .info-box {{
        background: linear-gradient(135deg, rgba(67, 97, 238, 0.08) 0%, rgba(114, 9, 183, 0.05) 100%);
        border-radius: 15px;
        padding: 2rem;
        border-left: 4px solid {COLORS["primary"]};
        margin: 1.5rem 0;
        font-family: 'Poppins', sans-serif;
        border: 1px solid rgba(67, 97, 238, 0.1);
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.6s ease-out;
    }}
    
    /* Section Headers */
    .section-header {{
        color: {COLORS["dark"]};
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 2rem;
        font-family: 'Montserrat', sans-serif;
        position: relative;
        display: inline-block;
        animation: slideInLeft 0.6s ease-out;
    }}
    
    .section-header::after {{
        content: '';
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%);
        border-radius: 2px;
        animation: gradientShift 3s ease infinite;
    }}
    
    /* Grid Items */
    .grid-item {{
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, rgba(255, 255, 255, 0.95) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(67, 97, 238, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }}
    
    .grid-item:hover {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 10px 25px rgba(67, 97, 238, 0.15);
        transform: translateY(-5px);
    }}
    
    /* Status Indicators */
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 2px solid;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .status-indicator:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }}
    
    .status-healthy {{
        background: rgba(6, 214, 160, 0.15);
        color: {COLORS["success"]};
        border-color: rgba(6, 214, 160, 0.3);
    }}
    
    .status-warning {{
        background: rgba(255, 209, 102, 0.15);
        color: {COLORS["warning"]};
        border-color: rgba(255, 209, 102, 0.3);
    }}
    
    .status-critical {{
        background: rgba(181, 23, 158, 0.15);
        color: #b5179e;
        border-color: rgba(181, 23, 158, 0.3);
    }}
    
    /* Floating Action Button */
    .fab {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(67, 97, 238, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1000;
        animation: pulse 2s infinite;
    }}
    
    .fab:hover {{
        transform: scale(1.1) rotate(90deg);
        box-shadow: 0 15px 40px rgba(67, 97, 238, 0.6);
    }}
    
    /* Loading Spinner */
    .spinner {{
        width: 60px;
        height: 60px;
        border: 4px solid rgba(67, 97, 238, 0.1);
        border-top: 4px solid {COLORS["primary"]};
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: linear-gradient(135deg, {COLORS["light"]} 0%, #ffffff 100%);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%);
        border-radius: 10px;
        border: 2px solid {COLORS["light"]};
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, {COLORS["primary_dark"]} 0%, #5a08a8 100%);
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2.5rem;
        }}
        
        .metric-card {{
            padding: 1.5rem;
        }}
        
        .stButton > button {{
            padding: 14px 24px !important;
            font-size: 14px !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# SECTION 1: REPLACED RAW HTML WITH STREAMLIT COMPONENTS
# ============================================

# Main Header Section - Replacing raw HTML with Streamlit components
st.markdown("""
<div style='position: relative; text-align: center; padding: 3rem 0 2rem 0;'>
    <!-- Animated Background Blobs -->
    <div style='position: absolute; top: 100px; right: 10%; width: 150px; height: 150px; 
         background: linear-gradient(135deg, #cf4cf020, #3a8ba420); border-radius: 50%; 
         filter: blur(50px); animation: float 6s infinite ease-in-out 1s;'></div>
</div>
""", unsafe_allow_html=True)

# Title and Icons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown(f"<div style='text-align: right;'><img src='{get_icon_svg('pill', COLORS['primary'], 80)}' style='animation: pulse 3s infinite;'></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 class='main-header'>MediNomix</h1>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='text-align: left;'><img src='{get_icon_svg('brain', COLORS['accent'], 80)}' style='animation: pulse 3s infinite 0.5s;'></div>", unsafe_allow_html=True)

# Sub-header
st.markdown("<div class='sub-header'>AI-Powered Medication Safety Intelligence Platform</div>", unsafe_allow_html=True)

# Status Indicators - Using columns instead of raw HTML
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
status_cols = st.columns(4)

with status_cols[0]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("safety", COLORS["success"], 20)}' style='width: 20px; height: 20px;'>
        Patient Safety First
    </span>
    """, unsafe_allow_html=True)

with status_cols[1]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("microchip", COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
        AI-Powered Analysis
    </span>
    """, unsafe_allow_html=True)

with status_cols[2]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("hospital", COLORS["accent"], 20)}' style='width: 20px; height: 20px;'>
        Hospital Grade
    </span>
    """, unsafe_allow_html=True)

with status_cols[3]:
    st.markdown(f"""
    <span class='status-indicator status-healthy'>
        <img src='{get_icon_svg("shield", COLORS["success"], 20)}' style='width: 20px; height: 20px;'>
        Real-time Protection
    </span>
    """, unsafe_allow_html=True)

# Modern Action Buttons with Base64 Icons
st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <div style='display: inline-flex; gap: 15px; background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); 
         padding: 20px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
         backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.3);'>
""", unsafe_allow_html=True)

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
    if st.button(f"**Get Help**", use_container_width=True, type="secondary"):
        st.info(f"""
        **Quick Tips:**
        1. Search any drug name to analyze confusion risks
        2. Use the heatmap to visualize risk patterns
        3. Check FDA alerts for known dangerous pairs
        4. Filter results by risk level for focused analysis
        """)

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Modern Navigation Tabs with Base64 Icons
tab1, tab2, tab3 = st.tabs([
    f"**Drug Analysis**", 
    f"**Analytics Dashboard**", 
    f"**About & Resources**"
])

with tab1:
    # Modern Search Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <img src='{get_icon_svg("search", COLORS["primary"], 80)}' style='margin-bottom: 20px; display: block; animation: pulse 2s infinite;'>
            <h2 class='section-header'>Drug Confusion Risk Analysis</h2>
            <p style='color: {COLORS["gray"]}; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                Enter a drug name to analyze potential confusion risks with similar medications using advanced AI algorithms
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Modern Search Bar - FIXED LABEL ISSUE
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        drug_name = st.text_input(
            "Enter drug name:",
            placeholder="e.g., metformin, lamictal, celebrex...",
            label_visibility="visible",
            key="search_input"
        )
        
        # Modern Search Buttons
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
        
        # Modern Risk Filter Buttons
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
        
        # Modern Results Header
        st.markdown(f"""
        <div class='info-box'>
            <h3 style='color: {COLORS["dark"]}; margin: 0; font-size: 1.6rem; display: flex; align-items: center; gap: 15px;'>
                <img src='{get_icon_svg("chart-network", COLORS["primary"], 24)}' style='width: 24px; height: 24px;'>
                Found {len(filtered_results)} Similar Drugs
            </h3>
            <p style='color: {COLORS["gray"]}; margin: 10px 0 0 0; display: flex; align-items: center; gap: 10px;'>
                <img src='{get_icon_svg("filter", COLORS["gray"], 18)}' style='width: 18px; height: 18px;'>
                Displaying {'all' if st.session_state.selected_risk == 'all' else st.session_state.selected_risk} risk levels
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Modern Drug Cards
        for idx, result in enumerate(filtered_results):
            risk_class = result['risk_category']
            risk_color = {
                "critical": "#b5179e",
                "high": COLORS["danger"],
                "medium": COLORS["warning"],
                "low": COLORS["success"]
            }.get(risk_class, COLORS["warning"])
            
            with st.container():
                # Card Container
                st.markdown(f"""
                <div class='risk-card {risk_class}'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem;'>
                        <div>
                            <h3 style='color: {COLORS["dark"]}; margin-bottom: 5px; font-size: 1.4rem; display: flex; align-items: center; gap: 10px;'>
                                <img src='{get_icon_svg("capsules", risk_color, 24)}' style='width: 24px; height: 24px;'>
                                {result['target_drug']['brand_name']}
                            </h3>
                            <p style='color: {COLORS["gray"]}; margin: 0; font-style: italic; display: flex; align-items: center; gap: 8px;'>
                                <img src='{get_icon_svg("vial", COLORS["gray"], 16)}' style='width: 16px; height: 16px;'>
                                {result['target_drug']['generic_name'] if result['target_drug']['generic_name'] else 'Generic name not available'}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span class='risk-badge' style='background-color: {risk_color}15; color: {risk_color}; border-color: {risk_color};'>
                                <img src='{get_icon_svg("exclamation", risk_color, 16)}' style='width: 16px; height: 16px;'>
                                {risk_class.upper()}
                            </span>
                            <div style='margin-top: 10px; font-size: 2rem; font-weight: 800; color: {risk_color};'>
                                {result['combined_risk']:.0f}%
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Modern Metrics Grid
                cols = st.columns(4)
                metrics = [
                    ("Spelling Similarity", f"{result['spelling_similarity']:.1f}%", "spell-check"),
                    ("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%", "wave-square"),
                    ("Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%", "stethoscope"),
                    ("Overall Risk", f"{result['combined_risk']:.1f}%", "tachometer")
                ]
                
                for col, (label, value, icon) in zip(cols, metrics):
                    with col:
                        st.markdown(f"""
                        <div class='grid-item'>
                            <div style='font-size: 0.9rem; color: {COLORS["gray"]}; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;'>
                                <img src='{get_icon_svg(icon, COLORS["gray"], 16)}' style='width: 16px; height: 16px;'>
                                {label}
                            </div>
                            <div style='font-size: 1.5rem; font-weight: 700; color: {COLORS["dark"]};'>{value}</div>
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
    # Modern Dashboard
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <img src='{get_icon_svg("dashboard", COLORS["primary"], 80)}' style='margin-bottom: 20px; display: block; animation: pulse 2s infinite;'>
        <h2 class='section-header'>Medication Safety Analytics</h2>
        <p style='color: {COLORS["gray"]}; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
            Real-time insights into drug confusion risks and safety patterns using advanced AI analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Modern Metrics Cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        metric_cols = st.columns(4)
        
        metric_data = [
            ("Total Drugs", metrics.get('total_drugs', 0), COLORS["primary"], "database"),
            ("High/Critical Pairs", metrics.get('high_risk_pairs', 0), "#b5179e", "alert"),
            ("Critical Pairs", metrics.get('critical_risk_pairs', 0), COLORS["danger"], "triangle"),
            ("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%", COLORS["accent"], "chart-line")
        ]
        
        for col, (title, value, color, icon) in zip(metric_cols, metric_data):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 1rem; color: {COLORS["gray"]}; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 10px;'>
                        <img src='{get_icon_svg(icon, color, 24)}' style='width: 24px; height: 24px;'>
                        <span>{title}</span>
                    </div>
                    <div style='font-size: 2.8rem; font-weight: 800; color: {color}; margin-bottom: 8px;'>{value}</div>
                    <div style='font-size: 0.85rem; color: {COLORS["gray"]}; opacity: 0.8;'>
                        {metric_data[metric_cols.index(col)][0].replace('Avg Risk Score', 'Average confusion risk').replace('Total Drugs', 'Total medications in database').replace('High/Critical Pairs', 'Pairs requiring attention').replace('Critical Pairs', 'Extreme risk pairs')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Heatmap Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h3 style='color: {COLORS["dark"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 15px;'>
            <img src='{get_icon_svg("chart-network", COLORS["primary"], 24)}' style='width: 24px; height: 24px;'>
            Drug Confusion Heatmap
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown(f"""
        <div class='info-box'>
            <p style='margin: 0; display: flex; align-items: flex-start; gap: 15px;'>
                <img src='{get_icon_svg("lightbulb", COLORS["primary"], 20)}' style='width: 20px; height: 20px; margin-top: 3px;'>
                <span><b>How to read this heatmap:</b> Each cell shows confusion risk between two drugs. 
                Green cells indicate low risk (<25%), yellow cells show moderate risk (25-50%), 
                orange cells indicate high risk (50-75%), and pink/magenta cells show critical risk (>75%). 
                Hover over any cell for detailed information.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"No heatmap data available. Search for drugs or seed the database first.")
    
    # Modern Charts Section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["dark"]}; margin-bottom: 2rem; display: flex; align-items: center; gap: 15px;'>
        <img src='{get_icon_svg("chart-pie", COLORS["primary"], 24)}' style='width: 24px; height: 24px;'>
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
            st.info(f"No risk breakdown data available.")
    
    with chart_col2:
        st.markdown(f"#### Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info(f"No top risk data available.")
    
    # FDA Alert Table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["dark"]}; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 15px;'>
        <img src='{get_icon_svg("alert", COLORS["danger"], 24)}' style='width: 24px; height: 24px;'>
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
    
    # Enhanced DataFrame Display
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
    # Modern About Section
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <img src='{get_icon_svg("hospital", COLORS["primary"], 80)}' style='margin-bottom: 20px; display: block; animation: pulse 2s infinite;'>
        <h2 class='section-header'>About MediNomix</h2>
        <p style='color: {COLORS["gray"]}; font-size: 1.2rem; max-width: 700px; margin: 0 auto; line-height: 1.6;'>
            A next-generation healthcare safety platform designed to prevent medication errors through advanced AI analysis and real-time monitoring
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
    
    # Problem & Solution Cards
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left; border-left-color: {COLORS["danger"]};'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <img src='{get_icon_svg("alert", COLORS["danger"], 32)}' style='width: 32px; height: 32px; margin-right: 20px;'>
                <h3 style='color: {COLORS["danger"]}; margin: 0;'>The Challenge</h3>
            </div>
            <div style='color: {COLORS["gray"]}; line-height: 1.7;'>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("warning", COLORS["danger"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span><b>25% of medication errors</b> involve name confusion (FDA)</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("users", COLORS["danger"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span><b>1.5 million Americans</b> harmed annually</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("dollar", COLORS["danger"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span><b>$42 billion</b> in preventable costs</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px;'>
                    <img src='{get_icon_svg("pill", COLORS["danger"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span>Common pairs: <b>Lamictal↔Lamisil</b>, <b>Celebrex↔Celexa</b></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left; border-left-color: {COLORS["success"]};'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <img src='{get_icon_svg("safety", COLORS["success"], 32)}' style='width: 32px; height: 32px; margin-right: 20px;'>
                <h3 style='color: {COLORS["success"]}; margin: 0;'>Our Solution</h3>
            </div>
            <div style='color: {COLORS["gray"]}; line-height: 1.7;'>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("brain", COLORS["success"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span><b>Multi-algorithm AI</b> risk assessment</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("chart-network", COLORS["success"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span><b>Real-time FDA data</b> integration</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <img src='{get_icon_svg("wave-square", COLORS["success"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span><b>Context-aware</b> similarity detection</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px;'>
                    <img src='{get_icon_svg("bolt", COLORS["success"], 18)}' style='width: 18px; height: 18px; margin-top: 3px;'>
                    <span><b>Instant alerts</b> and prevention guidance</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["dark"]}; margin-bottom: 2rem; display: flex; align-items: center; gap: 15px;'>
        <img src='{get_icon_svg("cogs", COLORS["primary"], 24)}' style='width: 24px; height: 24px;'>
        How It Works
    </h3>
    """, unsafe_allow_html=True)
    
    steps_cols = st.columns(4)
    step_data = [
        ("search", "Search", "Enter drug name", "User inputs any medication name for analysis"),
        ("brain", "Analyze", "Calculate risks", "Advanced AI algorithms assess multiple similarity factors"),
        ("chart-network", "Visualize", "View results", "Interactive charts, heatmaps, and risk scores"),
        ("safety", "Prevent", "Take action", "Safety alerts and prevention recommendations")
    ]
    
    for col, (icon, title, subtitle, desc) in zip(steps_cols, step_data):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='height: 240px;'>
                <div style='text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                    <div style='margin-bottom: 20px;'>
                        <div style='background: linear-gradient(135deg, {COLORS["primary"]}15, {COLORS["accent"]}15); 
                             color: {COLORS["primary"]}; width: 60px; height: 60px; border-radius: 15px; 
                             display: inline-flex; align-items: center; justify-content: center;
                             font-weight: bold; font-size: 1.8rem; margin-bottom: 15px;'>
                             <img src='{get_icon_svg(icon, COLORS["primary"], 28)}' style='width: 28px; height: 28px;'>
                        </div>
                        <h4 style='color: {COLORS["dark"]}; margin: 10px 0 5px 0;'>{title}</h4>
                        <p style='color: {COLORS["primary"]}; margin: 0; font-size: 0.9rem; font-weight: 600;'>{subtitle}</p>
                    </div>
                    <p style='color: {COLORS["gray"]}; font-size: 0.85rem; line-height: 1.6; margin-top: 10px;'>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# SECTION 2: REPLACED RAW FOOTER HTML WITH STREAMLIT COMPONENTS
# ============================================

# Footer Section - Using Streamlit components instead of raw HTML
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)

# Footer container
st.markdown(f"""
<div style='text-align: center; padding: 3rem 0 2rem 0; position: relative; 
     background: linear-gradient(135deg, {COLORS["surface"]}, rgba(255, 255, 255, 0.95));
     border-radius: 30px 30px 0 0; box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.05);
     border-top: 1px solid rgba(67, 97, 238, 0.1);'>
""", unsafe_allow_html=True)

# Footer top indicators
footer_cols = st.columns(3)
with footer_cols[0]:
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 10px; justify-content: center;'>
        <img src='{get_icon_svg("microchip", COLORS["accent"], 20)}' style='width: 20px; height: 20px;'>
        <span style='font-weight: 600;'>AI-Powered</span>
        <span style='color: {COLORS["gray"]}80;'>•</span>
        <span>Real-time analysis</span>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[1]:
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 10px; justify-content: center;'>
        <img src='{get_icon_svg("safety", COLORS["success"], 20)}' style='width: 20px; height: 20px;'>
        <span style='font-weight: 600; color: {COLORS["success"]}'>Patient Safety First</span>
        <span style='color: {COLORS["gray"]}80;'>•</span>
        <span>Healthcare focused</span>
    </div>
    """, unsafe_allow_html=True)

with footer_cols[2]:
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 10px; justify-content: center;'>
        <img src='{get_icon_svg("clock", COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
        <span style='font-weight: 600;'>Last Updated</span>
        <span>: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
    </div>
    """, unsafe_allow_html=True)

# Copyright section
st.markdown(f"""
<div style='margin: 25px 0;'>
    <div style='font-size: 1.1rem; color: {COLORS["dark"]}; font-weight: 700; margin-bottom: 10px;'>
        © 2024 MediNomix • Version 3.0 • Advanced Medication Safety Platform
    </div>
</div>
""", unsafe_allow_html=True)

# Footer links using columns
link_cols = st.columns(3)
with link_cols[0]:
    st.markdown(f"""
    <a href='https://github.com/precious-05/MediNomix' target='_blank' style='text-decoration: none; color: {COLORS["primary"]};'>
        <div style='display: flex; align-items: center; justify-content: center; gap: 8px;'>
            <img src='{get_icon_svg("book", COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
            <span style='font-weight: 600;'>GitHub</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

with link_cols[1]:
    st.markdown(f"""
    <a href='https://github.com/precious-05/MediNomix/issues' target='_blank' style='text-decoration: none; color: {COLORS["primary"]};'>
        <div style='display: flex; align-items: center; justify-content: center; gap: 8px;'>
            <img src='{get_icon_svg("bug", COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
            <span style='font-weight: 600;'>Report Bug</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

with link_cols[2]:
    st.markdown(f"""
    <a href='https://github.com/precious-05/MediNomix' target='_blank' style='text-decoration: none; color: {COLORS["primary"]};'>
        <div style='display: flex; align-items: center; justify-content: center; gap: 8px;'>
            <img src='{get_icon_svg("book-medical", COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
            <span style='font-weight: 600;'>Documentation</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

# Disclaimer section
st.markdown("""
<div style='margin-top: 30px; padding-top: 25px; border-top: 1px solid rgba(67, 97, 238, 0.1);'>
    <div style='font-size: 0.9rem; color: #5bacc0; font-style: italic; max-width: 800px; margin: 0 auto; line-height: 1.6;'>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='display: flex; align-items: center; justify-content: center; gap: 10px;'>
    <img src='{get_icon_svg("alert", COLORS["warning"], 20)}' style='width: 20px; height: 20px;'>
    <span>Important: Always consult healthcare professionals for medical decisions. This application is designed to assist, not replace, professional judgment.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# Modern Sidebar
with st.sidebar:
    # Logo and Title
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <div style='display: inline-flex; align-items: center; justify-content: center; width: 80px; height: 80px; 
             background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["accent"]}); 
             border-radius: 20px; margin-bottom: 15px;'>
            <img src='{get_icon_svg("pill", "#ffffff", 40)}' style='width: 40px; height: 40px;'>
        </div>
        <h3 style='color: {COLORS["dark"]}; margin: 10px 0 5px 0; font-family: Montserrat, sans-serif; font-weight: 800;'>MediNomix</h3>
        <p style='color: {COLORS["gray"]}; font-size: 0.9rem; font-weight: 500;'>AI-Powered Medication Safety</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown(f"""
    <h4 style='color: {COLORS["dark"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <img src='{get_icon_svg("bolt", COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
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
    
    if st.button(f"**Force Refresh**", use_container_width=True, type="secondary"):
        load_dashboard_data()
        st.rerun()
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Backend Status
    st.markdown(f"""
    <h4 style='color: {COLORS["dark"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <img src='{get_icon_svg('server', COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
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
        <div style='background: linear-gradient(135deg, rgba(239,71,111,0.1), rgba(181,23,158,0.05)); 
             padding: 15px; border-radius: 12px; margin-top: 10px; border: 1px solid rgba(239,71,111,0.2);'>
            <p style='margin: 0; font-size: 0.9rem; color: {COLORS["gray"]}; line-height: 1.5;'>
            <b>Fix:</b> Run in terminal:<br>
            <code style='background: {COLORS["light"]}; padding: 8px 12px; border-radius: 8px; 
                   font-size: 0.85rem; display: block; margin-top: 8px; font-family: monospace;'>
            python backend.py</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Risk Categories Guide
    st.markdown(f"""
    <h4 style='color: {COLORS["dark"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <img src='{get_icon_svg('alert', COLORS["primary"], 20)}' style='width: 20px; height: 20px;'>
        Risk Categories
    </h4>
    """, unsafe_allow_html=True)
    
    risk_categories = [
        ("Critical", "≥75%", "Immediate intervention required", "#b5179e"),
        ("High", "50-74%", "Review and verification needed", COLORS["danger"]),
        ("Medium", "25-49%", "Monitor closely", COLORS["warning"]),
        ("Low", "<25%", "Low priority", COLORS["success"])
    ]
    
    for name, range_, desc, color in risk_categories:
        st.markdown(f"""
        <div style='display: flex; align-items: flex-start; gap: 15px; margin-bottom: 15px; padding: 12px; 
             background: linear-gradient(135deg, {color}10, transparent 50%); border-radius: 10px;'>
            <div style='width: 12px; height: 12px; background-color: {color}; border-radius: 50%; margin-top: 5px; 
                 box-shadow: 0 0 10px {color}40;'></div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; color: {COLORS["dark"]};'>{name} {range_}</div>
                <div style='font-size: 0.85rem; color: {COLORS["gray"]}; margin-top: 4px;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Floating Action Button with Base64 Icon
st.markdown(f"""
<div class='fab' onclick="window.scrollTo({{top: 0, behavior: 'smooth'}});">
    <img src='{get_icon_svg("chevron-up", "#ffffff", 24)}' style='width: 24px; height: 24px;'>
</div>
""", unsafe_allow_html=True)