import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import time
import json
import base64
from PIL import Image
import io



# Page configuration
st.set_page_config(
    page_title="MediNomix | Medication Safety",
    page_icon="💊",  # Ye emoji hi rahega
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom favicon via HTML (browser tab icon)
try:
    with open("m11.jpg", "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    
    st.markdown(f"""
    <link rel="icon" type="image/x-icon" href="data:image/jpg;base64,{encoded}">
    """, unsafe_allow_html=True)
except:
    pass



# Backend URL
BACKEND_URL = "http://localhost:8000"
#WS_URL = "ws://localhost:8000/ws/dashboard"



# Modern Purple Theme Color Scheme
COLORS = {
    'primary': '#8B5CF6',
    'primary_hover': '#7C3AED',
    'secondary': '#EC4899',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#38BDF8',
    'purple': '#8B5CF6',
    'yellow': '#FBBF24',
    'pink': '#EC4899',
    'blue': '#0EA5E9',
    'dark': '#1F2937',
    'light': '#FFFFFF',
    'card_bg': '#FFFFFF',
    'sidebar_bg': '#F5F3FF',
    'border': 'rgba(139, 92, 246, 0.15)',
    'text_primary': '#1F2937',
    'text_secondary': '#6B7280',
    'text_muted': '#9CA3AF',
    'shadow': 'rgba(139, 92, 246, 0.15)',
    'shadow_hover': 'rgba(139, 92, 246, 0.25)',
    'gradient_primary': 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%)',
    'gradient_secondary': 'linear-gradient(135deg, #38BDF8 0%, #0EA5E9 50%, #8B5CF6 100%)',
    'gradient_success': 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
    'gradient_warning': 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)',
    'gradient_danger': 'linear-gradient(135deg, #EF4444 0%, #F87171 100%)',
    'gradient_purple': 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)',
    'gradient_purple_pink': 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%)',
    'gradient_dark': 'linear-gradient(135deg, #1F2937 0%, #374151 100%)',
    'gradient_modern': 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #38BDF8 100%)'
}



 
# -----------------------------  MAIN CSS    ----------------------------------------

st.markdown(f"""
<style>
/* ========== GLOBAL STYLES & SCROLLBAR ========== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
/* Add Font Awesome CDN */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.stApp {{
    background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F7 100%) !important;
    color: #1F2937 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 8px !important;
    height: 8px !important;
}}

::-webkit-scrollbar-track {{
    background: rgba(245, 243, 255, 0.5) !important;
    border-radius: 4px !important;
}}

::-webkit-scrollbar-thumb {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    border-radius: 4px !important;
}}

::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 50%, #DB2777 100%) !important;
}}

/* ========== ANIMATIONS ========== */
@keyframes fadeInUp {{
    from {{ 
        opacity: 0 !important;
        transform: translateY(20px) !important;
    }}
    to {{ 
        opacity: 1 !important;
        transform: translateY(0) !important;
    }}
}}

@keyframes slideInRight {{
    from {{ 
        opacity: 0 !important;
        transform: translateX(-20px) !important;
    }}
    to {{ 
        opacity: 1 !important;
        transform: translateX(0) !important;
    }}
}}

@keyframes pulseGlow {{
    0%, 100% {{ 
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15) !important;
    }}
    50% {{ 
        box-shadow: 0 6px 30px rgba(139, 92, 246, 0.25) !important;
    }}
}}

@keyframes gradientFlow {{
    0% {{ background-position: 0% 50% !important; }}
    50% {{ background-position: 100% 50% !important; }}
    100% {{ background-position: 0% 50% !important; }}
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0) !important; }}
    50% {{ transform: translateY(-10px) !important; }}
}}

/* ========== MODERN TABS STYLING ========== */
.stTabs {{
    background: transparent !important;
    padding: 0 !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 4px !important;
    background: white !important;
    padding: 8px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    margin-bottom: 24px !important;
    box-shadow: 
        0 4px 16px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    overflow-x: auto !important;
    white-space: nowrap !important;
    backdrop-filter: blur(10px) !important;
    animation: fadeInUp 0.8s ease !important;
}}

.stTabs [data-baseweb="tab"] {{
    height: 48px !important;
    padding: 0 24px !important;
    color: #6B7280 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    background: transparent !important;
    border-radius: 12px !important;
    border: none !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 120px !important;
    position: relative !important;
    overflow: hidden !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%) !important;
    color: #8B5CF6 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1) !important;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    color: white !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transform: translateY(-2px) !important;
    font-weight: 700 !important;
    animation: pulseGlow 2s ease-in-out infinite !important;
}}

.stTabs [aria-selected="true"]::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #EC4899 0%, #F472B6 100%) !important;
    border-radius: 12px 12px 0 0 !important;
}}

/* ========== ALERT MESSAGES AS CARDS ========== */
.alert-card {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin: 16px 0 !important;
    border-left: 4px solid !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    display: flex !important;
    align-items: center !important;
    gap: 16px !important;
    animation: slideInRight 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.alert-card::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent) !important;
}}

.alert-success {{
    border-left-color: #10B981 !important;
    background: linear-gradient(135deg, rgba(240, 253, 244, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-danger {{
    border-left-color: #EF4444 !important;
    background: linear-gradient(135deg, rgba(254, 242, 242, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-warning {{
    border-left-color: #F59E0B !important;
    background: linear-gradient(135deg, rgba(255, 251, 235, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-info {{
    border-left-color: #0EA5E9 !important;
    background: linear-gradient(135deg, rgba(240, 249, 255, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-purple {{
    border-left-color: #8B5CF6 !important;
    background: linear-gradient(135deg, rgba(245, 243, 255, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-icon {{
    font-size: 24px !important;
    min-width: 40px !important;
    text-align: center !important;
}}

.alert-content {{
    flex: 1 !important;
}}

.alert-title {{
    font-weight: 700 !important;
    font-size: 16px !important;
    margin-bottom: 4px !important;
    color: #1F2937 !important;
    letter-spacing: -0.01em !important;
}}

.alert-message {{
    font-size: 14px !important;
    color: #6B7280 !important;
    line-height: 1.6 !important;
    font-weight: 500 !important;
}}

/* ========== ALL STREAMLIT COMPONENTS STYLING ========== */

/* Radio buttons */
.stRadio [role="radiogroup"] {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    padding: 16px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
}}

.stRadio [role="radio"] {{
    margin-right: 12px !important;
}}

.stRadio label {{
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    letter-spacing: -0.01em !important;
}}

/* Select boxes */
.stSelectbox {{
    background: transparent !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}

.stSelectbox select {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 2px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    width: 100% !important;
    appearance: none !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%238B5CF6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: right 16px center !important;
    background-size: 16px !important;
    padding-right: 40px !important;
}}

.stSelectbox select:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}}

/* Text area */
.stTextArea textarea {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 2px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    min-height: 100px !important;
    font-family: 'Inter', monospace !important;
}}

.stTextArea textarea:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}}

/* Dataframe tables */
.dataframe {{
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.9) 0%, 
        rgba(245, 243, 255, 0.95) 100%) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: 
        0 12px 40px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    margin: 20px 0 !important;
    animation: fadeInUp 0.6s ease !important;
}}

.dataframe th {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 18px 24px !important;
    font-size: 14px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
}}

.dataframe td {{
    padding: 18px 24px !important;
    border-bottom: 1px solid rgba(139, 92, 246, 0.1) !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    color: #1F2937 !important;
    font-family: 'Inter', sans-serif !important;
    background: transparent !important;
}}

.dataframe tr:hover td {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%) !important;
}}

/* Metric cards */
[data-testid="stMetric"] {{
    background: white !important;
    border-radius: 20px !important;
    padding: 24px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-6px) scale(1.02) !important;
    box-shadow: 
        0 20px 40px rgba(139, 92, 246, 0.15),
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.2) !important;
}}

[data-testid="stMetricLabel"] {{
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #6B7280 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}}

[data-testid="stMetricValue"] {{
    font-size: 32px !important;
    font-weight: 800 !important;
    color: transparent !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 4px 0 !important;
}}

[data-testid="stMetricDelta"] {{
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 4px 8px !important;
    border-radius: 8px !important;
    margin-top: 4px !important;
}}

/* Expander */
.streamlit-expanderHeader {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 20px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    border: none !important;
    margin-bottom: 8px !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}}

.streamlit-expanderHeader:hover {{
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 16px 40px rgba(139, 92, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}}

.streamlit-expanderHeader::after {{
    content: '▶' !important;
    position: absolute !important;
    right: 20px !important;
    top: 50% !important;
    transform: translateY(-50%) rotate(90deg) !important;
    transition: transform 0.3s ease !important;
    opacity: 0.8 !important;
}}

.streamlit-expanderHeader[aria-expanded="true"]::after {{
    transform: translateY(-50%) rotate(-90deg) !important;
}}

.streamlit-expanderContent {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    padding: 24px !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

/* Progress bar */
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    background-size: 200% 100% !important;
    animation: gradientFlow 3s ease infinite !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3) !important;
}}

.stProgress > div > div {{
    background: rgba(139, 92, 246, 0.1) !important;
    border-radius: 10px !important;
    height: 10px !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}}

/* Spinner */
.stSpinner > div {{
    border-color: #8B5CF6 transparent transparent transparent !important;
    border-width: 3px !important;
    animation: spinner 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite !important;
}}

@keyframes spinner {{
    0% {{ transform: rotate(0deg) !important; }}
    100% {{ transform: rotate(360deg) !important; }}
}}

/* Checkbox */
.stCheckbox {{
    margin: 8px 0 !important;
}}

.stCheckbox label {{
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 8px 12px !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}}

.stCheckbox label:hover {{
    background: rgba(139, 92, 246, 0.05) !important;
    transform: translateX(4px) !important;
}}

/* Slider */
.stSlider {{
    margin: 16px 0 !important;
}}

.stSlider [data-baseweb="slider"] {{
    padding: 8px 0 !important;
}}

.stSlider [data-baseweb="thumb"] {{
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    border: 3px solid white !important;
    box-shadow: 
        0 4px 12px rgba(139, 92, 246, 0.3),
        0 0 0 4px rgba(139, 92, 246, 0.1) !important;
    transition: all 0.3s ease !important;
}}

.stSlider [data-baseweb="thumb"]:hover {{
    transform: scale(1.1) !important;
    box-shadow: 
        0 6px 20px rgba(139, 92, 246, 0.4),
        0 0 0 6px rgba(139, 92, 246, 0.15) !important;
}}

.stSlider [data-baseweb="track"] {{
    background: rgba(139, 92, 246, 0.1) !important;
    height: 8px !important;
    border-radius: 4px !important;
}}

.stSlider [data-baseweb="inner-track"] {{
    background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    height: 8px !important;
    border-radius: 4px !important;
}}

/* Number input */
.stNumberInput input {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 2px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.stNumberInput input:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}}

/* ========== BUTTONS STYLING ========== */
div.stButton > button:first-child {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    background-size: 200% 100% !important;
    color: white !important;
    border: none !important;
    padding: 14px 28px !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    min-height: 48px !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    position: relative !important;
    overflow: hidden !important;
    letter-spacing: -0.01em !important;
    animation: gradientFlow 3s ease infinite !important;
}}

div.stButton > button:first-child:hover {{
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 16px 40px rgba(139, 92, 246, 0.35),
        0 8px 32px rgba(139, 92, 246, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    background-position: 100% 50% !important;
}}

div.stButton > button:first-child:active {{
    transform: translateY(-2px) scale(1.01) !important;
    transition: all 0.1s ease !important;
}}

div.stButton > button:first-child::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
    transition: 0.6s !important;
}}

div.stButton > button:first-child:hover::before {{
    left: 100% !important;
}}

div.stButton > button:first-child::after {{
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    border-radius: 14px !important;
    padding: 2px !important;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), transparent) !important;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    -webkit-mask-composite: xor !important;
    mask-composite: exclude !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

div.stButton > button:first-child:hover::after {{
    opacity: 1 !important;
}}

div.stButton > button[kind="secondary"] {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #8B5CF6 !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

div.stButton > button[kind="secondary"]:hover {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%) !important;
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 12px 32px rgba(139, 92, 246, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.5) !important;
}}

/* ========== INPUT FIELDS ========== */
.stTextInput input {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    width: 100% !important;
    letter-spacing: -0.01em !important;
}}

.stTextInput input:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-2px) scale(1.01) !important;
    background: white !important;
}}

.stTextInput input::placeholder {{
    color: #9CA3AF !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
}}

.stTextInput input:hover {{
    border-color: rgba(139, 92, 246, 0.4) !important;
    box-shadow: 
        0 6px 24px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

/* ========== MODERN GUIDE SECTION ========== */
.modern-guide-container {{
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.95) 0%, 
        rgba(250, 249, 255, 0.98) 100%) !important;
    border-radius: 24px !important;
    padding: 40px !important;
    margin: 32px 0 !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    box-shadow: 
        0 20px 60px rgba(139, 92, 246, 0.1),
        0 8px 32px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.modern-guide-container::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 4px !important;
    background: linear-gradient(90deg, 
        #8B5CF6 0%, 
        #EC4899 50%, 
        #38BDF8 100%) !important;
    border-radius: 24px 24px 0 0 !important;
}}

.modern-guide-header {{
    text-align: center !important;
    margin-bottom: 40px !important;
    position: relative !important;
}}

.modern-guide-title-wrapper {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 16px !important;
    margin-bottom: 12px !important;
}}

.guide-main-icon {{
    font-size: 36px !important;
    color: transparent !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
}}

.modern-guide-title {{
    font-size: 28px !important;
    font-weight: 800 !important;
    color: transparent !important;
    background: linear-gradient(135deg, #1F2937 0%, #8B5CF6 100%) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    margin: 0 !important;
    letter-spacing: -0.02em !important;
}}

.modern-guide-subtitle {{
    color: #6B7280 !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    max-width: 600px !important;
    margin: 0 auto !important;
    line-height: 1.6 !important;
}}

/* Modern Guide Steps */
.modern-guide-step {{
    background: white !important;
    border-radius: 20px !important;
    padding: 32px !important;
    margin-bottom: 24px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    display: flex !important;
    align-items: flex-start !important;
    gap: 24px !important;
}}

.modern-guide-step:hover {{
    transform: translateY(-4px) !important;
    border-color: rgba(139, 92, 246, 0.25) !important;
    box-shadow: 
        0 16px 48px rgba(139, 92, 246, 0.12),
        0 8px 24px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.modern-step-number {{
    font-size: 14px !important;
    font-weight: 800 !important;
    color: white !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
    width: 36px !important;
    height: 36px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    margin-top: 8px !important;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
}}

.modern-step-content {{
    display: flex !important;
    align-items: flex-start !important;
    gap: 24px !important;
    flex: 1 !important;
}}

.modern-step-icon-wrapper {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 64px !important;
    height: 64px !important;
    border-radius: 16px !important;
    background: linear-gradient(135deg, 
        rgba(139, 92, 246, 0.1) 0%, 
        rgba(236, 72, 153, 0.1) 100%) !important;
    flex-shrink: 0 !important;
    transition: all 0.3s ease !important;
}}

.modern-guide-step:hover .modern-step-icon-wrapper {{
    transform: scale(1.1) rotate(5deg) !important;
    background: linear-gradient(135deg, 
        rgba(139, 92, 246, 0.2) 0%, 
        rgba(236, 72, 153, 0.2) 100%) !important;
}}

.step-icon {{
    font-size: 24px !important;
    color: #8B5CF6 !important;
}}

.modern-step-details {{
    flex: 1 !important;
}}

.modern-step-title {{
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #1F2937 !important;
    margin: 0 0 16px 0 !important;
    letter-spacing: -0.01em !important;
    background: linear-gradient(135deg, #1F2937 0%, #8B5CF6 50%) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}}

.modern-step-list {{
    margin: 0 !important;
    padding: 0 !important;
    list-style: none !important;
}}

.modern-step-list li {{
    color: #6B7280 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    line-height: 1.7 !important;
    margin-bottom: 12px !important;
    display: flex !important;
    align-items: flex-start !important;
    gap: 10px !important;
    padding-left: 4px !important;
}}

.list-icon {{
    color: #8B5CF6 !important;
    font-size: 12px !important;
    margin-top: 5px !important;
    flex-shrink: 0 !important;
}}

.highlight-text {{
    color: #8B5CF6 !important;
    font-weight: 600 !important;
    background: rgba(139, 92, 246, 0.1) !important;
    padding: 2px 8px !important;
    border-radius: 6px !important;
}}

.highlight-button {{
    color: white !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
    padding: 4px 12px !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3) !important;
}}

/* Pro Tips Section */
.modern-pro-tips {{
    background: linear-gradient(135deg, 
        rgba(245, 243, 255, 0.9) 0%, 
        rgba(240, 249, 255, 0.9) 100%) !important;
    border-radius: 20px !important;
    padding: 32px !important;
    margin-top: 32px !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.modern-pro-tips::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, 
        #EC4899 0%, 
        #8B5CF6 50%, 
        #38BDF8 100%) !important;
}}

.pro-tips-header {{
    display: flex !important;
    align-items: center !important;
    gap: 16px !important;
    margin-bottom: 24px !important;
}}

.pro-tips-icon-wrapper {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 48px !important;
    height: 48px !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%) !important;
    box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3) !important;
}}

.pro-tips-icon {{
    font-size: 24px !important;
    color: white !important;
}}

.pro-tips-title {{
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #1F2937 !important;
    margin: 0 !important;
    letter-spacing: -0.01em !important;
    background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}}

.pro-tips-content {{
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 20px !important;
}}

.pro-tip-item {{
    display: flex !important;
    align-items: flex-start !important;
    gap: 16px !important;
    padding: 20px !important;
    background: white !important;
    border-radius: 16px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    transition: all 0.3s ease !important;
}}

.pro-tip-item:hover {{
    transform: translateY(-3px) !important;
    border-color: rgba(139, 92, 246, 0.25) !important;
    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.1) !important;
}}

.tip-icon {{
    font-size: 20px !important;
    color: #10B981 !important;
    margin-top: 2px !important;
    flex-shrink: 0 !important;
}}

.tip-text {{
    flex: 1 !important;
}}

.tip-text strong {{
    display: block !important;
    color: #1F2937 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
    letter-spacing: -0.01em !important;
}}

.tip-text p {{
    color: #6B7280 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}}

/* ========== HERO SECTION ========== */

.hero-icon {{
    color: #FBA49 !important;
    text-shadow: 
        0 0 20px rgba(251, 191, 36, 0.8),
        0 0 40px rgba(251, 191, 36, 0.6) !important;
    font-size: 1.1em !important;
}}


.hero-section {{
    background: linear-gradient(135deg, 
        #8B5CF6 0%, 
        #0EA5E9 25%, 
        #6D28D9 50%, 
        #EC4899 75%, 
        #F472B6 100%) !important;
    background-size: 300% 300% !important;
    animation: gradientFlow 8s ease infinite !important;
    border-radius: 28px !important;
    padding: 48px !important;
    margin-bottom: 32px !important;
    position: relative !important;
    overflow: hidden !important;
    text-align: center !important;
    box-shadow: 
        0 24px 80px rgba(139, 92, 246, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}}


/* Add subtle pattern overlay */
.hero-section::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: 
        radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%) !important;
    z-index: 1 !important;
}}

.hero-section::after {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255, 255, 255, 0.5), 
        transparent) !important;
    z-index: 1 !important;
}}

.hero-title {{
    color: white !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    margin-bottom: 16px !important;
    text-shadow: 
        0 2px 4px rgba(0, 0, 0, 0.2),
        0 4px 12px rgba(0, 0, 0, 0.3) !important;
    letter-spacing: -0.03em !important;
    position: relative !important;
    z-index: 2 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 15px !important;
}}

.hero-subtitle {{
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 18px !important;
    max-width: 700px !important;
    margin: 0 auto 32px auto !important;
    line-height: 1.7 !important;
    font-weight: 500 !important;
    position: relative !important;
    z-index: 2 !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
}}

/* ========== SEARCH CONTAINER ========== */
.search-container {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(40px) !important;
    border-radius: 24px !important;
    padding: 40px !important;
    box-shadow: 
        0 24px 80px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    margin: 32px 0 !important;
    position: relative !important;
    overflow: hidden !important;
}}

.search-container:hover {{
    border-color: rgba(139, 92, 246, 0.3) !important;
    box-shadow: 
        0 32px 100px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.search-title {{
    font-size: 24px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    color: #1F2937 !important;
    letter-spacing: -0.02em !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}}

.search-subtitle {{
    color: #6B7280 !important;
    font-size: 16px !important;
    margin-bottom: 28px !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
}}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #F5F3FF 0%, #FAF9FF 100%) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
    box-shadow: 
        8px 0 40px rgba(139, 92, 246, 0.08),
        inset 1px 0 0 rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(20px) !important;
}}

/* ========== FOOTER ========== */
.neon-footer {{
    margin-top: 60px !important;
    padding: 48px 0 !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    border-radius: 28px 28px 0 0 !important;
    text-align: center !important;
    position: relative !important;
    overflow: hidden !important;
    animation: gradientFlow 8s ease infinite !important;
    background-size: 200% 200% !important;
    box-shadow: 
        0 -4px 40px rgba(139, 92, 246, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}}

.neon-footer::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
}}

.neon-footer h3 {{
    color: white !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    margin-bottom: 16px !important;
    position: relative !important;
    z-index: 1 !important;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}}

.neon-footer p {{
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 16px !important;
    max-width: 600px !important;
    margin: 0 auto 24px auto !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    position: relative !important;
    z-index: 1 !important;
}}

/* ========== MODERN CARD STYLES ========== */

/* Modern Stat Card */
.modern-stat-card {{
    background: white !important;
    border-radius: 20px !important;
    padding: 24px !important;
    position: relative !important;
    overflow: hidden !important;
    height: 100% !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    box-shadow: 
        0 6px 20px rgba(139, 92, 246, 0.08),
        0 1px 3px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

.modern-stat-card:hover {{
    transform: translateY(-6px) !important;
    border-color: rgba(139, 92, 246, 0.3) !important;
    box-shadow: 
        0 12px 32px rgba(139, 92, 246, 0.15),
        0 4px 12px rgba(0, 0, 0, 0.08) !important;
}}

.modern-stat-content {{
    position: relative !important;
    z-index: 2 !important;
    text-align: center !important;
}}

.modern-stat-icon-wrapper {{
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 64px !important;
    height: 64px !important;
    border-radius: 16px !important;
    margin-bottom: 20px !important;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%) !important;
    transition: all 0.3s ease !important;
}}

.modern-stat-card:hover .modern-stat-icon-wrapper {{
    transform: scale(1.1) rotate(5deg) !important;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
}}

.modern-stat-icon {{
    font-size: 32px !important;
    line-height: 1 !important;
}}

.modern-stat-number {{
    font-size: 36px !important;
    font-weight: 800 !important;
    margin: 12px 0 !important;
    color: transparent !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.03em !important;
    font-family: 'Inter', sans-serif !important;
}}

.modern-stat-label {{
    color: #6B7280 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    opacity: 0.9 !important;
}}

.modern-stat-decoration {{
    position: absolute !important;
    top: 0 !important;
    right: 0 !important;
    width: 60px !important;
    height: 60px !important;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%) !important;
    border-radius: 0 20px 0 40px !important;
}}

/* Modern Feature Card */
.modern-feature-card {{
    background: white !important;
    border-radius: 20px !important;
    padding: 32px 24px !important;
    position: relative !important;
    overflow: hidden !important;
    height: 100% !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 4px 16px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
}}

.modern-feature-card:hover {{
    transform: translateY(-8px) !important;
    border-color: rgba(139, 92, 246, 0.25) !important;
    box-shadow: 
        0 16px 40px rgba(139, 92, 246, 0.12),
        0 8px 20px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.modern-feature-icon-wrapper {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 80px !important;
    height: 80px !important;
    border-radius: 20px !important;
    margin-bottom: 24px !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
    position: relative !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

.modern-feature-card:hover .modern-feature-icon-wrapper {{
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 12px 24px rgba(139, 92, 246, 0.25) !important;
}}

.modern-feature-icon {{
    font-size: 40px !important;
    line-height: 1 !important;
    color: white !important;
    transition: transform 0.3s ease !important;
}}

.modern-feature-card:hover .modern-feature-icon {{
    transform: scale(1.1) !important;
}}

.modern-feature-content {{
    flex: 1 !important;
    width: 100% !important;
}}

.modern-feature-title {{
    font-size: 20px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    color: #1F2937 !important;
    letter-spacing: -0.01em !important;
    line-height: 1.3 !important;
}}

.modern-feature-desc {{
    color: #6B7280 !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    font-weight: 500 !important;
    margin: 0 !important;
}}

.modern-feature-hover-effect {{
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 4px !important;
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

.modern-feature-card:hover .modern-feature-hover-effect {{
    opacity: 1 !important;
}}

/* Modern Metric Box */
.modern-metric-box {{
    background: white !important;
    border-radius: 16px !important;
    padding: 24px 20px !important;
    position: relative !important;
    overflow: hidden !important;
    height: 100% !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-align: center !important;
}}

.modern-metric-box:hover {{
    transform: translateY(-4px) !important;
    border-color: rgba(139, 92, 246, 0.25) !important;
    box-shadow: 
        0 12px 28px rgba(139, 92, 246, 0.1),
        0 4px 12px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.modern-metric-label {{
    color: #6B7280 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 8px !important;
    opacity: 0.9 !important;
}}

.modern-metric-value {{
    font-size: 28px !important;
    font-weight: 800 !important;
    color: transparent !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.02em !important;
    font-family: 'Inter', sans-serif !important;
    margin: 4px 0 !important;
}}

.modern-metric-progress {{
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

.modern-metric-box:hover .modern-metric-progress {{
    opacity: 1 !important;
}}

/* Modern Content Card */
.modern-content-card {{
    background: white !important;
    border-radius: 24px !important;
    padding: 32px !important;
    margin-bottom: 24px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 8px 24px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.modern-content-card:hover {{
    transform: translateY(-4px) !important;
    border-color: rgba(139, 92, 246, 0.2) !important;
    box-shadow: 
        0 16px 48px rgba(139, 92, 246, 0.08),
        0 8px 24px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.modern-card-header {{
    margin-bottom: 24px !important;
    position: relative !important;
}}

.modern-card-title-wrapper {{
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 8px !important;
}}

.modern-card-title {{
    font-size: 24px !important;
    font-weight: 800 !important;
    margin: 0 !important;
    color: #1F2937 !important;
    letter-spacing: -0.02em !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}}

.modern-card-accent {{
    width: 40px !important;
    height: 4px !important;
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%) !important;
    border-radius: 2px !important;
}}

.modern-card-body {{
    color: #4B5563 !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
    font-weight: 500 !important;
}}

/* Optional: Add subtle background pattern */
.modern-content-card::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    right: 0 !important;
    width: 100px !important;
    height: 100px !important;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.03) 0%, rgba(236, 72, 153, 0.03) 100%) !important;
    border-radius: 0 0 0 100px !important;
    pointer-events: none !important;
}}

/* ========== RESPONSIVE DESIGN ========== */
@media (max-width: 768px) {{
    .stTabs [data-baseweb="tab"] {{
        min-width: 100px !important;
        padding: 0 16px !important;
        font-size: 13px !important;
        height: 44px !important;
    }}
    
    .hero-title {{
        font-size: 32px !important;
    }}
    
    .hero-subtitle {{
        font-size: 16px !important;
    }}
    
    .modern-guide-container {{
        padding: 24px !important;
    }}
    
    .modern-guide-title {{
        font-size: 24px !important;
    }}
    
    .modern-guide-step {{
        padding: 24px !important;
        flex-direction: column !important;
        gap: 20px !important;
    }}
    
    .modern-step-content {{
        flex-direction: column !important;
        gap: 20px !important;
    }}
    
    .modern-step-icon-wrapper {{
        width: 56px !important;
        height: 56px !important;
    }}
    
    .pro-tips-content {{
        grid-template-columns: 1fr !important;
    }}
    
    .pro-tips-header {{
        flex-direction: column !important;
        text-align: center !important;
        gap: 12px !important;
    }}
    
    .search-container {{
        padding: 24px !important;
    }}
    
    .modern-stat-card {{
        padding: 20px !important;
    }}
    
    .modern-stat-icon-wrapper {{
        width: 56px !important;
        height: 56px !important;
        margin-bottom: 16px !important;
    }}
    
    .modern-stat-number {{
        font-size: 28px !important;
    }}
    
    .modern-feature-card {{
        padding: 24px 16px !important;
    }}
    
    .modern-feature-icon-wrapper {{
        width: 64px !important;
        height: 64px !important;
        margin-bottom: 20px !important;
    }}
    
    .modern-feature-icon {{
        font-size: 32px !important;
    }}
    
    .modern-metric-box {{
        padding: 20px 16px !important;
    }}
    
    .modern-metric-value {{
        font-size: 24px !important;
    }}
    
    .modern-content-card {{
        padding: 24px !important;
    }}
    
    .modern-card-title {{
        font-size: 20px !important;
    }}
    
    .heatmap-container {{
    background: linear-gradient(135deg, 
        rgba(245, 243, 255, 0.8) 0%, 
        rgba(255, 255, 255, 0.9) 100%);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 24px;
    border: 1px solid rgba(139, 92, 246, 0.2);
    box-shadow: 
        0 20px 60px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    margin: 20px 0;
}}

.chart-title {{
    font-size: 22px;
    font-weight: 800;
    color: transparent;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
    text-align: center;
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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Home"

# ================================
# NEW ALERT FUNCTION AS CARDS
# ================================

def render_alert_card(message, alert_type="info", title=None):
    """Render alert messages as beautiful cards"""
    
    if alert_type == "success":
        icon = "✅"
        alert_class = "alert-success"
        default_title = "Success!"
    elif alert_type == "warning":
        icon = "⚠️"
        alert_class = "alert-warning"
        default_title = "Warning!"
    elif alert_type == "danger":
        icon = "❌"
        alert_class = "alert-danger"
        default_title = "Error!"
    else:
        icon = "ℹ️"
        alert_class = "alert-info"
        default_title = "Info"
    
    alert_title = title if title else default_title
    
    st.markdown(f"""
    <div class="alert-card {alert_class}">
        <div class="alert-icon">{icon}</div>
        <div class="alert-content">
            <div class="alert-title">{alert_title}</div>
            <div class="alert-message">{message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# REAL-TIME WEBSOCKET MANAGER
# ================================
#REMOVED

st.markdown(f"""
<style>
/* ========== GLOBAL STYLES & SCROLLBAR ========== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {{
    background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F7 100%) !important;
    color: #1F2937 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 8px !important;
    height: 8px !important;
}}

::-webkit-scrollbar-track {{
    background: rgba(245, 243, 255, 0.5) !important;
    border-radius: 4px !important;
}}

::-webkit-scrollbar-thumb {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    border-radius: 4px !important;
}}

::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 50%, #DB2777 100%) !important;
}}

/* ========== ANIMATIONS ========== */
@keyframes fadeInUp {{
    from {{ 
        opacity: 0 !important;
        transform: translateY(20px) !important;
    }}
    to {{ 
        opacity: 1 !important;
        transform: translateY(0) !important;
    }}
}}

@keyframes slideInRight {{
    from {{ 
        opacity: 0 !important;
        transform: translateX(-20px) !important;
    }}
    to {{ 
        opacity: 1 !important;
        transform: translateX(0) !important;
    }}
}}

@keyframes pulseGlow {{
    0%, 100% {{ 
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15) !important;
    }}
    50% {{ 
        box-shadow: 0 6px 30px rgba(139, 92, 246, 0.25) !important;
    }}
}}

@keyframes gradientFlow {{
    0% {{ background-position: 0% 50% !important; }}
    50% {{ background-position: 100% 50% !important; }}
    100% {{ background-position: 0% 50% !important; }}
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) !important; }}
    50% {{ transform: translateY(-10px) !important; }}
}}

/* ========== MODERN GLASS MORPHISM EFFECTS ========== */
.glass-morphism {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
}}

/* ========== MODERN TABS STYLING ========== */
.stTabs {{
    background: transparent !important;
    padding: 0 !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 4px !important;
    background: white !important;
    padding: 8px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    margin-bottom: 24px !important;
    box-shadow: 
        0 4px 16px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    overflow-x: auto !important;
    white-space: nowrap !important;
    backdrop-filter: blur(10px) !important;
    animation: fadeInUp 0.8s ease !important;
}}

.stTabs [data-baseweb="tab"] {{
    height: 48px !important;
    padding: 0 24px !important;
    color: #6B7280 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    background: transparent !important;
    border-radius: 12px !important;
    border: none !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: 120px !important;
    position: relative !important;
    overflow: hidden !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%) !important;
    color: #8B5CF6 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1) !important;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    color: white !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transform: translateY(-2px) !important;
    font-weight: 700 !important;
    animation: pulseGlow 2s ease-in-out infinite !important;
}}

.stTabs [aria-selected="true"]::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #EC4899 0%, #F472B6 100%) !important;
    border-radius: 12px 12px 0 0 !important;
}}

/* ========== ENHANCED DATAFRAME STYLING ========== */
.dataframe {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.85) 0%, rgba(245, 243, 255, 0.9) 100%) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: 
        0 12px 40px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6),
        inset 0 -1px 0 rgba(139, 92, 246, 0.1) !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    margin: 20px 0 !important;
    animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.dataframe::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), transparent) !important;
}}

.dataframe::after {{
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    border-radius: 20px !important;
    padding: 2px !important;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(236, 72, 153, 0.1), rgba(56, 189, 248, 0.1)) !important;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    -webkit-mask-composite: xor !important;
    mask-composite: exclude !important;
    pointer-events: none !important;
}}

.dataframe th {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 20px 24px !important;
    font-size: 14px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    border: none !important;
    position: relative !important;
    font-family: 'Inter', sans-serif !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s ease !important;
}}

.dataframe th:hover {{
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 50%, #5B21B6 100%) !important;
    transform: translateY(-1px) !important;
}}

.dataframe th::after {{
    content: '' !important;
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent) !important;
}}

.dataframe td {{
    padding: 18px 24px !important;
    border-bottom: 1px solid rgba(139, 92, 246, 0.15) !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    color: #1F2937 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: 'Inter', sans-serif !important;
    background: transparent !important;
    position: relative !important;
}}

.dataframe td::before {{
    content: '' !important;
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    bottom: 0 !important;
    width: 3px !important;
    background: linear-gradient(180deg, #8B5CF6 0%, #EC4899 100%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

.dataframe tr {{
    transition: all 0.3s ease !important;
    background: transparent !important;
}}

.dataframe tr:hover {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%) !important;
    transform: translateX(8px) !important;
    box-shadow: 
        -8px 0 24px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    border-radius: 12px !important;
    margin: 8px 0 !important;
}}

.dataframe tr:hover td {{
    color: #7C3AED !important;
    font-weight: 600 !important;
}}

.dataframe tr:hover td::before {{
    opacity: 1 !important;
}}

.dataframe tr:last-child td {{
    border-bottom: none !important;
}}

/* Zebra striping for better readability */
.dataframe tr:nth-child(even) {{
    background: rgba(245, 243, 255, 0.3) !important;
}}

.dataframe tr:nth-child(even):hover {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%) !important;
}}

/* ========== ALERT MESSAGES AS CARDS ========== */
.alert-card {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin: 16px 0 !important;
    border-left: 4px solid !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    display: flex !important;
    align-items: center !important;
    gap: 16px !important;
    animation: slideInRight 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.alert-card::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent) !important;
}}

.alert-success {{
    border-left-color: #10B981 !important;
    background: linear-gradient(135deg, rgba(240, 253, 244, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-danger {{
    border-left-color: #EF4444 !important;
    background: linear-gradient(135deg, rgba(254, 242, 242, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-warning {{
    border-left-color: #F59E0B !important;
    background: linear-gradient(135deg, rgba(255, 251, 235, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-info {{
    border-left-color: #0EA5E9 !important;
    background: linear-gradient(135deg, rgba(240, 249, 255, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-purple {{
    border-left-color: #8B5CF6 !important;
    background: linear-gradient(135deg, rgba(245, 243, 255, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
}}

.alert-icon {{
    font-size: 24px !important;
    min-width: 40px !important;
    text-align: center !important;
}}

.alert-content {{
    flex: 1 !important;
}}

.alert-title {{
    font-weight: 700 !important;
    font-size: 16px !important;
    margin-bottom: 4px !important;
    color: #1F2937 !important;
    letter-spacing: -0.01em !important;
}}

.alert-message {{
    font-size: 14px !important;
    color: #6B7280 !important;
    line-height: 1.6 !important;
    font-weight: 500 !important;
}}

/* ========== ALL STREAMLIT COMPONENTS STYLING ========== */

/* Radio buttons */
.stRadio [role="radiogroup"] {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    padding: 16px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
}}

.stRadio [role="radio"] {{
    margin-right: 12px !important;
}}

.stRadio label {{
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    letter-spacing: -0.01em !important;
}}

/* Select boxes */
.stSelectbox {{
    background: transparent !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}

.stSelectbox select {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 2px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    width: 100% !important;
    appearance: none !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%238B5CF6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: right 16px center !important;
    background-size: 16px !important;
    padding-right: 40px !important;
}}

.stSelectbox select:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}}

/* Text area */
.stTextArea textarea {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 2px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    min-height: 100px !important;
    font-family: 'Inter', monospace !important;
}}

.stTextArea textarea:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}}

/* Metric cards */
[data-testid="stMetric"] {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}}

[data-testid="stMetric"]::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 50%, #38BDF8 100%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-6px) scale(1.02) !important;
    box-shadow: 
        0 20px 40px rgba(139, 92, 246, 0.15),
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.2) !important;
}}

[data-testid="stMetric"]:hover::before {{
    opacity: 1 !important;
}}

[data-testid="stMetricLabel"] {{
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #6B7280 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}}

[data-testid="stMetricValue"] {{
    font-size: 32px !important;
    font-weight: 800 !important;
    color: transparent !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 4px 0 !important;
}}

[data-testid="stMetricDelta"] {{
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 4px 8px !important;
    border-radius: 8px !important;
    margin-top: 4px !important;
}}

/* Expander */
.streamlit-expanderHeader {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 20px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    border: none !important;
    margin-bottom: 8px !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}}

.streamlit-expanderHeader:hover {{
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 16px 40px rgba(139, 92, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}}

.streamlit-expanderHeader::after {{
    content: '▶' !important;
    position: absolute !important;
    right: 20px !important;
    top: 50% !important;
    transform: translateY(-50%) rotate(90deg) !important;
    transition: transform 0.3s ease !important;
    opacity: 0.8 !important;
}}

.streamlit-expanderHeader[aria-expanded="true"]::after {{
    transform: translateY(-50%) rotate(-90deg) !important;
}}

.streamlit-expanderContent {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    padding: 24px !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

/* Progress bar */
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    background-size: 200% 100% !important;
    animation: gradientFlow 3s ease infinite !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3) !important;
}}

.stProgress > div > div {{
    background: rgba(139, 92, 246, 0.1) !important;
    border-radius: 10px !important;
    height: 10px !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}}

/* Spinner */
.stSpinner > div {{
    border-color: #8B5CF6 transparent transparent transparent !important;
    border-width: 3px !important;
    animation: spinner 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite !important;
}}

@keyframes spinner {{
    0% {{ transform: rotate(0deg) !important; }}
    100% {{ transform: rotate(360deg) !important; }}
}}

/* Checkbox */
.stCheckbox {{
    margin: 8px 0 !important;
}}

.stCheckbox label {{
    color: #374151 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 8px 12px !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}}

.stCheckbox label:hover {{
    background: rgba(139, 92, 246, 0.05) !important;
    transform: translateX(4px) !important;
}}

/* Slider */
.stSlider {{
    margin: 16px 0 !important;
}}

.stSlider [data-baseweb="slider"] {{
    padding: 8px 0 !important;
}}

.stSlider [data-baseweb="thumb"] {{
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    border: 3px solid white !important;
    box-shadow: 
        0 4px 12px rgba(139, 92, 246, 0.3),
        0 0 0 4px rgba(139, 92, 246, 0.1) !important;
    transition: all 0.3s ease !important;
}}

.stSlider [data-baseweb="thumb"]:hover {{
    transform: scale(1.1) !important;
    box-shadow: 
        0 6px 20px rgba(139, 92, 246, 0.4),
        0 0 0 6px rgba(139, 92, 246, 0.15) !important;
}}

.stSlider [data-baseweb="track"] {{
    background: rgba(139, 92, 246, 0.1) !important;
    height: 8px !important;
    border-radius: 4px !important;
}}

.stSlider [data-baseweb="inner-track"] {{
    background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    height: 8px !important;
    border-radius: 4px !important;
}}

/* Number input */
.stNumberInput input {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 2px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.stNumberInput input:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}}

/* ========== BUTTONS STYLING ========== */
div.stButton > button:first-child {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    background-size: 200% 100% !important;
    color: white !important;
    border: none !important;
    padding: 14px 28px !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    min-height: 48px !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    position: relative !important;
    overflow: hidden !important;
    letter-spacing: -0.01em !important;
    animation: gradientFlow 3s ease infinite !important;
}}

div.stButton > button:first-child:hover {{
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 16px 40px rgba(139, 92, 246, 0.35),
        0 8px 32px rgba(139, 92, 246, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    background-position: 100% 50% !important;
}}

div.stButton > button:first-child:active {{
    transform: translateY(-2px) scale(1.01) !important;
    transition: all 0.1s ease !important;
}}

div.stButton > button:first-child::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
    transition: 0.6s !important;
}}

div.stButton > button:first-child:hover::before {{
    left: 100% !important;
}}

div.stButton > button:first-child::after {{
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    border-radius: 14px !important;
    padding: 2px !important;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), transparent) !important;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    -webkit-mask-composite: xor !important;
    mask-composite: exclude !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

div.stButton > button:first-child:hover::after {{
    opacity: 1 !important;
}}

div.stButton > button[kind="secondary"] {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #8B5CF6 !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

div.stButton > button[kind="secondary"]:hover {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%) !important;
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 12px 32px rgba(139, 92, 246, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.5) !important;
}}

/* ========== INPUT FIELDS ========== */
.stTextInput input {{
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    color: #374151 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    width: 100% !important;
    letter-spacing: -0.01em !important;
}}

.stTextInput input:focus {{
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    transform: translateY(-2px) scale(1.01) !important;
    background: white !important;
}}

.stTextInput input::placeholder {{
    color: #9CA3AF !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
}}

.stTextInput input:hover {{
    border-color: rgba(139, 92, 246, 0.4) !important;
    box-shadow: 
        0 6px 24px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}


/* Image hover effects for sidebar and hero */
.sidebar-main-icon img {{
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}}

.hero-title img {{
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}



/* ========== CUSTOM CARDS ========== */
.glass-card {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(40px) !important;
    -webkit-backdrop-filter: blur(40px) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    margin-bottom: 24px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 
        0 20px 60px rgba(139, 92, 246, 0.12),
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6),
        inset 0 -1px 0 rgba(0, 0, 0, 0.05) !important;
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.glass-card:hover {{
    transform: translateY(-8px) scale(1.01) !important;
    box-shadow: 
        0 32px 80px rgba(139, 92, 246, 0.2),
        0 20px 60px rgba(139, 92, 246, 0.12),
        0 8px 32px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6),
        inset 0 -1px 0 rgba(0, 0, 0, 0.05) !important;
    border-color: rgba(139, 92, 246, 0.2) !important;
}}

.glass-card::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.2), transparent) !important;
}}

.glass-card::after {{
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    border-radius: 24px !important;
    padding: 2px !important;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(236, 72, 153, 0.1), rgba(56, 189, 248, 0.1)) !important;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0) !important;
    -webkit-mask-composite: xor !important;
    mask-composite: exclude !important;
    opacity: 0 !important;
    transition: opacity 0.4s ease !important;
}}

.glass-card:hover::after {{
    opacity: 1 !important;
}}

.glass-card-header {{
    margin: -32px -32px 24px -32px !important;
    padding: 32px !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    border-radius: 24px 24px 0 0 !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
}}

.glass-card-header::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
    opacity: 0.5 !important;
}}

.glass-card-header h2 {{
    color: white !important;
    margin: 0 !important;
    font-size: 24px !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    letter-spacing: -0.02em !important;
    position: relative !important;
    z-index: 1 !important;
}}

/* ========== STAT CARDS ========== */
.stat-card {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(40px) !important;
    border-radius: 20px !important;
    padding: 28px !important;
    text-align: center !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    height: 100% !important;
    box-shadow: 
        0 12px 40px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.stat-card:hover {{
    transform: translateY(-8px) scale(1.03) !important;
    box-shadow: 
        0 24px 60px rgba(139, 92, 246, 0.2),
        0 12px 40px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.3) !important;
}}

.stat-card::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 50%, #38BDF8 100%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

.stat-card:hover::before {{
    opacity: 1 !important;
}}

.stat-icon {{
    font-size: 48px !important;
    margin-bottom: 16px !important;
    display: inline-block !important;
    transition: transform 0.3s ease !important;
}}

.stat-card:hover .stat-icon {{
    transform: scale(1.1) rotate(5deg) !important;
}}

.stat-number {{
    font-size: 36px !important;
    font-weight: 800 !important;
    margin: 12px 0 !important;
    color: transparent !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.03em !important;
}}

.stat-label {{
    color: #6B7280 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    opacity: 0.8 !important;
}}

/* ========== GUIDE SECTION ========== */
.guide-card {{
    background: linear-gradient(135deg, rgba(245, 243, 255, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
    backdrop-filter: blur(40px) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    margin: 24px 0 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    box-shadow: 
        0 20px 60px rgba(139, 92, 246, 0.12),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.guide-step {{
    display: flex !important;
    align-items: flex-start !important;
    gap: 20px !important;
    margin-bottom: 28px !important;
    padding: 24px !important;
    background: rgba(255, 255, 255, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px !important;
    border-left: 4px solid #8B5CF6 !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

.guide-step:hover {{
    transform: translateX(8px) scale(1.01) !important;
    box-shadow: 
        0 16px 48px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-left-color: #EC4899 !important;
}}

.step-icon {{
    font-size: 28px !important;
    min-width: 48px !important;
    text-align: center !important;
    padding: 10px !important;
    border-radius: 12px !important;
    background: rgba(139, 92, 246, 0.1) !important;
    transition: all 0.3s ease !important;
}}

.guide-step:hover .step-icon {{
    transform: scale(1.1) rotate(5deg) !important;
    background: rgba(139, 92, 246, 0.2) !important;
}}

.step-content h4 {{
    color: #1F2937 !important;
    margin: 0 0 12px 0 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}}

.step-content ul {{
    margin: 0 !important;
    padding-left: 20px !important;
    color: #6B7280 !important;
}}

.step-content li {{
    margin-bottom: 8px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    position: relative !important;
}}

.step-content li::before {{
    content: '→' !important;
    position: absolute !important;
    left: -20px !important;
    color: #8B5CF6 !important;
    font-weight: bold !important;
}}

/* ========== METRIC BOXES ========== */
.metric-box {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    text-align: center !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    height: 100% !important;
    position: relative !important;
    overflow: hidden !important;
}}

.metric-box:hover {{
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 16px 48px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.3) !important;
}}

.metric-box::after {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 2px !important;
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

.metric-box:hover::after {{
    opacity: 1 !important;
}}

.metric-label {{
    color: #6B7280 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    margin-bottom: 8px !important;
    opacity: 0.9 !important;
}}

.metric-value {{
    font-size: 24px !important;
    font-weight: 800 !important;
    color: transparent !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.02em !important;
}}

/* ========== RISK BADGES ========== */
.risk-badge {{
    display: inline-flex !important;
    align-items: center !important;
    padding: 8px 18px !important;
    border-radius: 50px !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    gap: 6px !important;
    box-shadow: 
        0 4px 16px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    backdrop-filter: blur(10px) !important;
}}

.risk-badge:hover {{
    transform: translateY(-2px) scale(1.05) !important;
    box-shadow: 
        0 8px 24px rgba(0, 0, 0, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}}

.risk-badge::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent) !important;
    transition: 0.5s !important;
}}

.risk-badge:hover::before {{
    left: 100% !important;
}}

.badge-critical {{
    background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
    color: white !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
}}

.badge-high {{
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
    color: white !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
}}

.badge-medium {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
    color: white !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
}}

.badge-low {{
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: white !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
}}

/* ========== CHART CONTAINERS ========== */
.chart-container {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(40px) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    margin: 20px 0 !important;
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
    height: 100% !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

.chart-container:hover {{
    transform: translateY(-4px) scale(1.01) !important;
    box-shadow: 
        0 28px 80px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.2) !important;
}}

.chart-title {{
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #1F2937 !important;
    margin-bottom: 20px !important;
    text-align: center !important;
    letter-spacing: -0.01em !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}}

/* ========== IMAGE STYLING ========== */
.medical-image {{
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
    border-radius: 16px !important;
    margin: 12px 0 !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    box-shadow: 
        0 12px 40px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    filter: saturate(1.1) contrast(1.05) !important;
}}

.medical-image:hover {{
    transform: scale(1.05) translateY(-4px) !important;
    box-shadow: 
        0 24px 60px rgba(139, 92, 246, 0.25),
        0 12px 40px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.4) !important;
    filter: saturate(1.2) contrast(1.1) brightness(1.05) !important;
}}

/* ========== HERO SECTION ========== */
.hero-section {{
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #6D28D9 100%) !important;
    border-radius: 28px !important;
    padding: 48px !important;
    margin-bottom: 32px !important;
    position: relative !important;
    overflow: hidden !important;
    text-align: center !important;
    box-shadow: 
        0 24px 80px rgba(139, 92, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    animation: gradientFlow 8s ease infinite !important;
    background-size: 200% 200% !important;
}}

.hero-section::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24-5 5-5 5 2.24 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E") !important;
    opacity: 0.4 !important;
}}

.hero-title {{
    color: white !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    margin-bottom: 16px !important;
    text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    letter-spacing: -0.03em !important;
    position: relative !important;
    z-index: 1 !important;
}}

.hero-subtitle {{
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 18px !important;
    max-width: 700px !important;
    margin: 0 auto 32px auto !important;
    line-height: 1.7 !important;
    font-weight: 500 !important;
    position: relative !important;
    z-index: 1 !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}}

/* ========== FEATURE CARDS ========== */
.feature-card {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(40px) !important;
    border-radius: 20px !important;
    padding: 32px !important;
    text-align: center !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 16px 48px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    height: 100% !important;
    position: relative !important;
    overflow: hidden !important;
}}

.feature-card:hover {{
    transform: translateY(-8px) scale(1.03) !important;
    box-shadow: 
        0 28px 80px rgba(139, 92, 246, 0.2),
        0 16px 48px rgba(139, 92, 246, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border-color: rgba(139, 92, 246, 0.3) !important;
}}

.feature-card::after {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 50%, #38BDF8 100%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}}

.feature-card:hover::after {{
    opacity: 1 !important;
}}

.feature-icon {{
    font-size: 48px !important;
    margin-bottom: 20px !important;
    display: inline-block !important;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

.feature-card:hover .feature-icon {{
    transform: scale(1.2) rotate(10deg) !important;
}}

.feature-title {{
    font-size: 20px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    color: #1F2937 !important;
    letter-spacing: -0.01em !important;
}}

.feature-desc {{
    color: #6B7280 !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    font-weight: 500 !important;
}}

/* ========== SEARCH CONTAINER ========== */
.search-container {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%) !important;
    backdrop-filter: blur(40px) !important;
    border-radius: 24px !important;
    padding: 40px !important;
    box-shadow: 
        0 24px 80px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
    margin: 32px 0 !important;
    position: relative !important;
    overflow: hidden !important;
}}

.search-container:hover {{
    border-color: rgba(139, 92, 246, 0.3) !important;
    box-shadow: 
        0 32px 100px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}}

.search-title {{
    font-size: 24px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    color: #1F2937 !important;
    letter-spacing: -0.02em !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}}

.search-subtitle {{
    color: #6B7280 !important;
    font-size: 16px !important;
    margin-bottom: 28px !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
}}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #F5F3FF 0%, #FAF9FF 100%) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
    box-shadow: 
        8px 0 40px rgba(139, 92, 246, 0.08),
        inset 1px 0 0 rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(20px) !important;
}}

[data-testid="stSidebar"] .glass-card {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(250, 249, 255, 0.95) 100%) !important;
}}

/* ========== FOOTER ========== */
.neon-footer {{
    margin-top: 60px !important;
    padding: 48px 0 !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%) !important;
    border-radius: 28px 28px 0 0 !important;
    text-align: center !important;
    position: relative !important;
    overflow: hidden !important;
    animation: gradientFlow 8s ease infinite !important;
    background-size: 200% 200% !important;
    box-shadow: 
        0 -4px 40px rgba(139, 92, 246, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}}

.neon-footer::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
}}

.neon-footer h3 {{
    color: white !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    margin-bottom: 16px !important;
    position: relative !important;
    z-index: 1 !important;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}}

.neon-footer p {{
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 16px !important;
    max-width: 600px !important;
    margin: 0 auto 24px auto !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    position: relative !important;
    z-index: 1 !important;
}}

/* ========== RESPONSIVE DESIGN ========== */
@media (max-width: 768px) {{
    .stTabs [data-baseweb="tab"] {{
        min-width: 100px !important;
        padding: 0 16px !important;
        font-size: 13px !important;
        height: 44px !important;
    }}
    
    .hero-title {{
        font-size: 32px !important;
    }}
    
    .hero-subtitle {{
        font-size: 16px !important;
    }}
    
    .stat-card {{
        padding: 20px !important;
    }}
    
    .stat-number {{
        font-size: 28px !important;
    }}
    
    .feature-card {{
        padding: 24px !important;
    }}
    
    .glass-card {{
        padding: 24px !important;
    }}
    
    .glass-card-header {{
        padding: 24px !important;
        margin: -24px -24px 20px -24px !important;
    }}
    
    .search-container {{
        padding: 24px !important;
    }}
    
    .dataframe th,
    .dataframe td {{
        padding: 12px 16px !important;
    }}
}}

/* ========== GRADIENT TEXT EFFECTS ========== */
.gradient-text {{
    background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 50%, #38BDF8 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 700 !important;
}}

/* ========== DATAFRAME SPECIFIC ENHANCEMENTS ========== */
/* Ensure proper contrast and readability */
.dataframe tr:nth-child(odd) {{
    background: rgba(245, 243, 255, 0.4) !important;
}}

.dataframe tr:nth-child(even) {{
    background: rgba(255, 255, 255, 0.6) !important;
}}

/* Hover effect for better interactivity */
.dataframe tr:hover {{
    background: linear-gradient(135deg, 
        rgba(139, 92, 246, 0.08) 0%, 
        rgba(124, 58, 237, 0.08) 50%, 
        rgba(236, 72, 153, 0.05) 100%) !important;
}}

/* Cell hover effects */
.dataframe td:hover {{
    background: rgba(139, 92, 246, 0.05) !important;
    box-shadow: inset 0 0 0 2px rgba(139, 92, 246, 0.1) !important;
}}

/* Header cell enhancements */
.dataframe th:first-child {{
    border-radius: 20px 0 0 0 !important;
}}

.dataframe th:last-child {{
    border-radius: 0 20px 0 0 !important;
}}

/* Last row styling */
.dataframe tr:last-child td:first-child {{
    border-radius: 0 0 0 20px !important;
}}

.dataframe tr:last-child td:last-child {{
    border-radius: 0 0 20px 0 !important;
}}

/* Cell content alignment */
.dataframe td:first-child {{
    font-weight: 600 !important;
    color: #7C3AED !important;
}}

/* Numerical cells styling */
.dataframe td:contains('%'),
.dataframe td:contains('$'),
.dataframe td:contains('.') {{
    font-family: 'Inter', monospace !important;
    font-weight: 600 !important;
    color: #1F2937 !important;
}}

/* Status indicators in cells */
.dataframe td:contains('Critical'),
.dataframe td:contains('High') {{
    color: #EF4444 !important;
    font-weight: 700 !important;
    position: relative !important;
}}

.dataframe td:contains('Critical')::after,
.dataframe td:contains('High')::after {{
    content: ' 🔥' !important;
}}

.dataframe td:contains('Medium') {{
    color: #F59E0B !important;
    font-weight: 600 !important;
}}

.dataframe td:contains('Low') {{
    color: #10B981 !important;
    font-weight: 600 !important;
}}

.dataframe td:contains('Low')::after {{
    content: ' ✅' !important;
}}
</style>
""", unsafe_allow_html=True)



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
    """Simple heatmap with guaranteed annotations"""
    if 'heatmap' not in st.session_state.dashboard_data:
        return None
    
    heatmap_data = st.session_state.dashboard_data['heatmap']
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Create text matrix for annotations
    text_matrix = []
    for row in risk_matrix:
        text_row = []
        for val in row:
            if val > 70:
                text_row.append(f'🔥<br><b style="color:white">{val:.0f}%</b>')
            elif val > 50:
                text_row.append(f'⚠️<br><b style="color:white">{val:.0f}%</b>')
            else:
                text_row.append(f'<b>{val:.0f}%</b>')
        text_matrix.append(text_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        text=text_matrix,
        texttemplate="%{text}",
        textfont={"size": 10},
        colorscale=[
            [0, '#F5F3FF'],
            [0.5, '#8B5CF6'],
            [1, '#EC4899']
        ],
        hoverinfo="x+y+z+text",
        hovertemplate=(
            "<b>%{y} ↔ %{x}</b><br>"
            "Risk: <b>%{z}%</b><br>"
            "<extra></extra>"
        )
    ))
    
    fig.update_layout(
        title="Drug Confusion Heatmap",
        height=500,
        xaxis_tickangle=-45
    )
    
    return fig


def create_risk_breakdown_chart():
    """Create modern risk breakdown donut chart - UPDATED VERSION"""
    if 'breakdown' not in st.session_state.dashboard_data:
        return None
    
    breakdown = st.session_state.dashboard_data['breakdown']
    if not breakdown:
        return None
    
    categories = [item['category'].title() for item in breakdown]
    counts = [item['count'] for item in breakdown]
    
    # Modern purple theme colors
    colors = [
        '#EC4899',  # Pink (Critical) - matches your gradient_purple_pink
        '#8B5CF6',  # Purple (High)
        '#7C3AED',  # Dark Purple (Medium)
        '#A78BFA'   # Light Purple (Low)
    ]
    
    # Icon mapping for each risk category
    icons = {
        'Critical': '🔥',
        'High': '⚠️',
        'Medium': '🔔',
        'Low': '✅'
    }
    
    # Add icons to labels
    labels_with_icons = [f"{icons.get(cat, '')} {cat}" for cat in categories]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels_with_icons,
        values=counts,
        hole=0.6,  # Larger hole for more modern look
        marker=dict(
            colors=colors,
            line=dict(color='white', width=3),
            pattern=dict(
                shape="",  # Can add patterns if needed
                solidity=0.7
            )
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(
            color=COLORS['text_primary'], 
            size=13, 
            family='Inter',
            weight='500'
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Count: %{value}<br>"
            "Percentage: %{percent}<br>"
            "<extra></extra>"
        ),
        pull=[0.05, 0.03, 0.02, 0.01],  # Subtle pull effect
        rotation=45,
        direction='clockwise',
        sort=False
    )])
    
    # Add center text for modern donut chart
    total = sum(counts)
    fig.add_annotation(
        text=f"<b>📊 Total<br>{total}</b>",
        x=0.5,
        y=0.5,
        font=dict(
            size=22,
            color=COLORS['text_primary'],
            family="Inter",
            weight="bold"
        ),
        showarrow=False,
        align="center"
    )
    
    fig.update_layout(
        title=dict(
            text="📈 Risk Distribution Analysis",
            font=dict(
                color=COLORS['text_primary'], 
                size=20, 
                family="Inter",
                weight="800"
            ),
            x=0.5,
            xanchor="center",
            y=0.98,
            yanchor="top",
            pad=dict(t=0, b=20)
        ),
        height=450,
        showlegend=True,
        # Glassmorphism background
        plot_bgcolor='rgba(245, 243, 255, 0.3)',
        paper_bgcolor='rgba(245, 243, 255, 0.2)',
        font_color=COLORS['text_primary'],
        legend=dict(
            font=dict(
                size=12, 
                color=COLORS['text_secondary'], 
                family="Inter",
                weight="500"
            ),
            bgcolor='rgba(255, 255, 255, 0.7)',
            bordercolor=COLORS['border'],
            borderwidth=1.5,
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            itemclick="toggleothers",
            itemdoubleclick="toggle"
        ),
        margin=dict(l=20, r=20, t=60, b=80),
        hoverlabel=dict(
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor=COLORS['primary'],
            font_size=12,
            font_family="Inter"
        ),
        uniformtext=dict(
            minsize=12,
            mode='hide'
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
    
    # Modern gradient colors matching your theme
    colors = ['#EF4444', '#F59E0B', '#8B5CF6', '#10B981']
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=counts,
        hole=0.5,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        hoverinfo='label+value+percent',
        textfont=dict(
            color=COLORS['text_primary'], 
            size=12, 
            family='Inter'
        ),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
        pull=[0.02, 0.02, 0.02, 0.02]
    )])
    
    fig.update_layout(
        title=dict(
            text="Risk Distribution",
            font=dict(
                color=COLORS['text_primary'], 
                size=16, 
                family="Inter"
            ),
            x=0.5,
            xanchor="center"
        ),
        height=400,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        legend=dict(
            font=dict(size=12, color=COLORS['text_secondary'], family="Inter"),
            bgcolor='white',
            bordercolor=COLORS['border'],
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_top_risks_chart():
    """Create top risks chart with vertical bars - IMPROVED VERSION"""
    if 'top_risks' not in st.session_state.dashboard_data:
        return None
    
    top_risks = st.session_state.dashboard_data['top_risks']
    if not top_risks:
        return None
    
    # Get top 10 pairs
    top_risks = top_risks[:10]
    
    pairs = [f"{item['drug1']} ↔ {item['drug2']}" for item in top_risks]
    scores = [item['risk_score'] for item in top_risks]
    
    # Create colors based on risk score
    colors = []
    for score in scores:
        if score >= 75:
            colors.append('#EF4444')  # Critical
        elif score >= 50:
            colors.append('#F59E0B')  # High
        elif score >= 25:
            colors.append('#8B5CF6')  # Medium
        else:
            colors.append('#10B981')  # Low
    
    # Calculate maximum score for dynamic scaling
    max_score = max(scores) if scores else 100
    y_axis_max = max_score * 1.15  # Add 15% padding at the top
    
    fig = go.Figure(data=[
        go.Bar(
            x=pairs,
            y=scores,
            marker_color=colors,
            text=[f"{score:.1f}%" for score in scores],
            textposition='outside',
            textfont=dict(
                size=11, 
                color=COLORS['text_primary'], 
                family="Inter",
                weight='bold'
            ),
            hovertemplate="<b>%{x}</b><br>Risk Score: <b>%{y:.1f}%</b><extra></extra>",
            width=0.7,  # WIDER BARS
            marker=dict(
                line=dict(width=2, color='white')
            )
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Top 10 High-Risk Drug Pairs",
            font=dict(
                color=COLORS['text_primary'], 
                size=18, 
                family="Inter",
                weight='bold'
            ),
            x=0.5,
            xanchor="center",
            y=0.95,
            yanchor="top"
        ),
        xaxis=dict(
            title=dict(
                text="Drug Pairs",
                font=dict(
                    size=12, 
                    color=COLORS['text_secondary'], 
                    family="Inter",
                    weight='bold'
                )
            ),
            tickfont=dict(
                size=10, 
                color=COLORS['text_secondary'], 
                family="Inter"
            ),
            tickangle=-30,  # Rotate for better readability
            showgrid=False,
            automargin=True,  # Auto-adjust margins
            tickmode='array',
            tickvals=list(range(len(pairs))),
            ticktext=pairs
        ),
        yaxis=dict(
            title=dict(
                text="Risk Score (%)",
                font=dict(
                    size=12, 
                    color=COLORS['text_secondary'], 
                    family="Inter",
                    weight='bold'
                )
            ),
            tickfont=dict(
                size=10, 
                color=COLORS['text_secondary'], 
                family="Inter"
            ),
            range=[0, y_axis_max],
            showgrid=True,
            gridcolor='rgba(139, 92, 246, 0.1)',
            zeroline=False
        ),
        height=450,  # Increased height for better visibility
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        margin=dict(l=80, r=50, t=80, b=150),  # Increased bottom margin for rotated labels
        hovermode='closest',
        bargap=0.2  # Gap between bars
    )
    
    # Add horizontal threshold lines
    fig.add_hline(
        y=75,
        line_dash="dash",
        line_color="#EF4444",
        line_width=1,
        opacity=0.3,
        annotation_text="Critical",
        annotation_position="right",
        annotation_font_size=10,
        annotation_font_color="#EF4444"
    )
    
    fig.add_hline(
        y=50,
        line_dash="dot",
        line_color="#F59E0B",
        line_width=1,
        opacity=0.3,
        annotation_text="High",
        annotation_position="right",
        annotation_font_size=10,
        annotation_font_color="#F59E0B"
    )
    
    return fig

# ================================
# UI COMPONENTS
# ================================

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
    """Render modern user guide section with Font Awesome icons"""
    
    st.markdown("""
    <div class="modern-guide-container">
        <div class="modern-guide-header">
            <div class="modern-guide-title-wrapper">
                <i class="fas fa-graduation-cap guide-main-icon"></i>
                <h2 class="modern-guide-title">User Guide & Expert Tips</h2>
            </div>
            <p class="modern-guide-subtitle">Follow these steps to maximize your experience with MediNomix</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Step 1
    st.markdown("""
    <div class="modern-guide-step">
        <div class="modern-step-number">01</div>
        <div class="modern-step-content">
            <div class="modern-step-icon-wrapper">
                <i class="fas fa-search step-icon"></i>
            </div>
            <div class="modern-step-details">
                <h3 class="modern-step-title">Search for a Medication</h3>
                <ul class="modern-step-list">
                    <li><i class="fas fa-chevron-right list-icon"></i> Navigate to the <span class="highlight-text">Drug Analysis</span> tab</li>
                    <li><i class="fas fa-chevron-right list-icon"></i> Enter any medication name (brand or generic)</li>
                    <li><i class="fas fa-chevron-right list-icon"></i> Click <span class="highlight-button">Analyze Drug</span> to start AI analysis</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 2
    st.markdown("""
    <div class="modern-guide-step">
        <div class="modern-step-number">02</div>
        <div class="modern-step-content">
            <div class="modern-step-icon-wrapper">
                <i class="fas fa-chart-line step-icon"></i>
            </div>
            <div class="modern-step-details">
                <h3 class="modern-step-title">Review Risk Assessment</h3>
                <ul class="modern-step-list">
                    <li><i class="fas fa-chevron-right list-icon"></i> View all similar drugs with confusion risks</li>
                    <li><i class="fas fa-chevron-right list-icon"></i> Filter by risk level (Critical, High, Medium, Low)</li>
                    <li><i class="fas fa-chevron-right list-icon"></i> Examine detailed similarity metrics</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 3
    st.markdown("""
    <div class="modern-guide-step">
        <div class="modern-step-number">03</div>
        <div class="modern-step-content">
            <div class="modern-step-icon-wrapper">
                <i class="fas fa-shield-alt step-icon"></i>
            </div>
            <div class="modern-step-details">
                <h3 class="modern-step-title">Take Preventive Action</h3>
                <ul class="modern-step-list">
                    <li><i class="fas fa-chevron-right list-icon"></i> Check <span class="highlight-text">Analytics</span> tab for statistics</li>
                    <li><i class="fas fa-chevron-right list-icon"></i> Monitor <span class="highlight-text">Real-Time</span> dashboard</li>
                    <li><i class="fas fa-chevron-right list-icon"></i> Use quick examples for demonstration</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- Pro Tips Section -->
    <div class="modern-pro-tips">
        <div class="pro-tips-header">
            <div class="pro-tips-icon-wrapper">
                <i class="fas fa-lightbulb pro-tips-icon"></i>
            </div>
            <h3 class="pro-tips-title">Professional Tips & Best Practices</h3>
        </div>
        <div class="pro-tips-content">
            <div class="pro-tip-item">
                <i class="fas fa-check-circle tip-icon"></i>
                <div class="tip-text">
                    <strong>Double-Verify Medication Names</strong>
                    <p>Always cross-check drug names before administration to prevent errors</p>
                </div>
            </div>
            <div class="pro-tip-item">
                <i class="fas fa-text-height tip-icon"></i>
                <div class="tip-text">
                    <strong>Use Tall Man Lettering</strong>
                    <p>Implement Tall Man lettering for look-alike drug names (e.g., DOPamine vs DOButamine)</p>
                </div>
            </div>
            <div class="pro-tip-item">
                <i class="fas fa-clipboard-list tip-icon"></i>
                <div class="tip-text">
                    <strong>Consult FDA High-Alert List</strong>
                    <p>Regularly review FDA's high-alert drug list for updated safety guidelines</p>
                </div>
            </div>
            <div class="pro-tip-item">
                <i class="fas fa-bell tip-icon"></i>
                <div class="tip-text">
                    <strong>Report Safety Incidents</strong>
                    <p>Document and report any confusion incidents through your institution's safety system</p>
                </div>
            </div>
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
        <div style="position: relative; z-index: 10;">
            <h1 class="hero-title">
                <i class="fas fa-capsules hero-icon"></i> MediNomix
            </h1>
            <p class="hero-subtitle">Advanced system that analyzes drug names for potential confusion risks, helping healthcare professionals prevent medication errors and improve patient safety.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# DRUG ANALYSIS TAB
# ================================

def render_drug_analysis_tab():
    """Render Drug Analysis tab"""
    
    render_glass_card(
        "Drug Confusion Risk Analysis",
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
        search_clicked = st.button("Analyze Drug", type="primary", use_container_width=True)
    
    with col3:
        if st.button("Load Examples", type="secondary", use_container_width=True):
            with st.spinner("Loading examples..."):
                if load_examples():
                    render_alert_card("Examples loaded successfully! Try searching: lamictal, celebrex, metformin", "success")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Examples with Images
    st.markdown("""
    <div style="margin: 24px 0;">
        <h3 style="color: #111827; margin-bottom: 16px; font-weight: 700;">✨ Quick Examples:</h3>
    </div>
    """, unsafe_allow_html=True)
    
    examples = ["Lamictal", "Metformin", "Celebrex", "Clonidine"]
    example_images = [
        "https://www.shutterstock.com/image-photo/lamotrigine-drug-prescription-medication-pills-260nw-2168515791.jpg",
        "https://t3.ftcdn.net/jpg/05/99/37/68/360_F_599376857_qFxGlExvZ576RG5CyNFajllibkCF7TAZ.jpg",
        "https://www.verywellhealth.com/thmb/6DChoTv1r2NyRc4HmOHvv46uO3A=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/VWH.GettyImages-471365176-dcb658055f7540a788a3382a0628ea32.jpg",
        "https://t4.ftcdn.net/jpg/06/00/08/53/360_F_600085338_S9G1HlJKiZpSKKTLZKaoa6Y8l752W8M6.jpg"
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
                        render_alert_card(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.", "success")
                        st.rerun()
    
    # Handle Search
    if search_clicked and drug_name:
        with st.spinner(f"🧠 Analyzing '{drug_name}'..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                render_alert_card(f"✅ Analysis complete! Found {len(st.session_state.search_results)} similar drugs.", "success")
                st.rerun()
            else:
                render_alert_card("❌ Could not analyze drug. Please check backend connection.", "danger")
    
    # Results Section
    if st.session_state.search_results:
        st.markdown("""
        <div style="margin-top: 40px;">
            <h2 style="color: #111827; margin-bottom: 24px; font-weight: 700;">Analysis Results</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Filters
        risk_filters = st.radio(
            " Filter by risk level:",
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
                        <h3 style="margin: 0 0 8px 0; color: #111827; font-weight: 700; font-size: 18px;">{result['target_drug']['brand_name']}</h3>
                        {f"<p style='margin: 0 0 12px 0; color: #4B5563; font-size: 14px; font-weight: 500;'>Generic: {result['target_drug']['generic_name']}</p>" if result['target_drug']['generic_name'] else ""}
                    </div>
                    <div style="text-align: center; min-width: 100px;">
                        <div style="font-size: 32px; font-weight: 800; color: {COLORS['primary']}; margin-bottom: 8px;">
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
    
    # Modern Dashboard Header Card
    st.markdown(f"""
    <div class="modern-dashboard-header">
        <div class="dashboard-header-content">
            <div class="dashboard-icon">
                <i class="fas fa-chart-line"></i>
            </div>
            <div>
                <h1 class="dashboard-title">Medication Safety Analytics Dashboard</h1>
                <p class="dashboard-subtitle">Real-time insights and analytics for medication safety monitoring</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data if needed
    if 'metrics' not in st.session_state.dashboard_data:
        with st.spinner("Loading analytics data..."):
            load_dashboard_data()
    
    # KPI Cards - Modern Version
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="dashboard-card">
                <div class="card-icon-wrapper" style="background: rgba(16, 185, 129, 0.1); border: 2px solid rgba(16, 185, 129, 0.2);">
                    <i class="fas fa-pills" style="color: #10B981;"></i>
                </div>
                <div class="card-value">{metrics.get('total_drugs', 0)}</div>
                <div class="card-label">Total Drugs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="dashboard-card">
                <div class="card-icon-wrapper" style="background: rgba(239, 68, 68, 0.1); border: 2px solid rgba(239, 68, 68, 0.2);">
                    <i class="fas fa-fire" style="color: #EF4444;"></i>
                </div>
                <div class="card-value">{metrics.get('critical_risk_pairs', 0)}</div>
                <div class="card-label">Critical Pairs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="dashboard-card">
                <div class="card-icon-wrapper" style="background: rgba(245, 158, 11, 0.1); border: 2px solid rgba(245, 158, 11, 0.2);">
                    <i class="fas fa-exclamation-triangle" style="color: #F59E0B;"></i>
                </div>
                <div class="card-value">{metrics.get('high_risk_pairs', 0)}</div>
                <div class="card-label">High Risk Pairs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="dashboard-card">
                <div class="card-icon-wrapper" style="background: rgba(139, 92, 246, 0.1); border: 2px solid rgba(139, 92, 246, 0.2);">
                    <i class="fas fa-chart-line" style="color: #8B5CF6;"></i>
                </div>
                <div class="card-value">{metrics.get('avg_risk_score', 0):.1f}%</div>
                <div class="card-label">Avg Risk Score</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Analytics Charts Section - NOW IN SEPARATE ROWS
    st.markdown("""
    <div class="dashboard-section-card">
        <div class="section-header">
            <div class="section-icon">
                <i class="fas fa-chart-pie"></i>
            </div>
            <div>
                <h2 class="section-title">Analytics Charts</h2>
                <p class="section-subtitle">Visual insights into medication confusion risks</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ================================================
    # ROW 1: Risk Distribution Chart (FULL WIDTH)
    # ================================================
    #st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-title-wrapper">
        <i class="fas fa-chart-pie chart-title-icon" style="color: #8B5CF6;"></i>
        <h3 class="chart-title">Risk Distribution Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    breakdown_chart = create_risk_breakdown_chart()
    if breakdown_chart:
        st.plotly_chart(breakdown_chart, use_container_width=True)
    else:
        st.markdown("""
        <div class="data-placeholder">
            <i class="fas fa-database" style="color: #9CA3AF;"></i>
            <p>No risk breakdown data available</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ================================================
    # ROW 2: Top Risks Chart (FULL WIDTH)
    # ================================================
    #st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-title-wrapper">
        <i class="fas fa-chart-bar chart-title-icon" style="color: #EC4899;"></i>
        <h3 class="chart-title">Top 10 High-Risk Drug Pairs</h3>
    </div>
    """, unsafe_allow_html=True)
    
    risks_chart = create_top_risks_chart()
    if risks_chart:
        st.plotly_chart(risks_chart, use_container_width=True)
    else:
        st.markdown("""
        <div class="data-placeholder">
            <i class="fas fa-database" style="color: #9CA3AF;"></i>
            <p>No top risk data available</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ================================================
    # Heatmap Section
    # ================================================
    
    # ================================================
# Heatmap Section - UPDATED WITH GLASS EFFECT
# ================================================
    st.markdown("""
    <div class="dashboard-section-card">
        <div class="section-header">
            <div class="section-icon">
                <i class="fas fa-th-large"></i>
            </div>
            <div>
                <h2 class="section-title">Drug Confusion Risk Heatmap</h2>
                <p class="section-subtitle">Visual matrix of potential drug confusion risks</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ADD THE CSS STYLES HERE
    st.markdown("""
    <style>
    .heatmap-glass-container {
        background: linear-gradient(135deg, 
            rgba(245, 243, 255, 0.85) 0%, 
            rgba(255, 255, 255, 0.95) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0 25px 0;
        border: 1.5px solid rgba(139, 92, 246, 0.25);
        box-shadow: 
            0 12px 40px rgba(139, 92, 246, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8),
            inset 0 -1px 0 rgba(139, 92, 246, 0.1);
        position: relative;
        overflow: hidden;
    }

    .heatmap-glass-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            #8B5CF6 0%, 
            #7C3AED 33%, 
            #EC4899 66%, 
            #F472B6 100%);
        border-radius: 20px 20px 0 0;
    }

    .modern-heatmap-title {
        font-size: 20px;
        font-weight: 800;
        color: transparent;
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
        text-align: center;
        letter-spacing: -0.01em;
        font-family: 'Inter', sans-serif;
    }

    .heatmap-legend-modern {
        display: flex;
        justify-content: center;
        gap: 24px;
        margin-top: 25px;
        padding-top: 20px;
        border-top: 1.5px solid rgba(139, 92, 246, 0.15);
        flex-wrap: wrap;
    }

    .legend-item-modern {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #4B5563;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 8px 16px;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.1);
        transition: all 0.3s ease;
    }

    .legend-item-modern:hover {
        background: white;
        border-color: rgba(139, 92, 246, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1);
    }

    .legend-color-modern {
        width: 18px;
        height: 18px;
        border-radius: 5px;
        border: 2px solid white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .data-placeholder-modern {
        text-align: center;
        padding: 60px 30px;
        color: #6B7280;
        background: rgba(249, 250, 251, 0.8);
        border-radius: 16px;
        border: 2px dashed rgba(139, 92, 246, 0.2);
        margin: 20px 0;
        font-family: 'Inter', sans-serif;
    }

    .data-placeholder-modern i {
        font-size: 48px;
        margin-bottom: 16px;
        color: #8B5CF6;
        opacity: 0.7;
    }

    .data-placeholder-modern p {
        margin: 0;
        font-weight: 500;
        font-size: 15px;
        max-width: 400px;
        margin: 0 auto;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)
    

    # WRAP THE HEATMAP IN THE GLASS CONTAINER
    #st.markdown('<div class="heatmap-glass-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="modern-heatmap-title">🔄 Drug Similarity Risk Matrix</h3>', unsafe_allow_html=True)

    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(
            heatmap_chart, 
            use_container_width=True, 
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'drug_confusion_heatmap',
                    'height': 600,
                    'width': 800,
                    'scale': 2
                }
            }
        )

        # Modern legend matching the new color scheme
        st.markdown(f"""
        <div class="heatmap-legend-modern">
            <div class="legend-item-modern">
                <div class="legend-color-modern" style="background: linear-gradient(135deg, #F5F3FF 0%, #DDD6FE 100%);"></div>
                <span>Low Risk (0-25%)</span>
            </div>
            <div class="legend-item-modern">
                <div class="legend-color-modern" style="background: #8B5CF6;"></div>
                <span>Medium (26-50%)</span>
            </div>
            <div class="legend-item-modern">
                <div class="legend-color-modern" style="background: #7C3AED;"></div>
                <span>High (51-75%)</span>
            </div>
            <div class="legend-item-modern">
                <div class="legend-color-modern" style="background: #EC4899;"></div>
                <span>Critical (76-100%)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Add helpful note
        st.markdown("""
        <div style="text-align: center; margin-top: 15px;">
            <p style="color: #6B7280; font-size: 13px; font-weight: 500;">
                <i class="fas fa-lightbulb" style="color: #F59E0B; margin-right: 6px;"></i>
                <strong>Tip:</strong> Hover over cells to see detailed risk percentages. Cells with 🔥 indicate critical risks.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="data-placeholder-modern">
            <i class="fas fa-heartbeat"></i>
            <p>No heatmap data available yet.<br>Search for medications in the <strong>Drug Analysis</strong> tab first.</p>
            <div style="margin-top: 15px;">
                <div style="display: inline-flex; gap: 10px; margin-top: 10px;">
                    <span style="background: rgba(139, 92, 246, 0.1); color: #8B5CF6; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 600;">Try: Lamictal</span>
                    <span style="background: rgba(139, 92, 246, 0.1); color: #8B5CF6; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 600;">Try: Metformin</span>
                    <span style="background: rgba(139, 92, 246, 0.1); color: #8B5CF6; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 600;">Try: Celebrex</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    
    # ================================================
    # FDA Alerts Section
    # ================================================
    st.markdown("""
    <div class="dashboard-section-card">
        <div class="section-header">
            <div class="section-icon">
                <i class="fas fa-exclamation-circle"></i>
            </div>
            <div>
                <h2 class="section-title">FDA High Alert Drug Pairs</h2>
                <p class="section-subtitle">Most commonly confused drug pairs according to FDA</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", "Reason": "Epilepsy medication vs Antifungal"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", "Reason": "Arthritis vs Depression medication"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", "Reason": "Diabetes vs Antibiotic"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", "Reason": "Blood Pressure vs Anxiety medication"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", "Reason": "Antipsychotic vs Allergy medication"},
    ])
    
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Drug 1": st.column_config.TextColumn("💊 Drug 1", width="medium"),
            "Drug 2": st.column_config.TextColumn("💊 Drug 2", width="medium"),
            "Risk Level": st.column_config.TextColumn("⚠️ Risk Level", width="small"),
            "Reason": st.column_config.TextColumn("📝 Reason", width="large")
        }
    )
    
    
    # ================================================
    # CSS Styles (keep this at the end of the function)
    # ================================================
    st.markdown(f"""
    <style>
    /* Modern Dashboard Header */
    .modern-dashboard-header {{
        background: linear-gradient(135deg, #F8F5FF 0%, #F3EFFF 100%);
        padding: 32px;
        border-radius: 24px;
        border: 2px solid #D6BCFA;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15);
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }}
    
    .modern-dashboard-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%);
    }}
    
    .dashboard-header-content {{
        display: flex;
        align-items: center;
        gap: 24px;
    }}
    
    .dashboard-icon {{
        font-size: 48px;
        color: #7C3AED;
        background: rgba(139, 92, 246, 0.1);
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        border: 2px solid rgba(139, 92, 246, 0.2);
    }}
    
    .dashboard-title {{
        margin: 0;
        color: #1F2937;
        font-weight: 800;
        font-size: 28px;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .dashboard-subtitle {{
        color: #6B7280;
        margin: 8px 0 0 0;
        font-size: 16px;
        font-weight: 500;
    }}
    
    /* Dashboard Cards */
    .dashboard-card {{
        background: linear-gradient(135deg, #F8F5FF 0%, #F3EFFF 100%);
        padding: 24px;
        border-radius: 20px;
        border: 2px solid #D6BCFA;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.1);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-6px);
        border-color: #A78BFA;
        box-shadow: 0 16px 48px rgba(139, 92, 246, 0.2);
    }}
    
    .card-icon-wrapper {{
        width: 64px;
        height: 64px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
    }}
    
    .card-icon-wrapper i {{
        font-size: 28px;
    }}
    
    .card-value {{
        font-size: 32px;
        font-weight: 800;
        color: #1F2937;
        margin: 8px 0;
    }}
    
    .card-label {{
        color: #6B7280;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    
    /* Section Cards */
    .dashboard-section-card {{
        background: linear-gradient(135deg, #F8F5FF 0%, #F3EFFF 100%);
        padding: 32px;
        border-radius: 24px;
        border: 2px solid #D6BCFA;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.1);
        margin-bottom: 32px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .dashboard-section-card:hover {{
        border-color: #A78BFA;
        box-shadow: 0 16px 48px rgba(139, 92, 246, 0.15);
    }}
    
    .section-header {{
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 32px;
    }}
    
    .section-icon {{
        font-size: 36px;
        color: #7C3AED;
        background: rgba(139, 92, 246, 0.1);
        width: 64px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        border: 2px solid rgba(139, 92, 246, 0.2);
    }}
    
    .section-title {{
        margin: 0;
        color: #1F2937;
        font-weight: 800;
        font-size: 24px;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .section-subtitle {{
        color: #6B7280;
        margin: 6px 0 0 0;
        font-size: 14px;
        font-weight: 500;
    }}
    
    /* Chart Wrapper - UPDATED FOR SEPARATE ROWS */
    .chart-wrapper {{
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 2px solid #E5E7EB;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        margin-bottom: 24px;  /* Space between rows */
        width: 100%;
    }}
    
    .chart-title-wrapper {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }}
    
    .chart-title-icon {{
        font-size: 24px;
        background: #F9FAFB;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        border: 2px solid #E5E7EB;
    }}
    
    .chart-title {{
        margin: 0;
        color: #1F2937;
        font-weight: 700;
        font-size: 18px;
    }}
    
    /* Data Placeholder */
    .data-placeholder {{
        text-align: center;
        padding: 60px 20px;
        color: #6B7280;
        background: #F9FAFB;
        border-radius: 12px;
        border: 2px dashed #E5E7EB;
        margin-top: 10px;
    }}
    
    .data-placeholder i {{
        font-size: 48px;
        margin-bottom: 16px;
        color: #9CA3AF;
    }}
    
    .data-placeholder p {{
        margin: 0;
        font-weight: 500;
        font-size: 14px;
    }}
    
    /* Heatmap Legend */
    .heatmap-legend {{
        display: flex;
        justify-content: center;
        gap: 32px;
        margin-top: 24px;
        padding-top: 24px;
        border-top: 2px solid #E5E7EB;
    }}
    
    .legend-item {{
        display: flex;
        align-items: center;
        gap: 8px;
        color: #4B5563;
        font-size: 13px;
        font-weight: 600;
    }}
    
    .legend-color {{
        width: 16px;
        height: 16px;
        border-radius: 4px;
        border: 2px solid white;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# ================================
# REAL-TIME DASHBOARD TAB
# ================================
def render_realtime_tab():
    """PROFESSIONAL REAL-TIME DASHBOARD WITH MODERN UI"""
    
    # ====================================
    # AUTO-REFRESH MECHANISM (NO CHANGE)
    # ====================================
    import time
    from datetime import datetime
    
    if 'refresh_counter' not in st.session_state:
        st.session_state.refresh_counter = 0
        st.session_state.last_refresh_time = time.time()
    
    current_time = time.time()
    time_since_refresh = current_time - st.session_state.last_refresh_time
    
    refresh_interval = 10
    if time_since_refresh > refresh_interval:
        st.session_state.refresh_counter += 1
        st.session_state.last_refresh_time = current_time
        st.rerun()
    
    seconds_until_refresh = refresh_interval - int(time_since_refresh)
    
    # ====================================
    # MODERN DASHBOARD UI
    # ====================================
    
    # Modern Header Card
    st.markdown(f"""
    <div class="realtime-header-card">
        <div class="realtime-header-content">
            <div class="realtime-main-icon">
                <i class="fas fa-bolt"></i>
            </div>
            <div>
                <h1 class="realtime-title">Real-Time Medication Safety Dashboard</h1>
                <p class="realtime-subtitle">
                    <i class="fas fa-sync-alt"></i> Auto-refreshes every {refresh_interval} seconds 
                    • <i class="fas fa-clock"></i> Last refresh: {datetime.now().strftime('%H:%M:%S')}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    


    # Live Status Banner with Modern Design
    st.markdown(f"""
    <div class="live-status-banner">
        <div class="status-indicator">
            <i class="fas fa-circle" style="animation: pulse 2s infinite; color: #11d1c1;"></i>
            <span class="status-text">LIVE UPDATES ACTIVE</span>
        </div>
        <div class="refresh-counter">
            <div class="counter-label">Next refresh in</div>
            <div class="counter-value">{seconds_until_refresh}s</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ====================================
    # FETCH REAL-TIME DATA (NO CHANGE)
    # ====================================
    try:
        response = requests.get(f"{BACKEND_URL}/api/metrics", timeout=5)
        
        if response.status_code == 200:
            metrics = response.json()
            
            # ====================================
            # MODERN METRICS CARDS SECTION
            # ====================================
            st.markdown("""
            <div class="section-header">
                <div class="section-icon">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <h2 class="section-title">Live Metrics</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="modern-metric-card">
                    <div class="metric-icon-container" style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(139, 92, 246, 0.2) 100%);">
                        <i class="fas fa-pills" style="color: #8B5CF6;"></i>
                    </div>
                    <div class="metric-value">{metrics.get('total_drugs', 0)}</div>
                    <div class="metric-label">Total Drugs</div>
                    <div class="metric-trend">
                        <i class="fas fa-arrow-up" style="color: #10B981;"></i>
                        <span style="color: #10B981;">+5%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="modern-metric-card">
                    <div class="metric-icon-container" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.2) 100%);">
                        <i class="fas fa-fire" style="color: #EF4444;"></i>
                    </div>
                    <div class="metric-value">{metrics.get('critical_risk_pairs', 0)}</div>
                    <div class="metric-label">Critical Pairs</div>
                    <div class="metric-trend">
                        <i class="fas fa-arrow-up" style="color: #EF4444;"></i>
                        <span style="color: #EF4444;">+2%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="modern-metric-card">
                    <div class="metric-icon-container" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.2) 100%);">
                        <i class="fas fa-exclamation-triangle" style="color: #F59E0B;"></i>
                    </div>
                    <div class="metric-value">{metrics.get('high_risk_pairs', 0)}</div>
                    <div class="metric-label">High Risk Pairs</div>
                    <div class="metric-trend">
                        <i class="fas fa-minus" style="color: #6B7280;"></i>
                        <span style="color: #6B7280;">0%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="modern-metric-card">
                    <div class="metric-icon-container" style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(56, 189, 248, 0.2) 100%);">
                        <i class="fas fa-chart-line" style="color: #38BDF8;"></i>
                    </div>
                    <div class="metric-value">{metrics.get('avg_risk_score', 0):.1f}%</div>
                    <div class="metric-label">Avg Risk Score</div>
                    <div class="metric-trend">
                        <i class="fas fa-arrow-down" style="color: #10B981;"></i>
                        <span style="color: #10B981;">-1.2%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # ====================================
            # MODERN RECENT ACTIVITY SECTION
            # ====================================
            st.markdown("""
            <div class="section-header" style="margin-top: 40px;">
                <div class="section-icon">
                    <i class="fas fa-history"></i>
                </div>
                <h2 class="section-title">Recent Activity</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if metrics.get('recent_searches'):
                for idx, search in enumerate(metrics['recent_searches'][:8]):
                    risk_score = search.get('highest_risk', 0)
                    
                    # Determine risk level and colors
                    if risk_score > 70:
                        risk_icon = "fas fa-fire"
                        risk_color = "#EF4444"
                        bg_color = "rgba(239, 68, 68, 0.1)"
                    elif risk_score > 50:
                        risk_icon = "fas fa-exclamation-triangle"
                        risk_color = "#F59E0B"
                        bg_color = "rgba(245, 158, 11, 0.1)"
                    else:
                        risk_icon = "fas fa-check-circle"
                        risk_color = "#10B981"
                        bg_color = "rgba(16, 185, 129, 0.1)"
                    
                    st.markdown(f"""
                    <div class="activity-card">
                        <div class="activity-icon">
                            <i class="fas fa-search" style="color: #8B5CF6;"></i>
                        </div>
                        <div class="activity-content">
                            <div class="activity-header">
                                <span class="activity-title">{search.get('drug_name', 'Unknown')}</span>
                                <span class="activity-badge" style="background: {bg_color}; color: {risk_color};">
                                    <i class="{risk_icon}"></i> {risk_score:.1f}% Risk
                                </span>
                            </div>
                            <div class="activity-details">
                                <span><i class="fas fa-capsules"></i> {search.get('similar_drugs_found', 0)} similar drugs found</span>
                                <span><i class="fas fa-clock"></i> {search.get('timestamp', '')[:19]}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if idx < len(metrics['recent_searches'][:8]) - 1:
                        st.markdown('<div class="activity-divider"></div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">
                        <i class="fas fa-search" style="color: #9CA3AF;"></i>
                    </div>
                    <h3 class="empty-state-title">No Recent Searches</h3>
                    <p class="empty-state-description">Search for medications to see activity here</p>
                </div>
                """, unsafe_allow_html=True)
            
            # ====================================
            # MODERN SYSTEM STATUS SECTION
            # ====================================
            st.markdown("""
            <div class="section-header" style="margin-top: 40px;">
                <div class="section-icon">
                    <i class="fas fa-server"></i>
                </div>
                <h2 class="section-title">System Status</h2>
            </div>
            """, unsafe_allow_html=True)
            
            status_col1, status_col2, status_col3 = st.columns(3)
            
            with status_col1:
                st.markdown(f"""
                <div class="status-card">
                    <div class="status-icon">
                        <i class="fas fa-users" style="color: #8B5CF6;"></i>
                    </div>
                    <div class="status-content">
                        <div class="status-value">{metrics.get('connected_clients', 0)}</div>
                        <div class="status-label">Connected Clients</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with status_col2:
                st.markdown(f"""
                <div class="status-card">
                    <div class="status-icon">
                        <i class="fas fa-chart-line" style="color: #10B981;"></i>
                    </div>
                    <div class="status-content">
                        <div class="status-value">{metrics.get('total_analyses', 0)}</div>
                        <div class="status-label">Total Analyses</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with status_col3:
                system_status = metrics.get('system_status', 'unknown')
                if system_status == 'healthy':
                    status_icon = "fas fa-check-circle"
                    status_color = "#1BC5C8"
                    status_text = "Healthy"
                else:
                    status_icon = "fas fa-exclamation-triangle"
                    status_color = "#F59E0B"
                    status_text = "Warning"
                
                st.markdown(f"""
                <div class="status-card">
                    <div class="status-icon">
                        <i class="{status_icon}" style="color: {status_color};"></i>
                    </div>
                    <div class="status-content">
                        <div class="status-value" style="color: {status_color};">{status_text}</div>
                        <div class="status-label">System Health</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        else:
            # Error State
            st.markdown("""
            <div class="error-state">
                <div class="error-icon">
                    <i class="fas fa-exclamation-circle" style="color: #EF4444;"></i>
                </div>
                <h3 class="error-title">Backend Connection Failed</h3>
                <p class="error-description">Make sure backend is running on http://localhost:8000</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.code("python backend.py", language="bash")
    
    except Exception as e:
        # Connection Error
        st.markdown(f"""
        <div class="error-state">
            <div class="error-icon">
                <i class="fas fa-plug" style="color: #EF4444;"></i>
            </div>
            <h3 class="error-title">Connection Error</h3>
            <p class="error-description">{str(e)[:100]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ====================================
    # MODERN MANUAL CONTROLS SECTION
    # ====================================
    st.markdown("""
    <div class="controls-section">
        <div class="section-header">
            <div class="section-icon">
                <i class="fas fa-cogs"></i>
            </div>
            <h2 class="section-title">Dashboard Controls</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("""
        <div class="info-card">
            <div class="info-header">
                <i class="fas fa-sync-alt" style="color: #8B5CF6;"></i>
                <h3 class="info-title">Auto-Refresh System</h3>
            </div>
            <div class="info-content">
                <div class="info-item">
                    <i class="fas fa-check-circle" style="color: #10B981;"></i>
                    <span>Page automatically reloads every 10 seconds</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-check-circle" style="color: #10B981;"></i>
                    <span>Fresh data fetched from backend each time</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-check-circle" style="color: #10B981;"></i>
                    <span>No WebSocket needed - works 100% reliably</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-check-circle" style="color: #10B981;"></i>
                    <span>Manual refresh available anytime</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="action-buttons">
            <button class="action-button primary" onclick="refreshNow()">
                <i class="fas fa-sync-alt"></i>
                <span>Refresh Now</span>
            </button>
            <button class="action-button secondary" onclick="seedDatabase()">
                <i class="fas fa-database"></i>
                <span>Seed Database</span>
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        # Actual Streamlit Buttons (hidden but functional)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Refresh Now", type="primary", use_container_width=True, key="refresh_btn"):
                st.session_state.refresh_counter += 1
                st.rerun()
        
        with col_b:
            if st.button("Seed Database", type="secondary", use_container_width=True, key="seed_btn"):
                try:
                    response = requests.post(f"{BACKEND_URL}/api/seed-database", timeout=10)
                    if response.status_code == 200:
                        st.success("✅ Database seeded successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to seed database")
                except:
                    st.error("Could not connect to backend")
    
    
    
    # ====================================
    # MODERN CSS STYLES
    # ====================================
    st.markdown("""
    <style>
    /* Modern Dashboard Header */
    .realtime-header-card {
        background: linear-gradient(135deg, #F8F5FF 0%, #F3EFFF 100%);
        padding: 32px;
        border-radius: 24px;
        border: 2px solid #D6BCFA;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    .realtime-header-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%);
    }
    
    .realtime-header-content {
        display: flex;
        align-items: center;
        gap: 24px;
    }
    
    .realtime-main-icon {
        font-size: 48px;
        color: #7C3AED;
        background: rgba(139, 92, 246, 0.1);
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        border: 2px solid rgba(139, 92, 246, 0.2);
    }
    
    .realtime-title {
        margin: 0;
        color: #1F2937;
        font-weight: 800;
        font-size: 28px;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .realtime-subtitle {
        color: #6B7280;
        margin: 8px 0 0 0;
        font-size: 16px;
        font-weight: 500;
    }
    
    .realtime-subtitle i {
        margin-right: 6px;
        color: #8B5CF6;
    }
    
    /* Live Status Banner */
    .live-status-banner {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3);
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .status-indicator i {
        font-size: 12px;
    }
    
    .status-text {
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 1px;
    }
    
    .refresh-counter {
        text-align: right;
    }
    
    .counter-label {
        font-size: 12px;
        opacity: 0.9;
        margin-bottom: 4px;
    }
    
    .counter-value {
        font-size: 32px;
        font-weight: 800;
        line-height: 1;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 40px 0 24px 0;
    }
    
    .section-icon {
        font-size: 24px;
        color: #7C3AED;
        background: rgba(139, 92, 246, 0.1);
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        border: 2px solid rgba(139, 92, 246, 0.2);
    }
    
    .section-title {
        margin: 0;
        color: #1F2937;
        font-weight: 700;
        font-size: 20px;
        letter-spacing: -0.01em;
    }
    
    /* Modern Metric Cards */
    .modern-metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9F7FF 100%);
        padding: 24px;
        border-radius: 20px;
        border: 2px solid #E5E7EB;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.1);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    
    .modern-metric-card:hover {
        transform: translateY(-8px);
        border-color: #D6BCFA;
        box-shadow: 0 16px 48px rgba(139, 92, 246, 0.2);
    }
    
    .metric-icon-container {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
    }
    
    .metric-icon-container i {
        font-size: 28px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: #1F2937;
        margin: 8px 0;
        line-height: 1;
    }
    
    .metric-label {
        color: #6B7280;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }
    
    .metric-trend {
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
    }
    
    /* Activity Cards */
    .activity-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9F7FF 100%);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.3s ease;
        margin-bottom: 4px;
    }
    
    .activity-card:hover {
        border-color: #D6BCFA;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.1);
        transform: translateX(4px);
    }
    
    .activity-icon {
        font-size: 20px;
        color: #8B5CF6;
        background: rgba(139, 92, 246, 0.1);
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .activity-content {
        flex: 1;
    }
    
    .activity-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .activity-title {
        font-weight: 700;
        color: #1F2937;
        font-size: 16px;
    }
    
    .activity-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .activity-details {
        display: flex;
        gap: 16px;
        color: #6B7280;
        font-size: 13px;
        font-weight: 500;
    }
    
    .activity-details i {
        margin-right: 4px;
    }
    
    .activity-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #E5E7EB, transparent);
        margin: 4px 0;
    }
    
    /* Status Cards */
    .status-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9F7FF 100%);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .status-card:hover {
        border-color: #D6BCFA;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.1);
    }
    
    .status-icon {
        font-size: 24px;
        background: rgba(139, 92, 246, 0.1);
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .status-content {
        flex: 1;
    }
    
    .status-value {
        font-size: 28px;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 4px;
        line-height: 1;
    }
    
    .status-label {
        color: #6B7280;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    /* Empty State */
    .empty-state {
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        padding: 48px 24px;
        border-radius: 20px;
        border: 2px dashed #E5E7EB;
        text-align: center;
        margin: 20px 0;
    }
    
    .empty-state-icon {
        font-size: 48px;
        color: #9CA3AF;
        margin-bottom: 16px;
    }
    
    .empty-state-title {
        color: #1F2937;
        font-weight: 700;
        font-size: 18px;
        margin: 0 0 8px 0;
    }
    
    .empty-state-description {
        color: #6B7280;
        font-size: 14px;
        margin: 0;
    }
    
    /* Error State */
    .error-state {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        padding: 48px 24px;
        border-radius: 20px;
        border: 2px solid #FECACA;
        text-align: center;
        margin: 20px 0;
    }
    
    .error-icon {
        font-size: 48px;
        color: #EF4444;
        margin-bottom: 16px;
    }
    
    .error-title {
        color: #1F2937;
        font-weight: 700;
        font-size: 18px;
        margin: 0 0 8px 0;
    }
    
    .error-description {
        color: #6B7280;
        font-size: 14px;
        margin: 0;
    }
    
    /* Controls Section */
    .controls-section {
        margin-top: 48px;
        padding-top: 32px;
        border-top: 2px solid #F3F4F6;
    }
    
    /* Info Card */
    .info-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 24px;
        border-radius: 20px;
        border: 2px solid #BAE6FD;
    }
    
    .info-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .info-header i {
        font-size: 24px;
    }
    
    .info-title {
        margin: 0;
        color: #0369A1;
        font-weight: 700;
        font-size: 18px;
    }
    
    .info-content {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .info-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        color: #475569;
        font-size: 14px;
    }
    
    .info-item i {
        margin-top: 2px;
    }
    
    /* Action Buttons */
    .action-buttons {
        display: flex;
        flex-direction: column;
        gap: 12px;
        height: 100%;
    }
    
    .action-button {
        padding: 16px;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .action-button.primary {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
    }
    
    .action-button.primary:hover {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3);
    }
    
    .action-button.secondary {
        background: #F3F4F6;
        color: #8B5CF6;
        border: 1px solid #E5E7EB;
    }
    
    .action-button.secondary:hover {
        background: #E5E7EB;
        border-color: #D1D5DB;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit buttons but keep functionality */
    [data-testid="column"]:has(button) {
        opacity: 0;
        height: 0;
        padding: 0;
        margin: 0;
        overflow: hidden;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .realtime-header-content {
            flex-direction: column;
            text-align: center;
            gap: 16px;
        }
        
        .live-status-banner {
            flex-direction: column;
            gap: 16px;
            text-align: center;
        }
        
        .activity-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
        }
        
        .activity-details {
            flex-direction: column;
            gap: 8px;
        }
        
        .info-header {
            flex-direction: column;
            text-align: center;
            gap: 8px;
        }
    }
    </style>
    """, unsafe_allow_html=True)








# ================================
# SIDEBAR
# ================================

def render_sidebar():
    """Render sidebar with system status"""
    
    with st.sidebar:
        # Main Header Card
        st.markdown(f"""
        <div class="sidebar-main-card">
            <div class="sidebar-main-icon">
                <img src="data:image/jpg;base64,{base64.b64encode(open('m11.jpg', 'rb').read()).decode()}" 
                     style="width: 100px; height: 120px; border-radius: 20%; object-fit: cover; border: 2px solid rgba(139, 92, 246, 0.3);">
            </div>
            <h2 class="sidebar-main-title">MediNomix</h2>
            <p class="sidebar-main-subtitle">Advanced Medication Safety</p>
        </div>
        
        <style>
        .sidebar-main-card {{
            background: linear-gradient(135deg, #F8F5FF 0%, #F3EFFF 100%);
            padding: 28px 20px;
            border-radius: 20px;
            border: 2px solid #D6BCFA;
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.15);
            text-align: center;
            margin-bottom: 28px;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .sidebar-main-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 50%, #EC4899 100%);
        }}
        
        .sidebar-main-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 16px 48px rgba(139, 92, 246, 0.25);
            border-color: #A78BFA;
        }}
        
        .sidebar-main-icon {{
            font-size: 48px;
            color: #7C3AED;
            margin-bottom: 16px;
            text-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
            display: inline-block;
            transition: transform 0.3s ease;
        }}
        
        .sidebar-main-card:hover .sidebar-main-icon {{
            transform: scale(1.1);
        }}
        
        .sidebar-main-title {{
            margin: 0;
            color: #1F2937;
            font-weight: 800;
            font-size: 24px;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .sidebar-main-subtitle {{
            color: #6B7280;
            margin: 6px 0 0 0;
            font-size: 13px;
            font-weight: 600;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # System Status Card
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-card-header">
                <i class="fas fa-server sidebar-header-icon"></i>
                <h3 class="sidebar-card-title">System Status</h3>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    st.markdown("""
                    <div class="status-success">
                        <i class="fas fa-check-circle status-icon"></i>
                        <div>
                            <div class="status-title">Backend Connected</div>
                            <div class="status-message">Server running smoothly</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <i class="fas fa-pills metric-icon"></i>
                            <div class="metric-value">{data.get('metrics', {}).get('drugs_in_database', 0)}</div>
                            <div class="metric-label">Drugs</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <i class="fas fa-chart-bar metric-icon"></i>
                            <div class="metric-value">{data.get('metrics', {}).get('total_analyses', 0)}</div>
                            <div class="metric-label">Analyses</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="status-warning">
                        <i class="fas fa-exclamation-triangle status-icon"></i>
                        <div>
                            <div class="status-title">Backend Issues</div>
                            <div class="status-message">Server has issues</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-error">
                    <i class="fas fa-times-circle status-icon"></i>
                    <div>
                        <div class="status-title">Cannot Connect</div>
                        <div class="status-message">Backend server offline</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.markdown("""
            <div class="status-error">
                <i class="fas fa-plug status-icon"></i>
                <div>
                    <div class="status-title">Backend Not Running</div>
                    <div class="status-message">Start server: python backend.py</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.code("python backend.py", language="bash")
       
        
        # Quick Links Card
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-card-header">
                <i class="fas fa-link sidebar-header-icon"></i>
                <h3 class="sidebar-card-title">Quick Links</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Documentation", use_container_width=True):
                render_alert_card("Documentation coming soon!", "info")
        with col2:
            if st.button("Report Bug", use_container_width=True):
                render_alert_card("Bug reporting coming soon!", "info")
        
        if st.button("Clear Cache", use_container_width=True, type="secondary"):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            render_alert_card("Cache cleared successfully!", "success")
            st.rerun()
        
        # Risk Categories Card
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-card-header">
                <i class="fas fa-exclamation-triangle sidebar-header-icon"></i>
                <h3 class="sidebar-card-title">Risk Categories</h3>
            </div>
        """, unsafe_allow_html=True)
        
        risk_levels = [
            ("Critical", "≥75%", "Immediate attention required", "#EF4444"),
            ("High", "50-74%", "Review and verify", "#F59E0B"),
            ("Medium", "25-49%", "Monitor closely", "#8B5CF6"),
            ("Low", "<25%", "Low priority", "#10B981")
        ]
        
        for name, score, desc, color in risk_levels:
            st.markdown(f"""
            <div class="risk-item">
                <div class="risk-header">
                    <span class="risk-badge" style="background: {color}">{name}</span>
                    <span class="risk-score">{score}</span>
                </div>
                <div class="risk-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        
        # Global CSS Styles
        st.markdown("""
        <style>
        .sidebar-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F9F7FF 100%);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 6px 24px rgba(139, 92, 246, 0.1);
            margin-bottom: 24px;
            transition: all 0.3s ease;
        }
        
        .sidebar-card:hover {
            border-color: #D6BCFA;
            box-shadow: 0 10px 32px rgba(139, 92, 246, 0.15);
        }
        
        .sidebar-card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .sidebar-header-icon {
            font-size: 18px;
            color: #7C3AED;
            background: #F3E8FF;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            border: 1px solid #E5D8FA;
        }
        
        .sidebar-card-title {
            margin: 0;
            color: #1F2937;
            font-weight: 700;
            font-size: 16px;
        }
        
        .status-success, .status-warning, .status-error {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        
        .status-success {
            background: #ECFDF5;
            border: 1px solid #D1FAE5;
        }
        
        .status-warning {
            background: #FEF3C7;
            border: 1px solid #FDE68A;
        }
        
        .status-error {
            background: #FEE2E2;
            border: 1px solid #FECACA;
        }
        
        .status-icon {
            font-size: 24px;
        }
        
        .status-success .status-icon { color: #10B981; }
        .status-warning .status-icon { color: #F59E0B; }
        .status-error .status-icon { color: #EF4444; }
        
        .status-title {
            font-weight: 700;
            font-size: 14px;
            color: #1F2937;
        }
        
        .status-message {
            font-size: 12px;
            color: #6B7280;
            margin-top: 2px;
        }
        
        .metric-card {
            background: #F5F3FF;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #E5D8FA;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: #D6BCFA;
            background: #F0EDFF;
        }
        
        .metric-icon {
            font-size: 20px;
            color: #7C3AED;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 800;
            color: #1F2937;
            margin: 4px 0;
        }
        
        .metric-label {
            font-size: 11px;
            color: #6B7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .risk-item {
            padding: 16px;
            border-bottom: 1px solid #F3F4F6;
            transition: all 0.3s ease;
        }
        
        .risk-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        
        .risk-item:hover {
            background: #F9FAFB;
            border-radius: 8px;
            transform: translateX(4px);
        }
        
        .risk-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .risk-badge {
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .risk-score {
            font-weight: 700;
            color: #1F2937;
            font-size: 12px;
        }
        
        .risk-desc {
            color: #4B5563;
            font-size: 12px;
            font-weight: 500;
            line-height: 1.5;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
            color: white !important;
            border: none !important;
            padding: 10px 16px !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3) !important;
        }
        
        .stButton > button[kind="secondary"] {
            background: #F3F4F6 !important;
            color: #7C3AED !important;
            border: 1px solid #E5E7EB !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: #E5E7EB !important;
            border-color: #D1D5DB !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        
# ================================
# FOOTER
# ================================

def render_footer():
    """Render footer"""
    
    st.markdown(f"""
    <div class="neon-footer">
        <div style="max-width: 600px; margin: 0 auto; padding: 0 20px;">
            <div style="margin-bottom: 24px;">
                <div style="font-size: 32px; margin-bottom: 12px;">💊</div>
                <h3 style="color: white !important; margin-bottom: 8px; font-weight: 700;">MediNomix</h3>
                <p style="color: rgba(255, 255, 255, 0.95) !important; font-size: 14px; max-width: 500px; margin: 0 auto;">
                    Preventing medication errors with artificial intelligence
                </p>
            </div>
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 20px; color: rgba(255, 255, 255, 0.8) !important; font-size: 12px;">
                <div style="margin-bottom: 8px; font-weight: 600;">© 2024 MediNomix. All rights reserved.</div>
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
    
    # Navigation Tabs (ORIGINAL - NO ICONS)
    tab1, tab2, tab3, tab4 = st.tabs([" Home", " Drug Analysis", " Analytics", " Real-Time"])
    
    with tab1:
        render_hero_section()
        
        # Stats Counter with themed Font Awesome icons
        col1, col2, col3, col4 = st.columns(4)
        render_stat_card("<i class='fas fa-users' style='color:#EC4899;'></i>", "1.5M+", "Patients Protected", col1)
        render_stat_card("<i class='fas fa-dollar-sign' style='color:#10B981;'></i>", "$42B", "Cost Saved", col2)
        render_stat_card("<i class='fas fa-bullseye' style='color:#8B5CF6;'></i>", "99.8%", "Accuracy Rate", col3)
        render_stat_card("<i class='fas fa-pills' style='color:#7C3AED;'></i>", "50K+", "Drugs Analyzed", col4)
        
        # Features Section with Images and Font Awesome icons
        st.markdown("""
        <div style="margin: 40px 0;">
            <h2 style="text-align: center; margin-bottom: 32px; color: #111827; font-weight: 800;">
                <i class="fas fa-magic" style="color:#EC4899; margin-right:10px;"></i>How MediNomix Works
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        features_cols = st.columns(3)
        features = [
            {"icon": "<i class='fas fa-search' style='color:#8B5CF6;'></i>", "title": "Search Medication", "desc": "Enter any drug name to analyze potential confusion risks"},
            {"icon": "<i class='fas fa-brain' style='color:#EC4899;'></i>", "title": "Analysis", "desc": "Our AI analyzes spelling, phonetic, and therapeutic similarities"},
            {"icon": "<i class='fas fa-shield-alt' style='color:#10B981;'></i>", "title": "Risk Prevention", "desc": "Get detailed risk assessments and prevention recommendations"}
        ]
        
        # Add images for features
        feature_images = [
            "https://img.freepik.com/premium-photo/modern-vital-sign-monitor-patient-background-ward-hospital_1095508-6659.jpg?semt=ais_hybrid&w=740&q=80",
            "https://www.workingbuildings.com/images/hazardousdrugs.png",
            "https://www.anxietyenders.com/images/handd.jpg"
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
        
        # Trust Section with Images - ICON COLOR FIXED TO WHITE
        render_glass_card("<i class='fas fa-handshake' style='color:white; margin-right:10px;'></i>Trusted by Healthcare Professionals")
        
        # Medical images grid with icon overlays
        medical_images = [
            "https://www.shutterstock.com/image-photo/portrait-man-doctor-standing-team-260nw-2478537933.jpg",
            "https://thumbs.dreamstime.com/b/healthcare-professionals-including-doctors-nurses-applauding-together-contemporary-medical-setting-representing-teamwork-398717867.jpg",
            "https://thumbs.dreamstime.com/b/four-healthcare-workers-scrubs-walking-corridor-104862472.jpg",
            "https://media.istockphoto.com/id/482078816/photo/female-doctorss-hands-holding-stethoscope.jpg?s=612x612&w=0&k=20&c=Mu1mh1_CAT40WVuwl8ljFGXyjbBK5GtaYGVgvOP6hl8="
        ]
        
        # Add icon titles for each medical image
        medical_icons = [
            "<i class='fas fa-user-md' style='color:#8B5CF6;'></i> Expert Doctors",
            "<i class='fas fa-users' style='color:#EC4899;'></i> Team Collaboration",
            "<i class='fas fa-hospital' style='color:#10B981;'></i> Modern Facilities",
            "<i class='fas fa-hand-holding-heart' style='color:#7C3AED;'></i> Compassionate Care"
        ]
        
        cols = st.columns(4)
        for idx, col in enumerate(cols):
            with col:
                # Display image with icon overlay
                st.markdown(f"""
                <div style="position: relative;">
                    <img src="{medical_images[idx]}" class="medical-image" alt="Medical Facility {idx+1}">
                    <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(139, 92, 246, 0.8)); padding: 15px; border-radius: 0 0 16px 16px;">
                        <div style="color: white; font-weight: 600; font-size: 14px; text-align: center;">
                            {medical_icons[idx]}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        render_drug_analysis_tab()
    
    with tab3:
        render_analytics_tab()
    
    with tab4:
        render_realtime_tab()
    
    # Render Sidebar
    render_sidebar()
    
    # Render Footer - BUG FIXED (no duplicate code showing)
    st.markdown(f"""
    <div class="neon-footer">
        <div style="max-width: 600px; margin: 0 auto; padding: 0 20px;">
            <div style="margin-bottom: 24px;">
                <div style="font-size: 48px; margin-bottom: 12px;">
                    <i class="fas fa-heartbeat" style="color:white; text-shadow: 0 0 20px rgba(255,255,255,0.5);"></i>
                </div>
                <h3 style="color: white !important; margin-bottom: 8px; font-weight: 700;">
                    <i class="fas fa-capsules" style="margin-right:10px;"></i>MediNomix
                </h3>
                <p style="color: rgba(255, 255, 255, 0.95) !important; font-size: 14px; max-width: 500px; margin: 0 auto;">
                    <i class="fas fa-shield-alt" style="margin-right:8px;"></i>Preventing medication errors with smart system
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# START APPLICATION
# ================================

if __name__ == "__main__":
    main()