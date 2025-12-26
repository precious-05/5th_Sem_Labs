"""
MediNomix - Advanced Medication Safety Platform
SIMPLE CLEAN VERSION - 100% Same Functionality
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import threading
import websocket
import time

# Page configuration
st.set_page_config(
    page_title="MediNomix | AI-Powered Medication Safety",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/dashboard"

# Colors
COLORS = {
    "primary": "#7C3AED",
    "primary_dark": "#5B21B6",
    "accent": "#38BDF8",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "dark": "#1F2937",
    "gray": "#9CA3AF",
    "light": "#F3F4F6",
}

# Initialize session state
for key in ['search_results', 'dashboard_data', 'selected_risk', 'heatmap_data', 
            'realtime_metrics', 'realtime_events', 'websocket_connected', 
            'last_update_time', 'connected_clients']:
    if key not in st.session_state:
        st.session_state[key] = None if key in ['heatmap_data', 'realtime_metrics', 'realtime_events'] else ([] if key == 'search_results' else {} if key in ['dashboard_data', 'last_update_time'] else "all" if key == 'selected_risk' else False if key == 'websocket_connected' else 0)

# ================================
# REAL-TIME WEBSOCKET MANAGER
# ================================

class RealTimeWebSocketManager:
    """Manages WebSocket connection for real-time updates"""
    
    def __init__(self):
        self.connected = False
        self.ws = None
        self.thread = None
        
    def start_connection(self):
        """Start WebSocket connection in a separate thread"""
        if not self.connected:
            self.thread = threading.Thread(target=self._connect_websocket, daemon=True)
            self.thread.start()
    
    def _connect_websocket(self):
        """Connect to WebSocket"""
        try:
            self.ws = websocket.WebSocketApp(
                WS_URL,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            self.ws.run_forever()
        except Exception as e:
            print(f"WebSocket error: {e}")
            self.connected = False
            st.session_state.websocket_connected = False
    
    def _on_open(self, ws):
        """WebSocket connection opened"""
        self.connected = True
        st.session_state.websocket_connected = True
        print("✅ WebSocket connected!")
    
    def _on_message(self, ws, message):
        """Handle incoming messages"""
        try:
            data = json.loads(message)
            message_type = data.get('type', '')
            
            if message_type in ['initial', 'update', 'initial_data']:
                st.session_state.realtime_metrics = data.get('data', {})
                st.session_state.last_update_time = datetime.now().strftime("%H:%M:%S")
                
        except json.JSONDecodeError as e:
            print(f"Error parsing message: {e}")
    
    def _on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"WebSocket error: {error}")
        self.connected = False
        st.session_state.websocket_connected = False
    
    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket connection closed"""
        self.connected = False
        st.session_state.websocket_connected = False
        print("🔌 WebSocket closed")
        time.sleep(5)
        self.start_connection()
    
    def disconnect(self):
        """Disconnect WebSocket"""
        if self.ws:
            self.ws.close()
        self.connected = False
        st.session_state.websocket_connected = False
    
    def get_status(self):
        """Get connection status"""
        if self.connected:
            return "connected", "🟢"
        return "disconnected", "🔴"
    
websocket_manager = RealTimeWebSocketManager()

# ================================
# HELPER FUNCTIONS
# ================================

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
        metrics_response = requests.get(f"{BACKEND_URL}/api/metrics")
        if metrics_response.status_code == 200:
            st.session_state.dashboard_data['metrics'] = metrics_response.json()
        
        risks_response = requests.get(f"{BACKEND_URL}/api/top-risks?limit=10")
        if risks_response.status_code == 200:
            st.session_state.dashboard_data['top_risks'] = risks_response.json()
        
        breakdown_response = requests.get(f"{BACKEND_URL}/api/risk-breakdown")
        if breakdown_response.status_code == 200:
            st.session_state.dashboard_data['breakdown'] = breakdown_response.json()
        
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
        textfont={"size": 11, "color": "#FFFFFF"},
        hoverongaps=False,
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br><b>Risk Score: %{z:.1f}%</b><br><extra></extra>",
    ))
    
    fig.update_layout(
        title="Drug Confusion Risk Matrix",
        xaxis_title="Drug Names",
        yaxis_title="Drug Names",
        height=600,
        font=dict(size=12),
        xaxis=dict(tickangle=45),
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
        height=400,
        showlegend=True,
        annotations=[
            dict(
                text=f"Total<br>{sum(counts)}",
                x=0.5, y=0.5,
                font=dict(size=16),
                showarrow=False
            )
        ]
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
            hovertemplate="<b>%{y}</b><br>Risk Score: <b>%{x:.1f}%</b><br>Category: %{customdata[0]}<br>%{customdata[1]}<extra></extra>",
            customdata=list(zip(categories, reasons)),
        )
    ])
    
    fig.update_layout(
        title="Top 10 High-Risk Drug Pairs",
        xaxis_title="Risk Score (%)",
        yaxis_title="Drug Pairs",
        height=500,
        xaxis=dict(range=[0, 105]),
        yaxis=dict(categoryorder='total ascending')
    )
    
    fig.add_vline(x=75, line_dash="dash", line_color="#b5179e", opacity=0.3)
    fig.add_vline(x=50, line_dash="dash", line_color=COLORS["danger"], opacity=0.3)
    fig.add_vline(x=25, line_dash="dash", line_color=COLORS["warning"], opacity=0.3)
    
    return fig

def display_realtime_metrics():
    """Display real-time metrics"""
    metrics = st.session_state.realtime_metrics or {}
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Drugs", metrics.get('total_drugs', 0))
    
    with col2:
        st.metric("Critical Pairs", metrics.get('critical_risk_pairs', 0))
    
    with col3:
        st.metric("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%")
    
    with col4:
        st.metric("Connected Clients", metrics.get('connected_clients', 0))
    
    if st.session_state.get('last_update_time'):
        st.caption(f"Last update: {st.session_state.last_update_time}")

# ================================
# MAIN APPLICATION
# ================================

# Title
st.title("MediNomix - Medication Safety Platform")
st.markdown("AI-Powered Medication Confusion Risk Analysis")

# Quick Actions
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Seed Database", use_container_width=True):
        with st.spinner("Seeding database..."):
            if seed_database():
                load_dashboard_data()
                st.rerun()
with col2:
    if st.button("Refresh Data", use_container_width=True):
        with st.spinner("Refreshing..."):
            load_dashboard_data()
            st.rerun()
with col3:
    if st.button("Quick Demo", use_container_width=True):
        with st.spinner("Testing with Metformin..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
with col4:
    if st.button("Connect Live", use_container_width=True):
        websocket_manager.start_connection()
        st.success("Real-time connection started!")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Drug Analysis", "Analytics Dashboard", "Real-Time Dashboard", "About"])

# TAB 1: DRUG ANALYSIS
with tab1:
    st.header("Drug Confusion Risk Analysis")
    
    drug_name = st.text_input("Enter drug name:", placeholder="e.g., metformin, lamictal, celebrex...")
    
    col1, col2 = st.columns(2)
    with col1:
        search_clicked = st.button("Analyze Drug", use_container_width=True, type="primary")
    with col2:
        if st.button("Show Examples", use_container_width=True):
            st.info("Try: metformin, lamictal, celebrex, clonidine, zyprexa")
    
    if search_clicked and drug_name:
        with st.spinner(f"Analyzing '{drug_name}'..."):
            result = search_drug(drug_name)
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.success(f"Found {len(st.session_state.search_results)} similar drugs.")
                st.rerun()
    
    # Results
    if st.session_state.search_results:
        st.divider()
        
        # Risk Filters
        st.subheader("Filter Results")
        risk_filters = ["All Risks", "Critical (≥75%)", "High (50-74%)", "Medium (25-49%)", "Low (<25%)"]
        selected_filter = st.radio("Risk Level:", risk_filters, horizontal=True)
        
        # Map selection to filter value
        filter_map = {
            "All Risks": "all",
            "Critical (≥75%)": "critical",
            "High (50-74%)": "high",
            "Medium (25-49%)": "medium",
            "Low (<25%)": "low"
        }
        selected_value = filter_map[selected_filter]
        
        # Filter results
        if selected_value == "all":
            filtered_results = st.session_state.search_results
        else:
            filtered_results = [
                r for r in st.session_state.search_results 
                if r['risk_category'] == selected_value
            ]
        
        st.info(f"Showing {len(filtered_results)} drugs ({selected_filter.lower()})")
        
        # Display results
        for result in filtered_results:
            with st.expander(f"{result['target_drug']['brand_name']} - {result['risk_category'].upper()} Risk ({result['combined_risk']:.0f}%)", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Spelling Similarity", f"{result['spelling_similarity']:.1f}%")
                    st.metric("Phonetic Similarity", f"{result['phonetic_similarity']:.1f}%")
                
                with col2:
                    st.metric("Therapeutic Context", f"{result['therapeutic_context_risk']:.1f}%")
                    st.metric("Overall Risk", f"{result['combined_risk']:.1f}%")
                
                if result['target_drug'].get('purpose'):
                    st.write("**Purpose:**", result['target_drug']['purpose'][:200] + "...")
                
                if result['target_drug'].get('manufacturer'):
                    st.write("**Manufacturer:**", result['target_drug']['manufacturer'])

# TAB 2: ANALYTICS DASHBOARD
with tab2:
    st.header("Analytics Dashboard")
    
    if st.button("Load Dashboard Data", type="secondary"):
        load_dashboard_data()
        st.rerun()
    
    # Load data if not loaded
    if 'metrics' not in st.session_state.dashboard_data:
        load_dashboard_data()
    
    # Metrics
    if 'metrics' in st.session_state.dashboard_data:
        metrics = st.session_state.dashboard_data['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Drugs", metrics.get('total_drugs', 0))
        with col2:
            st.metric("High/Critical Pairs", metrics.get('high_risk_pairs', 0))
        with col3:
            st.metric("Critical Pairs", metrics.get('critical_risk_pairs', 0))
        with col4:
            st.metric("Avg Risk Score", f"{metrics.get('avg_risk_score', 0):.1f}%")
    
    st.divider()
    
    # Heatmap
    st.subheader("Drug Confusion Heatmap")
    heatmap_chart = create_heatmap_chart()
    if heatmap_chart:
        st.plotly_chart(heatmap_chart, use_container_width=True)
    else:
        st.info("No heatmap data available. Seed the database first.")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Distribution")
        breakdown_chart = create_risk_breakdown_chart()
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
    
    with col2:
        st.subheader("Top Risk Pairs")
        risks_chart = create_top_risks_chart()
        if risks_chart:
            st.plotly_chart(risks_chart, use_container_width=True)
    
    st.divider()
    
    # FDA Alert Table
    st.subheader("FDA High Alert Drug Pairs")
    risky_pairs = pd.DataFrame([
        {"Drug 1": "Lamictal", "Drug 2": "Lamisil", "Risk Level": "Critical", 
         "Medical Use": "Epilepsy vs Fungal infection", "Alert Type": "FDA Safety Warning"},
        {"Drug 1": "Celebrex", "Drug 2": "Celexa", "Risk Level": "Critical", 
         "Medical Use": "Arthritis vs Depression", "Alert Type": "ISMP High Alert"},
        {"Drug 1": "Metformin", "Drug 2": "Metronidazole", "Risk Level": "High", 
         "Medical Use": "Diabetes vs Antibiotic", "Alert Type": "Common Error"},
        {"Drug 1": "Clonidine", "Drug 2": "Klonopin", "Risk Level": "High", 
         "Medical Use": "Blood pressure vs Anxiety", "Alert Type": "Sound-alike"},
        {"Drug 1": "Zyprexa", "Drug 2": "Zyrtec", "Risk Level": "Medium", 
         "Medical Use": "Antipsychotic vs Allergy", "Alert Type": "Look-alike"},
    ])
    
    st.dataframe(risky_pairs, use_container_width=True)

# TAB 3: REAL-TIME DASHBOARD
with tab3:
    st.header("Real-Time Dashboard")
    
    # Connection status
    if st.session_state.websocket_connected:
        st.success("✅ Real-time connection active")
    else:
        st.warning("⚠️ Real-time connection not active")
    
    # Auto-start WebSocket if not connected
    if not st.session_state.websocket_connected:
        websocket_manager.start_connection()
    
    if st.button("Refresh Metrics", type="secondary"):
        st.rerun()
    
    # Display metrics
    metrics = st.session_state.realtime_metrics or {}
    
    if metrics:
        display_realtime_metrics()
        
        if 'recent_searches' in metrics and metrics['recent_searches']:
            st.subheader("Recent Activity")
            for search in metrics['recent_searches'][:5]:
                timestamp = search.get('timestamp', '').split('T')[1].split('.')[0] if 'T' in search.get('timestamp', '') else ''
                st.info(
                    f"**{search.get('drug_name', 'Unknown')}** - "
                    f"Found {search.get('similar_drugs_found', 0)} risks - "
                    f"Highest risk: {search.get('highest_risk', 0):.1f}% "
                    f"({timestamp})"
                )
    else:
        st.info("No real-time data available yet.")

# TAB 4: ABOUT
with tab4:
    st.header("About MediNomix")
    
    st.write("""
    A medication safety platform designed to prevent medication errors through AI analysis.
    
    **Key Statistics:**
    - 25% of medication errors involve name confusion (FDA)
    - 1.5 million Americans harmed annually
    - $42 billion in preventable costs
    
    **Common Error Pairs:**
    - Lamictal ↔ Lamisil (Epilepsy vs Fungal infection)
    - Celebrex ↔ Celexa (Arthritis vs Depression)
    - Metformin ↔ Metronidazole (Diabetes vs Antibiotic)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Medication Errors", "25%", "involve name confusion", delta_color="inverse")
    
    with col2:
        st.metric("Annual Harm", "1.5M", "Americans affected", delta_color="inverse")

# ================================
# SIDEBAR
# ================================

with st.sidebar:
    st.title("MediNomix")
    st.caption("AI-Powered Medication Safety")
    
    st.divider()
    
    st.subheader("Quick Actions")
    
    if st.button("Test with Metformin", use_container_width=True):
        with st.spinner("Testing..."):
            result = search_drug("metformin")
            if result:
                st.session_state.search_results = result.get('similar_drugs', [])
                st.rerun()
    
    if st.button("Load Sample Data", use_container_width=True):
        if seed_database():
            load_dashboard_data()
            st.rerun()
    
    st.divider()
    
    st.subheader("System Status")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                st.success("✅ Backend Connected")
                st.metric("Drugs in DB", data.get('drugs_in_database', 0))
            else:
                st.warning("⚠️ Backend Error")
        else:
            st.error("❌ Cannot Connect")
    except:
        st.error("🔌 Backend Not Running")
        st.code("python backend.py", language="bash")
    
    st.divider()
    
    st.subheader("Risk Categories")
    
    risk_data = [
        ("Critical", "≥75%", "Immediate intervention"),
        ("High", "50-74%", "Review required"),
        ("Medium", "25-49%", "Monitor closely"),
        ("Low", "<25%", "Low priority"),
    ]
    
    for name, range_, desc in risk_data:
        st.markdown(f"**{name} {range_}**")
        st.caption(desc)

# Auto-start WebSocket
if not st.session_state.get('websocket_connected'):
    websocket_manager.start_connection()