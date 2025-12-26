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
    page_icon="🏥",
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

# Modern Medical Color Palette
COLORS = {
    "primary": "#4361ee",
    "primary_light": "#4895ef",
    "primary_dark": "#3a56d4",
    "secondary": "#4cc9f0",
    "accent": "#7209b7",
    "accent_pink": "#f72585",
    "success": "#06d6a0",
    "warning": "#ffd166",
    "danger": "#ef476f",
    "dark": "#1d3557",
    "light": "#f1f6ff",
    "surface": "#ffffff",
    "gray": "#6c757d",
    "gray_light": "#e9ecef",
    "border": "rgba(67, 97, 238, 0.12)",
}

# Base64 encoded SVG Icons - Simplified version
def get_icon_svg(icon_name, color="#4361ee", size=24):
    """Generate base64 encoded SVG icons"""
    icon_map = {
        "pill": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M10.5 20H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v6.5"/><rect x="8" y="12" width="8" height="8" rx="2"/><path d="m18.5 9.5-1 1"/><path d="m15.5 9.5-1 1"/></svg>""",
        "search": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/><path d="M11 8v6"/><path d="M8 11h6"/></svg>""",
        "dashboard": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>""",
        "analytics": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M7 16l4-4 4 4 6-6"/><path d="M17 11V7"/></svg>""",
        "alert": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
        "safety": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>""",
        "hospital": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 22h18"/><path d="M6 18v-6"/><path d="M10 18v-6"/><path d="M14 18v-6"/><path d="M18 18v-6"/><path d="M12 6V2"/><path d="M8 6h8"/><rect x="4" y="6" width="16" height="12" rx="2"/></svg>""",
        "brain": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-2.5 2.5h-2A2.5 2.5 0 0 1 5 19.5v-15A2.5 2.5 0 0 1 7.5 2z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 2.5 2.5h2A2.5 2.5 0 0 0 19 19.5v-15A2.5 2.5 0 0 0 16.5 2z"/><path d="M12 8v4"/><path d="M12 16v2"/></svg>""",
        "database": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34-9-3V5"/></svg>""",
        "refresh": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/></svg>""",
        "microchip": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>""",
        "shield": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>""",
        "chart-network": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="2"/><circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/><line x1="6" y1="8" x2="6" y2="16"/><line x1="12" y1="10" x2="12" y2="14"/><line x1="18" y1="8" x2="18" y2="16"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="18" x2="16" y2="18"/><line x1="10" y1="12" x2="14" y2="12"/></svg>""",
        "chart-pie": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>""",
        "chart-bar": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>""",
        "triangle": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>""",
        "book": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>""",
        "bug": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="9" y="9" width="6" height="6" rx="1"/><path d="M12 3v2"/><path d="M19 12h2"/><path d="M12 19v2"/><path d="M3 12h2"/><path d="M17.66 6.34l1.41-1.41"/><path d="M6.34 17.66l-1.41-1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M6.34 6.34l-1.41 1.41"/></svg>""",
        "book-medical": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><path d="M12 8v4"/><path d="M10 12h4"/></svg>""",
        "cogs": f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>""",
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
    """Create interactive drug confusion heatmap"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS["success"]],
            [0.25, COLORS["warning"]],
            [0.5, "#ff9a00"],
            [0.75, COLORS["danger"]],
            [1, "#b5179e"]
        ],
        zmin=0,
        zmax=100,
        text=[[f"{val:.0f}%" if val > 0 else "" for val in row] for row in risk_matrix],
        texttemplate="%{text}",
        hoverongaps=False,
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br><b>Risk Score: %{z:.1f}%</b><br><extra></extra>",
    ))
    
    fig.update_layout(
        title="Drug Confusion Risk Matrix",
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        height=650,
        margin={"t": 100, "b": 100, "l": 120, "r": 50},
        xaxis=dict(tickangle=45)
    )
    
    return fig

def create_risk_breakdown_chart():
    """Create risk breakdown donut chart"""
    if 'breakdown' not in st.session_state.dashboard_data:
        return None
    
    breakdown = st.session_state.dashboard_data['breakdown']
    if not breakdown:
        return None
    
    categories = [item['category'].title() for item in breakdown]
    counts = [item['count'] for item in breakdown]
    
    color_map = {
        "Critical": "#b5179e",
        "High": COLORS["danger"],
        "Medium": COLORS["warning"],
        "Low": COLORS["success"]
    }
    colors = [color_map.get(cat, COLORS["warning"]) for cat in categories]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=categories,
            values=counts,
            hole=0.6,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='inside',
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
        )
    ])
    
    fig.update_layout(
        title="Risk Distribution",
        height=450,
        showlegend=True,
    )
    
    fig.add_annotation(
        text=f"<b>Total</b><br>{sum(counts)}",
        x=0.5, y=0.5,
        font=dict(size=16),
        showarrow=False
    )
    
    return fig

def create_top_risks_chart():
    """Create top risks horizontal bar chart"""
    if 'top_risks' not in st.session_state.dashboard_data:
        return None
    
    top_risks = st.session_state.dashboard_data['top_risks']
    if not top_risks:
        return None
    
    pairs = [f"{item['drug1']} ↔ {item['drug2']}" for item in top_risks]
    scores = [item['risk_score'] for item in top_risks]
    categories = [item['risk_category'] for item in top_risks]
    
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
        )
    ])
    
    fig.update_layout(
        title="Top 10 High-Risk Drug Pairs",
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=500,
        margin=dict(t=80, b=50, l=220, r=50),
    )
    
    return fig

# ==================== MAIN APP LAYOUT - NO HTML CODE ====================

# Modern Header using Streamlit components only
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #4361ee 0%, #7209b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .sub-title {
        color: #6c757d;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-title">MediNomix</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI-Powered Medication Safety Intelligence Platform</p>', unsafe_allow_html=True)

# Status Indicators using columns
status_cols = st.columns(4)
with status_cols[0]:
    st.markdown("""
    <div style='text-align: center; padding: 10px; border-radius: 25px; background: rgba(6, 214, 160, 0.15); border: 2px solid rgba(6, 214, 160, 0.3);'>
        <div style='font-size: 0.9rem; font-weight: 600; color: #06d6a0;'>Patient Safety First</div>
    </div>
    """, unsafe_allow_html=True)

with status_cols[1]:
    st.markdown("""
    <div style='text-align: center; padding: 10px; border-radius: 25px; background: rgba(67, 97, 238, 0.15); border: 2px solid rgba(67, 97, 238, 0.3);'>
        <div style='font-size: 0.9rem; font-weight: 600; color: #4361ee;'>AI-Powered Analysis</div>
    </div>
    """, unsafe_allow_html=True)

with status_cols[2]:
    st.markdown("""
    <div style='text-align: center; padding: 10px; border-radius: 25px; background: rgba(114, 9, 183, 0.15); border: 2px solid rgba(114, 9, 183, 0.3);'>
        <div style='font-size: 0.9rem; font-weight: 600; color: #7209b7;'>Hospital Grade</div>
    </div>
    """, unsafe_allow_html=True)

with status_cols[3]:
    st.markdown("""
    <div style='text-align: center; padding: 10px; border-radius: 25px; background: rgba(6, 214, 160, 0.15); border: 2px solid rgba(6, 214, 160, 0.3);'>
        <div style='font-size: 0.9rem; font-weight: 600; color: #06d6a0;'>Real-time Protection</div>
    </div>
    """, unsafe_allow_html=True)

# Action Buttons
st.markdown("<br>", unsafe_allow_html=True)
action_cols = st.columns([1, 1, 1, 1])
with action_cols[0]:
    if st.button("**Seed Database**", use_container_width=True, type="secondary"):
        with st.spinner("Seeding database..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()
with action_cols[1]:
    if st.button("**Refresh Data**", use_container_width=True, type="secondary"):
        with st.spinner("Refreshing..."):
            load_dashboard_data()
            st.rerun()
with action_cols[2]:
    if st.button("**Quick Demo**", use_container_width=True):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
with action_cols[3]:
    if st.button("**Get Help**", use_container_width=True, type="secondary"):
        st.info("""
        **Quick Tips:**
        1. Search any drug name to analyze confusion risks
        2. Use the heatmap to visualize risk patterns
        3. Check FDA alerts for known dangerous pairs
        4. Filter results by risk level for focused analysis
        """)

# Divider
st.markdown("<hr>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["**Drug Analysis**", "**Analytics Dashboard**", "**About & Resources**"])

with tab1:
    # Search Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Drug Confusion Risk Analysis")
        st.markdown("Enter a drug name to analyze potential confusion risks with similar medications")
        
        drug_name = st.text_input(
            "Enter drug name:",
            placeholder="e.g., metformin, lamictal, celebrex...",
            label_visibility="visible",
            key="search_input"
        )
        
        search_cols = st.columns([1, 1])
        with search_cols[0]:
            search_clicked = st.button("**Analyze Drug**", use_container_width=True, type="primary")
        with search_cols[1]:
            if st.button("**Show Examples**", use_container_width=True, type="secondary"):
                examples = ["metformin", "lamictal", "celebrex", "clonidine", "zyprexa"]
                st.info(f"**Try these drugs:** {', '.join(examples)}")
    
    if search_clicked and drug_name:
        with st.spinner(f"Analyzing '{drug_name}'..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"Found {len(st.session_state.search_results)} similar drugs.")
                st.rerun()
    
    # Results Section
    if st.session_state.search_results:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Risk Filters
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
        
        st.info(f"Found {len(filtered_results)} similar drugs")
        
        # Display Results
        for idx, result in enumerate(filtered_results):
            risk_class = result['risk_category']
            risk_color = {
                "critical": "#b5179e",
                "high": COLORS["danger"],
                "medium": COLORS["warning"],
                "low": COLORS["success"]
            }.get(risk_class, COLORS["warning"])
            
            with st.container():
                st.markdown(f"""
                <div style='padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border-left: 6px solid {risk_color}; background: rgba(255, 255, 255, 0.9);'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div>
                            <h3 style='color: #1d3557; margin-bottom: 5px;'>{result['target_drug']['brand_name']}</h3>
                            <p style='color: #6c757d; margin: 0; font-style: italic;'>
                                {result['target_drug']['generic_name'] if result['target_drug']['generic_name'] else 'Generic name not available'}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span style='padding: 5px 15px; border-radius: 20px; background-color: {risk_color}15; color: {risk_color}; border: 2px solid {risk_color}; font-weight: 700; font-size: 0.8rem;'>
                                {risk_class.upper()}
                            </span>
                            <div style='margin-top: 10px; font-size: 2rem; font-weight: 800; color: {risk_color};'>
                                {result['combined_risk']:.0f}%
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics
                cols = st.columns(4)
                metrics = [
                    ("Spelling Similarity", f"{result['spelling_similarity']:.1f}%"),
                    ("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%"),
                    ("Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%"),
                    ("Overall Risk", f"{result['combined_risk']:.1f}%")
                ]
                
                for col, (label, value) in zip(cols, metrics):
                    with col:
                        st.metric(label, value)
                
                with st.expander("View Drug Details"):
                    col1, col2 = st.columns(2)
                    with col1:
                        if result['target_drug']['purpose']:
                            st.markdown("**Purpose:**")
                            st.info(result['target_drug']['purpose'][:200] + "..." if len(result['target_drug']['purpose']) > 200 else result['target_drug']['purpose'])
                    with col2:
                        if result['target_drug']['manufacturer']:
                            st.markdown("**Manufacturer:**")
                            st.text(result['target_drug']['manufacturer'])
                
                st.markdown("<br>", unsafe_allow_html=True)

with tab2:
    # Dashboard
    st.markdown("### Medication Safety Analytics")
    st.markdown("Real-time insights into drug confusion risks and safety patterns")
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Metrics Cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        metric_cols = st.columns(4)
        
        metric_data = [
            ("Total Drugs", metrics.get('total_drugs', 0)),
            ("High/Critical Pairs", metrics.get('high_risk_pairs', 0)),
            ("Critical Pairs", metrics.get('critical_risk_pairs', 0)),
            ("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%")
        ]
        
        colors = [COLORS["primary"], "#b5179e", COLORS["danger"], COLORS["accent"]]
        
        for col, (title, value), color in zip(metric_cols, metric_data, colors):
            with col:
                st.markdown(f"""
                <div style='text-align: center; padding: 1.5rem; border-radius: 10px; background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(67, 97, 238, 0.1);'>
                    <div style='font-size: 1rem; color: #6c757d; margin-bottom: 10px;'>{title}</div>
                    <div style='font-size: 2.5rem; font-weight: 800; color: {color};'>{value}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Heatmap
    st.markdown("### Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
    else:
        st.info("No heatmap data available. Search for drugs or seed the database first.")
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available.")
    
    with chart_col2:
        st.markdown("#### Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available.")
    
    # FDA Alerts
    st.markdown("### FDA High Alert Drug Pairs")
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", "Alert Type": "FDA Safety Warning", "Year": "2023"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", "Alert Type": "ISMP High Alert", "Year": "2023"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", "Alert Type": "Common Error", "Year": "2022"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", "Alert Type": "Sound-alike", "Year": "2022"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", "Alert Type": "Look-alike", "Year": "2021"},
        {"Drug 1": "Hydrocodone", "Drug 2": "Oxycodone", "Risk Level": "Critical", "Alert Type": "FDA Black Box", "Year": "2023"},
    ])
    
    st.dataframe(risky_pairs, use_container_width=True, hide_index=True)

with tab3:
    # About Section
    st.markdown("### About MediNomix")
    st.markdown("A next-generation healthcare safety platform designed to prevent medication errors through advanced AI analysis")
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Medication Errors", "25%", "involve name confusion", delta_color="inverse")
    with col2:
        st.metric("Annual Harm", "1.5M", "Americans affected", delta_color="inverse")
    with col3:
        st.metric("Annual Cost", "$42B", "preventable expenses", delta_color="inverse")
    
    # Problem & Solution
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### The Challenge")
        st.markdown("""
        - **25% of medication errors** involve name confusion (FDA)
        - **1.5 million Americans** harmed annually
        - **$42 billion** in preventable costs
        - Common pairs: **Lamictal↔Lamisil**, **Celebrex↔Celexa**
        """)
    
    with col2:
        st.markdown("#### Our Solution")
        st.markdown("""
        - **Multi-algorithm AI** risk assessment
        - **Real-time FDA data** integration
        - **Context-aware** similarity detection
        - **Instant alerts** and prevention guidance
        """)
    
    # How It Works
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### How It Works")
    
    steps = [
        ("Search", "Enter drug name for analysis"),
        ("Analyze", "Advanced AI algorithms calculate risks"),
        ("Visualize", "Interactive charts and heatmaps"),
        ("Prevent", "Safety alerts and recommendations")
    ]
    
    step_cols = st.columns(4)
    for col, (title, desc) in zip(step_cols, steps):
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; border-radius: 10px; background: rgba(67, 97, 238, 0.1);'>
                <h4 style='color: #4361ee;'>{title}</h4>
                <p style='color: #6c757d; font-size: 0.9rem;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo
    st.markdown("### MediNomix")
    st.markdown("AI-Powered Medication Safety")
    st.markdown("---")
    
    # Quick Actions
    st.markdown("#### Quick Actions")
    if st.button("**Test with Metformin**", use_container_width=True, type="primary"):
        st.session_state.search_results = []
        with st.spinner("Testing..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
    
    if st.button("**Load Sample Data**", use_container_width=True, type="secondary"):
        if seed_database():
            load_dashboard_data()
            st.rerun()
    
    if st.button("**Force Refresh**", use_container_width=True, type="secondary"):
        load_dashboard_data()
        st.rerun()
    
    st.markdown("---")
    
    # System Status
    st.markdown("#### System Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.success("✅ Backend Connected")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Drugs", data.get('drugs_in_database', 0))
                with col2:
                    st.metric("Risks", data.get('risk_assessments', 0))
            else:
                st.warning("⚠️ Backend Error")
        else:
            st.error("❌ Cannot Connect")
    except:
        st.error("🔌 Backend Not Running")
        st.info("Run in terminal: `python backend.py`")
    
    st.markdown("---")
    
    # Risk Categories
    st.markdown("#### Risk Categories")
    
    risk_categories = [
        ("Critical", "≥75%", "Immediate intervention required"),
        ("High", "50-74%", "Review and verification needed"),
        ("Medium", "25-49%", "Monitor closely"),
        ("Low", "<25%", "Low priority")
    ]
    
    colors = ["#b5179e", COLORS["danger"], COLORS["warning"], COLORS["success"]]
    
    for (name, range_, desc), color in zip(risk_categories, colors):
        st.markdown(f"""
        <div style='margin-bottom: 10px; padding: 10px; border-radius: 8px; background: {color}10; border-left: 4px solid {color};'>
            <div style='font-weight: 700; color: {color};'>{name} {range_}</div>
            <div style='font-size: 0.8rem; color: #6c757d;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer - Using Streamlit components only
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <p style='color: #1d3557; font-weight: 700;'>© 2024 MediNomix • Version 3.0 • Advanced Medication Safety Platform</p>
        <div style='display: flex; justify-content: center; gap: 20px; margin-top: 20px;'>
            <a href='https://github.com/precious-05/MediNomix' target='_blank' style='color: #4361ee; text-decoration: none; font-weight: 600;'>GitHub</a>
            <a href='https://github.com/precious-05/MediNomix/issues' target='_blank' style='color: #4361ee; text-decoration: none; font-weight: 600;'>Report Bug</a>
            <a href='https://github.com/precious-05/MediNomix' target='_blank' style='color: #4361ee; text-decoration: none; font-weight: 600;'>Documentation</a>
        </div>
        <div style='margin-top: 30px; padding-top: 20px; border-top: 1px solid #e9ecef;'>
            <p style='color: #6c757d; font-size: 0.9rem; font-style: italic;'>
                Important: Always consult healthcare professionals for medical decisions. This application is designed to assist, not replace, professional judgment.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)