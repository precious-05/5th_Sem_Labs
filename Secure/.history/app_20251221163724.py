"""
ConfusionGuard AI - Streamlit Frontend
REDESIGNED with Chain App Dev Template Style
Modern, beautiful interface with gradient design
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Page configuration - Full width, modern look
st.set_page_config(
    page_title="ConfusionGuard AI | Medication Safety",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Color scheme inspired by Chain App Dev template (Ocean Blue Gradient)
COLORS = {
    "gradient_start": "#1a2980",      # Dark Blue
    "gradient_end": "#26d0ce",        # Cyan
    "primary": "#2d5be3",             # Bright Blue
    "secondary": "#00c9ff",           # Light Blue
    "card_bg": "rgba(255, 255, 255, 0.95)",
    "transparent_grid": "rgba(0, 0, 0, 0.02)",
    "text_dark": "#1e3a8a",
    "text_light": "#64748b",
    "critical": "#ef4444",            # Red
    "high": "#f59e0b",                # Orange
    "medium": "#3b82f6",              # Blue
    "low": "#10b981",                 # Green
}

# Apply custom CSS for Chain App Dev template style
st.markdown(f"""
<style>
    /* Main gradient background like Chain App Dev */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['gradient_start']} 0%, {COLORS['gradient_end']} 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }}
    
    /* Beautiful card styling */
    .beautiful-card {{
        background: {COLORS['card_bg']};
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1.5rem;
    }}
    
    .beautiful-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }}
    
    /* Gradient button styling */
    .gradient-button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(45, 91, 227, 0.3);
        text-align: center;
        display: inline-block;
        margin: 5px;
    }}
    
    .gradient-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(45, 91, 227, 0.4);
    }}
    
    .secondary-button {{
        background: transparent;
        color: {COLORS['primary']};
        border: 2px solid {COLORS['primary']};
        padding: 10px 28px;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .secondary-button:hover {{
        background: {COLORS['primary']};
        color: white;
    }}
    
    /* Transparent grid for charts */
    .transparent-grid {{
        background: {COLORS['transparent_grid']};
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }}
    
    /* Modern header styling */
    .modern-header {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0f7fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }}
    
    .modern-subheader {{
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        font-weight: 300;
    }}
    
    /* Section headers */
    .section-header {{
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1.5rem;
        position: relative;
        display: inline-block;
    }}
    
    .section-header::after {{
        content: '';
        position: absolute;
        left: 0;
        bottom: -10px;
        width: 60px;
        height: 4px;
        background: {COLORS['secondary']};
        border-radius: 2px;
    }}
    
    /* Risk cards with beautiful design */
    .risk-card {{
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        border-left: 5px solid;
        transition: all 0.3s ease;
    }}
    
    .risk-card:hover {{
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }}
    
    .critical-card {{ border-left-color: {COLORS['critical']}; }}
    .high-card {{ border-left-color: {COLORS['high']}; }}
    .medium-card {{ border-left-color: {COLORS['medium']}; }}
    .low-card {{ border-left-color: {COLORS['low']}; }}
    
    /* Metric cards */
    .metric-card {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        padding: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        border-radius: 25px;
        padding: 10px 25px;
        background: transparent;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: white !important;
        color: {COLORS['primary']} !important;
        font-weight: 600;
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['secondary']};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['primary']};
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
for key in ['search_results', 'dashboard_data', 'selected_risk', 'heatmap_data']:
    if key not in st.session_state:
        st.session_state[key] = None if key == 'heatmap_data' else ([] if key == 'search_results' else {} if key == 'dashboard_data' else "all")

# Helper functions (SAME FUNCTIONALITY)
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
            st.error("❌ Failed to seed database")
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
    """Create interactive drug confusion heatmap on transparent grid"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Create heatmap with transparent grid background
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS["low"]],
            [0.4, COLORS["medium"]],
            [0.6, COLORS["high"]],
            [1, COLORS["critical"]]
        ],
        zmin=0,
        zmax=100,
        text=[[f"{val:.1f}%" if val > 0 else "" for val in row] for row in risk_matrix],
        texttemplate="%{text}",
        textfont={"size": 10, "color": "#1e3a8a"},
        hoverongaps=False,
        hoverinfo="text",
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>Risk: %{z:.1f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title={
            "text": "Drug Confusion Heatmap",
            "font": {"size": 20, "color": "white", "family": "Arial, sans-serif"}
        },
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        height=600,
        margin={"t": 80, "b": 50, "l": 100, "r": 50},
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        font={"color": "white"},
        xaxis=dict(
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.1)"
        )
    )
    
    return fig

def create_risk_breakdown_chart():
    """Create risk breakdown pie chart on transparent grid"""
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
    
    fig = go.Figure(data=[
        go.Pie(
            labels=categories,
            values=counts,
            hole=0.5,
            marker_colors=colors,
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            textfont={"color": "white", "size": 14}
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Risk Distribution",
            "font": {"size": 20, "color": "white", "family": "Arial, sans-serif"}
        },
        height=450,
        margin=dict(t=80, b=20, l=20, r=20),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",   # Transparent background
        font={"color": "white"}
    )
    
    return fig

def create_top_risks_chart():
    """Create top risks bar chart on transparent grid"""
    if 'top_risks' not in st.session_state.dashboard_data:
        return None
    
    top_risks = st.session_state.dashboard_data['top_risks']
    if not top_risks:
        return None
    
    pairs = [f"{item['drug1']} ↔ {item['drug2']}" for item in top_risks]
    scores = [item['risk_score'] for item in top_risks]
    categories = [item['risk_category'] for item in top_risks]
    
    color_map = {
        "critical": COLORS["critical"],
        "high": COLORS["high"],
        "medium": COLORS["medium"],
        "low": COLORS["low"]
    }
    colors = [color_map.get(cat, COLORS["medium"]) for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scores,
            y=pairs,
            orientation='h',
            marker_color=colors,
            text=[f"{score:.1f}%" for score in scores],
            textposition='outside',
            textfont={"color": "white", "size": 12},
            hovertemplate="<b>%{y}</b><br>Risk Score: %{x:.1f}%<br>Category: %{customdata}<extra></extra>",
            customdata=categories
        )
    ])
    
    fig.update_layout(
        title={
            "text": "Top Risk Pairs",
            "font": {"size": 20, "color": "white", "family": "Arial, sans-serif"}
        },
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=500,
        margin=dict(t=80, b=50, l=200, r=50),
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",   # Transparent background
        font={"color": "white"},
        xaxis=dict(
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.1)"
        )
    )
    
    return fig

# ==================== MAIN UI LAYOUT ====================

# Header with gradient background
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="modern-header">ConfusionGuard AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="modern-subheader">Advanced Medication Safety System • Preventing Errors Through AI Analysis</div>', unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <button class="gradient-button" onclick="window.location.reload()">🔄 Live</button>
    </div>
    """, unsafe_allow_html=True)

# Quick actions in beautiful cards
st.markdown("---")
st.markdown('<div class="section-header">Quick Actions</div>', unsafe_allow_html=True)

action_cols = st.columns(4)
with action_cols[0]:
    with st.container():
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("### 🧪 Test App")
        if st.button("Try with Metformin", use_container_width=True, type="primary"):
            st.session_state.search_results = []
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with action_cols[1]:
    with st.container():
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Load Data")
        if st.button("Seed Database", use_container_width=True, type="primary"):
            if seed_database():
                load_dashboard_data()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with action_cols[2]:
    with st.container():
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Dashboard")
        if st.button("Refresh Analytics", use_container_width=True):
            load_dashboard_data()
            st.success("Dashboard updated!")
        st.markdown('</div>', unsafe_allow_html=True)

with action_cols[3]:
    with st.container():
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Status")
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend Active")
            else:
                st.error("❌ Backend Issue")
        except:
            st.error("🔌 Not Connected")
        st.markdown('</div>', unsafe_allow_html=True)

# Main tabs with beautiful styling
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🔍 **Drug Analysis**", "📊 **Live Dashboard**", "ℹ️ **About System**"])

# TAB 1: DRUG ANALYSIS
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("### 🔬 Analyze Drug Confusion Risk")
        st.markdown("Enter a drug name to identify look-alike/sound-alike medication risks")
        
        drug_input = st.text_input(
            "Drug Name",
            placeholder="Enter brand or generic name...",
            label_visibility="collapsed"
        )
        
        search_cols = st.columns([3, 1])
        with search_cols[0]:
            if st.button("🚀 Start Analysis", use_container_width=True, type="primary"):
                if drug_input:
                    with st.spinner("Analyzing with AI algorithms..."):
                        result = search_drug(drug_input)
                        if result:
                            st.session_state.search_results = result.get('similar_drugs', [])
                            st.rerun()
                else:
                    st.warning("Please enter a drug name")
        
        with search_cols[1]:
            st.markdown("""
            <div style="text-align: center; margin-top: 10px;">
                <small>Try: <strong>metformin</strong>, <strong>lamictal</strong>, <strong>celebrex</strong></small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Quick Stats")
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                st.metric("Total Drugs", data.get('drugs_in_database', 0))
                st.metric("Risk Analyses", data.get('risk_assessments', 0))
                st.metric("Total Checks", data.get('total_analyses', 0))
            else:
                st.info("Connect to backend")
        except:
            st.info("Start backend server")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display search results in beautiful cards
    if st.session_state.search_results:
        st.markdown("---")
        st.markdown(f'<div class="section-header">Analysis Results ({len(st.session_state.search_results)} found)</div>', unsafe_allow_html=True)
        
        # Risk filter buttons as beautiful cards
        filter_cols = st.columns(5)
        risk_filters = {
            "All Risks": "all",
            "🔴 Critical": "critical",
            "🟠 High": "high",
            "🔵 Medium": "medium",
            "🟢 Low": "low"
        }
        
        for i, (label, value) in enumerate(risk_filters.items()):
            with filter_cols[i]:
                if st.button(label, use_container_width=True, type="primary" if value == "all" else "secondary"):
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
        
        # Display each result in a beautiful card
        for result in filtered_results:
            risk_class = result['risk_category']
            card_class = f"{risk_class}-card"
            
            with st.container():
                st.markdown(f'<div class="risk-card {card_class}">', unsafe_allow_html=True)
                
                # Card header
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"##### 💊 **{result['target_drug']['brand_name']}**")
                    if result['target_drug']['generic_name']:
                        st.markdown(f"*{result['target_drug']['generic_name']}*")
                
                with col2:
                    risk_color = COLORS[risk_class]
                    st.markdown(f"""
                    <div style="text-align: right;">
                        <span style="
                            padding: 6px 15px;
                            background: {risk_color};
                            color: white;
                            border-radius: 20px;
                            font-weight: bold;
                            font-size: 0.9rem;
                        ">
                            {risk_class.upper()}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Risk metrics in columns
                cols = st.columns(4)
                metrics = [
                    ("Spelling Similarity", f"{result['spelling_similarity']:.1f}%", "#3b82f6"),
                    ("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%", "#8b5cf6"),
                    ("Context Risk", f"{result['therapeutic_context_risk']:.1f}%", "#06b6d4"),
                    ("Overall Risk", f"{result['combined_risk']:.1f}%", risk_color)
                ]
                
                for col, (label, value, color) in zip(cols, metrics):
                    with col:
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <div style="font-size: 0.9rem; color: #64748b;">{label}</div>
                            <div style="font-size: 1.8rem; font-weight: bold; color: {color};">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Additional info
                if result['target_drug']['purpose']:
                    with st.expander("📋 Purpose & Details"):
                        st.write(result['target_drug']['purpose'])
                        if result['target_drug']['manufacturer']:
                            st.caption(f"**Manufacturer:** {result['target_drug']['manufacturer']}")
                
                st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: DASHBOARD
with tab2:
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Metrics in beautiful cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        metric_cols = st.columns(4)
        
        metric_data = [
            ("Total Drugs", metrics.get('total_drugs', 0), COLORS['primary']),
            ("High/Critical Pairs", metrics.get('high_risk_pairs', 0), COLORS['critical']),
            ("Critical Pairs", metrics.get('critical_risk_pairs', 0), COLORS['critical']),
            ("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%", COLORS['secondary'])
        ]
        
        for col, (title, value, color) in zip(metric_cols, metric_data):
            with col:
                st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 1rem; color: #64748b; margin-bottom: 10px;">{title}</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: {color};">{value}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts on transparent grid
    st.markdown("---")
    st.markdown('<div class="section-header">Interactive Analytics</div>', unsafe_allow_html=True)
    
    # Heatmap (Full width on transparent grid)
    st.markdown('<div class="transparent-grid">', unsafe_allow_html=True)
    st.subheader("🌡️ Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.caption("Interactive heatmap showing confusion risk percentages between drug pairs")
    else:
        st.info("No heatmap data available. Search for drugs or seed database first.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Other charts side by side on transparent grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="transparent-grid">', unsafe_allow_html=True)
        st.subheader("📊 Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="transparent-grid">', unsafe_allow_html=True)
        st.subheader("⚠️ Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Known risky pairs in beautiful table
    st.markdown("---")
    st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
    st.markdown("### 🚨 High-Risk Drug Pairs (FDA Alerts)")
    
    risky_pairs = pd.DataFrame([
        {"Drug Pair": "Lamictal ↔ Lamisil", "Risk": "🔴 Critical", "Description": "Epilepsy vs Fungal infection", "Alert": "FDA Safety Warning"},
        {"Drug Pair": "Celebrex ↔ Celexa", "Risk": "🔴 Critical", "Description": "Arthritis vs Depression", "Alert": "ISMP High Alert"},
        {"Drug Pair": "Metformin ↔ Metronidazole", "Risk": "🟠 High", "Description": "Diabetes vs Antibiotic", "Alert": "Common Error"},
        {"Drug Pair": "Clonidine ↔ Klonopin", "Risk": "🟠 High", "Description": "Blood pressure vs Anxiety", "Alert": "Sound-alike"},
        {"Drug Pair": "Hydrocodone ↔ Oxycodone", "Risk": "🔴 Critical", "Description": "Pain medication", "Alert": "FDA Black Box"},
    ])
    
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Drug Pair": st.column_config.TextColumn("Medication Pair", width="large"),
            "Risk": st.column_config.TextColumn("Risk Level", width="small"),
            "Alert": st.column_config.TextColumn("Alert Type", width="medium")
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: ABOUT SYSTEM
with tab3:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("## 🛡️ About ConfusionGuard AI")
        
        st.markdown("""
        **ConfusionGuard AI** is an advanced healthcare safety system designed to prevent medication errors 
        caused by confusing drug names (look-alike/sound-alike drugs). Our AI-powered platform analyzes 
        drug names in real-time to identify dangerous confusion risks.
        """)
        
        # Problem & Solution side by side
        prob_cols = st.columns(2)
        
        with prob_cols[0]:
            st.markdown("""
            ### 🚨 The Problem
            - **25%** of medication errors involve name confusion
            - **1.5 million** Americans harmed annually  
            - **$42 billion** in preventable costs
            - Common pairs: Lamictal↔Lamisil, Celebrex↔Celexa
            """)
        
        with prob_cols[1]:
            st.markdown("""
            ### 🛡️ Our Solution
            - **Real-time FDA data** analysis
            - **Multi-algorithm** risk scoring
            - **Interactive** visualizations
            - **Actionable** safety recommendations
            - **Healthcare professional** design
            """)
        
        # How it works in beautiful cards
        st.markdown("---")
        st.markdown("### 🚀 How It Works")
        
        steps = st.columns(4)
        step_data = [
            ("1", "🔍", "Search", "Enter drug name for analysis"),
            ("2", "⚙️", "Analyze", "AI algorithms assess similarity"),
            ("3", "📊", "Visualize", "Interactive charts & heatmaps"),
            ("4", "🛡️", "Prevent", "Get safety recommendations")
        ]
        
        for step, (num, icon, title, desc) in zip(steps, step_data):
            with step:
                st.markdown(f"""
                <div style='
                    text-align: center;
                    padding: 20px;
                    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                    border-radius: 15px;
                    color: white;
                    margin-bottom: 10px;
                '>
                    <div style='font-size: 2.5rem; margin-bottom: 10px;'>{icon}</div>
                    <div style='font-size: 1.8rem; font-weight: bold;'>{num}</div>
                </div>
                <div style='text-align: center; padding: 10px;'>
                    <div style='font-weight: bold; font-size: 1.1rem; color: white;'>{title}</div>
                    <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="beautiful-card">', unsafe_allow_html=True)
        st.markdown("### 📈 System Features")
        
        features = [
            ("🔬", "AI-Powered Analysis", "Advanced algorithms"),
            ("📊", "Live Dashboard", "Real-time metrics"),
            ("🌡️", "Heatmap Visualization", "Interactive charts"),
            ("⚠️", "Risk Alerts", "Priority warnings"),
            ("💊", "Drug Database", "FDA-compliant"),
            ("🔄", "Auto-Update", "Live data refresh")
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 10px;">{icon}</span>
                    <div>
                        <div style="font-weight: bold;">{title}</div>
                        <div style="font-size: 0.9rem; color: #64748b;">{desc}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
footer_cols = st.columns(4)
with footer_cols[0]:
    st.markdown("**🩺 Healthcare Focused**")
with footer_cols[1]:
    st.markdown("**🔬 AI-Powered Analysis**")
with footer_cols[2]:
    st.markdown("**📊 Real-time Dashboard**")
with footer_cols[3]:
    st.markdown(f"**🔄 Live: {datetime.now().strftime('%H:%M')}**")

st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.7);">
    <small>© 2024 ConfusionGuard AI | Medication Safety System | For educational purposes. Always consult healthcare professionals.</small>
</div>
""", unsafe_allow_html=True)