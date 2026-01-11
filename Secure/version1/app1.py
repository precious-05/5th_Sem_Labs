"""
ConfusionGuard AI - Streamlit Frontend
COMPLETE VERSION with ALL visualizations: Heatmap, Charts, Metrics
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="ConfusionGuard AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Color scheme
COLORS = {
    "primary": "#1E88E5",
    "secondary": "#43A047",
    "critical": "#DC2626",
    "high": "#F59E0B",
    "medium": "#3B82F6",
    "low": "#10B981",
    "background": "#F5F7FA",
    "surface": "#FFFFFF",
}

# Initialize session state
for key in ['search_results', 'dashboard_data', 'selected_risk', 'heatmap_data']:
    if key not in st.session_state:
        st.session_state[key] = None if key == 'heatmap_data' else ([] if key == 'search_results' else {} if key == 'dashboard_data' else "all")

# Helper functions
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
    """Create interactive drug confusion heatmap - SAME AS REFLEX VERSION"""
    if not st.session_state.heatmap_data:
        return None
    
    heatmap_data = st.session_state.heatmap_data
    drug_names = heatmap_data.get("drug_names", [])
    risk_matrix = heatmap_data.get("risk_matrix", [])
    
    if not drug_names or not risk_matrix:
        return None
    
    # Create heatmap - EXACT SAME AS REFLEX CODE
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
        textfont={"size": 10},
        hoverongaps=False,
        hoverinfo="text",
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>Risk: %{z:.1f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title={
            "text": "Drug Confusion Heatmap",
            "font": {"size": 16, "color": "#2D3748"}
        },
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        height=600,
        width=800,
        margin={"t": 50, "b": 50, "l": 100, "r": 50},
        plot_bgcolor=COLORS["surface"],
        paper_bgcolor=COLORS["surface"],
    )
    
    return fig

def create_risk_breakdown_chart():
    """Create risk breakdown pie chart"""
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
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
        )
    ])
    
    fig.update_layout(
        title="Risk Category Distribution",
        height=400,
        margin=dict(t=50, b=20, l=20, r=20),
        showlegend=False
    )
    
    return fig

def create_top_risks_chart():
    """Create top risks bar chart"""
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
            hovertemplate="<b>%{y}</b><br>Risk Score: %{x:.1f}%<br>Category: %{customdata}<extra></extra>",
            customdata=categories
        )
    ])
    
    fig.update_layout(
        title="Top 10 High-Risk Drug Pairs",
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=500,
        margin=dict(t=50, b=50, l=200, r=50),
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

# UI Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1E88E5;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #718096;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #E2E8F0;
    }
    .risk-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border-left: 5px solid;
        transition: transform 0.2s;
    }
    .risk-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .critical { border-left-color: #DC2626; }
    .high { border-left-color: #F59E0B; }
    .medium { border-left-color: #3B82F6; }
    .low { border-left-color: #10B981; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    st.markdown('<div class="main-header">🩺 ConfusionGuard AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Preventing Medication Errors Through AI Analysis</div>', unsafe_allow_html=True)
with col2:
    if st.button("🔄 Seed DB", use_container_width=True, help="Load sample drugs into database"):
        if seed_database():
            load_dashboard_data()
with col3:
    if st.button("📊 Refresh", use_container_width=True, help="Reload dashboard data"):
        load_dashboard_data()

# Main tabs
tab1, tab2, tab3 = st.tabs(["🔍 Search & Analyze", "📊 Dashboard", "ℹ️ About"])

with tab1:
    st.subheader("Check Drug Name Confusion Risk")
    st.write("Enter a drug name to analyze potential confusion with other medications")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        drug_name = st.text_input(
            "Drug Name",
            placeholder="e.g., metformin, lamictal, celebrex...",
            label_visibility="collapsed"
        )
    with col2:
        search_clicked = st.button("🔬 Analyze Risk", use_container_width=True, type="primary")
    
    if search_clicked and drug_name:
        with st.spinner("Analyzing drug confusion risks..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
    
    # Risk level filter
    if st.session_state.search_results:
        st.markdown("---")
        
        # Risk filter buttons
        cols = st.columns(5)
        risk_filters = {
            "All Risks": "all",
            "🔴 Critical": "critical",
            "🟠 High": "high",
            "🔵 Medium": "medium",
            "🟢 Low": "low"
        }
        
        for i, (label, value) in enumerate(risk_filters.items()):
            if cols[i].button(label, use_container_width=True):
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
        
        # Display results
        st.subheader(f"Found {len(filtered_results)} Similar Drugs")
        
        for result in filtered_results:
            risk_class = result['risk_category']
            risk_color = COLORS[risk_class]
            
            with st.container():
                # Card header
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### {result['target_drug']['brand_name']}")
                    if result['target_drug']['generic_name']:
                        st.caption(f"*{result['target_drug']['generic_name']}*")
                with col2:
                    st.markdown(f"""
                    <div style='text-align: right;'>
                        <span style='
                            padding: 6px 12px;
                            background-color: {risk_color};
                            color: white;
                            border-radius: 20px;
                            font-weight: bold;
                            font-size: 0.9rem;
                        '>
                            {risk_class.upper()}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Metrics in columns
                cols = st.columns(4)
                metrics = [
                    ("Spelling", f"{result['spelling_similarity']:.1f}%"),
                    ("Phonetic", f"{result['phonetic_similarity']:.1f}%"),
                    ("Context", f"{result['therapeutic_context_risk']:.1f}%"),
                    ("Overall Risk", f"{result['combined_risk']:.1f}%")
                ]
                
                for col, (label, value) in zip(cols, metrics):
                    with col:
                        st.metric(label, value, delta_color="inverse" if label == "Overall Risk" else "off")
                
                # Purpose (collapsible)
                if result['target_drug']['purpose']:
                    with st.expander("Purpose & Details"):
                        st.write(result['target_drug']['purpose'])
                        if result['target_drug']['manufacturer']:
                            st.caption(f"Manufacturer: {result['target_drug']['manufacturer']}")
                
                st.markdown("---")

with tab2:
    st.subheader("Confusion Risk Dashboard")
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Metrics row
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Drugs", metrics.get('total_drugs', 0))
        with col2:
            st.metric("High/Critical Pairs", metrics.get('high_risk_pairs', 0), 
                     delta_color="inverse", help="Pairs requiring immediate attention")
        with col3:
            st.metric("Critical Pairs", metrics.get('critical_risk_pairs', 0), 
                     delta_color="inverse", help="Extremely high-risk pairs")
        with col4:
            st.metric("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%")
    
    # Charts section
    st.markdown("---")
    
    # Heatmap (Full width)
    st.subheader("Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
        st.caption("Interactive heatmap showing confusion risk between drug pairs. Hover over cells to see risk percentages.")
    else:
        st.info("No heatmap data available. Search for drugs or seed database first.")
    
    # Other charts (Side by side)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
        else:
            st.info("No risk breakdown data available.")
    
    with col2:
        st.subheader("Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
        else:
            st.info("No top risk data available.")
    
    # Known risky pairs table
    st.markdown("---")
    st.subheader("Common High-Risk Drug Pairs (FDA Alerts)")
    
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "🔴 Critical", "Description": "Epilepsy vs Fungal infection", "Alert": "FDA Safety Warning"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "🔴 Critical", "Description": "Arthritis vs Depression", "Alert": "ISMP High Alert"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "🟠 High", "Description": "Diabetes vs Antibiotic", "Alert": "Common Error"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "🟠 High", "Description": "Blood pressure vs Anxiety", "Alert": "Sound-alike"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "🔵 Medium", "Description": "Antipsychotic vs Allergy", "Alert": "Look-alike"},
        {"Drug 1": "Hydrocodone", "Drug 2": "Oxycodone", "Risk Level": "🔴 Critical", "Description": "Pain medication", "Alert": "FDA Black Box"},
    ])
    
    st.dataframe(
        risky_pairs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk Level": st.column_config.TextColumn("Risk", width="small"),
            "Alert": st.column_config.TextColumn("Alert Type", width="medium")
        }
    )

with tab3:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("About ConfusionGuard AI")
    with col2:
        st.metric("Medication Errors", "25%", "involve name confusion", delta_color="inverse")
    
    st.markdown("""
    ConfusionGuard AI is a healthcare safety application designed to prevent medication errors 
    caused by confusing drug names (look-alike/sound-alike drugs).
    """)
    
    # Problem & Solution side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚨 The Problem")
        st.markdown("""
        - **25%** of medication errors involve name confusion (FDA)
        - **1.5 million** Americans harmed annually
        - **$42 billion** in preventable costs
        - Common pairs: Lamictal↔Lamisil, Celebrex↔Celexa
        """)
    
    with col2:
        st.markdown("#### 🛡️ Our Solution")
        st.markdown("""
        - **Real-time FDA data** analysis
        - **Multi-algorithm** risk scoring
        - **Interactive** visualizations
        - **Actionable** safety recommendations
        - **Healthcare professional** design
        """)
    
    # How it works
    st.markdown("---")
    st.subheader("How It Works")
    
    steps = st.columns(4)
    step_data = [
        ("1", "🔍 Search", "Enter drug name", "User inputs medication name"),
        ("2", "⚙️ Analyze", "Calculate risks", "Algorithms assess similarity"),
        ("3", "📊 Visualize", "View results", "Interactive charts & heatmaps"),
        ("4", "🛡️ Prevent", "Take action", "Safety recommendations")
    ]
    
    for step, (num, icon, title, desc) in zip(steps, step_data):
        with step:
            st.markdown(f"""
            <div style='
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                color: white;
                margin-bottom: 10px;
            '>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>{icon}</div>
                <div style='font-size: 1.8rem; font-weight: bold;'>{num}</div>
            </div>
            <div style='text-align: center; padding: 10px;'>
                <div style='font-weight: bold; font-size: 1.1rem;'>{title}</div>
                <div style='color: #666; font-size: 0.9rem;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2024 ConfusionGuard AI | For educational purposes. Always verify medications with healthcare professionals.")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2069/2069753.png", width=80)
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🧪 Test with Metformin", use_container_width=True, type="secondary"):
        st.session_state.search_results = []
        result = search_drug("metformin")
        if result:
            st.session_state.search_results = result.get('similar_drugs', [])
            st.rerun()
    
    if st.button("📥 Load All Sample Data", use_container_width=True):
        if seed_database():
            load_dashboard_data()
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚙️ Backend Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.success("✅ Backend Connected")
                cols = st.columns(2)
                cols[0].metric("Drugs", data.get('drugs_in_database', 0))
                cols[1].metric("Risks", data.get('risk_assessments', 0))
            else:
                st.error("❌ Backend Error")
        else:
            st.error("❌ Cannot connect")
    except:
        st.error("🔌 Backend not running")
        st.caption("Run in terminal: `python backend.py`")
    
    st.markdown("---")
    st.markdown("### 📈 Risk Categories")
    
    risk_info = [
        ("🔴 Critical", "≥75%", "Immediate intervention"),
        ("🟠 High", "50-74%", "Review required"),
        ("🔵 Medium", "25-49%", "Monitor closely"),
        ("🟢 Low", "<25%", "Low priority")
    ]
    
    for icon, range_, desc in risk_info:
        st.markdown(f"**{icon} {range_}**")
        st.caption(desc)
    
    st.markdown("---")
    st.markdown("#### 📊 Statistics")
    st.markdown("""
    - Analyzes **15+ drug attributes**
    - Uses **3+ similarity algorithms**
    - Real-time **FDA database** queries
    - **Interactive** visualizations
    """)

# Footer
st.markdown("---")
footer_cols = st.columns(3)
with footer_cols[0]:
    st.markdown("**FDA OpenFDA API** • Real-time data")
with footer_cols[1]:
    st.markdown("**Patient Safety First** • Healthcare focused")
with footer_cols[2]:
    st.markdown(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

st.caption("*This application is for educational purposes. Always consult healthcare professionals for medical decisions.*")