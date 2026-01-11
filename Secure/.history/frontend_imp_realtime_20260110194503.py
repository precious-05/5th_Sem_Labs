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
    page_title="MediNomix | Medication Safety",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/dashboard"



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

class RealTimeWebSocketManager:
    def __init__(self):
        self.connected = False
        self.ws = None
        self.connection_attempts = 0
        self.max_attempts = 3
        
    def start_connection(self):
        try:
            if self.connection_attempts >= self.max_attempts:
                return  # Stop trying after max attempts
                
            self.ws = websocket.WebSocketApp(
                WS_URL,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            # Better connection with timeout settings
            threading.Thread(
                target=self.ws.run_forever,
                kwargs={'ping_interval': 20, 'ping_timeout': 10},
                daemon=True
            ).start()
            self.connection_attempts += 1
        except Exception as e:
            # Don't show error if it's just slow connection
            if self.connection_attempts < self.max_attempts:
                # Try again after 2 seconds
                time.sleep(2)
                self.start_connection()
            else:
                # Only show error after max attempts
                st.warning(f"⚠️ Could not establish WebSocket connection after {self.max_attempts} attempts.")
    
    def _on_open(self, ws):
        self.connected = True
        st.session_state.websocket_connected = True
        # Show success but don't use emoji that might cause encoding issues
        st.success("Real-time WebSocket connection established successfully!")
    
    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            if data.get('type') in ['initial', 'update']:
                st.session_state.realtime_metrics = data.get('data', {})
                # Store timestamp of last update
                st.session_state.last_update_time = datetime.utcnow()
        except:
            pass
    
    def _on_error(self, ws, error):
        self.connected = False
        st.session_state.websocket_connected = False
        # Don't show error alerts that might disrupt user experience
    
    def _on_close(self, ws, close_status_code, close_msg):
        self.connected = False
        st.session_state.websocket_connected = False
        # Don't show disconnect messages - auto-reconnect will handle it

websocket_manager = RealTimeWebSocketManager()

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
                        font=dict(color="white", size=10, family="Poppins"),
                        bgcolor="rgba(239, 68, 68, 0.8)",
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
            titlefont=dict(color=COLORS['text_primary'], size=12, family="Poppins"),
            tickfont=dict(color=COLORS['text_secondary'], size=10, family="Poppins"),
            bgcolor="white",
            bordercolor=COLORS['border'],
            borderwidth=2
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="Drug Confusion Risk Heatmap",
            font=dict(color=COLORS['text_primary'], size=18, family="Poppins"),
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
            tickfont=dict(color=COLORS['text_secondary'], size=10, family="Poppins"),
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            linewidth=1
        ),
        yaxis=dict(
            tickfont=dict(color=COLORS['text_secondary'], size=10, family="Poppins"),
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            linewidth=1
        ),
        margin=dict(l=80, r=50, t=60, b=80),
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
        textfont=dict(color='white', size=12, family='Poppins'),
        marker_line=dict(color='white', width=2),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        title=dict(
            text="Risk Distribution",
            font=dict(color=COLORS['text_primary'], size=16, family="Poppins"),
            x=0.5,
            xanchor="center"
        ),
        height=400,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color=COLORS['text_primary'],
        legend=dict(
            font=dict(size=12, color=COLORS['text_secondary'], family="Poppins"),
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
            text=[f"🔥 {score:.0f}%" for score in scores],
            textposition='outside',
            marker_line_color='white',
            marker_line_width=1,
            textfont=dict(size=12, color=COLORS['text_primary'], family="Poppins"),
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><extra></extra>"
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="🚨 Top 10 High-Risk Drug Pairs",
            font=dict(color=COLORS['text_primary'], size=16, family="Poppins"),
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
            tickfont=dict(color=COLORS['text_secondary'], size=10, family="Poppins")
        ),
        yaxis=dict(
            tickfont=dict(color=COLORS['text_secondary'], size=10, family="Poppins")
        ),
        margin=dict(l=150, r=50, t=60, b=50)
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
    
    render_glass_card(
        "Medication Safety Analytics Dashboard",
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
    
    # Charts Section with proper card headers
    st.markdown('<div class="glass-card"><div class="glass-card-header"><h2>Analytics Charts</h2></div></div>', unsafe_allow_html=True)
    
    # First row: Two charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Risk Distribution</div>', unsafe_allow_html=True)
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🚨 Top 10 High-Risk Drug Pairs</div>', unsafe_allow_html=True)
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row: Heatmap full width with annotations
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> Drug Confusion Risk Heatmap</div>', unsafe_allow_html=True)
    
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown(f"""
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 20px; color: #4B5563; font-size: 12px; font-weight: 600;">
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['success']}; border-radius: 2px;"></div> Low Risk</div>
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['purple']}; border-radius: 2px;"></div> Medium Risk</div>
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['warning']}; border-radius: 2px;"></div> High Risk</div>
            <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background: {COLORS['danger']}; border-radius: 2px;"></div> Critical Risk</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs first.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FDA Alerts Section
    render_glass_card("🚨 FDA High Alert Drug Pairs", "Most commonly confused drug pairs according to FDA")
    
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

# ================================
# REAL-TIME DASHBOARD TAB
# ================================

def render_realtime_tab():
    """COMPLETE WORKING REAL-TIME DASHBOARD"""
    
    # ====================================
    # AUTO-REFRESH MECHANISM
    # ====================================
    import time
    from datetime import datetime
    
    # Initialize refresh counter
    if 'refresh_counter' not in st.session_state:
        st.session_state.refresh_counter = 0
        st.session_state.last_refresh_time = time.time()
    
    # Check if 10 seconds passed
    current_time = time.time()
    time_since_refresh = current_time - st.session_state.last_refresh_time
    
    # Auto-refresh every 10 seconds
    refresh_interval = 10  # seconds
    if time_since_refresh > refresh_interval:
        st.session_state.refresh_counter += 1
        st.session_state.last_refresh_time = current_time
        st.rerun()  # This refreshes the ENTIRE page
    
    seconds_until_refresh = refresh_interval - int(time_since_refresh)
    
    # ====================================
    # UI DISPLAY
    # ====================================
    render_glass_card(
        "⚡ Real-Time Medication Safety Dashboard",
        f"Auto-refreshes every {refresh_interval} seconds • Last refresh: {datetime.now().strftime('%H:%M:%S')}"
    )
    
    # Refresh Status Banner
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%); 
                color: white; padding: 12px 20px; border-radius: 12px; 
                margin-bottom: 20px; display: flex; justify-content: space-between; 
                align-items: center;">
        <div>
            <span style="font-size: 18px;">🔄</span>
            <span style="font-weight: 700; margin-left: 8px;">Live Updates Active</span>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 12px; opacity: 0.9;">Next refresh in</div>
            <div style="font-size: 24px; font-weight: 800;">{seconds_until_refresh}s</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ====================================
    # FETCH REAL-TIME DATA
    # ====================================
    try:
        # Get fresh data from backend
        response = requests.get(f"{BACKEND_URL}/api/metrics", timeout=5)
        
        if response.status_code == 200:
            metrics = response.json()
            
            # Display Live Metrics in Cards
            st.markdown("### 📊 Live Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="💊 Total Drugs",
                    value=metrics.get('total_drugs', 0),
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="🔥 Critical Pairs",
                    value=metrics.get('critical_risk_pairs', 0),
                    delta=f"{metrics.get('critical_risk_pairs', 0)} high risk"
                )
            
            with col3:
                st.metric(
                    label="⚠️ High Risk Pairs",
                    value=metrics.get('high_risk_pairs', 0),
                    delta=None
                )
            
            with col4:
                st.metric(
                    label="📈 Average Risk",
                    value=f"{metrics.get('avg_risk_score', 0):.1f}%",
                    delta=None
                )
            
            # ====================================
            # RECENT ACTIVITY SECTION
            # ====================================
            st.markdown("### 🕒 Recent Activity")
            
            if metrics.get('recent_searches'):
                for idx, search in enumerate(metrics['recent_searches'][:8]):
                    with st.container():
                        col_a, col_b, col_c = st.columns([1, 3, 2])
                        
                        with col_a:
                            st.markdown(f"<div style='text-align: center; padding: 8px;'><span style='font-size: 24px;'>💊</span></div>", unsafe_allow_html=True)
                        
                        with col_b:
                            st.markdown(f"**{search.get('drug_name', 'Unknown')}**")
                            st.caption(f"Found {search.get('similar_drugs_found', 0)} similar drugs")
                        
                        with col_c:
                            risk_score = search.get('highest_risk', 0)
                            risk_color = "#EF4444" if risk_score > 70 else "#F59E0B" if risk_score > 50 else "#10B981"
                            st.markdown(f"""
                            <div style="text-align: right;">
                                <div style="font-size: 20px; font-weight: 800; color: {risk_color};">
                                    {risk_score:.1f}%
                                </div>
                                <div style="font-size: 11px; color: #6B7280;">
                                    {search.get('timestamp', '')[:19]}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        if idx < len(metrics['recent_searches'][:8]) - 1:
                            st.divider()
            else:
                st.info("No recent searches found")
            
            # ====================================
            # SYSTEM STATUS
            # ====================================
            st.markdown("### 🖥️ System Status")
            
            status_col1, status_col2, status_col3 = st.columns(3)
            
            with status_col1:
                st.metric("Connected Clients", metrics.get('connected_clients', 0))
            
            with status_col2:
                st.metric("Total Analyses", metrics.get('total_analyses', 0))
            
            with status_col3:
                status = "🟢 Healthy" if metrics.get('system_status') == 'healthy' else "🟡 Warning"
                st.metric("System Health", status)
            
        else:
            st.error("❌ Could not fetch data from backend")
            st.info("Make sure backend is running on http://localhost:8000")
    
    except Exception as e:
        st.error(f"❌ Connection Error: {str(e)[:100]}")
        st.code("Backend not running. Start it with: python backend3.py")
    
    # ====================================
    # MANUAL CONTROLS
    # ====================================
    st.markdown("---")
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown(f"""
        <div style="background: #F0F9FF; padding: 16px; border-radius: 12px; border: 1px solid #E0F2FE;">
            <div style="font-weight: 700; color: #0369A1; margin-bottom: 8px;">⚡ How Auto-refresh Works</div>
            <div style="color: #475569; font-size: 14px;">
                1. Page automatically reloads every 10 seconds<br>
                2. Fresh data fetched from backend each time<br>
                3. No WebSocket needed - works 100% reliably<br>
                4. Manual refresh available anytime
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        if st.button("🔄 Refresh Now", type="primary", use_container_width=True):
            st.session_state.refresh_counter += 1
            st.rerun()
        
        if st.button("📊 Seed Database", type="secondary", use_container_width=True):
            try:
                response = requests.post(f"{BACKEND_URL}/api/seed-database", timeout=10)
                if response.status_code == 200:
                    st.success("✅ Database seeded successfully!")
                    st.rerun()
                else:
                    st.error("Failed to seed database")
            except:
                st.error("Could not connect to backend")
# ================================
# SIDEBAR
# ================================

def render_sidebar():
    """Render sidebar with system status"""
    
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 24px; padding: 20px 16px; background: {COLORS['gradient_primary']}; border-radius: 16px; box-shadow: 0 6px 20px rgba(16, 185, 129, 0.2);">
            <div style="font-size: 48px; margin-bottom: 8px; filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.2));">💊</div>
            <h2 style="margin: 0; color: white !important; font-weight: 800; font-size: 20px;">MediNomix</h2>
            <p style="color: rgba(255, 255, 255, 0.9); margin: 4px 0 0 0; font-size: 12px; font-weight: 600;">AI Medication Safety</p>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Card with alert card
        st.markdown('<div class="glass-card"><div class="glass-card-header"><h2>System Status</h2></div></div>', unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    render_alert_card("Backend server is running smoothly", "success", "✅ Backend Connected")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("💊 Drugs", data.get('metrics', {}).get('drugs_in_database', 0))
                    with col2:
                        st.metric("📊 Analyses", data.get('metrics', {}).get('total_analyses', 0))
                else:
                    render_alert_card("Backend server has issues", "warning", "⚠️ Backend Issues")
            else:
                render_alert_card("Cannot connect to backend server", "danger", "❌ Cannot Connect")
        except:
            render_alert_card("Backend server is not running", "danger", "🔌 Backend Not Running")
            st.code("python backend.py", language="bash")
        
        # Quick Links
        st.markdown('<div class="glass-card"><div class="glass-card-header"><h2>🔗 Quick Links</h2></div></div>', unsafe_allow_html=True)
        
        if st.button("📚 Documentation", use_container_width=True):
            render_alert_card("Documentation coming soon!", "info")
        
        if st.button("Report Bug", use_container_width=True):
            render_alert_card("Bug reporting coming soon!", "info")
        
        if st.button(" Clear Cache", use_container_width=True):
            st.session_state.search_results = []
            st.session_state.dashboard_data = {}
            render_alert_card("Cache cleared successfully!", "success")
            st.rerun()
        
        # Risk Categories Guide
        st.markdown('<div class="glass-card"><div class="glass-card-header"><h2>⚠️ Risk Categories</h2></div></div>', unsafe_allow_html=True)
        
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
                    <div style="font-weight: 700; color: #111827; font-size: 12px;">{score}</div>
                </div>
                <div style="color: #4B5563; font-size: 11px; font-weight: 500;">{desc}</div>
            </div>
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
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([" Home", " Drug Analysis", " Analytics", "⚡ Real-Time"])
    
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
            {"icon": "🧠", "title": "Analysis", "desc": "Our AI analyzes spelling, phonetic, and therapeutic similarities"},
            {"icon": "🛡️", "title": "Risk Prevention", "desc": "Get detailed risk assessments and prevention recommendations"}
        ]
        
        # Add images for features
        feature_images = [
            #"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZTkQ6XJ2jsfs9bcF6rhtE5yXz5bzOjyXayw&s",
            "https://img.freepik.com/premium-photo/modern-vital-sign-monitor-patient-background-ward-hospital_1095508-6659.jpg?semt=ais_hybrid&w=740&q=80",
            "https://www.workingbuildings.com/images/hazardousdrugs.png",
            #"https://static8.depositphotos.com/1000383/969/i/950/depositphotos_9696817-stock-photo-pills-and-tablets-macro-still.jpg"
            #"https://media.istockphoto.com/id/2158208276/photo/sleeping-pills-concept-capsules-spilling-out-of-bottle-on-purple-background.jpg?s=612x612&w=0&k=20&c=fwXZQ8YyjTdi-9zrgWXL47qKnyQ8FYe8JDRremK1FME="
           "https://www.anxietyenders.com/images/handd.jpg"
            #"https://www.shutterstock.com/image-photo/bluewhite-antibiotic-capsule-pills-spread-260nw-2317028543.jpg"
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
        render_glass_card("Trusted by Healthcare Professionals")
        
        # Medical images grid
        medical_images = [
            "https://www.shutterstock.com/image-photo/portrait-man-doctor-standing-team-260nw-2478537933.jpg",
            "https://thumbs.dreamstime.com/b/healthcare-professionals-including-doctors-nurses-applauding-together-contemporary-medical-setting-representing-teamwork-398717867.jpg",
            "https://thumbs.dreamstime.com/b/four-healthcare-workers-scrubs-walking-corridor-104862472.jpg",
            "https://media.istockphoto.com/id/482078816/photo/female-doctorss-hands-holding-stethoscope.jpg?s=612x612&w=0&k=20&c=Mu1mh1_CAT40WVuwl8ljFGXyjbBK5GtaYGVgvOP6hl8="
            #"https://media.istockphoto.com/id/695273346/photo/concept-of-family-medicine-with-ostetoscope-and-paper-cut.jpg?s=612x612&w=0&k=20&c=VfKxOeQcQ5TZOnFc2f7kzrJdN65xcTmBGC3J3cblZwg="
            #"https://img.freepik.com/free-photo/close-up-doctor-with-stethoscope_23-2149191355.jpg?semt=ais_hybrid&w=740&q=80"
            #"https://t3.ftcdn.net/jpg/02/19/91/48/360_F_219914874_fcqxEeJ6clfwf43OcCNAMGNBySKzF5hl.jpg"
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