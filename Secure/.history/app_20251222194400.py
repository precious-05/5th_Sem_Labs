"""
ConfusionGuard AI - Premium Healthcare Frontend
PROFESSIONAL UI with custom card styling, enhanced visuals, and premium UX
FUNCTIONALITY: 100% preserved, only UI improved with custom cards
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Page configuration - Premium
st.set_page_config(
    page_title="ConfusionGuard AI | Medication Safety",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/precious-05/MediNomix',
        'Report a bug': "https://github.com/yourusername/MediNomix/issues",
        'About': "### MediNomix AI v3.0\nMedication Safety Platform"
    }
)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Enhanced Color Scheme - Premium Healthcare
COLORS = {
    "primary": "#4F46E5",        # Indigo (from your button)
    "secondary": "#3EBAB4",      # Healthcare Green
    "accent": "#7C3AED",         # Purple accent
    "critical": "#CF19C6",       # Red
    "high": "#F59E0B",           # Orange
    "medium": "#833BF6",         # Blue
    "low": "#10B981",            # Green
    "background": "#F8FAFC",     # Light gray
    "surface": "#FFFFFF",        # White
    "text_primary": "#1E293B",   # Dark gray
    "text_secondary": "#64748B", # Medium gray
}

# Updated Online Image URLs (using reliable sources)
MEDICAL_ICONS = {
    "logo": "https://img.icons8.com/color/96/000000/medical-history.png",
    "dashboard": "https://img.icons8.com/color/96/000000/dashboard.png",
    "search": "https://img.icons8.com/color/96/000000/search--v1.png",
    "analysis": "https://img.icons8.com/color/96/000000/data-configuration.png",
    "alert": "https://img.icons8.com/color/96/000000/high-risk.png",
    "pharmacy": "https://img.icons8.com/color/96/000000/medicine-bottle.png",
    "stats": "https://img.icons8.com/color/96/000000/statistics.png",
    "safety": "https://img.icons8.com/color/96/000000/security-checked.png",
    "fda": "https://img.icons8.com/color/96/000000/fda-approval.png",
    "hospital": "https://img.icons8.com/color/96/000000/hospital.png",
}

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
            st.success("✅ Database seeded successfully!")
            return True
        else:
            st.error("❌Failed to seed database")
            return False
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
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
    """Create interactive drug confusion heatmap - Premium Design"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Enhanced heatmap with premium styling
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS["low"]],
            [0.3, COLORS["low"]],
            [0.4, COLORS["medium"]],
            [0.6, COLORS["high"]],
            [0.8, COLORS["critical"]],
            [1, "#B91C1C"]
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
            "text": "📊 Drug Confusion Risk Heatmap",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 24, "color": COLORS["text_primary"], "family": "Inter"}
        },
        xaxis_title="<b>Drug Names</b>",
        yaxis_title="<b>Drug Names</b>",
        height=650,
        margin={"t": 100, "b": 100, "l": 120, "r": 50},
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text_primary"]),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10),
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            gridcolor='rgba(0,0,0,0.05)'
        )
    )
    
    # Add annotations for high-risk cells
    for i in range(len(drug_names)):
        for j in range(len(drug_names)):
            if risk_matrix[i][j] > 70:
                fig.add_annotation(
                    x=j, y=i,
                    text="⚠️",
                    showarrow=False,
                    font=dict(size=14, color="white"),
                    xref="x",
                    yref="y"
                )
    
    return fig

def create_risk_breakdown_chart():
    """Create enhanced risk breakdown donut chart"""
    if 'breakdown' not in st.session_state.dashboard_data:
        return None
    
    breakdown = st.session_state.dashboard_data['breakdown']
    if not breakdown:
        return None
    
    categories = [item['category'].title() for item in breakdown]
    counts = [item['count'] for item in breakdown]
    
    color_map = {
        "Critical": COLORS["critical"],
        "High": COLORS["high"],
        "Medium": COLORS["medium"],
        "Low": COLORS["low"]
    }
    colors = [color_map.get(cat, COLORS["medium"]) for cat in categories]
    
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
            textfont=dict(size=13, color="white"),
            marker=dict(line=dict(color=COLORS["surface"], width=2))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "📈 Risk Distribution",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": COLORS["text_primary"], "family": "Inter"}
        },
        height=450,
        margin=dict(t=80, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05,
            font=dict(size=12, family="Inter")
        ),
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text_primary"]),
    )
    
    # Add center text
    fig.add_annotation(
        text=f"<b>Total</b><br>{sum(counts)}",
        x=0.5, y=0.5,
        font=dict(size=16, color=COLORS["text_primary"], family="Inter"),
        showarrow=False
    )
    
    return fig

def create_top_risks_chart():
    """Create enhanced top risks horizontal bar chart"""
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
        "critical": COLORS["critical"],
        "high": COLORS["high"],
        "medium": COLORS["medium"],
        "low": COLORS["low"]
    }
    colors = [color_map.get(cat.lower(), COLORS["medium"]) for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color=colors,
            text=[f"{score:.0f}%" for score in scores],
            textposition='outside',
            textfont=dict(size=11, color=COLORS["text_primary"], family="Inter"),
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><br>Category: %{customdata[0]}<br>%{customdata[1]}<extra></extra>",
            customdata=list(zip(categories, reasons)),
            marker=dict(line=dict(color=COLORS["surface"], width=1))
        )
    ])
    
    fig.update_layout(
        title={
            "text": "⚠️ Top 10 High-Risk Drug Pairs",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 22, "color": COLORS["text_primary"], "family": "Inter"}
        },
        xaxis_title="<b>Risk Score (%)</b>",
        yaxis_title="<b>Drug Pairs</b>",
        height=500,
        margin=dict(t=80, b=50, l=220, r=50),
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text_primary"]),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            range=[0, 105]
        ),
        yaxis=dict(
            tickfont=dict(size=11, family="Inter"),
            categoryorder='total ascending'
        )
    )
    
    # Add threshold lines
    fig.add_vline(x=75, line_dash="dash", line_color=COLORS["critical"], opacity=0.3)
    fig.add_vline(x=50, line_dash="dash", line_color=COLORS["high"], opacity=0.3)
    fig.add_vline(x=25, line_dash="dash", line_color=COLORS["medium"], opacity=0.3)
    
    return fig

# Premium CSS Styling with Custom Cards (Uiverse Style)
st.markdown(f"""
<style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Modern Professional Theme */
    .stApp {{
        background-color: {COLORS["background"]};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Header Styling */
    .main-header {{
        font-size: 3rem;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }}
    
    .sub-header {{
        color: {COLORS["text_secondary"]};
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }}
    
    /* NEW: Uiverse Card Styling (Adapted) */
    .metric-card {{
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 24px;
        line-height: 1.6;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        background: transparent;
        min-height: 180px;
        width: 100%;
    }}
    
    .metric-content {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 16px;
        padding: 28px;
        border-radius: 22px;
        color: #ffffff;
        overflow: hidden;
        background: {COLORS["primary"]};
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        width: 100%;
        height: 100%;
        text-align: center;
    }}
    
    .metric-content::before {{
        position: absolute;
        content: "";
        top: -4%;
        left: 50%;
        width: 90%;
        height: 90%;
        transform: translate(-50%);
        background: rgba(79, 70, 229, 0.2);
        z-index: -1;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }}
    
    .metric-content::after {{
        position: absolute;
        content: "";
        top: -8%;
        left: 50%;
        width: 80%;
        height: 80%;
        transform: translate(-50%);
        background: rgba(79, 70, 229, 0.1);
        z-index: -2;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }}
    
    .metric-card:hover {{
        transform: translateY(-8px);
    }}
    
    .metric-card:hover .metric-content::before {{
        rotate: -8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
    
    .metric-card:hover .metric-content::after {{
        rotate: 8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
    
    /* Card Variations based on color */
    .metric-card-primary .metric-content {{
        background: {COLORS["primary"]};
    }}
    .metric-card-primary .metric-content::before {{
        background: rgba(79, 70, 229, 0.2);
    }}
    .metric-card-primary .metric-content::after {{
        background: rgba(79, 70, 229, 0.1);
    }}
    
    .metric-card-secondary .metric-content {{
        background: {COLORS["secondary"]};
    }}
    .metric-card-secondary .metric-content::before {{
        background: rgba(5, 150, 105, 0.2);
    }}
    .metric-card-secondary .metric-content::after {{
        background: rgba(5, 150, 105, 0.1);
    }}
    
    .metric-card-accent .metric-content {{
        background: {COLORS["accent"]};
    }}
    .metric-card-accent .metric-content::before {{
        background: rgba(124, 58, 237, 0.2);
    }}
    .metric-card-accent .metric-content::after {{
        background: rgba(124, 58, 237, 0.1);
    }}
    
    /* Risk Card Styling - Uiverse Inspired */
    .risk-card {{
        position: relative;
        display: flex;
        flex-direction: column;
        border-radius: 24px;
        line-height: 1.6;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        background: transparent;
        margin-bottom: 1.5rem;
        width: 100%;
        min-height: 180px;
    }}
    
    .risk-content {{
        display: flex;
        flex-direction: column;
        padding: 28px;
        border-radius: 22px;
        color: #ffffff;
        overflow: hidden;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        width: 100%;
        height: 100%;
        position: relative;
    }}
    
    .risk-content::before {{
        position: absolute;
        content: "";
        top: -4%;
        left: 50%;
        width: 90%;
        height: 90%;
        transform: translate(-50%);
        z-index: -1;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        opacity: 0.3;
    }}
    
    .risk-content::after {{
        position: absolute;
        content: "";
        top: -8%;
        left: 50%;
        width: 80%;
        height: 80%;
        transform: translate(-50%);
        z-index: -2;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        opacity: 0.2;
    }}
    
    .risk-card:hover {{
        transform: translateY(-8px);
    }}
    
    .risk-card:hover .risk-content::before {{
        rotate: -8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
    
    .risk-card:hover .risk-content::after {{
        rotate: 8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
    
    /* Risk Card Color Variations */
    .risk-card.critical .risk-content {{
        background: {COLORS["critical"]};
    }}
    .risk-card.critical .risk-content::before {{
        background: {COLORS["critical"]};
    }}
    .risk-card.critical .risk-content::after {{
        background: {COLORS["critical"]};
    }}
    
    .risk-card.high .risk-content {{
        background: {COLORS["high"]};
    }}
    .risk-card.high .risk-content::before {{
        background: {COLORS["high"]};
    }}
    .risk-card.high .risk-content::after {{
        background: {COLORS["high"]};
    }}
    
    .risk-card.medium .risk-content {{
        background: {COLORS["medium"]};
    }}
    .risk-card.medium .risk-content::before {{
        background: {COLORS["medium"]};
    }}
    .risk-card.medium .risk-content::after {{
        background: {COLORS["medium"]};
    }}
    
    .risk-card.low .risk-content {{
        background: {COLORS["low"]};
    }}
    .risk-card.low .risk-content::before {{
        background: {COLORS["low"]};
    }}
    .risk-card.low .risk-content::after {{
        background: {COLORS["low"]};
    }}
    
    /* CUSTOM BUTTON STYLING - From your Uiverse design */
    .stButton > button {{
        position: relative !important;
        padding: 14px 32px !important;
        border: none !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        overflow: hidden !important;
        font-family: 'Inter', sans-serif !important;
        isolation: isolate !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        
        /* Background gradient */
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #6366f1 100%) !important;
        color: #fff !important;
        
        /* Shadows */
        box-shadow: 
            0 2px 4px rgba(79, 70, 229, 0.1),
            0 4px 8px rgba(79, 70, 229, 0.1),
            0 -1px 2px rgba(79, 70, 229, 0.05) !important;
    }}
    
    /* Button hover effects */
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 
            0 4px 8px rgba(79, 70, 229, 0.2),
            0 8px 16px rgba(79, 70, 229, 0.2),
            0 -2px 4px rgba(79, 70, 229, 0.1) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #6366f1 100%) !important;
        filter: brightness(1.1) !important;
    }}
    
    /* Button active effects */
    .stButton > button:active {{
        transform: translateY(1px) !important;
        box-shadow: 
            0 1px 2px rgba(79, 70, 229, 0.1) !important;
    }}
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {{
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, {COLORS["background"]} 100%) !important;
        color: {COLORS["text_primary"]} !important;
        border: 2px solid {COLORS["primary"]} !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, {COLORS["primary"]}15 0%, {COLORS["primary"]}10 100%) !important;
        border-color: {COLORS["accent"]} !important;
        color: {COLORS["primary"]} !important;
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {COLORS["surface"]};
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        font-family: 'Inter', sans-serif;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 60px;
        padding: 0 24px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        font-family: 'Inter', sans-serif;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(79, 70, 229, 0.1) !important;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {COLORS["surface"]};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Input Styling */
    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        padding: 12px 16px;
        font-size: 16px;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }}
    
    /* Metric Value Styling */
    .metric-value {{
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        font-family: 'Inter', sans-serif;
        margin: 5px 0;
        color: white !important;
    }}
    
    .metric-label {{
        font-size: 0.9rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Inter', sans-serif;
        margin-bottom: 8px;
    }}
    
    .metric-help {{
        font-size: 0.8rem !important;
        color: rgba(255, 255, 255, 0.7) !important;
        font-family: 'Inter', sans-serif;
        margin-top: 5px;
    }}
    
    /* Divider */
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS["primary"]} 20%, {COLORS["primary"]} 80%, transparent);
        margin: 2rem 0;
        opacity: 0.3;
    }}
    
    /* Badge Styling */
    .risk-badge {{
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-family: 'Inter', sans-serif;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* Info Box */
    .info-box {{
        background: linear-gradient(135deg, {COLORS["primary"]}15 0%, {COLORS["accent"]}15 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid {COLORS["primary"]};
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Premium Section Header */
    .section-header {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Shine animation for buttons */
    @keyframes shine {{
        from {{
            transform: translateX(-100%) rotate(45deg);
        }}
        to {{
            transform: translateX(100%) rotate(45deg);
        }}
    }}
    
    /* Custom shine effect for primary buttons */
    .stButton > button:before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 50%;
        height: 100%;
        background: linear-gradient(
            to right,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transform: translateX(-100%) rotate(45deg);
        z-index: 1;
    }}
    
    .stButton > button:hover:before {{
        animation: shine 1s ease;
    }}
    
    /* About Section Cards */
    .about-card {{
        position: relative;
        display: flex;
        flex-direction: column;
        border-radius: 24px;
        line-height: 1.6;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        background: transparent;
        width: 100%;
        min-height: 250px;
    }}
    
    .about-content {{
        display: flex;
        flex-direction: column;
        padding: 32px;
        border-radius: 22px;
        color: #ffffff;
        overflow: hidden;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        width: 100%;
        height: 100%;
        text-align: left;
    }}
    
    .about-content::before {{
        position: absolute;
        content: "";
        top: -4%;
        left: 50%;
        width: 90%;
        height: 90%;
        transform: translate(-50%);
        z-index: -1;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        opacity: 0.3;
    }}
    
    .about-content::after {{
        position: absolute;
        content: "";
        top: -8%;
        left: 50%;
        width: 80%;
        height: 80%;
        transform: translate(-50%);
        z-index: -2;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        opacity: 0.2;
    }}
    
    .about-card:hover {{
        transform: translateY(-8px);
    }}
    
    .about-card:hover .about-content::before {{
        rotate: -8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
    
    .about-card:hover .about-content::after {{
        rotate: 8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
    
    .about-card-problem .about-content {{
        background: {COLORS["critical"]};
    }}
    .about-card-problem .about-content::before {{
        background: {COLORS["critical"]};
    }}
    .about-card-problem .about-content::after {{
        background: {COLORS["critical"]};
    }}
    
    .about-card-solution .about-content {{
        background: {COLORS["secondary"]};
    }}
    .about-card-solution .about-content::before {{
        background: {COLORS["secondary"]};
    }}
    .about-card-solution .about-content::after {{
        background: {COLORS["secondary"]};
    }}
    
    /* Step Cards */
    .step-card {{
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        border-radius: 24px;
        line-height: 1.6;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        background: transparent;
        width: 100%;
        min-height: 220px;
    }}
    
    .step-content {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        padding: 28px;
        border-radius: 22px;
        color: #ffffff;
        overflow: hidden;
        background: {COLORS["accent"]};
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        width: 100%;
        height: 100%;
        text-align: center;
    }}
    
    .step-content::before {{
        position: absolute;
        content: "";
        top: -4%;
        left: 50%;
        width: 90%;
        height: 90%;
        transform: translate(-50%);
        background: rgba(124, 58, 237, 0.2);
        z-index: -1;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }}
    
    .step-content::after {{
        position: absolute;
        content: "";
        top: -8%;
        left: 50%;
        width: 80%;
        height: 80%;
        transform: translate(-50%);
        background: rgba(124, 58, 237, 0.1);
        z-index: -2;
        transform-origin: bottom;
        border-radius: inherit;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }}
    
    .step-card:hover {{
        transform: translateY(-8px);
    }}
    
    .step-card:hover .step-content::before {{
        rotate: -8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
    
    .step-card:hover .step-content::after {{
        rotate: 8deg;
        top: 0;
        width: 100%;
        height: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# Premium Header with Logo
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <img src='{MEDICAL_ICONS["logo"]}' width='90' style='margin-bottom: 15px;'>
        <div class='main-header'>ConfusionGuard AI</div>
        <div class='sub-header'>Advanced Medication Safety Platform</div>
    </div>
    """, unsafe_allow_html=True)

# Premium Action Buttons
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <div style='display: inline-flex; gap: 15px; background: white; padding: 15px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);'>
""", unsafe_allow_html=True)

action_cols = st.columns([1, 1, 1, 1, 1])
with action_cols[0]:
    if st.button("📥 **Seed Database**", use_container_width=True, type="secondary"):
        with st.spinner("Seeding database with sample drugs..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()
with action_cols[1]:
    if st.button("🔄 **Refresh Data**", use_container_width=True, type="secondary"):
        with st.spinner("Refreshing dashboard data..."):
            load_dashboard_data()
            st.rerun()
with action_cols[2]:
    if st.button("🧪 **Quick Demo**", use_container_width=True):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
with action_cols[3]:
    if st.button("📊 **View Stats**", use_container_width=True, type="secondary"):
        load_dashboard_data()
        st.rerun()
with action_cols[4]:
    if st.button("🆘 **Get Help**", use_container_width=True, type="secondary"):
        st.info("💡 **Quick Tips:**\n1. Search any drug name to analyze confusion risks\n2. Use the heatmap to visualize risk patterns\n3. Check FDA alerts for known dangerous pairs")

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Premium Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🔍 **Drug Analysis**", 
    "📊 **Analytics Dashboard**", 
    "🏥 **About & Resources**"
])

with tab1:
    # Premium Search Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <img src='{MEDICAL_ICONS["search"]}' width='70' style='margin-bottom: 15px;'>
            <h2 class='section-header'>Drug Confusion Risk Analysis</h2>
            <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
                Enter a drug name to analyze potential confusion risks with other medications
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Premium Search Bar
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        drug_name = st.text_input(
            "",
            placeholder="🔍 Enter drug name (e.g., metformin, lamictal, celebrex...)",
            label_visibility="collapsed",
            key="search_input"
        )
        
        # Premium Search Buttons
        search_cols = st.columns([1, 1])
        with search_cols[0]:
            search_clicked = st.button("**🔬 Analyze Drug**", use_container_width=True, type="primary")
        with search_cols[1]:
            if st.button("**💡 Show Examples**", use_container_width=True, type="secondary"):
                examples = ["metformin", "lamictal", "celebrex", "clonidine", "zyprexa"]
                st.info(f"**Try these drugs:** {', '.join(examples)}")
    
    if search_clicked and drug_name:
        with st.spinner(f"🔍 Analyzing '{drug_name}' for confusion risks..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"Analysis complete! Found {len(st.session_state.search_results)} similar drugs.")
                st.balloons()
                st.rerun()
    
    # Results Section
    if st.session_state.search_results:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Premium Risk Filter Buttons
        st.markdown("### 📋 Filter Results")
        risk_filters = {
            "📊 All Risks": "all",
            "🔴 Critical (≥75%)": "critical",
            "🟠 High (50-74%)": "high",
            "🔵 Medium (25-49%)": "medium",
            "🟢 Low (<25%)": "low"
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
        
        # Premium Results Header
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS["primary"]}15, {COLORS["accent"]}15); 
                    padding: 1.5rem; border-radius: 16px; margin: 1.5rem 0;'>
            <h3 style='color: {COLORS["text_primary"]}; margin: 0; font-size: 1.5rem;'>
                📄 Found {len(filtered_results)} Similar Drugs
            </h3>
            <p style='color: {COLORS["text_secondary"]}; margin: 5px 0 0 0;'>
                Displaying {'all' if st.session_state.selected_risk == 'all' else st.session_state.selected_risk} risk levels
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # NEW: Premium Uiverse Style Drug Cards
        for idx, result in enumerate(filtered_results):
            risk_class = result['risk_category']
            
            with st.container():
                # Card Container
                st.markdown(f"""
                <div class='risk-card {risk_class}'>
                    <div class='risk-content'>
                        <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 20px;'>
                            <div>
                                <h3 style='color: white; margin-bottom: 8px; font-size: 1.4rem;'>
                                    💊 {result['target_drug']['brand_name']}
                                </h3>
                                <p style='color: rgba(255, 255, 255, 0.9); margin: 0; font-style: italic; font-size: 0.95rem;'>
                                    {result['target_drug']['generic_name'] if result['target_drug']['generic_name'] else 'Generic name not available'}
                                </p>
                            </div>
                            <div style='text-align: right;'>
                                <div class='risk-badge'>
                                    {risk_class.upper()}
                                </div>
                                <div style='margin-top: 10px; font-size: 2.2rem; font-weight: 800; color: white;'>
                                    {result['combined_risk']:.0f}%
                                </div>
                            </div>
                        </div>
                        
                        <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 15px;'>
                """, unsafe_allow_html=True)
                
                # Premium Metrics Grid
                metrics = [
                    ("Spelling Similarity", f"{result['spelling_similarity']:.1f}%", "📝"),
                    ("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%", "🔊"),
                    ("Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%", "🏥"),
                    ("Overall Risk", f"{result['combined_risk']:.1f}%", "⚠️")
                ]
                
                for label, value, icon in metrics:
                    st.markdown(f"""
                    <div style='background: rgba(255, 255, 255, 0.15); padding: 12px; border-radius: 10px; text-align: center; backdrop-filter: blur(5px);'>
                        <div style='font-size: 0.85rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 5px;'>{icon} {label}</div>
                        <div style='font-size: 1.3rem; font-weight: 700; color: white;'>{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div></div>", unsafe_allow_html=True)
                
                # Additional Details
                with st.expander("📋 View Drug Details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        if result['target_drug']['purpose']:
                            st.markdown("**Purpose:**")
                            st.info(result['target_drug']['purpose'][:200] + "..." if len(result['target_drug']['purpose']) > 200 else result['target_drug']['purpose'])
                    with col2:
                        if result['target_drug']['manufacturer']:
                            st.markdown("**Manufacturer:**")
                            st.text(result['target_drug']['manufacturer'])
                
                st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

with tab2:
    # Premium Dashboard
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <img src='{MEDICAL_ICONS["dashboard"]}' width='70' style='margin-bottom: 15px;'>
        <h2 class='section-header'>Medication Safety Analytics</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
            Real-time insights into drug confusion risks and patterns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # NEW: Premium Uiverse Style Metrics Cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        metric_cols = st.columns(4)
        
        metric_data = [
            ("Total Drugs", metrics.get('total_drugs', 0), "💊", "metric-card-primary", "Total medications in database"),
            ("High/Critical Pairs", metrics.get('high_risk_pairs', 0), "⚠️", "metric-card-accent", "Pairs requiring attention"),
            ("Critical Pairs", metrics.get('critical_risk_pairs', 0), "🔥", "metric-card-primary", "Extreme risk pairs"),
            ("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%", "📈", "metric-card-secondary", "Average confusion risk")
        ]
        
        for col, (title, value, icon, card_class, help_text) in zip(metric_cols, metric_data):
            with col:
                st.markdown(f"""
                <div class='metric-card {card_class}'>
                    <div class='metric-content'>
                        <div class='metric-label'>{icon} {title}</div>
                        <div class='metric-value'>{value}</div>
                        <div class='metric-help'>{help_text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Heatmap Section
    st.markdown("### 🔥 Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown("""
        <div class='info-box'>
            <p style='margin: 0;'><b>How to read this heatmap:</b> Each cell shows confusion risk between two drugs. 
            Red cells indicate high risk (>75%), yellow cells show moderate risk (25-75%), 
            and green cells indicate low risk (<25%). Hover over any cell for detailed information.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("📭 No heatmap data available. Search for drugs or seed the database first.")
    
    # Premium Charts Section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Risk Analytics")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 📈 Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available.")
    
    with chart_col2:
        st.markdown("#### ⚠️ Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available.")
    
    # FDA Alert Table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🚨 FDA High Alert Drug Pairs")
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "🔴 Critical", 
         "Medical Use": "Epilepsy vs Fungal infection", "Alert Type": "FDA Safety Warning", "Year": "2023"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "🔴 Critical", 
         "Medical Use": "Arthritis vs Depression", "Alert Type": "ISMP High Alert", "Year": "2023"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "🟠 High", 
         "Medical Use": "Diabetes vs Antibiotic", "Alert Type": "Common Error", "Year": "2022"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "🟠 High", 
         "Medical Use": "Blood pressure vs Anxiety", "Alert Type": "Sound-alike", "Year": "2022"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "🔵 Medium", 
         "Medical Use": "Antipsychotic vs Allergy", "Alert Type": "Look-alike", "Year": "2021"},
        {"Drug 1": "Hydrocodone", "Drug 2": "Oxycodone", "Risk Level": "🔴 Critical", 
         "Medical Use": "Pain medication", "Alert Type": "FDA Black Box", "Year": "2023"},
    ])
    
    # Enhanced DataFrame Display
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk Level": st.column_config.TextColumn("Risk", width="small"),
            "Alert Type": st.column_config.TextColumn("Alert", width="medium"),
            "Year": st.column_config.NumberColumn("Year", width="small")
        }
    )

with tab3:
    # Premium About Section
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <img src='{MEDICAL_ICONS["hospital"]}' width='70' style='margin-bottom: 15px;'>
        <h2 class='section-header'>About ConfusionGuard AI</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
            A healthcare safety platform designed to prevent medication errors through advanced analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics - Uiverse Style Cards
    metric_cols = st.columns(3)
    metric_data = [
        ("Medication Errors", "25%", "involve name confusion", "metric-card-primary"),
        ("Annual Harm", "1.5M", "Americans affected", "metric-card-accent"),
        ("Annual Cost", "$42B", "preventable expenses", "metric-card-secondary")
    ]
    
    for col, (title, value, desc, card_class) in zip(metric_cols, metric_data):
        with col:
            st.markdown(f"""
            <div class='metric-card {card_class}'>
                <div class='metric-content'>
                    <div class='metric-label'>{title}</div>
                    <div class='metric-value'>{value}</div>
                    <div class='metric-help'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Problem & Solution Cards - Uiverse Style
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='about-card about-card-problem'>
            <div class='about-content'>
                <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                    <img src='{MEDICAL_ICONS["alert"]}' width='40' style='margin-right: 15px;'>
                    <h3 style='color: white; margin: 0; font-size: 1.4rem;'>The Problem</h3>
                </div>
                <ul style='padding-left: 20px; margin: 0; color: rgba(255, 255, 255, 0.95);'>
                    <li><b>25% of medication errors</b> involve name confusion (FDA)</li>
                    <li><b>1.5 million Americans</b> harmed annually</li>
                    <li><b>$42 billion</b> in preventable costs</li>
                    <li>Common pairs: <b>Lamictal↔Lamisil</b>, <b>Celebrex↔Celexa</b></li>
                    <li>Current EHR systems offer <b>basic alerts only</b></li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='about-card about-card-solution'>
            <div class='about-content'>
                <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                    <img src='{MEDICAL_ICONS["safety"]}' width='40' style='margin-right: 15px;'>
                    <h3 style='color: white; margin: 0; font-size: 1.4rem;'>Our Solution</h3>
                </div>
                <ul style='padding-left: 20px; margin: 0; color: rgba(255, 255, 255, 0.95);'>
                    <li><b>Real-time FDA data</b> analysis</li>
                    <li><b>Multi-algorithm</b> risk scoring</li>
                    <li><b>Interactive visualizations</b> and heatmaps</li>
                    <li><b>Actionable safety</b> recommendations</li>
                    <li><b>Healthcare professional</b> focused design</li>
                    <li><b>Context-aware</b> similarity detection</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works - Uiverse Style Step Cards
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🔄 How It Works")
    
    steps_cols = st.columns(4)
    step_data = [
        ("1", "🔍", "Search", "Enter drug name", "User inputs any medication name for analysis"),
        ("2", "⚙️", "Analyze", "Calculate risks", "Advanced algorithms assess multiple similarity factors"),
        ("3", "📊", "Visualize", "View results", "Interactive charts, heatmaps, and risk scores"),
        ("4", "🛡️", "Prevent", "Take action", "Safety alerts and prevention recommendations")
    ]
    
    for col, (num, icon, title, subtitle, desc) in zip(steps_cols, step_data):
        with col:
            st.markdown(f"""
            <div class='step-card'>
                <div class='step-content'>
                    <div style='font-size: 2.8rem; margin-bottom: 5px;'>{icon}</div>
                    <div style='background: rgba(255, 255, 255, 0.2); color: white; width: 36px; height: 36px; border-radius: 50%; 
                         display: flex; align-items: center; justify-content: center;
                         font-weight: bold; margin-bottom: 15px; font-size: 1.2rem;'>{num}</div>
                    <h4 style='color: white; margin: 5px 0; font-size: 1.2rem;'>{title}</h4>
                    <p style='color: rgba(255, 255, 255, 0.9); margin: 5px 0; font-size: 0.9rem; font-weight: 500;'>{subtitle}</p>
                    <p style='color: rgba(255, 255, 255, 0.8); font-size: 0.85rem; margin-top: 5px;'>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Premium Sidebar
with st.sidebar:
    # Logo and Title
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem 0;'>
        <img src='{MEDICAL_ICONS["logo"]}' width='80' style='margin-bottom: 10px;'>
        <h3 style='color: {COLORS["text_primary"]}; margin: 5px 0; font-family: Inter;'>ConfusionGuard AI</h3>
        <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; font-family: Inter;'>Medication Safety Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Quick Actions with Custom Buttons
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🧪 Test with Metformin", use_container_width=True, type="primary"):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
    
    if st.button("📥 Load Sample Data", use_container_width=True, type="secondary"):
        if seed_database():
            load_dashboard_data()
            st.rerun()
    
    if st.button("🔄 Force Refresh", use_container_width=True, type="secondary"):
        load_dashboard_data()
        st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Backend Status
    st.markdown("### ⚙️ System Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.success("✅ **Backend Connected**")
                status_cols = st.columns(2)
                with status_cols[0]:
                    st.metric("Drugs", data.get('drugs_in_database', 0))
                with status_cols[1]:
                    st.metric("Risks", data.get('risk_assessments', 0))
            else:
                st.error("❌ Backend Error")
        else:
            st.error("❌ Cannot Connect")
    except:
        st.error("🔌 **Backend Not Running**")
        st.markdown("""
        <div style='background: rgba(220, 38, 38, 0.1); padding: 10px; border-radius: 8px; margin-top: 10px;'>
            <p style='margin: 0; font-size: 0.9rem;'>
            <b>Fix:</b> Run in terminal:<br>
            <code>python backend.py</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Risk Categories Guide
    st.markdown("### 📈 Risk Categories")
    
    risk_categories = [
        ("🔴 Critical", "≥75%", "Immediate intervention required", COLORS["critical"]),
        ("🟠 High", "50-74%", "Review and verification needed", COLORS["high"]),
        ("🔵 Medium", "25-49%", "Monitor closely", COLORS["medium"]),
        ("🟢 Low", "<25%", "Low priority", COLORS["low"])
    ]
    
    for icon, range_, desc, color in risk_categories:
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <div style='width: 12px; height: 12px; background-color: {color}; border-radius: 50%; margin-right: 10px;'></div>
            <div>
                <div style='font-weight: 600; color: {COLORS["text_primary"]};'>{icon} {range_}</div>
                <div style='font-size: 0.85rem; color: {COLORS["text_secondary"]};'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Premium Footer
st.markdown("""
<style>
.premium-footer {
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
    border-top: 1px solid rgba(0,0,0,0.1);
    color: #64748B;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
}
.premium-footer a {
    color: #4F46E5;
    text-decoration: none;
    font-weight: 600;
}
.premium-footer a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='premium-footer'>
    <div style='display: flex; justify-content: center; gap: 30px; margin-bottom: 15px;'>
        <div><img src='{MEDICAL_ICONS["fda"]}' width='20' style='vertical-align: middle; margin-right: 8px;'> <b>FDA OpenFDA API</b> • Real-time data</div>
        <div><img src='{MEDICAL_ICONS["safety"]}' width='20' style='vertical-align: middle; margin-right: 8px;'> <b>Patient Safety First</b> • Healthcare focused</div>
        <div><b>Last Updated</b>: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
    </div>
    <div style='margin-top: 10px;'>
        © 2024 ConfusionGuard AI • Version 3.0 • For educational purposes
    </div>
    <div style='margin-top: 10px; font-size: 0.8rem; font-style: italic;'>
        Always consult healthcare professionals for medical decisions. This application is designed to assist, not replace, professional judgment.
    </div>
</div>
""", unsafe_allow_html=True)