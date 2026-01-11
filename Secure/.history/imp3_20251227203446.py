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

# Premium Color Scheme with attractive combinations
COLORS = {
    "primary_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "secondary_gradient": "linear-gradient(to right, #ff7e5f, #feb47b)",
    "accent_gradient": "linear-gradient(to right, #4776E6, #8E54E9)",
    "success_gradient": "linear-gradient(to right, #00b09b, #96c93d)",
    "warning_gradient": "linear-gradient(to right, #ff9966, #ff5e62)",
    "danger_gradient": "linear-gradient(to right, #ff416c, #ff4b2b)",
    "info_gradient": "linear-gradient(to right, #4facfe, #00f2fe)",
    "dark_gradient": "linear-gradient(135deg, #2c3e50 0%, #4a6491 100%)",
    "card_bg": "#ffffff",
    "sidebar_bg": "#f8f9fa",
    "text_dark": "#2d3748",
    "text_medium": "#4a5568",
    "text_light": "#718096",
    "border": "#e2e8f0",
    "hover_bg": "#f7fafc"
}

# Custom CSS for Bootstrap-like styling with attractive designs
st.markdown(f"""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');

/* Global Styles */
* {{
    font-family: 'Poppins', sans-serif;
}}

.stApp {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
    font-family: 'Poppins', sans-serif;
}}

/* Main Content Area */
.main .block-container {{
    background: white;
    border-radius: 20px;
    margin: 20px auto;
    padding: 30px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    max-width: 1400px;
}}

/* Premium Card Design - MODERN & ATTRACTIVE */
.custom-card {{
    background: {COLORS['card_bg']};
    border-radius: 20px;
    border: none;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    padding: 30px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
    color: {COLORS['text_dark']};
}}

.custom-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: {COLORS['primary_gradient']};
    border-radius: 20px 20px 0 0;
}}

.custom-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
    border-color: transparent;
}}

.card-header {{
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    border-radius: 15px 15px 0 0;
    padding: 25px 30px;
    margin: -30px -30px 30px -30px;
    border-bottom: 1px solid {COLORS['border']};
    color: {COLORS['text_dark']};
}}

.card-header h2 {{
    margin: 0;
    color: {COLORS['text_dark']};
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'Montserrat', sans-serif;
    background: {COLORS['primary_gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}}

.card-header p {{
    margin: 12px 0 0 0;
    color: {COLORS['text_medium']};
    font-size: 1rem;
    font-weight: 400;
    opacity: 0.9;
}}

/* ATTRACTIVE BUTTONS WITH PREMIUM STYLES */
.gradient-btn {{
    background: {COLORS['accent_gradient']};
    color: white !important;
    border: none;
    padding: 16px 40px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    display: inline-block;
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
    z-index: 1;
    box-shadow: 0 8px 25px rgba(71, 118, 230, 0.3);
}}

.gradient-btn::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to right, #8E54E9, #4776E6);
    border-radius: 50px;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.4s ease;
}}

.gradient-btn:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 35px rgba(71, 118, 230, 0.4);
    color: white !important;
}}

.gradient-btn:hover::before {{
    opacity: 1;
}}

.secondary-btn {{
    background: white;
    color: {COLORS['text_dark']} !important;
    border: 2px solid {COLORS['border']};
    padding: 14px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: 'Poppins', sans-serif;
    position: relative;
    overflow: hidden;
}}

.secondary-btn:hover {{
    background: linear-gradient(135deg, #fdfbfb 0%, #f5f7fa 100%);
    transform: translateY(-2px);
    border-color: {COLORS['primary_gradient']};
    color: {COLORS['text_dark']} !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}}

.action-btn {{
    background: {COLORS['secondary_gradient']};
    color: white !important;
    border: none;
    padding: 14px 28px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: 'Poppins', sans-serif;
    box-shadow: 0 6px 20px rgba(255, 126, 95, 0.3);
}}

.action-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(255, 126, 95, 0.4);
    color: white !important;
}}

/* CUSTOM NAVIGATION - TOP POSITION FIXED */
.custom-nav {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 0;
    box-shadow: 0 4px 30px rgba(0,0,0,0.1);
    margin-bottom: 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    border-radius: 0 0 20px 20px;
    border-bottom: 3px solid;
    border-image: {COLORS['primary_gradient']} 1;
}}

.nav-container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 80px;
}}

.nav-logo {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 28px;
    background: {COLORS['primary_gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 12px;
    letter-spacing: -0.5px;
}}

.nav-items {{
    display: flex;
    gap: 5px;
    background: rgba(248, 249, 250, 0.8);
    padding: 8px;
    border-radius: 50px;
    backdrop-filter: blur(10px);
}}

.nav-item {{
    padding: 12px 28px;
    color: {COLORS['text_medium']};
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 50px;
    font-family: 'Poppins', sans-serif;
    font-size: 15px;
    text-decoration: none;
    border: 2px solid transparent;
}}

.nav-item:hover {{
    color: #667eea;
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}}

.nav-item.active {{
    background: {COLORS['primary_gradient']};
    color: white !important;
    font-weight: 700;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    border: 2px solid white;
}}

/* Stat Cards - ATTRACTIVE DESIGN */
.stat-card {{
    background: white;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    transition: all 0.4s ease;
    color: {COLORS['text_dark']};
    height: 100%;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

.stat-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    border-radius: 20px;
}}

.stat-card:hover {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 50px rgba(0,0,0,0.15);
}}

.stat-icon {{
    font-size: 50px;
    margin-bottom: 20px;
    color: #667eea;
    position: relative;
    z-index: 1;
}}

.stat-number {{
    font-size: 42px;
    font-weight: 800;
    background: {COLORS['primary_gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 15px 0;
    font-family: 'Montserrat', sans-serif;
    position: relative;
    z-index: 1;
}}

.stat-label {{
    color: {COLORS['text_medium']};
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    position: relative;
    z-index: 1;
}}

/* Feature Cards - BEAUTIFUL DESIGN */
.feature-card {{
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 20px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 15px 40px rgba(0,0,0,0.08);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    color: {COLORS['text_dark']};
    border: 1px solid rgba(255, 255, 255, 0.3);
    position: relative;
    overflow: hidden;
}}

.feature-card::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
    transition: all 0.6s ease;
    opacity: 0;
}}

.feature-card:hover::before {{
    opacity: 1;
    transform: translate(25%, 25%);
}}

.feature-card:hover {{
    transform: translateY(-10px) scale(1.03);
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
}}

.feature-icon {{
    font-size: 60px;
    margin-bottom: 25px;
    color: #667eea;
    position: relative;
    z-index: 1;
}}

.feature-card h3 {{
    margin-bottom: 20px;
    color: {COLORS['text_dark']};
    font-size: 1.4rem;
    font-weight: 700;
    font-family: 'Montserrat', sans-serif;
    position: relative;
    z-index: 1;
}}

.feature-card p {{
    color: {COLORS['text_medium']};
    line-height: 1.7;
    font-size: 1rem;
    font-family: 'Poppins', sans-serif;
    position: relative;
    z-index: 1;
}}

/* Risk Badges - ATTRACTIVE STYLES */
.risk-badge {{
    display: inline-block;
    padding: 10px 28px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-family: 'Montserrat', sans-serif;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}

.risk-badge::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 100%);
    border-radius: 50px;
}}

.badge-critical {{
    background: {COLORS['danger_gradient']};
    color: white;
    box-shadow: 0 6px 25px rgba(255, 65, 108, 0.4);
}}

.badge-high {{
    background: {COLORS['warning_gradient']};
    color: white;
    box-shadow: 0 6px 25px rgba(255, 158, 11, 0.4);
}}

.badge-medium {{
    background: {COLORS['info_gradient']};
    color: white;
    box-shadow: 0 6px 25px rgba(79, 172, 254, 0.4);
}}

.badge-low {{
    background: {COLORS['success_gradient']};
    color: white;
    box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
}}

.risk-badge:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}}

/* Hero Section */
.hero-section {{
    background: {COLORS['primary_gradient']};
    padding: 100px 0;
    border-radius: 25px;
    margin-bottom: 50px;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
}}

.hero-section::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    animation: rotate 20s linear infinite;
}}

@keyframes rotate {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

.hero-title {{
    font-size: 58px;
    font-weight: 800;
    margin-bottom: 25px;
    font-family: 'Montserrat', sans-serif;
    position: relative;
    line-height: 1.2;
    text-shadow: 0 4px 20px rgba(0,0,0,0.2);
}}

.hero-subtitle {{
    font-size: 22px;
    opacity: 0.95;
    max-width: 750px;
    margin: 0 auto 45px;
    font-family: 'Poppins', sans-serif;
    line-height: 1.7;
    position: relative;
    font-weight: 400;
}}

/* Input Fields - LARGE & BEAUTIFUL */
.stTextInput > div > div > input {{
    font-family: 'Poppins', sans-serif !important;
    font-size: 18px !important;
    padding: 20px 25px !important;
    border-radius: 15px !important;
    border: 2px solid {COLORS['border']} !important;
    background: white !important;
    color: {COLORS['text_dark']} !important;
    height: auto !important;
    min-height: 65px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05) !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: #667eea !important;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
    outline: none !important;
    transform: translateY(-1px);
}}

.stTextInput > div > div > input::placeholder {{
    color: {COLORS['text_light']} !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 16px !important;
    opacity: 0.7;
}}

/* Streamlit Button Styling - BEAUTIFUL */
.stButton > button {{
    font-family: 'Montserrat', sans-serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 18px 40px !important;
    border-radius: 50px !important;
    min-height: 65px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: none !important;
    background: {COLORS['accent_gradient']} !important;
    color: white !important;
    box-shadow: 0 8px 25px rgba(71, 118, 230, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.stButton > button:hover {{
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 15px 35px rgba(71, 118, 230, 0.4) !important;
    color: white !important;
}}

.stButton > button:before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to right, #8E54E9, #4776E6);
    border-radius: 50px;
    opacity: 0;
    transition: opacity 0.4s ease;
}}

.stButton > button:hover:before {{
    opacity: 1;
}}

/* Secondary Button Style */
div[data-testid="stButton"]:has(button[kind="secondary"]) > button {{
    background: white !important;
    color: {COLORS['text_dark']} !important;
    border: 2px solid {COLORS['border']} !important;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08) !important;
}}

div[data-testid="stButton"]:has(button[kind="secondary"]) > button:hover {{
    background: linear-gradient(135deg, #fdfbfb 0%, #f5f7fa 100%) !important;
    border-color: {COLORS['primary_gradient']} !important;
    color: {COLORS['text_dark']} !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15) !important;
}}

/* Metric Cards */
.stMetric {{
    font-family: 'Poppins', sans-serif !important;
    color: {COLORS['text_dark']} !important;
}}

.stMetric > div {{
    padding: 25px !important;
    border-radius: 20px !important;
    background: white !important;
    border: none !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08) !important;
    transition: all 0.3s ease !important;
}}

.stMetric > div:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.15) !important;
}}

.stMetric > div > div[data-testid="stMetricValue"] {{
    font-size: 40px !important;
    font-weight: 800 !important;
    font-family: 'Montserrat', sans-serif !important;
    color: {COLORS['text_dark']} !important;
    background: {COLORS['primary_gradient']} !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}}

.stMetric > div > div[data-testid="stMetricLabel"] {{
    font-size: 15px !important;
    color: {COLORS['text_medium']} !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    margin-top: 10px !important;
}}

/* Sidebar Styling - VISIBLE LINKS */
[data-testid="stSidebar"] {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    font-family: 'Poppins', sans-serif !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important;
    margin: 12px 0 !important;
    background: rgba(255, 255, 255, 0.95) !important;
    color: {COLORS['text_dark']} !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1) !important;
    font-weight: 600 !important;
    font-family: 'Montserrat', sans-serif !important;
    transition: all 0.3s ease !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: white !important;
    border-color: white !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
    color: {COLORS['text_dark']} !important;
}}

/* Make sidebar links clearly visible */
[data-testid="stSidebar"] * {{
    color: white !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    color: {COLORS['text_dark']} !important;
}}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {{
    color: white !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}}

/* Image Gallery - NO SLIDER, BEAUTIFUL GRID */
.image-gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    margin: 30px 0;
}}

.gallery-image {{
    width: 100%;
    height: 250px;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}}

.gallery-image:hover {{
    transform: translateY(-10px) scale(1.03);
    box-shadow: 0 25px 60px rgba(0,0,0,0.25);
}}

.gallery-image img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
}}

.gallery-image:hover img {{
    transform: scale(1.1);
}}

.gallery-overlay {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    color: white;
    padding: 20px;
    transform: translateY(100%);
    transition: transform 0.4s ease;
}}

.gallery-image:hover .gallery-overlay {{
    transform: translateY(0);
}}

/* Scrollbar Styling */
::-webkit-scrollbar {{
    width: 14px;
    height: 14px;
}}

::-webkit-scrollbar-track {{
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb {{
    background: {COLORS['primary_gradient']};
    border-radius: 10px;
    border: 3px solid #f5f7fa;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {COLORS['accent_gradient']};
}}

/* Footer */
.custom-footer {{
    background: linear-gradient(135deg, #2c3e50 0%, #4a6491 100%);
    padding: 50px 0;
    margin-top: 70px;
    border-radius: 25px 25px 0 0;
    text-align: center;
    color: white;
    font-family: 'Poppins', sans-serif;
    box-shadow: 0 -20px 50px rgba(0,0,0,0.1);
}}

/* Typography Improvements */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Montserrat', sans-serif !important;
    color: {COLORS['text_dark']} !important;
    font-weight: 700 !important;
    margin-bottom: 1rem !important;
}}

p, span, div, li {{
    font-family: 'Poppins', sans-serif !important;
    color: {COLORS['text_medium']} !important;
    line-height: 1.7 !important;
}}

strong, b {{
    font-weight: 700 !important;
    color: {COLORS['text_dark']} !important;
}}

/* Radio buttons - VISIBLE */
.stRadio > div {{
    font-family: 'Poppins', sans-serif !important;
    color: {COLORS['text_dark']} !important;
    font-size: 16px !important;
    background: white !important;
    padding: 15px !important;
    border-radius: 15px !important;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05) !important;
}}

.stRadio > div > label {{
    font-family: 'Poppins', sans-serif !important;
    font-size: 16px !important;
    color: {COLORS['text_dark']} !important;
    padding: 15px 25px !important;
    margin: 10px 0 !important;
    border-radius: 12px !important;
    border: 2px solid {COLORS['border']} !important;
    background: white !important;
    transition: all 0.3s ease !important;
}}

.stRadio > div > label:hover {{
    background: {COLORS['hover_bg']} !important;
    border-color: #c7d2fe !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
}}

/* Remove Streamlit branding */
#MainMenu {{
    visibility: hidden;
}}
footer {{
    visibility: hidden;
}}
.stDeployButton {{
    display: none;
}}

/* Dataframe styling */
.dataframe {{
    font-family: 'Poppins', sans-serif !important;
    color: {COLORS['text_dark']} !important;
    border-radius: 15px !important;
    overflow: hidden !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08) !important;
}}

.dataframe th {{
    background: {COLORS['primary_gradient']} !important;
    color: white !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;
    padding: 15px !important;
}}

.dataframe td {{
    padding: 12px 15px !important;
    border-bottom: 1px solid {COLORS['border']} !important;
}}

/* Plotly charts styling */
.js-plotly-plot .plotly {{
    font-family: 'Poppins', sans-serif !important;
    border-radius: 15px !important;
    overflow: hidden !important;
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
        title=dict(text="Drug Confusion Risk Matrix", font=dict(size=24, family='Montserrat')),
        height=650,
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        plot_bgcolor='white',
        font=dict(family='Poppins', size=16, color=COLORS['text_dark'])
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
        marker_colors=['#ff416c', '#ff9966', '#00b09b', '#4facfe'],
        textfont=dict(family='Poppins', size=16, color=COLORS['text_dark'])
    )])
    
    fig.update_layout(
        title=dict(text="Risk Distribution", font=dict(size=24, family='Montserrat')),
        height=450,
        showlegend=True,
        font=dict(family='Poppins', size=16, color=COLORS['text_dark'])
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
            marker_color='#8E54E9',
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            textfont=dict(family='Poppins', size=14, color=COLORS['text_dark'])
        )
    ])
    
    fig.update_layout(
        title=dict(text="Top 10 High-Risk Drug Pairs", font=dict(size=24, family='Montserrat')),
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=550,
        plot_bgcolor='white',
        font=dict(family='Poppins', size=16, color=COLORS['text_dark'])
    )
    
    return fig

# ================================
# IMAGE GALLERY (NO SLIDER)
# ================================

def create_image_gallery():
    """Create beautiful image gallery without slider"""
    # Medical images from Unsplash
    images = [
        {
            "url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "title": "Modern Pharmacy"
        },
        {
            "url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-1.2.1&auto=format&fit=crop&w-800&q=80",
            "title": "Healthcare Technology"
        },
        {
            "url": "https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "title": "Medical Research"
        },
        {
            "url": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "title": "Patient Safety"
        }
    ]
    
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <h2 style="margin: 0; color: #2d3748;">🏥 Trusted by Healthcare Professionals</h2>
            <p style="margin: 10px 0 0 0; color: #4a5568;">See how leading hospitals use MediNomix to prevent medication errors</p>
        </div>
        
        <div class="image-gallery">
    """, unsafe_allow_html=True)
    
    # Display images in grid
    for img in images:
        st.markdown(f"""
        <div class="gallery-image">
            <img src="{img['url']}" alt="{img['title']}">
            <div class="gallery-overlay">
                <h4 style="margin: 0; font-family: 'Montserrat', sans-serif;">{img['title']}</h4>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ================================
# CUSTOM NAVIGATION BAR (FIXED POSITION)
# ================================

def render_navigation():
    """Render custom Bootstrap-style navigation bar at TOP"""
    st.markdown("""
    <div class="custom-nav">
        <div class="nav-container">
            <div class="nav-logo">
                💊 MediNomix AI
            </div>
            <div class="nav-items">
    """, unsafe_allow_html=True)
    
    # Create navigation buttons at TOP
    tabs = ["Home", "Drug Analysis", "Analytics", "Real-Time"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.active_tab = "Home"
            st.rerun()
    
    with col2:
        if st.button("🔍 Analysis", key="nav_analysis", use_container_width=True):
            st.session_state.active_tab = "Drug Analysis"
            st.rerun()
    
    with col3:
        if st.button("📊 Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.active_tab = "Analytics"
            st.rerun()
    
    with col4:
        if st.button("⚡ Real-Time", key="nav_realtime", use_container_width=True):
            st.session_state.active_tab = "Real-Time"
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
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Prevent Medication Errors with AI</h1>
        <p class="hero-subtitle">Advanced AI-powered system that analyzes drug names for potential confusion risks, helping healthcare professionals prevent medication errors and improve patient safety worldwide.</p>
        <button class="gradient-btn" style="margin-top: 30px; padding: 20px 50px; font-size: 20px;">Start Free Analysis</button>
    </div>
    """, unsafe_allow_html=True)

def render_stats_counter():
    """Render animated stats counter"""
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; margin-bottom: 50px;">
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
    <div style="margin: 50px 0;">
        <h2 style="text-align: center; margin-bottom: 40px; color: #2d3748; font-family: 'Montserrat', sans-serif; font-size: 36px;">How MediNomix Works</h2>
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
                <h3 style="margin-bottom: 20px; color: #2d3748; font-family: 'Montserrat', sans-serif;">{feature['title']}</h3>
                <p style="color: #4a5568; line-height: 1.7; font-size: 17px; font-family: 'Poppins', sans-serif;">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def render_user_guide():
    """Render user guide accordion"""
    st.markdown("""
    <div class="custom-card" style="margin: 50px 0;">
        <div class="card-header">
            <h2 style="margin: 0; color: #2d3748;">📚 User Guide & Quick Start</h2>
            <p style="margin: 10px 0 0 0; color: #4a5568;">Follow these simple steps to get started with MediNomix</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Step 1: Search for a Medication", expanded=True):
        st.markdown("""
        <div style="padding: 25px; font-family: 'Poppins', sans-serif; color: #4a5568; background: linear-gradient(135deg, #fdfbfb 0%, #f5f7fa 100%); border-radius: 15px;">
        <ol style="line-height: 1.8; font-size: 17px;">
            <li><strong style="color: #2d3748;">Navigate to the Drug Analysis tab</strong> using the top navigation menu</li>
            <li><strong style="color: #2d3748;">Enter any medication name</strong> (brand or generic) in the search box</li>
            <li><strong style="color: #2d3748;">Click "Analyze Drug"</strong> to start the AI-powered analysis</li>
            <li><strong style="color: #2d3748;">Try our quick examples:</strong> Lamictal, Metformin, or Celebrex</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Step 2: Review Risk Assessment"):
        st.markdown("""
        <div style="padding: 25px; font-family: 'Poppins', sans-serif; color: #4a5568; background: linear-gradient(135deg, #fdfbfb 0%, #f5f7fa 100%); border-radius: 15px;">
        <ol style="line-height: 1.8; font-size: 17px;">
            <li><strong style="color: #2d3748;">View all similar drugs</strong> with confusion risk scores</li>
            <li><strong style="color: #2d3748;">Filter by risk level:</strong> Critical, High, Medium, or Low</li>
            <li><strong style="color: #2d3748;">Examine detailed similarity metrics:</strong> Spelling, Phonetic, Therapeutic Context</li>
            <li><strong style="color: #2d3748;">Check risk badges</strong> for quick visual identification</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Step 3: Take Preventive Action"):
        st.markdown("""
        <div style="padding: 25px; font-family: 'Poppins', sans-serif; color: #4a5568; background: linear-gradient(135deg, #fdfbfb 0%, #f5f7fa 100%); border-radius: 15px;">
        <ol style="line-height: 1.8; font-size: 17px;">
            <li><strong style="color: #2d3748;">Check the Analytics tab</strong> for overall system statistics</li>
            <li><strong style="color: #2d3748;">Monitor the Real-Time dashboard</strong> for live updates and alerts</li>
            <li><strong style="color: #2d3748;">Use the heatmap visualization</strong> to identify high-risk drug pairs</li>
            <li><strong style="color: #2d3748;">Review FDA alerts</strong> for known high-risk medication combinations</li>
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
            <h2 style="margin: 0; color: #2d3748;">🔍 Drug Confusion Risk Analysis</h2>
            <p style="margin: 10px 0 0 0; color: #4a5568;">Search any medication to analyze confusion risks with similar drugs. First search may take 5-10 seconds as we fetch live FDA data.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Search Section in Card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #eef2f7 100%); padding: 30px; border-radius: 20px; margin: 25px 0; border: 2px dashed #cbd5e1;">
        <h3 style="color: #2d3748; margin-bottom: 20px; font-family: 'Montserrat', sans-serif;">Enter Medication Name</h3>
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
    <div style="margin: 25px 0;">
        <h4 style="color: #4a5568; margin-bottom: 20px; font-family: 'Poppins', sans-serif; font-weight: 600;">💡 Quick Examples:</h4>
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
        <div style="margin-top: 40px;">
            <h3 style="color: #2d3748; margin-bottom: 25px; font-family: 'Montserrat', sans-serif; font-size: 28px;">📊 Analysis Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Filters
        st.markdown("<div style='margin-bottom: 25px;'>", unsafe_allow_html=True)
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
        for result in filtered_results[:20]:
            risk_color_class = f"badge-{result['risk_category']}"
            risk_percentage = result['combined_risk']
            
            st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0 0 10px 0; color: #2d3748; font-family: 'Montserrat', sans-serif; font-size: 22px;">{result['target_drug']['brand_name']}</h3>
                        {f"<p style='margin: 0 0 15px 0; color: #4a5568; font-family: 'Poppins', sans-serif; font-size: 16px;'><strong>Generic:</strong> {result['target_drug']['generic_name']}</p>" if result['target_drug']['generic_name'] else ""}
                        {f"<p style='margin: 0 0 15px 0; color: #4a5568; font-family: 'Poppins', sans-serif; font-size: 15px;'><strong>Manufacturer:</strong> {result['target_drug']['manufacturer']}</p>" if result['target_drug']['manufacturer'] else ""}
                    </div>
                    <div style="text-align: center; min-width: 140px;">
                        <div style="font-size: 45px; font-weight: 800; font-family: 'Montserrat', sans-serif; background: {COLORS['primary_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;">
                            {risk_percentage:.0f}%
                        </div>
                        <span class="risk-badge {risk_color_class}" style="display: inline-block; margin-top: 5px;">{result['risk_category'].upper()}</span>
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
                    <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #f8f9fa 0%, #eef2f7 100%); border-radius: 15px; margin: 10px 0; border: 1px solid #e2e8f0;">
                        <div style="font-size: 15px; color: #718096; margin-bottom: 10px; font-family: 'Poppins', sans-serif; font-weight: 600;">{label}</div>
                        <div style="font-size: 32px; font-weight: 800; color: #2d3748; font-family: 'Montserrat', sans-serif;">{value}</div>
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
            <p style="margin: 10px 0 0 0; color: #4a5568;">Comprehensive analytics and insights into medication confusion risks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data if needed
    if 'metrics' not in st.session_state.dashboard_data:
        with st.spinner("📊 Loading analytics data..."):
            load_dashboard_data()
    
    # Row 1: KPI Cards
    st.markdown("<div style='margin: 25px 0;'>", unsafe_allow_html=True)
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
    st.markdown("<div style='margin: 40px 0;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #2d3748; margin-bottom: 25px; font-family: 'Montserrat', sans-serif;">Risk Distribution</h3>
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
            <h3 style="color: #2d3748; margin-bottom: 25px; font-family: 'Montserrat', sans-serif;">Top Risk Pairs</h3>
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
        <h3 style="color: #2d3748; margin-bottom: 25px; font-family: 'Montserrat', sans-serif;">Drug Confusion Risk Heatmap</h3>
    """, unsafe_allow_html=True)
    
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; color: #718096; font-size: 16px; font-family: 'Poppins', sans-serif;">
            🟢 Low Risk &nbsp;&nbsp; 🟡 Medium Risk &nbsp;&nbsp; 🔴 High Risk
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs or load examples first.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 4: FDA Alerts
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #2d3748; margin-bottom: 25px; font-family: 'Montserrat', sans-serif;">🚨 FDA High Alert Drug Pairs</h3>
        <p style="color: #718096; margin-bottom: 30px; font-family: 'Poppins', sans-serif; font-size: 16px;">Known high-risk medication pairs identified by FDA</p>
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
            <p style="margin: 10px 0 0 0; color: #4a5568;">Live monitoring and real-time updates of medication confusion risks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Connection Status
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.websocket_connected:
            st.markdown("""
            <div style="background: linear-gradient(to right, #00b09b, #96c93d); color: white; padding: 25px; border-radius: 20px; margin-bottom: 30px;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 35px; margin-right: 20px;">✅</div>
                    <div>
                        <div style="font-weight: 700; font-size: 22px; font-family: 'Montserrat', sans-serif;">Real-time Connection Active</div>
                        <div style="font-size: 16px; opacity: 0.95; font-family: 'Poppins', sans-serif;">Live data streaming enabled - Updates every 10 seconds</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #eef2f7 100%); padding: 25px; border-radius: 20px; margin-bottom: 30px; border: 2px dashed #cbd5e1;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 35px; margin-right: 20px; color: #718096;">🔌</div>
                    <div>
                        <div style="font-weight: 700; color: #2d3748; font-size: 22px; font-family: 'Montserrat', sans-serif;">Connecting to Real-Time Server</div>
                        <div style="color: #718096; font-size: 16px; font-family: 'Poppins', sans-serif;">Live updates will appear here once connection is established</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Refresh Connection", type="secondary", use_container_width=True):
            websocket_manager.start_connection()
            st.rerun()
    
    # Auto-start WebSocket if not connected
    if not st.session_state.websocket_connected:
        websocket_manager.start_connection()
    
    # Display Real-time Metrics
    metrics = st.session_state.realtime_metrics or {}
    
    if metrics:
        # Real-time KPI Cards
        st.markdown("<div style='margin: 30px 0;'>", unsafe_allow_html=True)
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
        <div class="custom-card" style="margin-top: 40px;">
            <h3 style="color: #2d3748; margin-bottom: 30px; font-family: 'Montserrat', sans-serif;">🕒 Recent Activity Timeline</h3>
        """, unsafe_allow_html=True)
        
        if metrics.get('recent_searches'):
            for idx, search in enumerate(metrics['recent_searches'][:5]):
                timestamp = search.get('timestamp', '')
                drug_name = search.get('drug_name', 'Unknown')
                similar_drugs = search.get('similar_drugs_found', 0)
                highest_risk = search.get('highest_risk', 0)
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 25px; background: {'linear-gradient(135deg, #f8f9fa 0%, #eef2f7 100%)' if idx % 2 == 0 else 'white'}; border-radius: 15px; margin-bottom: 15px; border: 1px solid #e2e8f0; transition: all 0.3s ease;">
                    <div style="margin-right: 25px;">
                        <div style="width: 55px; height: 55px; background: {COLORS['primary_gradient']}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-family: 'Montserrat', sans-serif; font-size: 20px; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">{idx+1}</div>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 700; color: #2d3748; font-family: 'Montserrat', sans-serif; font-size: 18px;">{drug_name}</div>
                        <div style="color: #718096; font-family: 'Poppins', sans-serif; font-size: 15px; margin-top: 5px;">Found {similar_drugs} similar drugs • Highest risk: {highest_risk:.1f}%</div>
                    </div>
                    <div style="color: #94a3b8; font-family: 'Poppins', sans-serif; font-size: 14px; white-space: nowrap;">{timestamp[:19] if timestamp else 'Just now'}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity data available. Try searching for drugs first.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # System Status
        st.markdown("""
        <div class="custom-card" style="margin-top: 30px;">
            <h3 style="color: #2d3748; margin-bottom: 30px; font-family: 'Montserrat', sans-serif;">⚙️ System Status</h3>
            <div style="display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #f8f9fa 0%, #eef2f7 100%); padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0;">
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
            try:
                dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                formatted_time = dt.strftime("%H:%M:%S")
            except:
                formatted_time = last_updated[:19]
        else:
            formatted_time = "N/A"
        
        st.markdown(f"""
                <div>
                    <div style="font-size: 15px; color: #718096; font-family: 'Poppins', sans-serif; margin-bottom: 8px;">Status</div>
                    <div style="font-weight: 700; color: {status_color}; font-family: 'Montserrat', sans-serif; font-size: 22px;">{status_icon} {status_text}</div>
                </div>
                <div>
                    <div style="font-size: 15px; color: #718096; font-family: 'Poppins', sans-serif; margin-bottom: 8px;">Last Updated</div>
                    <div style="font-weight: 700; color: #2d3748; font-family: 'Montserrat', sans-serif; font-size: 22px;">{formatted_time}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 70px 20px;">
            <div style="font-size: 70px; margin-bottom: 30px;">⏳</div>
            <h3 style="color: #2d3748; margin-bottom: 20px; font-family: 'Montserrat', sans-serif;">Waiting for Real-Time Data</h3>
            <p style="color: #718096; font-family: 'Poppins', sans-serif; font-size: 18px; max-width: 500px; margin: 0 auto;">Live updates will appear here once connection is established.</p>
            <button class="gradient-btn" style="margin-top: 30px;" onclick="window.location.reload()">Refresh Page</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>")

# ================================
# SIDEBAR WITH VISIBLE LINKS
# ================================

def render_sidebar():
    """Render sidebar with visible links"""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 35px;">
            <div style="font-size: 55px; margin-bottom: 20px; color: white;">💊</div>
            <h2 style="margin: 0; color: white; font-family: 'Montserrat', sans-serif; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">MediNomix AI</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 30px 0; font-family: 'Poppins', sans-serif;">Medication Safety Platform</p>
            <div style="height: 4px; background: rgba(255,255,255,0.5); border-radius: 2px; margin: 0 auto 35px auto; width: 70px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Card
        st.markdown("""
        <div class="custom-card" style="margin-bottom: 25px; background: rgba(255,255,255,0.95);">
            <h3 style="color: #2d3748; margin-bottom: 20px; font-family: 'Montserrat', sans-serif;">System Status</h3>
        """, unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    st.markdown("""
                    <div style="background: linear-gradient(to right, #00b09b, #96c93d); color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
                        <div style="font-size: 28px; margin-bottom: 10px;">✅</div>
                        <div style="font-weight: 700; font-size: 20px; font-family: 'Montserrat', sans-serif;">Backend Connected</div>
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
        
        # Quick Links - VISIBLE
        st.markdown("""
        <div class="custom-card" style="background: rgba(255,255,255,0.95);">
            <h3 style="color: #2d3748; margin-bottom: 20px; font-family: 'Montserrat', sans-serif;">🔗 Quick Links</h3>
        """, unsafe_allow_html=True)
        
        # Links with clear visibility
        link_style = """
            <div style="margin: 15px 0; padding: 15px; background: linear-gradient(135deg, #f8f9fa 0%, #eef2f7 100%); 
                    border-radius: 12px; border-left: 4px solid #667eea; transition: all 0.3s ease; cursor: pointer;"
                    onmouseover="this.style.transform='translateX(5px)'; this.style.background='linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)'"
                    onmouseout="this.style.transform='translateX(0)'; this.style.background='linear-gradient(135deg, #f8f9fa 0%, #eef2f7 100%)'">
                <div style="font-weight: 600; color: #2d3748; font-family: 'Poppins', sans-serif;">{text}</div>
                <div style="font-size: 13px; color: #718096; margin-top: 5px; font-family: 'Poppins', sans-serif;">{desc}</div>
            </div>
        """
        
        st.markdown(link_style.format(text="📚 Documentation", desc="User guides and API documentation"), unsafe_allow_html=True)
        
        if st.button("📖 Open Documentation", use_container_width=True, type="secondary"):
            st.info("Documentation: https://medinimix-ai-docs.example.com")
        
        st.markdown(link_style.format(text="🐛 Report Bug", desc="Found an issue? Let us know"), unsafe_allow_html=True)
        
        if st.button("⚠️ Report Issue", use_container_width=True, type="secondary"):
            st.info("Email: support@medinimix-ai.com")
        
        st.markdown(link_style.format(text="🔄 Clear Cache", desc="Refresh application data"), unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All Data", use_container_width=True, type="secondary"):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            st.session_state.realtime_metrics = {}
            st.success("✅ All cache cleared successfully!")
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Risk Categories Guide
        st.markdown("""
        <div class="custom-card" style="background: rgba(255,255,255,0.95);">
            <h3 style="color: #2d3748; margin-bottom: 20px; font-family: 'Montserrat', sans-serif;">📊 Risk Categories</h3>
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
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="risk-badge {badge_class}" style="font-size: 12px; padding: 8px 20px;">{name}</span>
                    <span style="font-weight: 700; color: #2d3748; font-family: 'Montserrat', sans-serif;">{score}</span>
                </div>
                <div style="color: #64748b; font-family: 'Poppins', sans-serif; font-size: 14px; line-height: 1.5;">{desc}</div>
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
            <div style="margin-bottom: 30px;">
                <div style="font-size: 40px; margin-bottom: 20px; color: white;">💊</div>
                <div style="font-weight: 700; color: white; margin-bottom: 15px; font-family: 'Montserrat', sans-serif; font-size: 28px;">MediNomix AI</div>
                <div style="color: rgba(255,255,255,0.9); font-family: 'Poppins', sans-serif; font-size: 18px;">Preventing medication errors with artificial intelligence</div>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 30px; color: rgba(255,255,255,0.7); font-family: 'Poppins', sans-serif; font-size: 15px;">
                <div style="margin-bottom: 15px;">© 2024 MediNomix AI. All rights reserved.</div>
                <div style="font-size: 14px; line-height: 1.7; max-width: 600px; margin: 0 auto;">Disclaimer: This tool is for educational purposes and should not replace professional medical advice. Always consult healthcare professionals for medical decisions.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# MAIN APPLICATION RENDERER
# ================================

def main():
    """Main application renderer"""
    
    # Render Navigation Bar at TOP
    render_navigation()
    
    # Render based on active tab
    if st.session_state.active_tab == "Home":
        render_hero_section()
        render_stats_counter()
        render_features_section()
        render_user_guide()
        create_image_gallery()  # Beautiful image gallery (no slider)
        
    elif st.session_state.active_tab == "Drug Analysis":
        render_drug_analysis_tab()
        
    elif st.session_state.active_tab == "Analytics":
        render_analytics_tab()
        
    elif st.session_state.active_tab == "Real-Time":
        render_realtime_tab()
    
    # Render Sidebar with VISIBLE links
    render_sidebar()
    
    # Render Footer
    render_footer()

# ================================
# START APPLICATION
# ================================

if __name__ == "__main__":
    main()