"""
MediNomix - Advanced Medication Safety Platform
PROFESSIONAL UI with premium healthcare theme and enhanced visuals
FUNCTIONALITY: 100% preserved, only UI improved
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

# Professional Healthcare AI Theme Colors
COLORS = {
    "primary": "#4F46E5",        # Indigo - Trust & Intelligence
    "secondary": "#3EBAB4",      # Teal - Secondary actions
    "accent": "#7C3AED",         # Purple - AI/ML sophistication
    "critical": "#CF19C6",       # Magenta - Critical risk
    "high": "#F59E0B",           # Orange - High risk
    "medium": "#833BF6",         # Purple-blue - Medium risk
    "low": "#10B981",           # Green - Low risk
    "background": "#F8FAFC",     # Light gray background
    "surface": "#FFFFFF",        # White surfaces
    "text_primary": "#1E293B",   # Dark gray text
    "text_secondary": "#64748B", # Medium gray text
    "border": "rgba(79,70,229,0.08)",  # Soft indigo borders
}

# Reliable Base64 encoded icons (no external dependencies)
ICONS = {
    "logo": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE5IDE0VjIwSDUuMDAwMDFWMTQiIHN0cm9rZT0iIzRGNjBFNSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTEyIDRMMTggMTBINkwxMiA0WiIgc3Ryb2tlPSIjN0MzQUVEIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K",
    "dashboard": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjgiIGhlaWdodD0iOCIgZmlsbD0iIzRGNjBFNSIgcng9IjIiLz4KPHJlY3QgeD0iMTIiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGZpbGw9IiM3QzNBRUQiIHJ4PSIyIi8+CjxyZWN0IHk9IjEyIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiBmaWxsPSIjN0MzQUVEIiByeD0iMiIvPgo8cmVjdCB4PSIxMiIgeT0iMTIiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGZpbGw9IiM0RjYwRTUiIHJ4PSIyIi8+Cjwvc3ZnPgo=",
    "search": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIxIDIxTDE2LjY1NiAxNi42NTZNMjEgMjFDMTkuMzQ2IDIyLjY1NCAxNi43NzEgMjQgMTQgMjRDNy45MjUgMjQgMyAxOS4wNzUgMyAxM0MzIDYuOTI1IDcuOTI1IDIgMTQgMkMyMC4wNzUgMiAyNSA2LjkyNSAyNSAxM0MyNSAxNi43NzEgMjMuNjU0IDE5LjM0NiAyMSAyMVpNMTkgMTNDMTkgOS4xMzQgMTYuODY2IDcgMTQgN1M5IDkuMTM0IDkgMTNTMTEuMTM0IDE5IDE0IDE5QzE2Ljg2NiAxOSAxOSAxNi44NjYgMTkgMTNaIiBzdHJva2U9IiM0RjYwRTUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=",
    "analysis": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgNVYxOUgyMSIgb3BhY2l0eT0iMC41IiBzdHJva2U9IiM0RjYwRTUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xOCAxNEwxNS41IDExTDEzIDE0TDkgMTBIMTgiIHN0cm9rZT0iIzRGNjBFNSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+Cg==",
    "alert": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDlWMTJNMTIgMTZIMTIuMDFNNSA5LjA3MDYzTDUgMTQuOTI5NEM1IDE2LjMwODkgNS44NTg0NyAxNy41NzY3IDcuMTQwNiAxOC4wOTM5TDEwLjg1OTQgMTkuOTE2MUMxMS41NzI3IDIwLjIyMzIgMTIuNDI3MyAyMC4yMjMyIDEzLjE0MDYgMTkuOTE2MUwxNi44NTk0IDE4LjA5MzlDMTguMTQxNSAxNy41NzY3IDE5IDE2LjMwODkgMTkgMTQuOTI5NFY5LjA3MDYzQzE5IDcuNjkxMTEgMTguMTQxNSA2LjQyMzMzIDE2Ljg1OTQgNS45MDYxTDEzLjE0MDYgNC4wODM5M0MxMi40MjczIDMuNzc2NzUgMTEuNTcyNyAzLjc3Njc1IDEwLjg1OTQgNC4wODM5M0w3LjE0MDYgNS45MDYxMUM1Ljg1ODQ3IDYuNDIzMzMgNSA3LjY5MTExIDUgOS4wNzA2M1oiIHN0cm9rZT0iI0NGMTlDNiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+Cg==",
    "stats": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgMTdWMTlIOSIgb3BhY2l0eT0iMC43IiBzdHJva2U9IiM0RjYwRTUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xNSAxMVYxOUgyMSIgb3BhY2l0eT0iMC43IiBzdHJva2U9IiM0RjYwRTUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0zIDEzTDEwIDdMMTYgMTJMMjEgOSIgc3Ryb2tlPSIjN0MzQUVEIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K",
    "safety": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMyA3VjEyQzMgMTcuNTUgNi44NCAyMi43NCAxMiAyM0MxNy4xNiAyMi43NCAyMSAxNy41NSAyMSAxMlY3TDEyIDJaIiBzdHJva2U9IiMxMEI5ODEiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+CjxwYXRoIGQ9Ik05IDEyTDExIDE0TDE1IDEwIiBzdHJva2U9IiMxMEI5ODEiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=",
    "hospital": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgMjJIMjEiIHN0cm9rZT0iIzRGNjBFNSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTQgMTlWM0M0IDIuNDQ3NzIgNC40NDc3MiAyIDUgMkg5QzkuNTUyMjggMiAxMCAyLjQ0NzcyIDEwIDNWMTkiIHN0cm9rZT0iIzRGNjBFNSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTE0IDE5VjNDMTQgMi40NDc3MiAxNC40NDc3IDIgMTUgMkgxOUMxOS41NTIzIDIgMjAgMi40NDc3MiAyMCAzVjE5IiBzdHJva2U9IiM0RjYwRTUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xIDlIMjMiIHN0cm9rZT0iIzRGNjBFNSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+Cg==",
    "ai": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTkgM0g0LjVDNC4yMjM4NiAzIDQgMy4yMjM4NiA0IDMuNVY4LjVDNCA4Ljc3NjE0IDQuMjIzODYgOSA0LjUgOUg5QzkuMjc2MTQgOSA5LjUgOC43NzYxNCA5LjUgOC41VjMuNUM5LjUgMy4yMjM4NiA5LjI3NjE0IDMgOSAzWiIgc3Ryb2tlPSIjN0MzQUVEIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNMTkuNSAzSDE1QzE0LjcyMzkgMyAxNC41IDMuMjIzODYgMTQuNSAzLjVWOC41QzE0LjUgOC43NzYxNCAxNC43MjM5IDkgMTUgOUgxOS41QzE5Ljc3NjEgOSAyMCA4Ljc3NjE0IDIwIDguNVYzLjVDMjAgMy4yMjM4NiAxOS43NzYxIDMgMTkuNSAzWiIgc3Ryb2tlPSIjN0MzQUVEIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNOSAxNUg0LjVDNC4yMjM4NiAxNSA0IDE1LjIyMzkgNCAxNS41VjIwLjVDNCAyMC43NzYxIDQuMjIzODYgMjEgNC41IDIxSDlDOS4yNzYxNCAyMSA5LjUgMjAuNzc2MSA5LjUgMjAuNVYxNS41QzkuNSAxNS4yMjM5IDkuMjc2MTQgMTUgOSAxNVoiIHN0cm9rZT0iIzRGNjBFNSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTE5LjUgMTVIMTVDMTQuNzIzOSAxNSAxNC41IDE1LjIyMzkgMTQuNSAxNS41VjIwLjVDMTQuNSAyMC43NzYxIDE0LjcyMzkgMjEgMTUgMjFIMTkuNUMyMC43NzYxIDIxIDIxIDIwLjc3NjEgMjEgMjAuNVYxNS41QzIxIDE1LjIyMzkgMjAuNzc2MSAxNSAxOS41IDE1WiIgc3Ryb2tlPSIjN0MzQUVEIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K"
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
    """Create interactive drug confusion heatmap - Premium Design"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Enhanced heatmap with professional color scheme
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=drug_names,
        y=drug_names,
        colorscale=[
            [0, COLORS["low"]],
            [0.25, "#3CB371"],  # Medium-low green
            [0.5, COLORS["medium"]],
            [0.75, COLORS["high"]],
            [1, COLORS["critical"]]
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
            "text": "Drug Confusion Risk Heatmap",
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
            "text": "Risk Distribution",
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
            "text": "Top 10 High-Risk Drug Pairs",
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

# Premium CSS Styling with Professional Healthcare Theme
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
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Professional Card Styling */
    .metric-card {{
        background: {COLORS["surface"]};
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(15,23,42,0.06);
        text-align: center;
        border: 1px solid {COLORS["border"]};
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(15,23,42,0.10);
        border-color: {COLORS["primary"]};
    }}
    
    /* Risk Card Styling */
    .risk-card {{
        background: {COLORS["surface"]};
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(15,23,42,0.06);
        margin-bottom: 1.5rem;
        border-left: 6px solid;
        transition: all 0.3s ease;
        border-top: 1px solid {COLORS["border"]};
        font-family: 'Inter', sans-serif;
    }}
    
    .risk-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(15,23,42,0.10);
    }}
    
    .risk-card.critical {{ 
        border-left-color: {COLORS["critical"]};
        background: linear-gradient(90deg, rgba(207,25,198,0.05) 0%, {COLORS["surface"]} 100%);
    }}
    .risk-card.high {{ 
        border-left-color: {COLORS["high"]};
        background: linear-gradient(90deg, rgba(245,158,11,0.05) 0%, {COLORS["surface"]} 100%);
    }}
    .risk-card.medium {{ 
        border-left-color: {COLORS["medium"]};
        background: linear-gradient(90deg, rgba(131,59,246,0.05) 0%, {COLORS["surface"]} 100%);
    }}
    .risk-card.low {{ 
        border-left-color: {COLORS["low"]};
        background: linear-gradient(90deg, rgba(16,185,129,0.05) 0%, {COLORS["surface"]} 100%);
    }}
    
    /* Unified Button Styling */
    .stButton > button {{
        position: relative !important;
        padding: 14px 28px !important;
        border: none !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        overflow: hidden !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        
        /* Unified gradient for all buttons */
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
        color: #fff !important;
        
        /* Professional shadow */
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important;
    }}
    
    /* Button hover effects */
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.25) !important;
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
    }}
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {{
        background: linear-gradient(135deg, {COLORS["surface"]} 0%, {COLORS["background"]} 100%) !important;
        color: {COLORS["primary"]} !important;
        border: 2px solid {COLORS["primary"]} !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.08) !important;
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
        color: white !important;
        border-color: transparent !important;
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
        height: 56px;
        padding: 0 24px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        font-family: 'Inter', sans-serif;
        color: {COLORS["text_secondary"]};
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(79, 70, 229, 0.08) !important;
        color: {COLORS["primary"]} !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["accent"]} 100%) !important;
        color: white !important;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {COLORS["surface"]};
        font-family: 'Inter', sans-serif;
        border-right: 1px solid {COLORS["border"]};
    }}
    
    /* Input Styling */
    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 2px solid {COLORS["border"]};
        padding: 12px 16px;
        font-size: 15px;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s;
        background: {COLORS["surface"]};
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }}
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {{
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Divider */
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS["border"]} 50%, transparent);
        margin: 2rem 0;
    }}
    
    /* Badge Styling */
    .risk-badge {{
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-family: 'Inter', sans-serif;
        display: inline-block;
    }}
    
    /* Info Box */
    .info-box {{
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid {COLORS["primary"]};
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
        border: 1px solid {COLORS["border"]};
    }}
    
    /* Premium Section Header */
    .section-header {{
        color: {COLORS["text_primary"]};
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
    }}
    
    /* AI Highlight */
    .ai-highlight {{
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(79, 70, 229, 0.1));
        border-radius: 8px;
        padding: 2px 8px;
        font-weight: 600;
        color: {COLORS["accent"]};
    }}
    
    /* Grid item styling */
    .grid-item {{
        background: {COLORS["surface"]};
        border-radius: 12px;
        padding: 16px;
        border: 1px solid {COLORS["border"]};
        transition: all 0.3s;
    }}
    
    .grid-item:hover {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
    }}
    
    /* Status indicators */
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }}
    
    .status-healthy {{
        background: rgba(16, 185, 129, 0.1);
        color: {COLORS["low"]};
        border: 1px solid rgba(16, 185, 129, 0.2);
    }}
    
    .status-warning {{
        background: rgba(245, 158, 11, 0.1);
        color: {COLORS["high"]};
        border: 1px solid rgba(245, 158, 11, 0.2);
    }}
    
    .status-critical {{
        background: rgba(207, 25, 198, 0.1);
        color: {COLORS["critical"]};
        border: 1px solid rgba(207, 25, 198, 0.2);
    }}
</style>
""", unsafe_allow_html=True)

# Premium Header with Logo
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <img src='{ICONS["logo"]}' width='80' style='margin-bottom: 15px;'>
        <div class='main-header'>MediNomix</div>
        <div class='sub-header'>AI-Powered Medication Safety Platform</div>
    </div>
    """, unsafe_allow_html=True)

# Professional Action Buttons
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <div style='display: inline-flex; gap: 12px; background: white; padding: 12px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid rgba(79,70,229,0.08);'>
""", unsafe_allow_html=True)

action_cols = st.columns([1, 1, 1, 1])
with action_cols[0]:
    if st.button("**Seed Database**", use_container_width=True, type="secondary"):
        with st.spinner("Seeding database with sample drugs..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()
with action_cols[1]:
    if st.button("**Refresh Data**", use_container_width=True, type="secondary"):
        with st.spinner("Refreshing dashboard data..."):
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
        st.info("**Quick Tips:**\n1. Search any drug name to analyze confusion risks\n2. Use the heatmap to visualize risk patterns\n3. Check FDA alerts for known dangerous pairs")

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Professional Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "**Drug Analysis**", 
    "**Analytics Dashboard**", 
    "**About & Resources**"
])

with tab1:
    # Professional Search Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <img src='{ICONS["search"]}' width='60' style='margin-bottom: 15px;'>
            <h2 class='section-header'>Drug Confusion Risk Analysis</h2>
            <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
                Enter a drug name to analyze potential confusion risks with other medications
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional Search Bar
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        drug_name = st.text_input(
            "",
            placeholder="Enter drug name (e.g., metformin, lamictal, celebrex...)",
            label_visibility="collapsed",
            key="search_input"
        )
        
        # Professional Search Buttons
        search_cols = st.columns([1, 1])
        with search_cols[0]:
            search_clicked = st.button("**Analyze Drug**", use_container_width=True, type="primary")
        with search_cols[1]:
            if st.button("**Show Examples**", use_container_width=True, type="secondary"):
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
        
        # Professional Risk Filter Buttons
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
        
        # Professional Results Header
        st.markdown(f"""
        <div class='info-box'>
            <h3 style='color: {COLORS["text_primary"]}; margin: 0; font-size: 1.4rem;'>
                Found {len(filtered_results)} Similar Drugs
            </h3>
            <p style='color: {COLORS["text_secondary"]}; margin: 8px 0 0 0;'>
                Displaying {'all' if st.session_state.selected_risk == 'all' else st.session_state.selected_risk} risk levels
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional Drug Cards
        for idx, result in enumerate(filtered_results):
            risk_class = result['risk_category']
            risk_color = COLORS[risk_class]
            
            with st.container():
                # Card Container
                st.markdown(f"""
                <div class='risk-card {risk_class}'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div>
                            <h3 style='color: {COLORS["text_primary"]}; margin-bottom: 5px;'>
                                {result['target_drug']['brand_name']}
                            </h3>
                            <p style='color: {COLORS["text_secondary"]}; margin: 0; font-style: italic;'>
                                {result['target_drug']['generic_name'] if result['target_drug']['generic_name'] else 'Generic name not available'}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span class='risk-badge' style='background-color: {risk_color}; color: white;'>
                                {risk_class.upper()}
                            </span>
                            <div style='margin-top: 5px; font-size: 1.8rem; font-weight: 700; color: {risk_color};'>
                                {result['combined_risk']:.0f}%
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Professional Metrics Grid
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
                        <div class='grid-item'>
                            <div style='font-size: 0.85rem; color: {COLORS["text_secondary"]}; margin-bottom: 5px;'>{label}</div>
                            <div style='font-size: 1.3rem; font-weight: 700; color: {COLORS["text_primary"]};'>{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Additional Details
                with st.expander("View Drug Details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        if result['target_drug']['purpose']:
                            st.markdown("**Purpose:**")
                            st.info(result['target_drug']['purpose'][:200] + "..." if len(result['target_drug']['purpose']) > 200 else result['target_drug']['purpose'])
                    with col2:
                        if result['target_drug']['manufacturer']:
                            st.markdown("**Manufacturer:**")
                            st.text(result['target_drug']['manufacturer'])
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

with tab2:
    # Professional Dashboard
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <img src='{ICONS["dashboard"]}' width='60' style='margin-bottom: 15px;'>
        <h2 class='section-header'>Medication Safety Analytics</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
            Real-time insights into drug confusion risks and patterns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Professional Metrics Cards
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        metric_cols = st.columns(4)
        
        metric_data = [
            ("Total Drugs", metrics.get('total_drugs', 0), COLORS["primary"], "Total medications in database"),
            ("High/Critical Pairs", metrics.get('high_risk_pairs', 0), COLORS["critical"], "Pairs requiring attention"),
            ("Critical Pairs", metrics.get('critical_risk_pairs', 0), COLORS["critical"], "Extreme risk pairs"),
            ("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%", COLORS["accent"], "Average confusion risk")
        ]
        
        for col, (title, value, color, help_text) in zip(metric_cols, metric_data):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.9rem; color: {COLORS["text_secondary"]}; margin-bottom: 8px;'>{title}</div>
                    <div style='font-size: 2.2rem; font-weight: 800; color: {color}; margin-bottom: 5px;'>{value}</div>
                    <div style='font-size: 0.8rem; color: {COLORS["text_secondary"]};'>{help_text}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Heatmap Section
    st.markdown("### Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.markdown("""
        <div class='info-box'>
            <p style='margin: 0;'><b>How to read this heatmap:</b> Each cell shows confusion risk between two drugs. 
            Green cells indicate low risk (<25%), purple cells show moderate risk (25-75%), 
            orange cells indicate high risk (50-75%), and magenta cells show critical risk (>75%). 
            Hover over any cell for detailed information.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No heatmap data available. Search for drugs or seed the database first.")
    
    # Professional Charts Section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### Risk Analytics")
    
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
    
    # FDA Alert Table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### FDA High Alert Drug Pairs")
    
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
            "Risk Level": st.column_config.TextColumn("Risk", width="small"),
            "Alert Type": st.column_config.TextColumn("Alert", width="medium"),
            "Year": st.column_config.NumberColumn("Year", width="small")
        }
    )

with tab3:
    # Professional About Section
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <img src='{ICONS["hospital"]}' width='60' style='margin-bottom: 15px;'>
        <h2 class='section-header'>About MediNomix</h2>
        <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem;'>
            A healthcare safety platform designed to prevent medication errors through advanced AI analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Medication Errors", "25%", "involve name confusion", delta_color="inverse")
    with col2:
        st.metric("Annual Harm", "1.5M", "Americans affected", delta_color="inverse")
    with col3:
        st.metric("Annual Cost", "$42B", "preventable expenses", delta_color="inverse")
    
    # Problem & Solution Cards
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left;'>
            <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                <img src='{ICONS["alert"]}' width='32' style='margin-right: 15px;'>
                <h3 style='color: {COLORS["critical"]}; margin: 0;'>The Problem</h3>
            </div>
            <ul style='padding-left: 20px; margin: 0; color: {COLORS["text_primary"]};'>
                <li><b>25% of medication errors</b> involve name confusion (FDA)</li>
                <li><b>1.5 million Americans</b> harmed annually</li>
                <li><b>$42 billion</b> in preventable costs</li>
                <li>Common pairs: <b>Lamictal↔Lamisil</b>, <b>Celebrex↔Celexa</b></li>
                <li>Current EHR systems offer <b>basic alerts only</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left;'>
            <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                <img src='{ICONS["safety"]}' width='32' style='margin-right: 15px;'>
                <h3 style='color: {COLORS["low"]}; margin: 0;'>Our Solution</h3>
            </div>
            <ul style='padding-left: 20px; margin: 0; color: {COLORS["text_primary"]};'>
                <li><b>Real-time FDA data</b> analysis</li>
                <li><b>Multi-algorithm</b> risk scoring</li>
                <li><b>Interactive visualizations</b> and heatmaps</li>
                <li><b>Actionable safety</b> recommendations</li>
                <li><b>Healthcare professional</b> focused design</li>
                <li><b>Context-aware</b> similarity detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### How It Works")
    
    steps_cols = st.columns(4)
    step_data = [
        ("Search", "Enter drug name", "User inputs any medication name for analysis"),
        ("Analyze", "Calculate risks", "Advanced algorithms assess multiple similarity factors"),
        ("Visualize", "View results", "Interactive charts, heatmaps, and risk scores"),
        ("Prevent", "Take action", "Safety alerts and prevention recommendations")
    ]
    
    for col, (title, subtitle, desc) in zip(steps_cols, step_data):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='height: 220px;'>
                <div style='text-align: center;'>
                    <div style='background: linear-gradient(135deg, {COLORS["primary"]}15, {COLORS["accent"]}15); 
                         color: {COLORS["primary"]}; width: 50px; height: 50px; border-radius: 12px; 
                         display: inline-flex; align-items: center; justify-content: center;
                         font-weight: bold; margin-bottom: 20px; font-size: 1.5rem;'>
                         {steps_cols.index(col) + 1}
                    </div>
                    <h4 style='color: {COLORS["text_primary"]}; margin: 10px 0;'>{title}</h4>
                    <p style='color: {COLORS["text_secondary"]}; margin: 5px 0; font-size: 0.9rem; font-weight: 500;'>{subtitle}</p>
                    <p style='color: {COLORS["text_secondary"]}; font-size: 0.85rem; margin-top: 10px;'>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Professional Sidebar
with st.sidebar:
    # Logo and Title
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem 0;'>
        <img src='{ICONS["logo"]}' width='70' style='margin-bottom: 10px;'>
        <h3 style='color: {COLORS["text_primary"]}; margin: 5px 0; font-family: Inter;'>MediNomix</h3>
        <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; font-family: Inter;'>AI-Powered Medication Safety</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Quick Actions with Unified Buttons
    st.markdown("### Quick Actions")
    
    if st.button("Test with Metformin", use_container_width=True, type="primary"):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
    
    if st.button("Load Sample Data", use_container_width=True, type="secondary"):
        if seed_database():
            load_dashboard_data()
            st.rerun()
    
    if st.button("Force Refresh", use_container_width=True, type="secondary"):
        load_dashboard_data()
        st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Backend Status
    st.markdown("### System Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.markdown('<div class="status-indicator status-healthy">✅ Backend Connected</div>', unsafe_allow_html=True)
                status_cols = st.columns(2)
                with status_cols[0]:
                    st.metric("Drugs", data.get('drugs_in_database', 0))
                with status_cols[1]:
                    st.metric("Risks", data.get('risk_assessments', 0))
            else:
                st.markdown('<div class="status-indicator status-warning">⚠️ Backend Error</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-critical">❌ Cannot Connect</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="status-indicator status-critical">🔌 Backend Not Running</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: rgba(207, 25, 198, 0.05); padding: 10px; border-radius: 8px; margin-top: 10px; border: 1px solid rgba(207, 25, 198, 0.1);'>
            <p style='margin: 0; font-size: 0.85rem; color: {COLORS["text_secondary"]};'>
            <b>Fix:</b> Run in terminal:<br>
            <code style='background: {COLORS["background"]}; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;'>python backend.py</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Risk Categories Guide
    st.markdown("### Risk Categories")
    
    risk_categories = [
        ("Critical", "≥75%", "Immediate intervention required", COLORS["critical"]),
        ("High", "50-74%", "Review and verification needed", COLORS["high"]),
        ("Medium", "25-49%", "Monitor closely", COLORS["medium"]),
        ("Low", "<25%", "Low priority", COLORS["low"])
    ]
    
    for name, range_, desc, color in risk_categories:
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <div style='width: 10px; height: 10px; background-color: {color}; border-radius: 50%; margin-right: 10px;'></div>
            <div>
                <div style='font-weight: 600; color: {COLORS["text_primary"]};'>{name} {range_}</div>
                <div style='font-size: 0.8rem; color: {COLORS["text_secondary"]};'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Professional Footer
st.markdown(f"""
<style>
.medinomix-footer {{
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
    border-top: 1px solid {COLORS["border"]};
    color: {COLORS["text_secondary"]};
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
}}
.medinomix-footer a {{
    color: {COLORS["primary"]};
    text-decoration: none;
    font-weight: 600;
}}
.medinomix-footer a:hover {{
    text-decoration: underline;
}}
</style>

<div class='medinomix-footer'>
    <div style='display: flex; justify-content: center; gap: 30px; margin-bottom: 15px;'>
        <div><span class='ai-highlight'>AI-Powered</span> • Real-time analysis</div>
        <div><span style='color: {COLORS["low"]}; font-weight: 600;'>Patient Safety First</span> • Healthcare focused</div>
        <div><b>Last Updated</b>: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
    </div>
    <div style='margin-top: 10px;'>
        © 2024 MediNomix • Version 3.0 • For educational purposes
    </div>
    <div style='margin-top: 10px; font-size: 0.8rem; font-style: italic;'>
        Always consult healthcare professionals for medical decisions. This application is designed to assist, not replace, professional judgment.
    </div>
</div>
""", unsafe_allow_html=True)