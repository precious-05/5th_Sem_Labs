"""
Deadlock Avoidance and Recovery Simulator
Beautiful GUI with Centered Layout and Fixed Positioning
"""

import numpy as np
from nicegui import ui

class DeadlockSimulator:
    def __init__(self):
        self.process_names = ["Chrome Browser", "VS Code", "Photoshop", 
                             "Excel", "Spotify", "Zoom", "Discord", "Word"]
        self.resource_names = ["CPU Cores", "RAM Memory", "GPU Memory", 
                              "Disk I/O", "Network Bandwidth", "USB Ports"]
        self.num_processes = 4
        self.num_resources = 3
        self.initialize_system()
    
    def initialize_system(self, num_processes=None, num_resources=None):
        if num_processes:
            self.num_processes = num_processes
        if num_resources:
            self.num_resources = num_resources
            
        self.processes = self.process_names[:self.num_processes]
        self.resources = self.resource_names[:self.num_resources]
        
        # Initialize matrices
        self.allocated = np.random.randint(0, 3, (self.num_processes, self.num_resources))
        self.max_need = self.allocated + np.random.randint(1, 4, (self.num_processes, self.num_resources))
        
        # Calculate available resources
        total_allocated = self.allocated.sum(axis=0)
        self.available = total_allocated + np.random.randint(2, 6, self.num_resources)
        
        self.history = [f"✅ System initialized with {self.num_processes} processes and {self.num_resources} resources"]
        self.safe_sequence = []
    
    def calculate_need(self):
        return self.max_need - self.allocated
    
    def bankers_algorithm(self):
        need = self.calculate_need()
        work = self.available.copy()
        finish = [False] * self.num_processes
        
        safe_sequence = []
        
        for _ in range(self.num_processes):
            for i in range(self.num_processes):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(self.num_resources)):
                    work += self.allocated[i]
                    finish[i] = True
                    safe_sequence.append(self.processes[i])
                    break
        
        is_safe = all(finish)
        self.safe_sequence = safe_sequence
        return is_safe, safe_sequence
    
    def request_resources(self, pid, request):
        if pid < 0 or pid >= self.num_processes:
            return False
        
        need = self.calculate_need()
        
        # Check request validity
        for j in range(self.num_resources):
            if request[j] > need[pid][j]:
                self.history.append(f"❌ {self.processes[pid]}: Request exceeds maximum need for {self.resources[j]}")
                return False
            if request[j] > self.available[j]:
                self.history.append(f"⏳ {self.processes[pid]}: Waiting for {self.resources[j]} (insufficient)")
                return False
        
        # Try allocation
        old_allocated = self.allocated.copy()
        old_available = self.available.copy()
        
        self.allocated[pid] += request
        self.available -= request
        
        is_safe, _ = self.bankers_algorithm()
        
        if is_safe:
            self.history.append(f"✅ {self.processes[pid]}: Resources allocated successfully")
            return True
        else:
            self.allocated = old_allocated
            self.available = old_available
            self.history.append(f"⚠️ {self.processes[pid]}: Request denied - would lead to deadlock")
            return False
    
    def recover(self, pid):
        if 0 <= pid < self.num_processes:
            self.available += self.allocated[pid]
            self.history.append(f"🔄 {self.processes[pid]} terminated. Resources freed: {self.allocated[pid].sum()} units")
            self.allocated[pid] = 0
            self.max_need[pid] = 0
            return True
        return False

# Create simulator
sim = DeadlockSimulator()

# Custom CSS for beautiful UI with centered layout
css = '''
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

#app {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
}

/* Container for centering */
.container-center {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* Header styling */
.header-gradient {
    background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    margin-bottom: 20px !important;
    padding: 20px 30px !important;
}

/* Main content wrapper */
.content-wrapper {
    display: flex;
    gap: 20px;
    width: 100%;
    min-height: calc(100vh - 180px);
}

/* Left panel fixed width */
.left-panel {
    flex: 0 0 380px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* Right panel flexible */
.right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-width: 0; /* Prevents overflow */
}

/* Card styling */
.q-card {
    border-radius: 16px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1) !important;
    border: none !important;
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.95) !important;
    width: 100% !important;
    margin: 0 !important;
}

/* Button styling */
.q-btn {
    border-radius: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    margin: 0 !important;
}

.q-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
}

/* Process and resource cards */
.process-card {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
    min-width: 120px;
    flex-shrink: 0;
}

.process-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.resource-card {
    background: linear-gradient(135deg, #10b981 0%, #047857 100%);
    color: white;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    transition: all 0.3s ease;
    min-width: 120px;
    flex-shrink: 0;
}

.resource-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.deadlocked-card {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

/* Status indicators */
.safe-indicator {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 600;
    text-align: center;
    width: 100%;
}

.unsafe-indicator {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 600;
    text-align: center;
    width: 100%;
}

/* Matrix table styling */
.ag-theme-alpine {
    --ag-header-background-color: #f8fafc;
    --ag-header-foreground-color: #475569;
    --ag-border-color: #e2e8f0;
    --ag-row-border-color: #e2e8f0;
    border-radius: 12px !important;
    overflow: hidden !important;
    width: 100% !important;
}

/* Tab content fixed height */
.tab-content {
    min-height: 250px;
    max-height: 250px;
    overflow: hidden;
}

/* Footer styling */
.footer-gradient {
    background: linear-gradient(90deg, #374151 0%, #1f2937 100%);
    color: white !important;
    border-radius: 16px;
    margin-top: 20px !important;
}

/* Scrollable content */
.scrollable-content {
    max-height: 300px;
    overflow-y: auto;
    padding-right: 10px;
}

/* Grid layout for cards */
.grid-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
    .content-wrapper {
        flex-direction: column;
    }
    
    .left-panel {
        flex: none;
        width: 100%;
    }
    
    .right-panel {
        flex: none;
        width: 100%;
    }
}

/* Form controls */
.q-select, .q-input {
    width: 100% !important;
}

.resource-input {
    background: #f8fafc !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    width: 100% !important;
}

.resource-input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Icon styling */
.q-icon {
    margin: 0 !important;
}

/* Header text */
.header-title {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: white !important;
    text-align: center;
    margin: 0 !important;
}

.header-subtitle {
    font-size: 1rem !important;
    color: rgba(255, 255, 255, 0.9) !important;
    text-align: center;
    margin: 0 !important;
}
'''

ui.add_head_html(f'<style>{css}</style>')

# Page setup
ui.page_title("🎮 Deadlock Simulator")

# Main container
with ui.column().classes('container-center'):
    # Header
    with ui.header().classes('header-gradient text-white'):
        with ui.column().classes('w-full items-center'):
            ui.label('🔐 Deadlock Avoidance Simulator').classes('header-title')
            ui.label('Visualizing Banker\'s Algorithm with Real Applications').classes('header-subtitle mt-2')
            
            with ui.row().classes('gap-2 mt-4'):
                ui.button('🔄 Reset System', 
                         on_click=lambda: (sim.initialize_system(sim.num_processes, sim.num_resources), 
                                         refresh())).props('flat color=white')
                ui.button('❓ Help', 
                         on_click=lambda: ui.notify('💡 This simulator shows how operating systems prevent deadlocks using Banker\'s Algorithm')).props('flat color=white')

    # Main content wrapper
    with ui.row().classes('content-wrapper'):
        # Left panel - Controls
        with ui.column().classes('left-panel'):
            # System Configuration Card
            with ui.card():
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center mb-4'):
                        ui.icon('settings', size='lg', color='primary')
                        ui.label('System Configuration').classes('text-lg font-bold ml-2')
                    
                    with ui.column().classes('space-y-4'):
                        with ui.row().classes('items-center'):
                            ui.icon('computer', color='blue')
                            ui.label('Applications:').classes('ml-2 flex-shrink-0 w-24')
                            p_slider = ui.slider(min=2, max=6, value=4).classes('flex-grow mx-4')
                            p_label = ui.label('4').classes('font-bold text-blue-600 w-8 text-center')
                        
                        with ui.row().classes('items-center'):
                            ui.icon('memory', color='green')
                            ui.label('Resources:').classes('ml-2 flex-shrink-0 w-24')
                            r_slider = ui.slider(min=2, max=4, value=3).classes('flex-grow mx-4')
                            r_label = ui.label('3').classes('font-bold text-green-600 w-8 text-center')
                        
                        def update_sliders():
                            p_label.text = str(int(p_slider.value))
                            r_label.text = str(int(r_slider.value))
                        
                        p_slider.on('update:model-value', update_sliders)
                        r_slider.on('update:model-value', update_sliders)
                        
                        ui.button('🔄 Apply Configuration', 
                                 on_click=lambda: (sim.initialize_system(int(p_slider.value), int(r_slider.value)), 
                                                 refresh(),
                                                 ui.notify('⚙️ System reconfigured successfully!'))).props('color=primary').classes('w-full')
            
            # System Status Card
            with ui.card():
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center mb-4'):
                        ui.icon('security', size='lg', color='primary')
                        ui.label('System Safety Status').classes('text-lg font-bold ml-2')
                    
                    status_container = ui.column().classes('w-full')
                    
                    def update_status():
                        status_container.clear()
                        with status_container:
                            is_safe, sequence = sim.bankers_algorithm()
                            if is_safe:
                                with ui.column().classes('safe-indicator'):
                                    ui.icon('check_circle', size='xl')
                                    ui.label('SYSTEM IS SAFE').classes('text-lg font-bold mt-2')
                                    ui.label('No deadlock possible').classes('text-sm opacity-90')
                                    ui.separator().classes('my-3')
                                    ui.label('Safe Execution Order:').classes('text-sm font-medium')
                                    with ui.column().classes('scrollable-content'):
                                        for i, proc in enumerate(sequence):
                                            ui.label(f'{i+1}. {proc}').classes('bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mb-1')
                            else:
                                with ui.column().classes('unsafe-indicator'):
                                    ui.icon('warning', size='xl')
                                    ui.label('SYSTEM IS UNSAFE').classes('text-lg font-bold mt-2')
                                    ui.label('Deadlock may occur!').classes('text-sm opacity-90')
                                    ui.separator().classes('my-3')
                                    ui.label('⚠️ No safe sequence found').classes('text-sm font-medium')
                    
                    ui.button('🔍 Check System Safety', on_click=update_status).props('color=primary').classes('w-full')
            
            # Resource Request Card
            with ui.card():
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center mb-4'):
                        ui.icon('add_circle', size='lg', color='primary')
                        ui.label('Resource Request').classes('text-lg font-bold ml-2')
                    
                    proc_select = ui.select(
                        label='Select Application',
                        options=sim.processes,
                        value=sim.processes[0] if sim.processes else ''
                    ).classes('w-full mb-4')
                    
                    ui.label('Request Resources:').classes('font-medium mb-2')
                    req_inputs = []
                    with ui.column().classes('space-y-2'):
                        for i, res in enumerate(sim.resources):
                            with ui.row().classes('items-center'):
                                ui.icon('square', color='green')
                                ui.label(f'{res}:').classes('ml-2 w-32')
                                req_inputs.append(ui.number(value=0, min=0, max=5).classes('flex-grow'))
                    
                    ui.button('📤 Submit Request', 
                             on_click=lambda: (sim.request_resources(sim.processes.index(proc_select.value), 
                                                                   [inp.value for inp in req_inputs]),
                                             refresh(),
                                             update_status())).props('color=secondary').classes('w-full mt-4')
            
            # Recovery Actions Card
            with ui.card():
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center mb-4'):
                        ui.icon('emergency', size='lg', color='red')
                        ui.label('Deadlock Recovery').classes('text-lg font-bold ml-2')
                    
                    ui.label('Select application to terminate:').classes('font-medium mb-2')
                    rec_select = ui.select(
                        options=sim.processes,
                        value=sim.processes[0] if sim.processes else ''
                    ).classes('w-full mb-4')
                    
                    ui.button('💥 Force Terminate', 
                             on_click=lambda: (sim.recover(sim.processes.index(rec_select.value)),
                                             refresh(),
                                             update_status(),
                                             ui.notify(f'⚠️ {rec_select.value} terminated to prevent deadlock'))).props('color=red').classes('w-full')

        # Right panel - Visualizations
        with ui.column().classes('right-panel'):
            # Matrices Display
            with ui.card():
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center mb-4'):
                        ui.icon('table_chart', size='lg', color='primary')
                        ui.label('Resource Allocation Matrices').classes('text-lg font-bold ml-2')
                    
                    tabs = ui.tabs().classes('w-full')
                    with tabs:
                        ui.tab('📊 Allocated')
                        ui.tab('🎯 Maximum Need')
                        ui.tab('📝 Current Need')
                        ui.tab('📦 Available')
                        ui.tab('📜 History')
                    
                    panels = ui.tab_panels(tabs, value='📊 Allocated').classes('w-full tab-content')
                    
                    with panels:
                        # Allocated Matrix
                        with ui.tab_panel('📊 Allocated'):
                            alloc_grid = ui.aggrid({
                                'columnDefs': [{'headerName': 'Application', 'field': 'process', 'width': 180}] + 
                                             [{'headerName': res, 'field': f'R{i}', 'width': 100} 
                                              for i, res in enumerate(sim.resources)],
                                'rowData': [],
                                'defaultColDef': {'filter': True, 'sortable': True},
                                'domLayout': 'autoHeight'
                            }).classes('w-full')
                        
                        # Max Matrix
                        with ui.tab_panel('🎯 Maximum Need'):
                            max_grid = ui.aggrid({
                                'columnDefs': [{'headerName': 'Application', 'field': 'process', 'width': 180}] + 
                                             [{'headerName': res, 'field': f'R{i}', 'width': 100} 
                                              for i, res in enumerate(sim.resources)],
                                'rowData': [],
                                'defaultColDef': {'filter': True, 'sortable': True},
                                'domLayout': 'autoHeight'
                            }).classes('w-full')
                        
                        # Need Matrix
                        with ui.tab_panel('📝 Current Need'):
                            need_grid = ui.aggrid({
                                'columnDefs': [{'headerName': 'Application', 'field': 'process', 'width': 180}] + 
                                             [{'headerName': res, 'field': f'R{i}', 'width': 100} 
                                              for i, res in enumerate(sim.resources)],
                                'rowData': [],
                                'defaultColDef': {'filter': True, 'sortable': True},
                                'domLayout': 'autoHeight'
                            }).classes('w-full')
                        
                        # Available Resources
                        with ui.tab_panel('📦 Available'):
                            avail_grid = ui.aggrid({
                                'columnDefs': [
                                    {'headerName': 'Resource', 'field': 'resource', 'width': 180},
                                    {'headerName': 'Available Units', 'field': 'count', 'width': 150},
                                    {'headerName': 'Status', 'field': 'status', 'width': 120,
                                     'cellRenderer': 'agAnimateShowChangeCellRenderer'}
                                ],
                                'rowData': [],
                                'domLayout': 'autoHeight'
                            }).classes('w-full')
                        
                        # History
                        with ui.tab_panel('📜 History'):
                            hist_area = ui.textarea(label='System Events').props('readonly auto-grow').classes('w-full h-full')
            
            # Visualization Section
            with ui.card():
                with ui.card_section().classes('p-4'):
                    with ui.row().classes('items-center mb-4'):
                        ui.icon('hub', size='lg', color='primary')
                        ui.label('Resource Allocation Graph').classes('text-lg font-bold ml-2')
                    
                    graph_container = ui.column().classes('w-full items-center')
                    
                    def draw_graph():
                        graph_container.clear()
                        with graph_container:
                            # Processes (Applications)
                            ui.label('Applications').classes('text-lg font-bold mb-3 text-gray-700')
                            with ui.row().classes('grid-cards mb-6'):
                                for i, proc in enumerate(sim.processes):
                                    need = sim.calculate_need()
                                    is_deadlocked = any(need[i][j] > sim.available[j] for j in range(sim.num_resources))
                                    
                                    card_class = "deadlocked-card" if is_deadlocked else "process-card"
                                    with ui.column().classes(card_class):
                                        ui.icon('apps', size='md')
                                        ui.label(proc).classes('text-sm mt-1 truncate')
                                        ui.label(f'Allocated: {sim.allocated[i].sum()}').classes('text-xs opacity-80')
                            
                            # Resources
                            ui.label('System Resources').classes('text-lg font-bold mb-3 text-gray-700')
                            with ui.row().classes('grid-cards'):
                                for i, res in enumerate(sim.resources):
                                    with ui.column().classes('resource-card'):
                                        ui.icon('memory', size='md')
                                        ui.label(res).classes('text-sm mt-1 truncate')
                                        ui.label(f'Free: {sim.available[i]}').classes('text-xs opacity-80')
            
            # Algorithm Info
            with ui.expansion('ℹ️ About Banker\'s Algorithm', icon='info').classes('w-full'):
                ui.markdown('''
                ### 🎯 Banker\'s Algorithm - Deadlock Avoidance
                
                **How it works:**
                1. **Need Calculation**: `Need = Maximum - Allocated`
                2. **Safety Check**: System grants requests only if it remains in a safe state
                3. **Safe State**: All applications can complete without deadlock
                4. **Unsafe State**: Deadlock may occur
                
                **Real-world analogy:**
                Imagine a banker (OS) with limited cash (resources). Customers (applications) request loans. 
                The banker only approves if there's enough cash remaining to satisfy all customers' maximum needs.
                
                **Key Benefits:**
                ✅ Prevents deadlock before it happens
                ✅ Maximizes resource utilization
                ✅ Guarantees system stability
                ''').classes('p-4')

# Refresh function
def refresh():
    # Update matrices
    alloc_data = []
    for i, proc in enumerate(sim.processes):
        row = {'process': proc}
        for j, res in enumerate(sim.resources):
            row[f'R{j}'] = int(sim.allocated[i][j])
        alloc_data.append(row)
    alloc_grid.options['rowData'] = alloc_data
    alloc_grid.update()
    
    max_data = []
    for i, proc in enumerate(sim.processes):
        row = {'process': proc}
        for j, res in enumerate(sim.resources):
            row[f'R{j}'] = int(sim.max_need[i][j])
        max_data.append(row)
    max_grid.options['rowData'] = max_data
    max_grid.update()
    
    need = sim.calculate_need()
    need_data = []
    for i, proc in enumerate(sim.processes):
        row = {'process': proc}
        for j, res in enumerate(sim.resources):
            row[f'R{j}'] = int(need[i][j])
        need_data.append(row)
    need_grid.options['rowData'] = need_data
    need_grid.update()
    
    avail_data = []
    for i, res in enumerate(sim.resources):
        status = "🟢 Sufficient" if sim.available[i] > 0 else "🔴 Critical"
        avail_data.append({
            'resource': res,
            'count': int(sim.available[i]),
            'status': status
        })
    avail_grid.options['rowData'] = avail_data
    avail_grid.update()
    
    # Update history
    hist_area.value = '\n'.join(sim.history[-10:])
    
    # Update dropdowns
    proc_select.options = sim.processes
    rec_select.options = sim.processes
    if sim.processes:
        proc_select.value = sim.processes[0]
        rec_select.value = sim.processes[0]
    
    # Update graph
    draw_graph()
    
    # Update status
    update_status()

# Initial setup
refresh()

# Footer
with ui.footer().classes('footer-gradient p-4 text-center'):
    with ui.column().classes('w-full items-center'):
        ui.label('Deadlock Avoidance Simulator | Operating Systems Project | Banker\'s Algorithm Visualization').classes('text-white font-medium')

# Add animations
ui.add_head_html('''
<style>
    @keyframes spin-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .animate-spin-slow {
        animation: spin-slow 3s linear infinite;
    }
    
    /* Scrollbar styling */
    .scrollable-content::-webkit-scrollbar {
        width: 8px;
    }
    
    .scrollable-content::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .scrollable-content::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    .scrollable-content::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>
''')

# Run the app
ui.run(
    title='🎮 Deadlock Simulator', 
    port=8082, 
    reload=False,
    favicon='🔐',
    dark=False
)