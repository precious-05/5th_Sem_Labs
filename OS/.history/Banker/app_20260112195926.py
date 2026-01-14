import streamlit as st
import pandas as pd
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="OS Deadlock Manager",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, Professional CSS Theme
st.markdown("""
<style>
    /* Modern Clean Theme */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #7c3aed;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --light: #f8fafc;
        --dark: #1e293b;
        --gray: #64748b;
        --border: #e2e8f0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.15);
        color: white;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 0;
    }
    
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .card-title {
        color: var(--dark);
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .status-card {
        border-left: 4px solid var(--success);
    }
    
    .status-card.danger {
        border-left-color: var(--danger);
    }
    
    .status-card.warning {
        border-left-color: var(--warning);
    }
    
    .matrix-card {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .matrix-header {
        background: var(--light);
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border);
        font-weight: 600;
        color: var(--dark);
    }
    
    .matrix-content {
        padding: 1rem;
        overflow-x: auto;
    }
    
    .btn-primary {
        background: linear-gradient(90deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .btn-primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .btn-secondary {
        background: var(--light);
        color: var(--dark);
        border: 1px solid var(--border);
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        width: 100%;
    }
    
    .btn-secondary:hover {
        background: #f1f5f9;
        border-color: var(--primary);
    }
    
    .tab-container {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-top: 1.5rem;
    }
    
    .process-step {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .step-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--light);
        border: 2px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: var(--dark);
        position: relative;
        z-index: 2;
    }
    
    .step-circle.active {
        background: var(--primary);
        border-color: var(--primary);
        color: white;
    }
    
    .step-circle.completed {
        background: var(--success);
        border-color: var(--success);
        color: white;
    }
    
    .step-line {
        flex: 1;
        height: 2px;
        background: var(--border);
        margin: 0 -15px;
        position: relative;
        z-index: 1;
    }
    
    .step-line.active {
        background: var(--primary);
    }
    
    .resource-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        background: var(--light);
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 2px;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--gray);
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border);
    }
    
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background: var(--light);
        padding: 0.75rem;
        text-align: center;
        font-weight: 600;
        color: var(--dark);
        border-bottom: 2px solid var(--border);
    }
    
    .dataframe td {
        padding: 0.75rem;
        text-align: center;
        border-bottom: 1px solid var(--border);
    }
    
    .dataframe tr:hover {
        background: #f8fafc;
    }
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
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
        
        for _ in range(self.n):
            found = False
            for i in range(self.n):
                if not finish[i]:
                    if all(need[i][j] <= work[j] for j in range(self.m)):
                        work = [work[j] + allocation[i][j] for j in range(self.m)]
                        safe_sequence.append(i)
                        finish[i] = True
                        found = True
                        break
            if not found:
                return False, []
        
        return True, safe_sequence
    
    def resource_request(self, process_id, request, allocation, max_demand, available):
        """Handle resource request using Banker's Algorithm"""
        need = [max_demand[process_id][j] - allocation[process_id][j] for j in range(self.m)]
        
        if any(request[j] > need[j] for j in range(self.m)):
            return False, "Process exceeded maximum claim"
        
        if any(request[j] > available[j] for j in range(self.m)):
            return False, "Resources not available"
        
        # Temporarily allocate
        new_allocation = [row[:] for row in allocation]
        new_available = available[:]
        
        for j in range(self.m):
            new_allocation[process_id][j] += request[j]
            new_available[j] -= request[j]
        
        # Check safety
        is_safe, sequence = self.is_safe_state(new_allocation, max_demand, new_available)
        
        if is_safe:
            return True, "Request granted"
        return False, "Request would lead to unsafe state"
    
    def detect_deadlock(self, allocation, request, available):
        """Detect deadlock in the system"""
        work = available.copy()
        finish = [sum(allocation[i]) == 0 for i in range(self.n)]
        
        while True:
            found = False
            for i in range(self.n):
                if not finish[i] and all(request[i][j] <= work[j] for j in range(self.m)):
                    work = [work[j] + allocation[i][j] for j in range(self.m)]
                    finish[i] = True
                    found = True
            
            if not found:
                break
        
        return [i for i in range(self.n) if not finish[i]]

# Initialize session state
if 'system_data' not in st.session_state:
    st.session_state.system_data = {
        'initialized': False,
        'processes': 5,
        'resources': 3,
        'allocation': [],
        'max_demand': [],
        'available': [],
        'request_history': [],
        'current_process': 0
    }

def initialize_system():
    """Initialize system with default values"""
    np.random.seed(42)
    p = st.session_state.system_data['processes']
    r = st.session_state.system_data['resources']
    
    # Generate reasonable allocation
    allocation = np.random.randint(0, 3, (p, r)).tolist()
    
    # Generate max demand (always >= allocation)
    max_demand = []
    for i in range(p):
        max_row = []
        for j in range(r):
            max_val = allocation[i][j] + np.random.randint(1, 4)
            max_row.append(max_val)
        max_demand.append(max_row)
    
    # Generate available resources
    total_allocated = np.sum(allocation, axis=0)
    available = [total_allocated[j] + np.random.randint(2, 5) for j in range(r)]
    
    st.session_state.system_data.update({
        'allocation': allocation,
        'max_demand': max_demand,
        'available': available,
        'initialized': True,
        'request_history': []
    })

def update_parameters():
    """Update system parameters"""
    st.session_state.system_data['processes'] = st.session_state.process_count
    st.session_state.system_data['resources'] = st.session_state.resource_count

# Header
st.markdown("""
<div class="main-header">
    <h1><i class="fas fa-shield-alt"></i> Deadlock Manager</h1>
    <p>Banker's Algorithm for Deadlock Avoidance and Recovery</p>
</div>
""", unsafe_allow_html=True)

# Main Layout - No Sidebar
col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    # System Configuration Card
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <i class="fas fa-cog"></i> System Configuration
            </div>
        """, unsafe_allow_html=True)
        
        process_count = st.number_input(
            "Number of Processes",
            min_value=3,
            max_value=8,
            value=st.session_state.system_data['processes'],
            key="process_count",
            on_change=update_parameters
        )
        
        resource_count = st.number_input(
            "Number of Resources",
            min_value=2,
            max_value=5,
            value=st.session_state.system_data['resources'],
            key="resource_count",
            on_change=update_parameters
        )
        
        if st.button("Initialize System", use_container_width=True):
            initialize_system()
            st.success("System initialized successfully!")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # System Status Card
        if st.session_state.system_data['initialized']:
            with st.container():
                banker = BankersAlgorithm(
                    st.session_state.system_data['processes'],
                    st.session_state.system_data['resources']
                )
                
                is_safe, sequence = banker.is_safe_state(
                    st.session_state.system_data['allocation'],
                    st.session_state.system_data['max_demand'],
                    st.session_state.system_data['available']
                )
                
                status_class = "status-card" + (" danger" if not is_safe else "")
                status_icon = "fa-exclamation-triangle" if not is_safe else "fa-check-circle"
                status_color = "var(--danger)" if not is_safe else "var(--success)"
                
                st.markdown(f"""
                <div class="card {status_class}">
                    <div class="card-title">
                        <i class="fas {status_icon}" style="color: {status_color}"></i>
                        System Status
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: {status_color}; text-align: center; margin: 1rem 0;">
                        {'SAFE' if is_safe else 'UNSAFE'}
                    </div>
                    <div style="text-align: center; color: var(--gray);">
                        {f'Safe sequence: {" → ".join([f"P{p}" for p in sequence])}' if is_safe else 'Potential deadlock detected'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

with col2:
    if st.session_state.system_data['initialized']:
        # Matrix Display
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <i class="fas fa-table"></i> System Matrices
            </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different matrices
        mat_tab1, mat_tab2, mat_tab3, mat_tab4 = st.tabs(["Allocation", "Max Demand", "Available", "Need"])
        
        with mat_tab1:
            alloc_df = pd.DataFrame(
                st.session_state.system_data['allocation'],
                index=[f"P{i}" for i in range(st.session_state.system_data['processes'])],
                columns=[f"R{j}" for j in range(st.session_state.system_data['resources'])]
            )
            st.dataframe(alloc_df, use_container_width=True)
        
        with mat_tab2:
            max_df = pd.DataFrame(
                st.session_state.system_data['max_demand'],
                index=[f"P{i}" for i in range(st.session_state.system_data['processes'])],
                columns=[f"R{j}" for j in range(st.session_state.system_data['resources'])]
            )
            st.dataframe(max_df, use_container_width=True)
        
        with mat_tab3:
            avail_df = pd.DataFrame(
                [st.session_state.system_data['available']],
                columns=[f"R{j}" for j in range(st.session_state.system_data['resources'])],
                index=["Available"]
            )
            st.dataframe(avail_df, use_container_width=True)
        
        with mat_tab4:
            need = [[st.session_state.system_data['max_demand'][i][j] - 
                    st.session_state.system_data['allocation'][i][j] 
                    for j in range(st.session_state.system_data['resources'])] 
                   for i in range(st.session_state.system_data['processes'])]
            need_df = pd.DataFrame(
                need,
                index=[f"P{i}" for i in range(st.session_state.system_data['processes'])],
                columns=[f"R{j}" for j in range(st.session_state.system_data['resources'])]
            )
            st.dataframe(need_df, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Resource Request Section
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <i class="fas fa-hand-paper"></i> Resource Request
            </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            process_id = st.selectbox(
                "Select Process",
                [f"P{i}" for i in range(st.session_state.system_data['processes'])],
                key="req_process"
            )
        
        pid = int(process_id[1:])
        
        st.markdown("**Request Amount:**")
        request_cols = st.columns(st.session_state.system_data['resources'])
        request = []
        for j in range(st.session_state.system_data['resources']):
            with request_cols[j]:
                st.markdown(f"**R{j}**")
                max_req = st.session_state.system_data['max_demand'][pid][j] - st.session_state.system_data['allocation'][pid][j]
                req_val = st.number_input(
                    f"R{j}_req",
                    min_value=0,
                    max_value=max_req,
                    value=0,
                    label_visibility="collapsed"
                )
                request.append(req_val)
        
        if st.button("Submit Request", use_container_width=True):
            banker = BankersAlgorithm(
                st.session_state.system_data['processes'],
                st.session_state.system_data['resources']
            )
            
            granted, message = banker.resource_request(
                pid,
                request,
                st.session_state.system_data['allocation'],
                st.session_state.system_data['max_demand'],
                st.session_state.system_data['available']
            )
            
            if granted:
                # Update allocation
                for j in range(st.session_state.system_data['resources']):
                    st.session_state.system_data['allocation'][pid][j] += request[j]
                    st.session_state.system_data['available'][j] -= request[j]
                st.success(f"Request granted")
            else:
                st.error(f"Request denied: {message}")
            
            st.session_state.system_data['request_history'].append({
                'process': process_id,
                'request': request.copy(),
                'granted': granted,
                'time': time.strftime("%H:%M:%S")
            })
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

with col3:
    if st.session_state.system_data['initialized']:
        # Available Resources Card
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <i class="fas fa-boxes"></i> Available Resources
            </div>
        """, unsafe_allow_html=True)
        
        for j in range(st.session_state.system_data['resources']):
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.markdown(f"**R{j}**")
            with col_b:
                st.progress(
                    st.session_state.system_data['available'][j] / 
                    (st.session_state.system_data['available'][j] + 
                     sum(st.session_state.system_data['allocation'][i][j] 
                         for i in range(st.session_state.system_data['processes'])))
                )
                st.caption(f"{st.session_state.system_data['available'][j]} units")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Deadlock Detection Card
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <i class="fas fa-search"></i> Deadlock Detection
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Run Detection", use_container_width=True):
            banker = BankersAlgorithm(
                st.session_state.system_data['processes'],
                st.session_state.system_data['resources']
            )
            
            # Create random request matrix for detection
            request_matrix = np.random.randint(0, 2, 
                (st.session_state.system_data['processes'], 
                 st.session_state.system_data['resources'])).tolist()
            
            deadlocked = banker.detect_deadlock(
                st.session_state.system_data['allocation'],
                request_matrix,
                st.session_state.system_data['available']
            )
            
            if deadlocked:
                st.error(f"Deadlock detected in processes: {[f'P{p}' for p in deadlocked]}")
                
                if st.button("Recover by Termination", use_container_width=True):
                    # Terminate first deadlocked process
                    if deadlocked:
                        terminated = deadlocked[0]
                        # Release resources
                        for j in range(st.session_state.system_data['resources']):
                            st.session_state.system_data['available'][j] += \
                                st.session_state.system_data['allocation'][terminated][j]
                            st.session_state.system_data['allocation'][terminated][j] = 0
                        st.success(f"Process P{terminated} terminated. Resources released.")
                        st.rerun()
            else:
                st.success("No deadlock detected")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Request History Card
        if st.session_state.system_data['request_history']:
            st.markdown("""
            <div class="card">
                <div class="card-title">
                    <i class="fas fa-history"></i> Recent Requests
                </div>
            """, unsafe_allow_html=True)
            
            for i, req in enumerate(reversed(st.session_state.system_data['request_history'][-3:])):
                status_icon = "fa-check-circle text-green-500" if req['granted'] else "fa-times-circle text-red-500"
                status_color = "var(--success)" if req['granted'] else "var(--danger)"
                
                st.markdown(f"""
                <div style="padding: 0.75rem; background: var(--light); border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {status_color}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{req['process']}</strong>
                            <span style="color: var(--gray); font-size: 0.9rem; margin-left: 0.5rem;">
                                <i class="fas fa-clock"></i> {req['time']}
                            </span>
                        </div>
                        <i class="fas {'fa-check-circle' if req['granted'] else 'fa-times-circle'}" 
                           style="color: {status_color}"></i>
                    </div>
                    <div style="font-size: 0.9rem; color: var(--gray); margin-top: 0.25rem;">
                        Request: {req['request']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 1rem;">
        <i class="fas fa-laptop-code" style="font-size: 1.5rem; color: var(--primary);"></i>
    </div>
    <div style="font-weight: 600; color: var(--dark); margin-bottom: 0.5rem;">
        Operating System Deadlock Management System
    </div>
    <div style="color: var(--gray);">
        <i class="fas fa-user-graduate"></i> Developed by Alina Liaquat
    </div>
    <div style="font-size: 0.8rem; color: var(--gray); margin-top: 0.5rem;">
        Banker's Algorithm Implementation | Computer Science Project
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize if not done
if not st.session_state.system_data['initialized']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 12px; margin-top: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <i class="fas fa-server" style="font-size: 4rem; color: var(--primary); margin-bottom: 1.5rem; opacity: 0.7;"></i>
            <h3 style="color: var(--dark); margin-bottom: 1rem;">System Not Initialized</h3>
            <p style="color: var(--gray); margin-bottom: 2rem;">Configure the system parameters and click "Initialize System" to begin.</p>
        </div>
        """, unsafe_allow_html=True)