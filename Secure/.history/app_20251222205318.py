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
    "primary": "#4361ee",        # Medical Blue - Trust & Professionalism
    "primary_light": "#4895ef",
    "primary_dark": "#3a56d4",
    "secondary": "#4cc9f0",      # Teal - Healthcare Safety
    "accent": "#7209b7",         # Purple - AI Intelligence
    "accent_pink": "#f72585",    # Medical Pink - Alerts
    "success": "#06d6a0",        # Green - Safe/Low Risk
    "warning": "#ffd166",        # Yellow - Medium Risk
    "danger": "#ef476f",         # Red - Critical Risk
    "dark": "#1d3557",           # Dark Blue - Text
    "light": "#f1f6ff",          # Light Background
    "surface": "#ffffff",        # Card Background
    "gray": "#6c757d",
    "gray_light": "#e9ecef",
    "border": "rgba(67, 97, 238, 0.12)",
}

# FontAwesome Icons (Base64)
ICONS = {
    "pill": "fas fa-pills",
    "search": "fas fa-search-medical",
    "dashboard": "fas fa-chart-line",
    "analytics": "fas fa-chart-bar",
    "alert": "fas fa-exclamation-triangle",
    "warning": "fas fa-radiation-alt",
    "safety": "fas fa-shield-alt",
    "hospital": "fas fa-hospital",
    "flask": "fas fa-flask",
    "brain": "fas fa-brain",
    "database": "fas fa-database",
    "refresh": "fas fa-sync-alt",
    "download": "fas fa-download",
    "trash": "fas fa-trash-alt",
    "info": "fas fa-info-circle",
    "stats": "fas fa-chart-pie",
    "heartbeat": "fas fa-heartbeat",
    "capsules": "fas fa-capsules",
    "syringe": "fas fa-syringe",
    "stethoscope": "fas fa-stethoscope",
    "user_md": "fas fa-user-md",
    "tablets": "fas fa-tablets",
    "prescription": "fas fa-prescription",
    "vial": "fas fa-vial",
    "microscope": "fas fa-microscope",
    "shield": "fas fa-shield-virus",
    "chart_network": "fas fa-project-diagram",
    "bell": "fas fa-bell",
    "clock": "fas fa-clock",
    "check": "fas fa-check-circle",
    "times": "fas fa-times-circle",
    "chevron_right": "fas fa-chevron-right",
    "chevron_down": "fas fa-chevron-down",
    "filter": "fas fa-filter",
    "sort": "fas fa-sort-amount-down",
    "eye": "fas fa-eye",
    "edit": "fas fa-edit",
    "copy": "fas fa-copy",
    "share": "fas fa-share-alt",
    "print": "fas fa-print",
    "book": "fas fa-book-medical",
    "calendar": "fas fa-calendar-alt",
    "users": "fas fa-users",
    "globe": "fas fa-globe-americas",
    "database_add": "fas fa-database",
    "robot": "fas fa-robot",
    "ai": "fas fa-microchip",
    "network": "fas fa-network-wired",
    "wave": "fas fa-wave-square",
    "thermometer": "fas fa-thermometer-half",
    "tachometer": "fas fa-tachometer-alt",
    "gradient": "fas fa-fill-drip",
    "layers": "fas fa-layer-group",
    "magic": "fas fa-magic",
    "bolt": "fas fa-bolt",
    "star": "fas fa-star",
    "award": "fas fa-award",
    "certificate": "fas fa-certificate",
    "lightbulb": "fas fa-lightbulb",
    "rocket": "fas fa-rocket",
    "atom": "fas fa-atom",
    "dna": "fas fa-dna",
    "virus": "fas fa-virus",
    "lungs": "fas fa-lungs",
    "heart": "fas fa-heart",
    "brain_circuit": "fas fa-brain",
    "code": "fas fa-code",
    "github": "fab fa-github",
    "linkedin": "fab fa-linkedin",
    "twitter": "fab fa-twitter",
    "youtube": "fab fa-youtube",
    "paper": "fas fa-file-medical-alt",
    "balance": "fas fa-balance-scale",
    "lock": "fas fa-lock",
    "unlock": "fas fa-unlock",
    "key": "fas fa-key",
    "cloud": "fas fa-cloud",
    "server": "fas fa-server",
    "mobile": "fas fa-mobile-alt",
    "desktop": "fas fa-desktop",
    "tablet": "fas fa-tablet-alt",
    "wifi": "fas fa-wifi",
    "signal": "fas fa-signal",
    "battery": "fas fa-battery-full",
    "plug": "fas fa-plug",
    "cogs": "fas fa-cogs",
    "tools": "fas fa-tools",
    "wrench": "fas fa-wrench",
    "hammer": "fas fa-hammer",
    "truck": "fas fa-truck-medical",
    "ambulance": "fas fa-ambulance",
    "first_aid": "fas fa-first-aid",
    "briefcase": "fas fa-briefcase-medical",
    "clipboard": "fas fa-clipboard-check",
    "notes": "fas fa-notes-medical",
    "history": "fas fa-history",
    "timeline": "fas fa-timeline",
    "calendar_check": "fas fa-calendar-check",
    "clock_rotate": "fas fa-clock-rotate-left",
    "hourglass": "fas fa-hourglass-half",
    "stopwatch": "fas fa-stopwatch",
    "flag": "fas fa-flag",
    "map": "fas fa-map-marked-alt",
    "location": "fas fa-map-marker-alt",
    "compass": "fas fa-compass",
    "globe_stand": "fas fa-globe-stand",
    "earth": "fas fa-earth-americas",
    "satellite": "fas fa-satellite",
    "rocket_launch": "fas fa-rocket",
    "spaceshuttle": "fas fa-space-shuttle",
    "meteor": "fas fa-meteor",
    "sun": "fas fa-sun",
    "moon": "fas fa-moon",
    "cloud_sun": "fas fa-cloud-sun",
    "cloud_moon": "fas fa-cloud-moon",
    "rainbow": "fas fa-rainbow",
    "poo_storm": "fas fa-poo-storm",
    "wind": "fas fa-wind",
    "snowflake": "fas fa-snowflake",
    "fire": "fas fa-fire",
    "water": "fas fa-water",
    "seedling": "fas fa-seedling",
    "leaf": "fas fa-leaf",
    "tree": "fas fa-tree",
    "mountain": "fas fa-mountain",
    "campground": "fas fa-campground",
    "hiking": "fas fa-hiking",
    "biking": "fas fa-biking",
    "running": "fas fa-running",
    "swimmer": "fas fa-swimmer",
    "skiing": "fas fa-skiing",
    "skating": "fas fa-skating",
    "snowboarding": "fas fa-snowboarding",
    "futbol": "fas fa-futbol",
    "basketball": "fas fa-basketball-ball",
    "baseball": "fas fa-baseball-ball",
    "football": "fas fa-football-ball",
    "hockey": "fas fa-hockey-puck",
    "golf": "fas fa-golf-ball",
    "tennis": "fas fa-tennis-ball",
    "volleyball": "fas fa-volleyball-ball",
    "chess": "fas fa-chess",
    "dice": "fas fa-dice",
    "puzzle": "fas fa-puzzle-piece",
    "gamepad": "fas fa-gamepad",
    "vr_cardboard": "fas fa-vr-cardboard",
    "robot_arm": "fas fa-robot",
    "industry": "fas fa-industry",
    "oil_can": "fas fa-oil-can",
    "gas_pump": "fas fa-gas-pump",
    "charging": "fas fa-charging-station",
    "solar": "fas fa-solar-panel",
    "wind_turbine": "fas fa-wind-turbine",
    "recycle": "fas fa-recycle",
    "trash_restore": "fas fa-trash-restore",
    "leaf_recycle": "fas fa-leaf",
    "earth_europe": "fas fa-earth-europe",
    "globe_africa": "fas fa-globe-africa",
    "globe_asia": "fas fa-globe-asia",
    "globe_europe": "fas fa-globe-europe",
    "flag_usa": "fas fa-flag-usa",
    "monument": "fas fa-monument",
    "landmark": "fas fa-landmark",
    "university": "fas fa-university",
    "school": "fas fa-school",
    "graduation": "fas fa-graduation-cap",
    "book_open": "fas fa-book-open",
    "book_reader": "fas fa-book-reader",
    "user_graduate": "fas fa-user-graduate",
    "chalkboard": "fas fa-chalkboard-teacher",
    "laptop_code": "fas fa-laptop-code",
    "keyboard": "fas fa-keyboard",
    "mouse": "fas fa-mouse",
    "hdmi": "fas fa-hdmi",
    "usb": "fas fa-usb",
    "ethernet": "fas fa-ethernet",
    "bluetooth": "fas fa-bluetooth",
    "bluetooth_b": "fas fa-bluetooth-b",
    "wifi_2": "fas fa-wifi",
    "signal_2": "fas fa-signal",
    "battery_3": "fas fa-battery-three-quarters",
    "battery_4": "fas fa-battery-full",
    "plug_2": "fas fa-plug",
    "power_off": "fas fa-power-off",
    "play": "fas fa-play-circle",
    "pause": "fas fa-pause-circle",
    "stop": "fas fa-stop-circle",
    "record": "fas fa-record-vinyl",
    "forward": "fas fa-forward",
    "backward": "fas fa-backward",
    "fast_forward": "fas fa-fast-forward",
    "fast_backward": "fas fa-fast-backward",
    "step_forward": "fas fa-step-forward",
    "step_backward": "fas fa-step-backward",
    "random": "fas fa-random",
    "retweet": "fas fa-retweet",
    "repeat": "fas fa-repeat",
    "undo": "fas fa-undo",
    "redo": "fas fa-redo",
    "expand": "fas fa-expand",
    "compress": "fas fa-compress",
    "maximize": "fas fa-maximize",
    "minimize": "fas fa-minimize",
    "crop": "fas fa-crop",
    "crop_alt": "fas fa-crop-alt",
    "image": "fas fa-image",
    "images": "fas fa-images",
    "photo_video": "fas fa-photo-video",
    "film": "fas fa-film",
    "video": "fas fa-video",
    "music": "fas fa-music",
    "headphones": "fas fa-headphones",
    "headset": "fas fa-headset",
    "microphone": "fas fa-microphone",
    "microphone_alt": "fas fa-microphone-alt",
    "volume_up": "fas fa-volume-up",
    "volume_down": "fas fa-volume-down",
    "volume_mute": "fas fa-volume-mute",
    "volume_off": "fas fa-volume-off",
    "bell_slash": "fas fa-bell-slash",
    "calendar_times": "fas fa-calendar-times",
    "calendar_minus": "fas fa-calendar-minus",
    "calendar_plus": "fas fa-calendar-plus",
    "calendar_day": "fas fa-calendar-day",
    "calendar_week": "fas fa-calendar-week",
    "calendar_month": "fas fa-calendar",
    "birthday": "fas fa-birthday-cake",
    "cake": "fas fa-birthday-cake",
    "cookie": "fas fa-cookie",
    "cookie_bite": "fas fa-cookie-bite",
    "ice_cream": "fas fa-ice-cream",
    "hamburger": "fas fa-hamburger",
    "pizza": "fas fa-pizza-slice",
    "beer": "fas fa-beer",
    "wine_glass": "fas fa-wine-glass",
    "wine_bottle": "fas fa-wine-bottle",
    "whiskey": "fas fa-glass-whiskey",
    "cocktail": "fas fa-cocktail",
    "coffee": "fas fa-coffee",
    "tea": "fas fa-mug-hot",
    "utensils": "fas fa-utensils",
    "utensil_spoon": "fas fa-utensil-spoon",
    "knife": "fas fa-utensil-knife",
    "fork": "fas fa-utensils",
    "bowl": "fas fa-bowl-food",
    "carrot": "fas fa-carrot",
    "apple": "fas fa-apple-alt",
    "lemon": "fas fa-lemon",
    "pepper": "fas fa-pepper-hot",
    "fish": "fas fa-fish",
    "egg": "fas fa-egg",
    "cheese": "fas fa-cheese",
    "bread": "fas fa-bread-slice",
    "bacon": "fas fa-bacon",
    "drumstick": "fas fa-drumstick-bite",
    "hotdog": "fas fa-hotdog",
    "burrito": "fas fa-burrito",
    "taco": "fas fa-taco"
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
    
    /* FontAwesome Icons */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
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
        text-shadow: 0 4px 20px rgba({int(COLORS["primary"].split('#')[1][0:2], 16)}, {int(COLORS["primary"].split('#')[1][2:4], 16)}, {int(COLORS["primary"].split('#')[1][4:6], 16)}, 0.1);
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

# Modern Header with Animated Elements
st.markdown(f"""
<div style='text-align: center; padding: 3rem 0 2rem 0; position: relative;'>
    <div class='floating-element' style='position: absolute; top: 50px; left: 10%; width: 100px; height: 100px; 
         background: linear-gradient(135deg, {COLORS["primary"]}20, {COLORS["accent"]}20); border-radius: 50%; 
         filter: blur(40px); animation: float 8s infinite ease-in-out;'></div>
    
    <div class='floating-element' style='position: absolute; top: 100px; right: 10%; width: 150px; height: 150px; 
         background: linear-gradient(135deg, {COLORS["secondary"]}20, {COLORS["success"]}20); border-radius: 50%; 
         filter: blur(50px); animation: float 6s infinite ease-in-out 1s;'></div>
    
    <div style='display: inline-flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px;'>
        <i class='{ICONS["pill"]}' style='font-size: 4rem; color: {COLORS["primary"]}; 
           animation: pulse 3s infinite;'></i>
        <h1 class='main-header'>MediNomix</h1>
        <i class='{ICONS["brain"]}' style='font-size: 4rem; color: {COLORS["accent"]}; 
           animation: pulse 3s infinite 0.5s;'></i>
    </div>
    <div class='sub-header'>AI-Powered Medication Safety Intelligence Platform</div>
    
    <div style='margin-top: 2rem; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;'>
        <span class='status-indicator status-healthy'><i class='{ICONS["safety"]}'></i> Patient Safety First</span>
        <span class='status-indicator status-healthy'><i class='{ICONS["ai"]}'></i> AI-Powered Analysis</span>
        <span class='status-indicator status-healthy'><i class='{ICONS["hospital"]}'></i> Hospital Grade</span>
        <span class='status-indicator status-healthy'><i class='{ICONS["shield"]}'></i> Real-time Protection</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Modern Action Buttons with Animations
st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <div style='display: inline-flex; gap: 15px; background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7)); 
         padding: 20px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
         backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.3);'>
""", unsafe_allow_html=True)

action_cols = st.columns([1, 1, 1, 1])
with action_cols[0]:
    if st.button(f"**{ICONS['database_add']} Seed Database**", use_container_width=True, type="secondary"):
        with st.spinner("Seeding database with sample drugs..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()
with action_cols[1]:
    if st.button(f"**{ICONS['refresh']} Refresh Data**", use_container_width=True, type="secondary"):
        with st.spinner("Refreshing dashboard data..."):
            load_dashboard_data()
            st.rerun()
with action_cols[2]:
    if st.button(f"**{ICONS['flask']} Quick Demo**", use_container_width=True):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
with action_cols[3]:
    if st.button(f"**{ICONS['info']} Get Help**", use_container_width=True, type="secondary"):
        st.info(f"""
        **{ICONS['lightbulb']} Quick Tips:**
        1. Search any drug name to analyze confusion risks
        2. Use the heatmap to visualize risk patterns
        3. Check FDA alerts for known dangerous pairs
        4. Filter results by risk level for focused analysis
        """)

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Modern Navigation Tabs with Icons
tab1, tab2, tab3 = st.tabs([
    f"**{ICONS['search']} Drug Analysis**", 
    f"**{ICONS['dashboard']} Analytics Dashboard**", 
    f"**{ICONS['info']} About & Resources**"
])

with tab1:
    # Modern Search Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <i class='{ICONS["search"]}' style='font-size: 4rem; color: {COLORS["primary"]}; 
               margin-bottom: 20px; display: block; animation: pulse 2s infinite;'></i>
            <h2 class='section-header'>Drug Confusion Risk Analysis</h2>
            <p style='color: {COLORS["gray"]}; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                Enter a drug name to analyze potential confusion risks with similar medications using advanced AI algorithms
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Modern Search Bar
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        drug_name = st.text_input(
            "",
            placeholder="Enter drug name (e.g., metformin, lamictal, celebrex...)",
            label_visibility="collapsed",
            key="search_input"
        )
        
        # Modern Search Buttons
        search_cols = st.columns([1, 1])
        with search_cols[0]:
            search_clicked = st.button(f"**{ICONS['search']} Analyze Drug**", use_container_width=True, type="primary")
        with search_cols[1]:
            if st.button(f"**{ICONS['lightbulb']} Show Examples**", use_container_width=True, type="secondary"):
                examples = ["metformin", "lamictal", "celebrex", "clonidine", "zyprexa"]
                st.info(f"**{ICONS['flask']} Try these drugs:** {', '.join(examples)}")
    
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
            f"{ICONS['warning']} All Risks": "all",
            f"{ICONS['radiation-alt']} Critical (≥75%)": "critical",
            f"{ICONS['exclamation-triangle']} High (50-74%)": "high",
            f"{ICONS['thermometer-half']} Medium (25-49%)": "medium",
            f"{ICONS['check']} Low (<25%)": "low"
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
                <i class='{ICONS["chart-network"]}' style='color: {COLORS["primary"]};'></i>
                Found {len(filtered_results)} Similar Drugs
            </h3>
            <p style='color: {COLORS["gray"]}; margin: 10px 0 0 0; display: flex; align-items: center; gap: 10px;'>
                <i class='{ICONS["filter"]}'></i>
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
                                <i class='{ICONS["capsules"]}' style='color: {risk_color};'></i>
                                {result['target_drug']['brand_name']}
                            </h3>
                            <p style='color: {COLORS["gray"]}; margin: 0; font-style: italic; display: flex; align-items: center; gap: 8px;'>
                                <i class='{ICONS["vial"]}' style='font-size: 0.9rem;'></i>
                                {result['target_drug']['generic_name'] if result['target_drug']['generic_name'] else 'Generic name not available'}
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span class='risk-badge' style='background-color: {risk_color}15; color: {risk_color}; border-color: {risk_color};'>
                                <i class='{ICONS["exclamation-triangle"] if risk_class in ["critical", "high"] else ICONS["thermometer-half"] if risk_class == "medium" else ICONS["check"]}'></i>
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
                    (f"{ICONS['spell-check']} Spelling Similarity", f"{result['spelling_similarity']:.1f}%"),
                    (f"{ICONS['wave-square']} Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%"),
                    (f"{ICONS['stethoscope']} Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%"),
                    (f"{ICONS['tachometer']} Overall Risk", f"{result['combined_risk']:.1f}%")
                ]
                
                for col, (label, value) in zip(cols, metrics):
                    with col:
                        st.markdown(f"""
                        <div class='grid-item'>
                            <div style='font-size: 0.9rem; color: {COLORS["gray"]}; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;'>
                                {label.split(' ')[0]} {label.split(' ')[1] if len(label.split(' ')) > 1 else ''}
                            </div>
                            <div style='font-size: 1.5rem; font-weight: 700; color: {COLORS["dark"]};'>{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Additional Details
                with st.expander(f"{ICONS['info']} View Drug Details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        if result['target_drug']['purpose']:
                            st.markdown(f"**{ICONS['book-medical']} Purpose:**")
                            st.info(result['target_drug']['purpose'][:200] + "..." if len(result['target_drug']['purpose']) > 200 else result['target_drug']['purpose'])
                    with col2:
                        if result['target_drug']['manufacturer']:
                            st.markdown(f"**{ICONS['industry']} Manufacturer:**")
                            st.text(result['target_drug']['manufacturer'])
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

with tab2:
    # Modern Dashboard
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <i class='{ICONS["dashboard"]}' style='font-size: 4rem; color: {COLORS["primary"]}; 
           margin-bottom: 20px; display: block; animation: pulse 2s infinite;'></i>
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
            (f"{ICONS['database']} Total Drugs", metrics.get('total_drugs', 0), COLORS["primary"], "Total medications in database"),
            (f"{ICONS['warning']} High/Critical Pairs", metrics.get('high_risk_pairs', 0), "#b5179e", "Pairs requiring attention"),
            (f"{ICONS['radiation-alt']} Critical Pairs", metrics.get('critical_risk_pairs', 0), COLORS["danger"], "Extreme risk pairs"),
            (f"{ICONS['chart-line']} Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%", COLORS["accent"], "Average confusion risk")
        ]
        
        for col, (title, value, color, help_text) in zip(metric_cols, metric_data):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 1rem; color: {COLORS["gray"]}; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 10px;'>
                        {title.split(' ')[0]} <span>{' '.join(title.split(' ')[1:])}</span>
                    </div>
                    <div style='font-size: 2.8rem; font-weight: 800; color: {color}; margin-bottom: 8px;'>{value}</div>
                    <div style='font-size: 0.85rem; color: {COLORS["gray"]}; opacity: 0.8;'>{help_text}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Heatmap Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h3 style='color: {COLORS["dark"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 15px;'>
            <i class='{ICONS["chart-network"]}' style='color: {COLORS["primary"]};'></i>
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
                <i class='{ICONS["lightbulb"]}' style='color: {COLORS["primary"]}; font-size: 1.2rem; margin-top: 3px;'></i>
                <span><b>How to read this heatmap:</b> Each cell shows confusion risk between two drugs. 
                Green cells indicate low risk (<25%), yellow cells show moderate risk (25-50%), 
                orange cells indicate high risk (50-75%), and pink/magenta cells show critical risk (>75%). 
                Hover over any cell for detailed information.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"{ICONS['info']} No heatmap data available. Search for drugs or seed the database first.")
    
    # Modern Charts Section
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["dark"]}; margin-bottom: 2rem; display: flex; align-items: center; gap: 15px;'>
        <i class='{ICONS["chart-pie"]}' style='color: {COLORS["primary"]};'></i>
        Risk Analytics
    </h3>
    """, unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown(f"#### {ICONS['chart-pie']} Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info(f"{ICONS['info']} No risk breakdown data available.")
    
    with chart_col2:
        st.markdown(f"#### {ICONS['chart-bar']} Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info(f"{ICONS['info']} No top risk data available.")
    
    # FDA Alert Table
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["dark"]}; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 15px;'>
        <i class='{ICONS["exclamation-triangle"]}' style='color: {COLORS["danger"]};'></i>
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
        <i class='{ICONS["hospital"]}' style='font-size: 4rem; color: {COLORS["primary"]}; 
           margin-bottom: 20px; display: block; animation: pulse 2s infinite;'></i>
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
                  help=f"{ICONS['warning']} FDA Statistics")
    with col2:
        st.metric("Annual Harm", "1.5M", "Americans affected", delta_color="inverse",
                  help=f"{ICONS['users']} National Impact")
    with col3:
        st.metric("Annual Cost", "$42B", "preventable expenses", delta_color="inverse",
                  help=f"{ICONS['dollar-sign']} Economic Burden")
    
    # Problem & Solution Cards
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left; border-left-color: {COLORS["danger"]};'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <i class='{ICONS["exclamation-triangle"]}' style='font-size: 2rem; color: {COLORS["danger"]}; margin-right: 20px;'></i>
                <h3 style='color: {COLORS["danger"]}; margin: 0;'>The Challenge</h3>
            </div>
            <div style='color: {COLORS["gray"]}; line-height: 1.7;'>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <i class='{ICONS["warning"]}' style='color: {COLORS["danger"]}; margin-top: 3px;'></i>
                    <span><b>25% of medication errors</b> involve name confusion (FDA)</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <i class='{ICONS["users"]}' style='color: {COLORS["danger"]}; margin-top: 3px;'></i>
                    <span><b>1.5 million Americans</b> harmed annually</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <i class='{ICONS["dollar-sign"]}' style='color: {COLORS["danger"]}; margin-top: 3px;'></i>
                    <span><b>$42 billion</b> in preventable costs</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px;'>
                    <i class='{ICONS["pills"]}' style='color: {COLORS["danger"]}; margin-top: 3px;'></i>
                    <span>Common pairs: <b>Lamictal↔Lamisil</b>, <b>Celebrex↔Celexa</b></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: left; border-left-color: {COLORS["success"]};'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <i class='{ICONS["shield-alt"]}' style='font-size: 2rem; color: {COLORS["success"]}; margin-right: 20px;'></i>
                <h3 style='color: {COLORS["success"]}; margin: 0;'>Our Solution</h3>
            </div>
            <div style='color: {COLORS["gray"]}; line-height: 1.7;'>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <i class='{ICONS["brain"]}' style='color: {COLORS["success"]}; margin-top: 3px;'></i>
                    <span><b>Multi-algorithm AI</b> risk assessment</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <i class='{ICONS["chart-network"]}' style='color: {COLORS["success"]}; margin-top: 3px;'></i>
                    <span><b>Real-time FDA data</b> integration</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px;'>
                    <i class='{ICONS["wave-square"]}' style='color: {COLORS["success"]}; margin-top: 3px;'></i>
                    <span><b>Context-aware</b> similarity detection</span>
                </div>
                <div style='display: flex; align-items: flex-start; gap: 10px;'>
                    <i class='{ICONS["bolt"]}' style='color: {COLORS["success"]}; margin-top: 3px;'></i>
                    <span><b>Instant alerts</b> and prevention guidance</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <h3 style='color: {COLORS["dark"]}; margin-bottom: 2rem; display: flex; align-items: center; gap: 15px;'>
        <i class='{ICONS["cogs"]}' style='color: {COLORS["primary"]};'></i>
        How It Works
    </h3>
    """, unsafe_allow_html=True)
    
    steps_cols = st.columns(4)
    step_data = [
        (f"{ICONS['search']}", "Search", "Enter drug name", "User inputs any medication name for analysis"),
        (f"{ICONS['brain']}", "Analyze", "Calculate risks", "Advanced AI algorithms assess multiple similarity factors"),
        (f"{ICONS['chart-network']}", "Visualize", "View results", "Interactive charts, heatmaps, and risk scores"),
        (f"{ICONS['shield-alt']}", "Prevent", "Take action", "Safety alerts and prevention recommendations")
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
                             <i class='{icon}'></i>
                        </div>
                        <h4 style='color: {COLORS["dark"]}; margin: 10px 0 5px 0;'>{title}</h4>
                        <p style='color: {COLORS["primary"]}; margin: 0; font-size: 0.9rem; font-weight: 600;'>{subtitle}</p>
                    </div>
                    <p style='color: {COLORS["gray"]}; font-size: 0.85rem; line-height: 1.6; margin-top: 10px;'>{desc}</p>
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
            <i class='{ICONS["pill"]}' style='font-size: 2.5rem; color: white;'></i>
        </div>
        <h3 style='color: {COLORS["dark"]}; margin: 10px 0 5px 0; font-family: Montserrat, sans-serif; font-weight: 800;'>MediNomix</h3>
        <p style='color: {COLORS["gray"]}; font-size: 0.9rem; font-weight: 500;'>AI-Powered Medication Safety</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown(f"""
    <h4 style='color: {COLORS["dark"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <i class='{ICONS["bolt"]}' style='color: {COLORS["primary"]};'></i>
        Quick Actions
    </h4>
    """, unsafe_allow_html=True)
    
    if st.button(f"**{ICONS['flask']} Test with Metformin**", use_container_width=True, type="primary"):
        st.session_state.search_results = []
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
    
    if st.button(f"**{ICONS['database']} Load Sample Data**", use_container_width=True, type="secondary"):
        if seed_database():
            load_dashboard_data()
            st.rerun()
    
    if st.button(f"**{ICONS['sync-alt']} Force Refresh**", use_container_width=True, type="secondary"):
        load_dashboard_data()
        st.rerun()
    
    st.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Backend Status
    st.markdown(f"""
    <h4 style='color: {COLORS["dark"]}; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px;'>
        <i class='{ICONS['server']}' style='color: {COLORS["primary"]};'></i>
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
            <b><i class='{ICONS["tools"]}' style='margin-right: 8px;'></i>Fix:</b> Run in terminal:<br>
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
        <i class='{ICONS['exclamation-triangle']}' style='color: {COLORS["primary"]};'></i>
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

# Floating Action Button
st.markdown(f"""
<div class='fab' onclick="window.scrollTo({{top: 0, behavior: 'smooth'}});">
    <i class='{ICONS["chevron-up"]}'></i>
</div>
""", unsafe_allow_html=True)

# Modern Footer
st.markdown(f"""
<style>
.medinomix-footer {{
    text-align: center;
    padding: 3rem 0 2rem 0;
    margin-top: 4rem;
    position: relative;
    background: linear-gradient(135deg, {COLORS["surface"]}, rgba(255, 255, 255, 0.95));
    border-radius: 30px 30px 0 0;
    box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.05);
    border-top: 1px solid rgba(67, 97, 238, 0.1);
}}
.medinomix-footer::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["accent"]}, {COLORS["primary"]});
    background-size: 200% auto;
    animation: gradientShift 3s ease infinite;
}}
.medinomix-footer a {{
    color: {COLORS["primary"]};
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}}
.medinomix-footer a:hover {{
    color: {COLORS["accent"]};
    text-decoration: none;
}}
.medinomix-footer a::after {{
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["accent"]});
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.medinomix-footer a:hover::after {{
    width: 100%;
}}
</style>

<div class='medinomix-footer'>
    <div style='display: flex; justify-content: center; gap: 40px; margin-bottom: 25px; flex-wrap: wrap;'>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <i class='{ICONS["ai"]}' style='color: {COLORS["accent"]};'></i>
            <span style='font-weight: 600;'>AI-Powered</span>
            <span style='color: {COLORS["gray"]}80;'>•</span>
            <span>Real-time analysis</span>
        </div>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <i class='{ICONS["shield-alt"]}' style='color: {COLORS["success"]};'></i>
            <span style='font-weight: 600; color: {COLORS["success"]}'>Patient Safety First</span>
            <span style='color: {COLORS["gray"]}80;'>•</span>
            <span>Healthcare focused</span>
        </div>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <i class='{ICONS["clock"]}' style='color: {COLORS["primary"]};'></i>
            <span style='font-weight: 600;'>Last Updated</span>
            <span>: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
        </div>
    </div>
    
    <div style='margin: 25px 0;'>
        <div style='font-size: 1.1rem; color: {COLORS["dark"]}; font-weight: 700; margin-bottom: 10px;'>
            © 2024 MediNomix • Version 3.0 • Advanced Medication Safety Platform
        </div>
        <div style='display: flex; justify-content: center; gap: 20px; margin-top: 20px;'>
            <a href='https://github.com/precious-05/MediNomix' target='_blank'>
                <i class='{ICONS["github"]}' style='font-size: 1.2rem;'></i> GitHub
            </a>
            <a href='https://github.com/precious-05/MediNomix/issues' target='_blank'>
                <i class='{ICONS["bug"]}' style='font-size: 1.2rem;'></i> Report Bug
            </a>
            <a href='https://github.com/precious-05/MediNomix' target='_blank'>
                <i class='{ICONS["book"]}' style='font-size: 1.2rem;'></i> Documentation
            </a>
        </div>
    </div>
    
    <div style='margin-top: 30px; padding-top: 25px; border-top: 1px solid rgba(67, 97, 238, 0.1);'>
        <div style='font-size: 0.9rem; color: {COLORS["gray"]}; font-style: italic; max-width: 800px; margin: 0 auto; line-height: 1.6;'>
            <i class='{ICONS["exclamation-triangle"]}' style='color: {COLORS["warning"]}; margin-right: 10px;'></i>
            Important: Always consult healthcare professionals for medical decisions. This application is designed to assist, not replace, professional judgment.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)