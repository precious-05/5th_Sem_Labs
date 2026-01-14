import streamlit as st
import pandas as pd
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="OS Deadlock Simulator",
    page_icon="⚡",
    layout="wide"
)

# Modern Dark Tech Theme with Fixed Text Colors
st.markdown("""
<style>
    /* Modern Dark Tech Theme */
    :root {
        --bg-dark: #0F172A;
        --panel-dark: #1E293B;
        --panel-darker: #0F172A;
        --accent-purple: #A855F7;
        --accent-purple-light: #C084FC;
        --accent-blue: #38BDF8;
        --accent-blue-light: #7DD3FC;
        --success: #10B981;
        --success-light: #34D399;
        --danger: #EF4444;
        --danger-light: #F87171;
        --warning: #F59E0B;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --border-color: #334155;
        --shadow-color: rgba(0, 0, 0, 0.3);
    }
    
    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #0D1524 100%);
        color: var(--text-primary) !important;
    }
    
    /* Fix ALL Streamlit text colors */
    .stMarkdown, p, h1, h2, h3, h4, h5, h6, div, span, label {
        color: var(--text-primary) !important;
    }
    
    /* Fix Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
        color: white !important;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4);
        background: linear-gradient(135deg, var(--accent-purple-light), var(--accent-blue-light));
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Fix Number Input Styling */
    div[data-baseweb="input"] {
        background: var(--panel-dark) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="input"] input {
    color: var(--text-primary) !important;
    background: transparent !important;
}

/* Add these lines */
div[data-baseweb="input"] input::placeholder {
    color: rgba(255, 255, 255, 0.7) !important;
}

div[data-baseweb="input"] input[type="number"] {
    color: black !important;
}
    
    /* Fix Select Box Styling */
    div[data-baseweb="select"] {
        background: var(--panel-dark) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] div {
        color: var(--text-primary) !important;
        background: transparent !important;
    }
    
    /* Fix Placeholder Text */
    input::placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.7 !important;
    }
    
    /* Fix Labels */
    label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--panel-dark);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(to bottom, var(--accent-purple), var(--accent-blue));
        border-radius: 4px;
    }
    
    /* Main Header - Tech Style */
    .tech-header {
        background: linear-gradient(90deg, var(--panel-darker), var(--panel-dark));
        padding: 30px 40px;
        margin: -20px -20px 30px -20px;
        border-bottom: 1px solid var(--accent-purple);
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .tech-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-purple), var(--accent-blue));
    }
    
    .tech-header h1 {
        color: var(--text-primary);
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 8px;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    .tech-header p {
        color: var(--accent-blue);
        font-size: 16px;
        margin: 0;
        font-weight: 400;
    }
    
    /* Tech Cards */
    .tech-card {
        background: var(--panel-dark);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 12px var(--shadow-color);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .tech-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-purple), var(--accent-blue));
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tech-card:hover::before {
        opacity: 1;
    }
    
    .tech-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(168, 85, 247, 0.2);
        border-color: var(--accent-purple);
    }
    
    .tech-card-title {
        color: var(--accent-blue);
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        margin: 5px;
        color: white !important;
    }
    
    .status-safe {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        color: var(--success-light) !important;
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }
    
    .status-unsafe {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
        color: var(--danger-light) !important;
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
    }
    
    /* Resource Bars */
    .resource-bar-container {
        margin: 15px 0;
    }
    
    .resource-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 14px;
        color: var(--text-secondary);
    }
    
    .resource-bar {
        height: 20px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    
    .resource-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent-purple), var(--accent-blue));
        border-radius: 10px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 10px;
        color: white !important;
        font-size: 12px;
        font-weight: 600;
        min-width: 40px;
    }
    
    /* Matrix Tables */
    .matrix-container {
        overflow-x: auto;
        margin: 15px 0;
    }
    
    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        background: rgba(15, 23, 42, 0.5);
        color: var(--text-primary) !important;
    }
    
    .matrix-table th {
        background: linear-gradient(90deg, var(--panel-dark), rgba(56, 189, 248, 0.1));
        padding: 14px;
        text-align: center;
        font-weight: 600;
        color: var(--accent-blue) !important;
        border: 1px solid var(--border-color);
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    .matrix-table td {
        padding: 14px;
        text-align: center;
        border: 1px solid var(--border-color);
        color: var(--text-primary) !important;
        background: rgba(15, 23, 42, 0.3);
        transition: background 0.3s;
    }
    
    .matrix-table tr:hover td {
        background: rgba(168, 85, 247, 0.1);
    }
    
    /* Footer */
    .tech-footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        background: rgba(15, 23, 42, 0.8);
        border-top: 1px solid var(--border-color);
        color: var(--text-secondary) !important;
        font-size: 14px;
        position: relative;
    }
    
    .tech-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 20%;
        right: 20%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-purple), transparent);
    }
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: var(--panel-dark);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        gap: 8px;
        padding: 10px 20px;
        font-weight: 500;
        color: var(--text-secondary) !important;
        border: 1px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(168, 85, 247, 0.1);
        color: var(--text-primary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(56, 189, 248, 0.1));
        color: var(--accent-blue) !important;
        border: 1px solid var(--accent-purple);
        box-shadow: 0 2px 8px rgba(168, 85, 247, 0.2);
    }
    
    /* Success/Error Messages */
    .stAlert {
        border: 1px solid !important;
        border-radius: 8px !important;
        padding: 16px !important;
        margin: 10px 0 !important;
    }
    
    .stAlert[data-baseweb="notification"][kind="success"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), transparent) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
        color: var(--success-light) !important;
    }
    
    .stAlert[data-baseweb="notification"][kind="error"] {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), transparent) !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
        color: var(--danger-light) !important;
    }
    
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), transparent) !important;
        border-color: rgba(245, 158, 11, 0.3) !important;
        color: var(--warning) !important;
    }
    
    /* Process Names */
    .process-name {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 500;
        color: var(--accent-blue-light) !important;
    }
    
    .resource-name {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 500;
        color: var(--accent-purple-light) !important;
    }
    
    /* Dataframe Styling */
    .dataframe {
        color: var(--text-primary) !important;
    }
    
    .dataframe th {
        color: var(--accent-blue) !important;
    }
    
    .dataframe td {
        color: var(--text-primary) !important;
    }
    
    /* Info Boxes */
    .info-box {
        padding: 15px;
        background: rgba(56, 189, 248, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin: 10px 0;
        color: var(--accent-blue-light) !important;
    }
    
    /* Sequence Display */
    .sequence-display {
        font-family: 'Courier New', monospace;
        padding: 12px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 6px;
        border: 1px solid var(--border-color);
        color: var(--success-light) !important;
        margin: 10px 0;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Request History Items */
    .request-item {
        border-left: 3px solid;
        padding: 12px;
        margin-bottom: 10px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 0 8px 8px 0;
    }
    
    .request-item.granted {
        border-left-color: var(--success);
    }
    
    .request-item.denied {
        border-left-color: var(--danger);
    }
    
    /* Remove all emojis from buttons */
    .button-icon {
        margin-right: 8px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Banker's Algorithm Implementation
class BankersAlgorithm:
    def __init__(self, num_processes, num_resources):
        self.num_processes = num_processes
        self.num_resources = num_resources
        
    def is_safe_state(self, allocation, max_demand, available):
        """Check if system is in safe state using Banker's Algorithm"""
        n = self.num_processes
        m = self.num_resources
        
        work = available.copy()
        finish = [False] * n
        safe_sequence = []
        
        # Calculate need matrix
        need = [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
        
        for _ in range(n):
            found = False
            for i in range(n):
                if not finish[i]:
                    can_allocate = True
                    for j in range(m):
                        if need[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        for j in range(m):
                            work[j] += allocation[i][j]
                        safe_sequence.append(i)
                        finish[i] = True
                        found = True
                        break
            
            if not found:
                return False, []
        
        return True, safe_sequence
    
    def resource_request(self, process_id, request, allocation, max_demand, available):
        """Handle resource request using Banker's Algorithm"""
        n = self.num_processes
        m = self.num_resources
        
        # Check if request <= need
        need = [max_demand[process_id][j] - allocation[process_id][j] for j in range(m)]
        for j in range(m):
            if request[j] > need[j]:
                return False, "Process exceeded maximum claim"
        
        # Check if request <= available
        for j in range(m):
            if request[j] > available[j]:
                return False, "Resources not available"
        
        # Try to allocate temporarily
        temp_allocation = [row[:] for row in allocation]
        temp_available = available[:]
        
        for j in range(m):
            temp_allocation[process_id][j] += request[j]
            temp_available[j] -= request[j]
        
        # Check if new state is safe
        is_safe, sequence = self.is_safe_state(temp_allocation, max_demand, temp_available)
        
        if is_safe:
            return True, "Request granted. System remains safe."
        else:
            return False, "Request denied. Would lead to unsafe state."
    
    def detect_deadlock(self, allocation, request, available):
        """Detect deadlock using deadlock detection algorithm"""
        n = self.num_processes
        m = self.num_resources
        
        work = available.copy()
        finish = [sum(allocation[i]) == 0 for i in range(n)]
        
        while True:
            found = False
            for i in range(n):
                if not finish[i]:
                    can_allocate = True
                    for j in range(m):
                        if request[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        for j in range(m):
                            work[j] += allocation[i][j]
                        finish[i] = True
                        found = True
            
            if not found:
                break
        
        deadlocked = [i for i in range(n) if not finish[i]]
        return deadlocked

# Process and Resource Names
PROCESS_NAMES = [
    "Chrome Browser",
    "VS Code Editor", 
    "Spotify Player",
    "Discord Client",
    "Zoom Meeting",
    "Adobe Photoshop",
    "Blender 3D",
    "MySQL Server",
    "Docker Engine",
    "Node.js Server"
]

RESOURCE_NAMES = [
    "CPU Cores",
    "GPU Memory", 
    "RAM Allocation",
    "Disk I/O",
    "Network Bandwidth",
    "USB Ports",
    "Audio Channels",
    "File Handles"
]

# Initialize session state
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False
    st.session_state.num_processes = 5
    st.session_state.num_resources = 3
    st.session_state.allocation = []
    st.session_state.max_demand = []
    st.session_state.available = []
    st.session_state.request_history = []

def initialize_system():
    """Initialize system with random values"""
    np.random.seed(42)
    
    n = st.session_state.num_processes
    m = st.session_state.num_resources
    
    # Generate allocation matrix
    allocation = np.random.randint(0, 3, (n, m)).tolist()
    
    # Generate max demand matrix
    max_demand = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(allocation[i][j] + np.random.randint(1, 4))
        max_demand.append(row)
    
    # Generate available resources
    total_allocated = np.sum(allocation, axis=0)
    available = [total_allocated[j] + np.random.randint(2, 6) for j in range(m)]
    
    # Store in session state
    st.session_state.allocation = allocation
    st.session_state.max_demand = max_demand
    st.session_state.available = available
    st.session_state.system_initialized = True
    st.session_state.request_history = []

# Header
st.markdown("""
<div class="tech-header">
    <h1>OS Deadlock Simulator</h1>
    <p>Advanced Banker's Algorithm Visualization with Real Process Names</p>
</div>
""", unsafe_allow_html=True)

# Main Layout
col1, col2, col3 = st.columns([1.2, 1.8, 1])

with col1:
    # Configuration Card
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">
            System Configuration
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<label>Number of Processes</label>', unsafe_allow_html=True)
    num_processes = st.number_input(
        "",
        min_value=3,
        max_value=10,
        value=st.session_state.num_processes,
        key="input_processes",
        label_visibility="collapsed"
    )
    
    st.markdown('<label>Number of Resources</label>', unsafe_allow_html=True)
    num_resources = st.number_input(
        "",
        min_value=2,
        max_value=8,
        value=st.session_state.num_resources,
        key="input_resources",
        label_visibility="collapsed"
    )
    
    st.session_state.num_processes = num_processes
    st.session_state.num_resources = num_resources
    
    if st.button("Initialize System", use_container_width=True, key="init_btn"):
        with st.spinner("Initializing system resources..."):
            time.sleep(0.5)
            initialize_system()
            st.success("System initialized successfully!")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Available Resources Card
    if st.session_state.system_initialized:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">
                Resource Monitor
            </div>
        """, unsafe_allow_html=True)
        
        for j in range(st.session_state.num_resources):
            resource_name = RESOURCE_NAMES[j % len(RESOURCE_NAMES)]
            total_allocated = sum(st.session_state.allocation[i][j] for i in range(st.session_state.num_processes))
            total = st.session_state.available[j] + total_allocated
            percentage = (st.session_state.available[j] / total * 100) if total > 0 else 0
            
            st.markdown(f"""
            <div class="resource-bar-container">
                <div class="resource-label">
                    <span class="resource-name">{resource_name}</span>
                    <span>{st.session_state.available[j]}/{total}</span>
                </div>
                <div class="resource-bar">
                    <div class="resource-fill" style="width: {percentage}%">
                        {int(percentage)}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if st.session_state.system_initialized:
        # System Matrices Card
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">
                Resource Allocation Matrix
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Allocation", "Maximum", "Available"])
        
        with tab1:
            alloc_df = pd.DataFrame(
                st.session_state.allocation,
                index=[f"<span class='process-name'>{PROCESS_NAMES[i % len(PROCESS_NAMES)]}</span>" 
                       for i in range(st.session_state.num_processes)],
                columns=[f"<span class='resource-name'>{RESOURCE_NAMES[j % len(RESOURCE_NAMES)]}</span>" 
                         for j in range(st.session_state.num_resources)]
            )
            st.markdown(alloc_df.to_html(escape=False), unsafe_allow_html=True)
        
        with tab2:
            max_df = pd.DataFrame(
                st.session_state.max_demand,
                index=[f"<span class='process-name'>{PROCESS_NAMES[i % len(PROCESS_NAMES)]}</span>" 
                       for i in range(st.session_state.num_processes)],
                columns=[f"<span class='resource-name'>{RESOURCE_NAMES[j % len(RESOURCE_NAMES)]}</span>" 
                         for j in range(st.session_state.num_resources)]
            )
            st.markdown(max_df.to_html(escape=False), unsafe_allow_html=True)
        
        with tab3:
            avail_df = pd.DataFrame(
                [st.session_state.available],
                columns=[f"<span class='resource-name'>{RESOURCE_NAMES[j % len(RESOURCE_NAMES)]}</span>" 
                         for j in range(st.session_state.num_resources)],
                index=["<span class='process-name'>Available Resources</span>"]
            )
            st.markdown(avail_df.to_html(escape=False), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Resource Request Card
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">
                Resource Request Manager
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<label>Select Process</label>', unsafe_allow_html=True)
        selected_process = st.selectbox(
            "",
            [f"{PROCESS_NAMES[i % len(PROCESS_NAMES)]}" 
             for i in range(st.session_state.num_processes)],
            key="selected_process",
            label_visibility="collapsed"
        )
        pid = next(i for i in range(st.session_state.num_processes) 
                  if PROCESS_NAMES[i % len(PROCESS_NAMES)] == selected_process)
        
        st.markdown('<label>Request Resources</label>', unsafe_allow_html=True)
        cols = st.columns(st.session_state.num_resources)
        request = []
        for j in range(st.session_state.num_resources):
            with cols[j]:
                resource_name = RESOURCE_NAMES[j % len(RESOURCE_NAMES)]
                max_req = st.session_state.max_demand[pid][j] - st.session_state.allocation[pid][j]
                st.markdown(f"<div style='font-size: 12px; color: var(--text-secondary);'>{resource_name}</div>", 
                           unsafe_allow_html=True)
                req = st.number_input(
                    "",
                    min_value=0,
                    max_value=max_req,
                    value=0,
                    key=f"req_input_{j}",
                    label_visibility="collapsed",
                    placeholder="0"
                )
                request.append(req)
        
        if st.button("Submit Resource Request", use_container_width=True, key="submit_request"):
            if sum(request) > 0:
                with st.spinner("Processing request with Banker's Algorithm..."):
                    time.sleep(0.8)
                    banker = BankersAlgorithm(st.session_state.num_processes, st.session_state.num_resources)
                    granted, message = banker.resource_request(
                        pid, request, 
                        st.session_state.allocation,
                        st.session_state.max_demand,
                        st.session_state.available
                    )
                    
                    if granted:
                        # Update allocation and available
                        for j in range(st.session_state.num_resources):
                            st.session_state.allocation[pid][j] += request[j]
                            st.session_state.available[j] -= request[j]
                        st.success(message)
                    else:
                        st.error(message)
                    
                    # Add to history
                    st.session_state.request_history.append({
                        'process': selected_process,
                        'request': request.copy(),
                        'granted': granted,
                        'time': time.strftime("%H:%M:%S")
                    })
                    st.rerun()
            else:
                st.warning("Please request at least one resource unit")
        
        st.markdown("</div>", unsafe_allow_html=True)

with col3:
    if st.session_state.system_initialized:
        # System Status Card
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">
                System Safety Status
            </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Analyzing system safety..."):
            time.sleep(0.3)
            banker = BankersAlgorithm(st.session_state.num_processes, st.session_state.num_resources)
            is_safe, sequence = banker.is_safe_state(
                st.session_state.allocation,
                st.session_state.max_demand,
                st.session_state.available
            )
        
        if is_safe:
            st.markdown("""
            <div class="status-indicator status-safe">
                SYSTEM SAFE
            </div>
            """, unsafe_allow_html=True)
            
            # FIXED: Properly display safe sequence
            sequence_names = [PROCESS_NAMES[p % len(PROCESS_NAMES)] for p in sequence]
            sequence_text = " → ".join(sequence_names)
            
            st.markdown(f"""
            <div style="margin-top: 20px;">
                <div style="color: var(--success-light); font-weight: 600; margin-bottom: 10px;">
                    Safe Execution Sequence:
                </div>
                <div class="sequence-display">
                    {sequence_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-indicator status-unsafe">
                SYSTEM UNSAFE
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin-top: 20px; padding: 15px; background: rgba(239, 68, 68, 0.1); 
                        border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.3);">
                <div style="color: var(--danger-light); font-weight: 600; margin-bottom: 10px;">
                    Warning: Potential Deadlock
                </div>
                <div style="color: var(--text-secondary); font-size: 14px;">
                    System may enter deadlock if processes request additional resources.
                    Consider reallocating resources or increasing availability.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Run Safety Analysis", use_container_width=True, key="safety_check"):
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Deadlock Detection Card
        st.markdown("""
        <div class="tech-card">
            <div class="tech-card-title">
                Deadlock Detection
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Scan for Deadlocks", use_container_width=True, key="detect_deadlock"):
            with st.spinner("Scanning system for deadlock conditions..."):
                time.sleep(1)
                banker = BankersAlgorithm(st.session_state.num_processes, st.session_state.num_resources)
                
                # Generate random request matrix for simulation
                request_matrix = np.random.randint(0, 2, 
                    (st.session_state.num_processes, st.session_state.num_resources)).tolist()
                
                deadlocked = banker.detect_deadlock(
                    st.session_state.allocation,
                    request_matrix,
                    st.session_state.available
                )
                
                if deadlocked:
                    deadlocked_names = [PROCESS_NAMES[p % len(PROCESS_NAMES)] for p in deadlocked]
                    st.error(f"**DEADLOCK DETECTED!** \n\n**Blocked Processes:**\n{', '.join(deadlocked_names)}")
                    
                    if st.button(f"Terminate {deadlocked_names[0]}", use_container_width=True):
                        # Release resources of first deadlocked process
                        terminated = deadlocked[0]
                        for j in range(st.session_state.num_resources):
                            st.session_state.available[j] += st.session_state.allocation[terminated][j]
                            st.session_state.allocation[terminated][j] = 0
                        st.success(f"Process {deadlocked_names[0]} terminated. Resources released.")
                        st.rerun()
                else:
                    st.success("**NO DEADLOCK DETECTED**\n\nAll processes can proceed with current resource allocation.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Request History
        if st.session_state.request_history:
            st.markdown("""
            <div class="tech-card">
                <div class="tech-card-title">
                    Request History
                </div>
            """, unsafe_allow_html=True)
            
            for req in reversed(st.session_state.request_history[-3:]):
                item_class = "granted" if req['granted'] else "denied"
                
                st.markdown(f"""
                <div class="request-item {item_class}">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <div style="font-weight: 600; color: var(--text-primary) !important;">
                                {req['process']}
                            </div>
                            <div style="color: var(--text-secondary) !important; font-size: 12px; margin-top: 4px;">
                                {req['time']}
                            </div>
                        </div>
                        <div style="font-size: 18px; color: {'var(--success)' if req['granted'] else 'var(--danger)'} !important;">
                            {'✓' if req['granted'] else '✗'}
                        </div>
                    </div>
                    <div style="color: var(--accent-blue-light) !important; font-size: 13px; margin-top: 8px;">
                        Request: {req['request']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="tech-footer">
    <div style="margin-bottom: 15px; font-size: 16px; color: var(--accent-blue) !important; font-weight: 500;">
        OS Deadlock Simulation System
    </div>
    <div style="color: var(--text-primary) !important; margin-bottom: 8px; font-weight: 500;">
        Developed by Alina Liaquat
    </div>
    <div style="color: var(--text-secondary) !important; font-size: 13px;">
        Advanced Banker's Algorithm Implementation | Operating Systems Project
    </div>
</div>
""", unsafe_allow_html=True)

# Initialization Message
if not st.session_state.system_initialized:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 60px 40px; background: rgba(30, 41, 59, 0.8); 
                    border-radius: 16px; margin-top: 40px; border: 2px solid rgba(168, 85, 247, 0.3);
                    box-shadow: 0 0 30px rgba(168, 85, 247, 0.1);">
            <div style="font-size: 72px; color: var(--accent-purple) !important; margin-bottom: 20px;">
                ⚙️
            </div>
            <h3 style="color: var(--accent-blue) !important; margin-bottom: 15px; font-weight: 600;">
                System Initialization Required
            </h3>
            <p style="color: var(--text-secondary) !important; margin-bottom: 30px; line-height: 1.6;">
                Configure system parameters and initialize to begin deadlock simulation<br>
                Monitor real process behavior and resource allocation in real-time
            </p>
            <div style="color: var(--accent-purple-light) !important; font-size: 14px; padding: 12px; 
                      background: rgba(168, 85, 247, 0.1); border-radius: 8px;">
                Set processes & resources, then click "Initialize System"
            </div>
        </div>
        """, unsafe_allow_html=True)