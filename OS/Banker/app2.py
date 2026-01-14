import streamlit as st
import pandas as pd
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="OS Deadlock Manager",
    page_icon="⚙️",
    layout="wide"
)

# Clean OS-Style Theme with No JavaScript
st.markdown("""
<style>
    /* Modern OS Theme - Windows/Mac Inspired */
    :root {
        --os-blue: #0078D4;
        --os-dark-blue: #005A9E;
        --os-gray: #F3F3F3;
        --os-dark-gray: #2D2D2D;
        --os-light-gray: #F8F8F8;
        --os-border: #E0E0E0;
        --os-success: #107C10;
        --os-warning: #F7630C;
        --os-danger: #D13438;
        --os-text: #323130;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Main Header - OS Style */
    .os-header {
        background: linear-gradient(135deg, var(--os-dark-blue), var(--os-blue));
        padding: 25px 40px;
        margin: -20px -20px 30px -20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        color: white;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .os-header h1 {
        color: white;
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .os-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 16px;
        margin: 0;
    }
    
    /* OS Style Cards */
    .os-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid var(--os-border);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .os-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .os-card-title {
        color: var(--os-dark-blue);
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--os-border);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-safe {
        background-color: var(--os-success);
        box-shadow: 0 0 8px var(--os-success);
    }
    
    .status-unsafe {
        background-color: var(--os-danger);
        box-shadow: 0 0 8px var(--os-danger);
    }
    
    /* OS Style Buttons */
    .os-button {
        background: linear-gradient(to bottom, var(--os-blue), var(--os-dark-blue));
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 4px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        font-size: 14px;
    }
    
    .os-button:hover {
        background: linear-gradient(to bottom, var(--os-dark-blue), var(--os-blue));
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 120, 212, 0.3);
    }
    
    .os-button:active {
        transform: translateY(0);
    }
    
    .os-button-secondary {
        background: var(--os-light-gray);
        color: var(--os-text);
        border: 1px solid var(--os-border);
    }
    
    .os-button-secondary:hover {
        background: var(--os-gray);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Resource Indicators */
    .resource-bar {
        height: 24px;
        background: var(--os-gray);
        border-radius: 12px;
        overflow: hidden;
        margin: 10px 0;
        border: 1px solid var(--os-border);
    }
    
    .resource-fill {
        height: 100%;
        background: linear-gradient(to right, var(--os-blue), var(--os-dark-blue));
        border-radius: 12px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* Matrix Tables */
    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }
    
    .matrix-table th {
        background: var(--os-light-gray);
        padding: 12px;
        text-align: center;
        font-weight: 600;
        color: var(--os-dark-blue);
        border: 1px solid var(--os-border);
    }
    
    .matrix-table td {
        padding: 12px;
        text-align: center;
        border: 1px solid var(--os-border);
        background: white;
    }
    
    .matrix-table tr:hover td {
        background: var(--os-gray);
    }
    
    /* Process Steps */
    .process-steps {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 30px 0;
        position: relative;
    }
    
    .process-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        z-index: 2;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--os-gray);
        border: 2px solid var(--os-border);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-bottom: 8px;
        transition: all 0.3s;
    }
    
    .step-circle.active {
        background: var(--os-blue);
        border-color: var(--os-blue);
        color: white;
    }
    
    .step-line {
        position: absolute;
        top: 20px;
        left: 20%;
        right: 20%;
        height: 2px;
        background: var(--os-border);
        z-index: 1;
    }
    
    /* Footer */
    .os-footer {
        text-align: center;
        padding: 25px;
        margin-top: 40px;
        background: white;
        border-top: 1px solid var(--os-border);
        color: var(--os-text);
        font-size: 14px;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: var(--os-light-gray);
        padding: 4px;
        border-radius: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: var(--os-light-gray);
        border-radius: 4px;
        gap: 8px;
        padding: 10px 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Input Styling */
    .stNumberInput, .stSelectbox {
        border: 1px solid var(--os-border);
        border-radius: 4px;
    }
    
    .stNumberInput input, .stSelectbox div {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Banker's Algorithm Implementation - FIXED
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
                    # Check if process i's needs can be satisfied
                    can_allocate = True
                    for j in range(m):
                        if need[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        # Execute process i
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
                return False, "Error: Process exceeded maximum claim"
        
        # Check if request <= available
        for j in range(m):
            if request[j] > available[j]:
                return False, "Error: Resources not available"
        
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
<div class="os-header">
    <h1>Operating System Deadlock Manager</h1>
    <p>Banker's Algorithm for Deadlock Avoidance and Recovery</p>
</div>
""", unsafe_allow_html=True)

# Main Layout - Three Columns
col1, col2, col3 = st.columns([1.2, 1.8, 1])

with col1:
    # Configuration Card
    st.markdown("""
    <div class="os-card">
        <div class="os-card-title">
            ⚙️ System Configuration
        </div>
    """, unsafe_allow_html=True)
    
    num_processes = st.number_input(
        "Number of Processes",
        min_value=3,
        max_value=10,
        value=st.session_state.num_processes,
        key="input_processes"
    )
    
    num_resources = st.number_input(
        "Number of Resources",
        min_value=2,
        max_value=5,
        value=st.session_state.num_resources,
        key="input_resources"
    )
    
    st.session_state.num_processes = num_processes
    st.session_state.num_resources = num_resources
    
    if st.button("🚀 Initialize System", use_container_width=True, key="init_btn"):
        initialize_system()
        st.success("System initialized successfully!")
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Available Resources Card
    if st.session_state.system_initialized:
        st.markdown("""
        <div class="os-card">
            <div class="os-card-title">
                📦 Available Resources
            </div>
        """, unsafe_allow_html=True)
        
        for j in range(st.session_state.num_resources):
            st.markdown(f"**Resource R{j}**")
            total = st.session_state.available[j] + sum(
                st.session_state.allocation[i][j] for i in range(st.session_state.num_processes)
            )
            percentage = (st.session_state.available[j] / total * 100) if total > 0 else 0
            
            st.markdown(f"""
            <div class="resource-bar">
                <div class="resource-fill" style="width: {percentage}%">
                    {st.session_state.available[j]} / {total}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if st.session_state.system_initialized:
        # System Matrices Card
        st.markdown("""
        <div class="os-card">
            <div class="os-card-title">
                📊 System Matrices
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Allocation", "Maximum", "Available"])
        
        with tab1:
            alloc_df = pd.DataFrame(
                st.session_state.allocation,
                index=[f"P{i}" for i in range(st.session_state.num_processes)],
                columns=[f"R{j}" for j in range(st.session_state.num_resources)]
            )
            st.dataframe(alloc_df, use_container_width=True)
        
        with tab2:
            max_df = pd.DataFrame(
                st.session_state.max_demand,
                index=[f"P{i}" for i in range(st.session_state.num_processes)],
                columns=[f"R{j}" for j in range(st.session_state.num_resources)]
            )
            st.dataframe(max_df, use_container_width=True)
        
        with tab3:
            avail_df = pd.DataFrame(
                [st.session_state.available],
                columns=[f"R{j}" for j in range(st.session_state.num_resources)],
                index=["Available"]
            )
            st.dataframe(avail_df, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Resource Request Card
        st.markdown("""
        <div class="os-card">
            <div class="os-card-title">
                📨 Resource Request
            </div>
        """, unsafe_allow_html=True)
        
        selected_process = st.selectbox(
            "Select Process",
            [f"P{i}" for i in range(st.session_state.num_processes)],
            key="selected_process"
        )
        pid = int(selected_process[1:])
        
        st.markdown("**Request Amount:**")
        cols = st.columns(st.session_state.num_resources)
        request = []
        for j in range(st.session_state.num_resources):
            with cols[j]:
                max_req = st.session_state.max_demand[pid][j] - st.session_state.allocation[pid][j]
                req = st.number_input(
                    f"R{j}",
                    min_value=0,
                    max_value=max_req,
                    value=0,
                    key=f"req_{j}"
                )
                request.append(req)
        
        if st.button("📤 Submit Request", use_container_width=True, key="submit_request"):
            if sum(request) > 0:
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
                st.warning("Please request at least one resource.")
        
        st.markdown("</div>", unsafe_allow_html=True)

with col3:
    if st.session_state.system_initialized:
        # System Status Card
        st.markdown("""
        <div class="os-card">
            <div class="os-card-title">
                📈 System Status
            </div>
        """, unsafe_allow_html=True)
        
        banker = BankersAlgorithm(st.session_state.num_processes, st.session_state.num_resources)
        is_safe, sequence = banker.is_safe_state(
            st.session_state.allocation,
            st.session_state.max_demand,
            st.session_state.available
        )
        
        status_class = "status-safe" if is_safe else "status-unsafe"
        status_text = "SAFE" if is_safe else "UNSAFE"
        status_color = "var(--os-success)" if is_safe else "var(--os-danger)"
        
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <span class="status-indicator {status_class}"></span>
            <span style="font-size: 24px; font-weight: 600; color: {status_color}">
                {status_text}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if is_safe:
            st.markdown(f"""
            <div style="background: #E8F5E9; padding: 15px; border-radius: 6px; margin-top: 15px;">
                <div style="font-weight: 600; color: var(--os-success); margin-bottom: 8px;">
                    ✅ Safe Sequence Found
                </div>
                <div style="font-size: 14px; color: #666;">
                    {' → '.join([f'P{p}' for p in sequence])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #FFEBEE; padding: 15px; border-radius: 6px; margin-top: 15px;">
                <div style="font-weight: 600; color: var(--os-danger); margin-bottom: 8px;">
                    ⚠️ System Unsafe
                </div>
                <div style="font-size: 14px; color: #666;">
                    Deadlock may occur if processes request resources
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Safety Check Button
        if st.button("🔍 Check Safety", use_container_width=True, key="safety_check"):
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Deadlock Detection Card
        st.markdown("""
        <div class="os-card">
            <div class="os-card-title">
                ⚠️ Deadlock Detection
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔎 Detect Deadlock", use_container_width=True, key="detect_deadlock"):
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
                st.error(f"🚨 Deadlock detected in processes: {', '.join([f'P{p}' for p in deadlocked])}")
                
                if st.button("🔄 Recover (Terminate P{})".format(deadlocked[0]), use_container_width=True):
                    # Release resources of first deadlocked process
                    terminated = deadlocked[0]
                    for j in range(st.session_state.num_resources):
                        st.session_state.available[j] += st.session_state.allocation[terminated][j]
                        st.session_state.allocation[terminated][j] = 0
                    st.success(f"Process P{terminated} terminated. Resources released.")
                    st.rerun()
            else:
                st.success("✅ No deadlock detected")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Request History
        if st.session_state.request_history:
            st.markdown("""
            <div class="os-card">
                <div class="os-card-title">
                    📝 Recent Requests
                </div>
            """, unsafe_allow_html=True)
            
            for req in reversed(st.session_state.request_history[-3:]):
                border_color = "var(--os-success)" if req['granted'] else "var(--os-danger)"
                icon = "✅" if req['granted'] else "❌"
                
                st.markdown(f"""
                <div style="border-left: 3px solid {border_color}; padding-left: 10px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{req['process']}</strong>
                            <span style="color: #666; font-size: 12px; margin-left: 8px;">
                                {req['time']}
                            </span>
                        </div>
                        <span style="font-size: 18px;">{icon}</span>
                    </div>
                    <div style="color: #666; font-size: 12px;">
                        Request: {req['request']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="os-footer">
    <div style="margin-bottom: 10px; font-size: 16px; font-weight: 500;">
        Operating System Deadlock Management System
    </div>
    <div style="color: var(--os-blue); margin-bottom: 5px;">
        Developed by Alina Liaquat
    </div>
    <div style="color: #666; font-size: 13px;">
        Banker's Algorithm Implementation | Computer Science Project
    </div>
</div>
""", unsafe_allow_html=True)

# Initialization Message
if not st.session_state.system_initialized:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 60px 40px; background: white; 
                    border-radius: 12px; margin-top: 40px; border: 2px dashed var(--os-border);">
            <div style="font-size: 64px; color: var(--os-blue); margin-bottom: 20px;">
                ⚙️
            </div>
            <h3 style="color: var(--os-dark-blue); margin-bottom: 15px;">
                System Not Initialized
            </h3>
            <p style="color: #666; margin-bottom: 30px;">
                Configure the system parameters and click "Initialize System" to begin
            </p>
            <div style="color: #999; font-size: 14px;">
                Set number of processes and resources, then initialize
            </div>
        </div>
        """, unsafe_allow_html=True)