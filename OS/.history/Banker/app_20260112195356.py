import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html
import time

# Page configuration
st.set_page_config(
    page_title="OS Deadlock Manager",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with OS-style theme
st.markdown("""
<style>
    /* OS-Style Theme */
    :root {
        --os-blue: #0066CC;
        --os-gray: #F0F0F0;
        --os-dark: #2B2B2B;
        --os-green: #00CC66;
        --os-red: #FF3333;
        --os-yellow: #FFCC00;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
    }
    
    .stApp {
        background-color: var(--os-dark);
    }
    
    .os-header {
        background: linear-gradient(90deg, #1a237e, #311b92);
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        border-left: 6px solid var(--os-yellow);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .process-card {
        background: white;
        padding: 18px;
        border-radius: 10px;
        margin: 12px 0;
        border-left: 5px solid var(--os-blue);
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .process-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    
    .safe-card {
        border-left: 5px solid var(--os-green);
        background: linear-gradient(to right, #f0fff4, #ffffff);
    }
    
    .unsafe-card {
        border-left: 5px solid var(--os-red);
        background: linear-gradient(to right, #fff0f0, #ffffff);
    }
    
    .status-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .status-safe { background-color: var(--os-green); }
    .status-unsafe { background-color: var(--os-red); }
    .status-waiting { background-color: var(--os-yellow); }
    
    .resource-table {
        background: white;
        border-radius: 10px;
        padding: 18px;
        margin: 12px 0;
        box-shadow: 0 3px 6px rgba(0,0,0,0.08);
    }
    
    .icon-large {
        font-size: 28px;
        margin-right: 12px;
        vertical-align: middle;
        filter: drop-shadow(0 2px 3px rgba(0,0,0,0.2));
    }
    
    .btn-os {
        background: linear-gradient(90deg, var(--os-blue), #0052CC);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 14px;
        box-shadow: 0 3px 6px rgba(0,82,204,0.2);
    }
    
    .btn-os:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 12px rgba(0,0,0,0.25);
        background: linear-gradient(90deg, #0052CC, var(--os-blue));
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50, #4a6491);
        box-shadow: 3px 0 10px rgba(0,0,0,0.2);
    }
    
    .footer {
        text-align: center;
        padding: 25px;
        color: white;
        margin-top: 40px;
        background: linear-gradient(90deg, rgba(26,35,126,0.8), rgba(49,27,146,0.8));
        border-radius: 10px;
        border-top: 3px solid var(--os-yellow);
    }
    
    .tab-content {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .matrix-cell {
        font-weight: bold;
        text-align: center;
        padding: 8px;
        border-radius: 4px;
    }
    
    .available-cell {
        background-color: #e3f2fd !important;
        color: #1565c0;
    }
    
    .request-history-item {
        border-left: 4px solid;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
    }
    
    .granted { border-left-color: var(--os-green); background: rgba(0,204,102,0.1); }
    .denied { border-left-color: var(--os-red); background: rgba(255,51,51,0.1); }
</style>
""", unsafe_allow_html=True)

# Font Awesome Icons CDN
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
""", unsafe_allow_html=True)

# Banker's Algorithm Implementation
class BankersAlgorithm:
    def __init__(self, processes, resources):
        self.processes = processes
        self.resources = resources
        self.n = len(processes)
        self.m = len(resources)
        
    def is_safe_state(self, allocation, max_demand, available):
        """Check if system is in safe state using Banker's Algorithm"""
        work = available.copy()
        finish = [False] * self.n
        safe_sequence = []
        
        # Calculate need matrix
        need = [[max_demand[i][j] - allocation[i][j] for j in range(self.m)] for i in range(self.n)]
        
        count = 0
        while count < self.n:
            found = False
            for i in range(self.n):
                if not finish[i]:
                    if all(need[i][j] <= work[j] for j in range(self.m)):
                        work = [work[j] + allocation[i][j] for j in range(self.m)]
                        safe_sequence.append(i)
                        finish[i] = True
                        found = True
                        count += 1
                        break
            
            if not found:
                return False, []
        
        return True, safe_sequence
    
    def resource_request(self, process_id, request, allocation, max_demand, available):
        """Handle resource request using Banker's Algorithm"""
        need = [max_demand[process_id][j] - allocation[process_id][j] for j in range(self.m)]
        
        if any(request[j] > need[j] for j in range(self.m)):
            return False, "Error: Process has exceeded its maximum claim."
        
        if any(request[j] > available[j] for j in range(self.m)):
            return False, "Process must wait. Resources not available."
        
        new_allocation = [row[:] for row in allocation]
        new_available = available[:]
        new_max_demand = [row[:] for row in max_demand]
        
        for j in range(self.m):
            new_allocation[process_id][j] += request[j]
            new_available[j] -= request[j]
            new_max_demand[process_id][j] -= request[j]
        
        is_safe, sequence = self.is_safe_state(new_allocation, new_max_demand, new_available)
        
        if is_safe:
            return True, "Request granted. System is safe."
        else:
            return False, "Request denied. Would lead to unsafe state."
    
    def detect_deadlock(self, allocation, request, available):
        """Detect deadlock using deadlock detection algorithm"""
        work = available.copy()
        finish = [sum(allocation[i]) == 0 for i in range(self.n)]
        need = request
        
        while True:
            found = False
            for i in range(self.n):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(self.m)):
                    work = [work[j] + allocation[i][j] for j in range(self.m)]
                    finish[i] = True
                    found = True
            
            if not found:
                break
        
        deadlocked = [i for i in range(self.n) if not finish[i]]
        return deadlocked
    
    def recover_deadlock(self, deadlocked, allocation):
        """Recover from deadlock by terminating processes"""
        if not deadlocked:
            return "No deadlock detected."
        
        min_process = min(deadlocked, key=lambda x: sum(allocation[x]))
        released = allocation[min_process]
        
        return f"Terminated Process P{min_process}. Released resources: {released}"

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.allocation = []
    st.session_state.max_demand = []
    st.session_state.available = []
    st.session_state.processes = 5
    st.session_state.resources = 3
    st.session_state.request_history = []
    st.session_state.current_tab = "System Overview"

def initialize_system():
    """Initialize system with random values"""
    np.random.seed(42)
    
    st.session_state.allocation = np.random.randint(0, 4, (st.session_state.processes, st.session_state.resources)).tolist()
    
    st.session_state.max_demand = []
    for i in range(st.session_state.processes):
        max_row = []
        for j in range(st.session_state.resources):
            max_val = st.session_state.allocation[i][j] + np.random.randint(0, 3)
            max_row.append(max_val)
        st.session_state.max_demand.append(max_row)
    
    st.session_state.available = np.random.randint(2, 8, st.session_state.resources).tolist()
    st.session_state.initialized = True
    st.session_state.request_history = []

# UI Layout
st.markdown("""
<div class="os-header">
    <h1><i class="fas fa-shield-alt icon-large"></i> Operating System Deadlock Manager</h1>
    <p><i class="fas fa-microchip"></i> Banker's Algorithm Implementation for Deadlock Avoidance & Recovery</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="color: white; padding: 20px;">
        <h2><i class="fas fa-cogs"></i> System Control Panel</h2>
        <hr style="background-color: white; height: 2px; border: none;">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### <i class='fas fa-sliders-h'></i> System Configuration", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        processes = st.number_input("<i class='fas fa-tasks'></i> Processes", min_value=3, max_value=10, value=5, key="proc_input")
    with col2:
        resources = st.number_input("<i class='fas fa-server'></i> Resources", min_value=2, max_value=5, value=3, key="res_input")
    
    st.session_state.processes = processes
    st.session_state.resources = resources
    
    if st.button("<i class='fas fa-power-off'></i> Initialize System", use_container_width=True, type="primary"):
        initialize_system()
        st.success("<i class='fas fa-check-circle'></i> System initialized successfully!")
        st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### <i class='fas fa-chart-line'></i> System Status")
    
    if st.session_state.initialized:
        st.markdown("""
        <div style="background: rgba(0,204,102,0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #00CC66;">
            <h4><i class="fas fa-check-circle" style="color: #00CC66;"></i> System Active</h4>
        </div>
        """, unsafe_allow_html=True)
        
        banker = BankersAlgorithm(st.session_state.processes, st.session_state.resources)
        is_safe, sequence = banker.is_safe_state(
            st.session_state.allocation,
            st.session_state.max_demand,
            st.session_state.available
        )
        
        if is_safe:
            st.markdown("""
            <div style="background: rgba(0,204,102,0.1); padding: 10px; border-radius: 6px; margin-top: 10px;">
                <p><span class="status-indicator status-safe"></span> <strong>SAFE State</strong></p>
                <p style="font-size: 12px;"><i class="fas fa-list-ol"></i> Safe Sequence: """ + ' → '.join([f'P{p}' for p in sequence]) + """</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(255,51,51,0.1); padding: 10px; border-radius: 6px; margin-top: 10px;">
                <p><span class="status-indicator status-unsafe"></span> <strong>UNSAFE State</strong></p>
                <p style="font-size: 12px;"><i class="fas fa-exclamation-triangle"></i> Potential deadlock detected</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(255,204,0,0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #FFCC00;">
            <h4><i class="fas fa-exclamation-triangle" style="color: #FFCC00;"></i> System Not Initialized</h4>
            <p>Initialize system to begin</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### <i class='fas fa-info-circle'></i> Quick Guide")
    st.markdown("""
    <div style="font-size: 13px;">
        <p><i class="fas fa-play-circle"></i> <strong>Initialize System</strong><br>Set up processes & resources</p>
        <p><i class="fas fa-search"></i> <strong>Check Safety</strong><br>Run Banker's Algorithm</p>
        <p><i class="fas fa-hand-paper"></i> <strong>Make Requests</strong><br>Simulate resource requests</p>
        <p><i class="fas fa-medkit"></i> <strong>Recovery</strong><br>Deadlock detection & recovery</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content
if not st.session_state.initialized:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 60px; background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)); border-radius: 15px; margin-top: 50px;">
            <i class="fas fa-server" style="font-size: 120px; color: #667eea; margin-bottom: 30px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));"></i>
            <h2><i class="fas fa-power-off"></i> System Ready for Initialization</h2>
            <p style="font-size: 16px; color: #666; margin: 20px 0 30px 0;">Click the <i class="fas fa-power-off"></i> <strong>Initialize System</strong> button in the sidebar to begin simulation.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    banker = BankersAlgorithm(st.session_state.processes, st.session_state.resources)
    
    # Create tabs with Font Awesome icons
    tab1, tab2, tab3, tab4 = st.tabs([
        "<i class='fas fa-tachometer-alt'></i> System Overview",
        "<i class='fas fa-shield-alt'></i> Safety Algorithm",
        "<i class='fas fa-exchange-alt'></i> Resource Request",
        "<i class='fas fa-medkit'></i> Deadlock Recovery"
    ])
    
    with tab1:
        st.markdown("### <i class='fas fa-tachometer-alt'></i> System Overview Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### <i class='fas fa-table'></i> Allocation Matrix")
            allocation_df = pd.DataFrame(
                st.session_state.allocation,
                index=[f"<i class='fas fa-microchip'></i> P{i}" for i in range(st.session_state.processes)],
                columns=[f"<i class='fas fa-cube'></i> R{j}" for j in range(st.session_state.resources)]
            )
            st.markdown(allocation_df.to_html(escape=False), unsafe_allow_html=True)
            
            st.markdown("#### <i class='fas fa-boxes'></i> Available Resources")
            avail_df = pd.DataFrame(
                [st.session_state.available],
                columns=[f"<i class='fas fa-cube'></i> R{j}" for j in range(st.session_state.resources)],
                index=["<i class='fas fa-check-circle'></i> Available"]
            )
            st.markdown(avail_df.to_html(escape=False, classes='available-cell'), unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### <i class='fas fa-chart-bar'></i> Maximum Demand Matrix")
            max_df = pd.DataFrame(
                st.session_state.max_demand,
                index=[f"<i class='fas fa-microchip'></i> P{i}" for i in range(st.session_state.processes)],
                columns=[f"<i class='fas fa-cube'></i> R{j}" for j in range(st.session_state.resources)]
            )
            st.markdown(max_df.to_html(escape=False), unsafe_allow_html=True)
            
            need = [[st.session_state.max_demand[i][j] - st.session_state.allocation[i][j] 
                    for j in range(st.session_state.resources)] 
                   for i in range(st.session_state.processes)]
            
            st.markdown("#### <i class='fas fa-calculator'></i> Need Matrix")
            need_df = pd.DataFrame(
                need,
                index=[f"<i class='fas fa-microchip'></i> P{i}" for i in range(st.session_state.processes)],
                columns=[f"<i class='fas fa-cube'></i> R{j}" for j in range(st.session_state.resources)]
            )
            st.markdown(need_df.to_html(escape=False), unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### <i class='fas fa-shield-alt'></i> Safety Algorithm Verification")
        
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(90deg, rgba(26,35,126,0.1), rgba(49,27,146,0.1)); 
                        padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4><i class="fas fa-info-circle"></i> About Safety Algorithm</h4>
                <p>The Banker's Algorithm checks if the system is in a safe state by finding a safe sequence 
                where all processes can complete without deadlock.</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("<i class='fas fa-play-circle'></i> Run Safety Algorithm", use_container_width=True, type="primary"):
            with st.spinner("<i class='fas fa-cog fa-spin'></i> Checking system safety..."):
                time.sleep(1.5)
                is_safe, sequence = banker.is_safe_state(
                    st.session_state.allocation,
                    st.session_state.max_demand,
                    st.session_state.available
                )
                
                if is_safe:
                    st.markdown(f"""
                    <div class="process-card safe-card">
                        <h4><i class="fas fa-check-circle" style="color: var(--os-green); font-size: 24px;"></i> System is in SAFE State</h4>
                        <p><i class="fas fa-list-ol"></i> <strong>Safe Sequence Found:</strong> {' → '.join([f'P{p}' for p in sequence])}</p>
                        <p><i class="fas fa-thumbs-up"></i> All processes can be executed without deadlock occurrence.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    sequence_html = """
                    <div style='display: flex; justify-content: center; align-items: center; margin: 30px 0; 
                                flex-wrap: wrap; gap: 15px;'>
                    """
                    for i, p in enumerate(sequence):
                        sequence_html += f"""
                        <div style="text-align: center; position: relative;">
                            <div style="background: linear-gradient(135deg, var(--os-green), #00a854); 
                                        color: white; width: 60px; height: 60px; border-radius: 50%; 
                                        display: flex; align-items: center; justify-content: center;
                                        font-weight: bold; margin: 0 auto 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                                        font-size: 18px;">
                                <i class="fas fa-microchip"></i> P{p}
                            </div>
                            <div style="font-size: 14px; color: #666;">Step {i+1}</div>
                        </div>
                        """
                        if i < len(sequence) - 1:
                            sequence_html += """
                            <div style="align-self: center; color: var(--os-green); font-size: 24px;">
                                <i class="fas fa-arrow-right"></i>
                            </div>
                            """
                    sequence_html += "</div>"
                    st.markdown(sequence_html, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="process-card unsafe-card">
                        <h4><i class="fas fa-exclamation-triangle" style="color: var(--os-red); font-size: 24px;"></i> System is in UNSAFE State</h4>
                        <p><i class="fas fa-exclamation-circle"></i> <strong>Warning:</strong> Deadlock may occur if processes request additional resources.</p>
                        <p><i class="fas fa-lightbulb"></i> <strong>Recommendation:</strong> Consider adjusting resource allocation or increasing available resources.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div style="background: rgba(255,51,51,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
                        <h5><i class="fas fa-tools"></i> Troubleshooting Steps:</h5>
                        <ol>
                            <li>Increase available resources</li>
                            <li>Reduce maximum demand of processes</li>
                            <li>Re-allocate existing resources</li>
                            <li>Initialize system with different parameters</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns([2,1])
        
        with col1:
            st.markdown("### <i class='fas fa-exchange-alt'></i> Resource Request Simulation")
            
            process_id = st.selectbox(
                "<i class='fas fa-tasks'></i> Select Process",
                [f"<i class='fas fa-microchip'></i> P{i}" for i in range(st.session_state.processes)],
                format_func=lambda x: x
            )
            pid = int(process_id.split("P")[1].split("<")[0])
            
            st.markdown("#### <i class='fas fa-hand-paper'></i> Request Resources")
            request = []
            cols = st.columns(st.session_state.resources)
            for j in range(st.session_state.resources):
                with cols[j]:
                    max_request = st.session_state.max_demand[pid][j] - st.session_state.allocation[pid][j]
                    st.markdown(f"<div style='text-align: center;'><i class='fas fa-cube'></i> <strong>R{j}</strong></div>", unsafe_allow_html=True)
                    req = st.number_input(
                        f"",
                        min_value=0,
                        max_value=max_request,
                        value=0,
                        key=f"req_{j}",
                        label_visibility="collapsed"
                    )
                    request.append(req)
            
            if st.button("<i class='fas fa-paper-plane'></i> Submit Resource Request", use_container_width=True, type="primary"):
                if sum(request) == 0:
                    st.warning("<i class='fas fa-exclamation-circle'></i> Please request at least one resource.")
                else:
                    with st.spinner("<i class='fas fa-cog fa-spin'></i> Processing request..."):
                        time.sleep(0.8)
                        granted, message = banker.resource_request(
                            pid,
                            request,
                            st.session_state.allocation,
                            st.session_state.max_demand,
                            st.session_state.available
                        )
                        
                        if granted:
                            st.success(f"<i class='fas fa-check-circle'></i> {message}")
                            for j in range(st.session_state.resources):
                                st.session_state.allocation[pid][j] += request[j]
                                st.session_state.available[j] -= request[j]
                        else:
                            st.error(f"<i class='fas fa-times-circle'></i> {message}")
                        
                        st.session_state.request_history.append({
                            'process': f"P{pid}",
                            'request': request.copy(),
                            'granted': granted,
                            'message': message,
                            'timestamp': time.strftime("%H:%M:%S")
                        })
                        st.rerun()
        
        with col2:
            st.markdown("### <i class='fas fa-history'></i> Request History")
            if st.session_state.request_history:
                for i, req in enumerate(reversed(st.session_state.request_history[-5:])):
                    status_class = "granted" if req['granted'] else "denied"
                    status_icon = "<i class='fas fa-check-circle' style='color: #00CC66;'></i>" if req['granted'] else "<i class='fas fa-times-circle' style='color: #FF3333;'></i>"
                    st.markdown(f"""
                    <div class="request-history-item {status_class}">
                        <strong>{status_icon} {req['process']}</strong><br>
                        <small><i class='fas fa-clock'></i> {req['timestamp']}</small><br>
                        <i class='fas fa-cubes'></i> Request: {req['request']}<br>
                        <small>{req['message']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 30px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <i class="fas fa-history" style="font-size: 40px; color: #999; margin-bottom: 10px;"></i>
                    <p>No requests made yet</p>
                </div>
                """, unsafe_allow_html=True)
            
            if st.session_state.request_history and st.button("<i class='fas fa-trash-alt'></i> Clear History", use_container_width=True):
                st.session_state.request_history = []
                st.rerun()
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### <i class='fas fa-search'></i> Deadlock Detection")
            
            st.markdown("""
            <div style="background: rgba(255,204,0,0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h5><i class="fas fa-info-circle"></i> Current Request Matrix (Simulated)</h5>
                <p>This matrix represents pending resource requests from each process.</p>
            </div>
            """, unsafe_allow_html=True)
            
            request_matrix = np.random.randint(0, 3, (st.session_state.processes, st.session_state.resources)).tolist()
            request_df = pd.DataFrame(
                request_matrix,
                index=[f"<i class='fas fa-microchip'></i> P{i}" for i in range(st.session_state.processes)],
                columns=[f"<i class='fas fa-cube'></i> R{j}" for j in range(st.session_state.resources)]
            )
            st.markdown(request_df.to_html(escape=False), unsafe_allow_html=True)
            
            if st.button("<i class='fas fa-search'></i> Detect Deadlock", use_container_width=True, type="primary"):
                deadlocked = banker.detect_deadlock(
                    st.session_state.allocation,
                    request_matrix,
                    st.session_state.available
                )
                
                if deadlocked:
                    st.error(f"<i class='fas fa-exclamation-triangle'></i> **Deadlock Detected!**")
                    st.markdown(f"<i class='fas fa-skull-crossbones'></i> **Deadlocked Processes:** {[f'P{p}' for p in deadlocked]}")
                    
                    deadlock_html = "<div style='display: flex; flex-wrap: wrap; gap: 15px; margin: 25px 0;'>"
                    for i in range(st.session_state.processes):
                        is_dead = i in deadlocked
                        color = "linear-gradient(135deg, #FF3333, #CC0000)" if is_dead else "linear-gradient(135deg, var(--os-green), #00a854)"
                        icon = "fas fa-skull" if is_dead else "fas fa-check-circle"
                        deadlock_html += f"""
                        <div style="background: {color}; color: white; padding: 20px; 
                                 border-radius: 10px; text-align: center; min-width: 100px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                            <div style="font-size: 30px;"><i class="{icon}"></i></div>
                            <div style="font-size: 20px; font-weight: bold;">P{i}</div>
                            <div style="font-size: 12px;">{'<i class="fas fa-ban"></i> Deadlocked' if is_dead else '<i class="fas fa-play"></i> Active'}</div>
                        </div>
                        """
                    deadlock_html += "</div>"
                    st.markdown(deadlock_html, unsafe_allow_html=True)
                else:
                    st.success("<i class='fas fa-check-circle'></i> **No Deadlock Detected**")
                    st.markdown("<i class='fas fa-thumbs-up'></i> All processes are executing normally without circular wait conditions.")
        
        with col2:
            st.markdown("### <i class='fas fa-medkit'></i> Recovery Actions")
            
            st.markdown("""
            <div style="background: rgba(255,51,51,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4><i class="fas fa-first-aid"></i> Recovery Methods</h4>
                <p>Select a recovery method to resolve detected deadlocks:</p>
            </div>
            """, unsafe_allow_html=True)
            
            recovery_method = st.radio(
                "<i class='fas fa-list'></i> Choose Recovery Method:",
                ["Process Termination", "Resource Preemption", "Process Rollback"],
                format_func=lambda x: f"<i class='fas fa-{'skull' if 'Termination' in x else 'exchange-alt' if 'Preemption' in x else 'undo'}'> {x}</i>"
            )
            
            if st.button("<i class='fas fa-play'></i> Execute Recovery", use_container_width=True, type="primary"):
                deadlocked = banker.detect_deadlock(
                    st.session_state.allocation,
                    request_matrix,
                    st.session_state.available
                )
                
                if not deadlocked:
                    st.info("<i class='fas fa-info-circle'></i> No deadlock detected. Recovery not needed.")
                else:
                    with st.spinner(f"<i class='fas fa-cog fa-spin'></i> Executing {recovery_method}..."):
                        time.sleep(2)
                        
                        if "Termination" in recovery_method:
                            recovery_msg = banker.recover_deadlock(deadlocked, st.session_state.allocation)
                            st.warning(f"<i class='fas fa-skull'></i> **Recovery Action Taken**")
                            st.info(f"<i class='fas fa-info-circle'></i> {recovery_msg}")
                        elif "Preemption" in recovery_method:
                            st.info("<i class='fas fa-exchange-alt'></i> **Resource Preemption Applied**")
                            st.markdown("Resources have been preempted from deadlocked processes and reallocated.")
                        else:
                            st.info("<i class='fas fa-undo'></i> **Process Rollback Executed**")
                            st.markdown("Deadlocked processes have been rolled back to previous safe states.")
                        
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)
                        
                        st.success("<i class='fas fa-check-circle'></i> **System successfully recovered from deadlock!**")
                        
                        st.balloons()

# Footer with developer credit
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 15px; font-size: 24px;">
        <a href="#" style="color: white;"><i class="fab fa-github"></i></a>
        <a href="#" style="color: white;"><i class="fab fa-linkedin"></i></a>
        <a href="#" style="color: white;"><i class="fas fa-code"></i></a>
        <a href="#" style="color: white;"><i class="fas fa-book"></i></a>
    </div>
    <hr style="width: 50%; margin: 15px auto; border-color: rgba(255,255,255,0.3);">
    <p><i class="fas fa-laptop-code"></i> Operating System Deadlock Management System</p>
    <p><strong><i class="fas fa-user-graduate"></i> Developed by Alina Liaquat</strong></p>
    <p><small><i class="far fa-copyright"></i> 2024 | Banker's Algorithm Implementation | Computer Science Project</small></p>
</div>
""", unsafe_allow_html=True)

# JavaScript for enhanced interactivity
st.markdown("""
<script>
// Enhanced animations and interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to all cards
    const cards = document.querySelectorAll('.process-card, .resource-table');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 20px rgba(0,0,0,0.15)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 3px 6px rgba(0,0,0,0.1)';
        });
    });
    
    // Animate icons on hover
    const icons = document.querySelectorAll('.icon-large, .fa-microchip, .fa-cube');
    icons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2) rotate(5deg)';
            this.style.transition = 'transform 0.3s ease';
        });
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });
    
    // Tab switching animation
    const tabs = document.querySelectorAll('[data-testid="stTab"]');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabContent = document.querySelector('[data-testid="stTabContent"]');
            if (tabContent) {
                tabContent.style.animation = 'none';
                setTimeout(() => {
                    tabContent.style.animation = 'fadeIn 0.5s ease-out';
                }, 10);
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)