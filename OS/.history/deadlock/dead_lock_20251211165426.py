"""
Deadlock Avoidance and Recovery Simulator
Perfectly Centered Layout with Fixed Structure
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

# Custom CSS for beautiful UI
css = '''
/* Background and base styles */
body {
    background: linear-gradient(135deg, #e2fffb 0%, #f9ffff 100%);

    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

/* Main container for centering */
.main-container {
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}

/* Header styling */
.custom-header {
    background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%) !important;
    border-radius: 16px;
    padding: 25px 30px !important;
    margin-left: 300px;
    margin-bottom: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    text-align: center;
}

/* Content wrapper */
.content-wrapper {
    display: flex;
    gap: 20px;
    width: 100%;
    margin-bottom: 20px;
}

/* Left panel */
.left-panel {
    flex: 0 0 200px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* Right panel */
.right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-width: 0;
}

/* Card styling */
.custom-card {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1) !important;
    border: none !important;
    backdrop-filter: blur(10px);
    padding: 20px !important;
}

/* Button styling */
.custom-button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
}

.custom-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
}

/* Process and resource cards */
.process-card {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border-radius: 12px;
    padding: 12px;
    margin: 8px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
    min-width: 140px;
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
    margin: 8px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    transition: all 0.3s ease;
    min-width: 140px;
    flex-shrink: 0;
}

.resource-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* Deadlock animation */
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
    margin-bottom: 15px;
}

.unsafe-indicator {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 15px;
}

/* Table styling */
.ag-theme-alpine {
    --ag-header-background-color: #f8fafc;
    --ag-header-foreground-color: #475569;
    --ag-border-color: #e2e8f0;
    --ag-row-border-color: #e2e8f0;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Footer styling */
.custom-footer {
    background: linear-gradient(90deg, #374151 0%, #1f2937 100%) !important;
    border-radius: 16px;
    padding: 20px !important;
    color: white !important;
    text-align: center;
    margin-top: 20px;
}

/* Responsive design */
@media (max-width: 1200px) {
    .content-wrapper {
        flex-direction: column;
    }
    
    .left-panel {
        width: 100%;
        flex: none;
    }
    
    .right-panel {
        width: 100%;
        flex: none;
    }
}

/* Form controls */
.custom-select, .custom-input {
    width: 100% !important;
    margin-bottom: 10px !important;
}

.resource-input {
    background: #f8fafc !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
}

.resource-input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Title styling */
.main-title {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: white !important;
    margin-bottom: 8px !important;
}

.subtitle {
    font-size: 1.1rem !important;
    color: rgba(255, 255, 255, 0.9) !important;
    margin-bottom: 20px !important;
}

/* Section headers */
.section-title {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #1f2937 !important;
    margin-bottom: 15px !important;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Grid layout */
.cards-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    margin: 15px 0;
}

/* Scrollable areas */
.scrollable {
    max-height: 200px;
    overflow-y: auto;
    padding-right: 10px;
}

/* Custom scrollbar */
.scrollable::-webkit-scrollbar {
    width: 6px;
}

.scrollable::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.scrollable::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}

.scrollable::-webkit-scrollbar-thumb:hover {
    background: #555;
}
'''

ui.add_head_html(f'<style>{css}</style>')

# Page setup
ui.page_title("🎮 Deadlock Simulator")
ui.query('.nicegui-content').classes('p-0')

# Main container
with ui.column().classes('main-container'):
    # Header (using a card instead of header element)
    with ui.card().classes('custom-header'):
        with ui.column().classes('w-full items-center'):
            ui.label('🔐 Deadlock Avoidance Simulator').classes('main-title')
            ui.label('Visualizing Banker\'s Algorithm with Real Applications').classes('subtitle')
            
            with ui.row().classes('gap-4 mt-2'):
                ui.button('🔄 Reset System', 
                         on_click=lambda: (sim.initialize_system(sim.num_processes, sim.num_resources), 
                                         refresh())).props('flat color=white').classes('custom-button')
                ui.button('❓ Help', 
                         on_click=lambda: ui.notify('💡 This simulator shows how operating systems prevent deadlocks using Banker\'s Algorithm')).props('flat color=white').classes('custom-button')

    # Main content
    with ui.row().classes('content-wrapper'):
        # Left panel - Controls
        with ui.column().classes('left-panel'):
            # System Configuration Card
            with ui.card().classes('custom-card'):
                with ui.row().classes('items-center mb-4'):
                    ui.icon('settings', size='lg', color='primary')
                    ui.label('System Configuration').classes('section-title')
                
                with ui.column().classes('space-y-4'):
                    with ui.row().classes('items-center'):
                        ui.icon('computer', color='blue')
                        ui.label('Applications:').classes('ml-2 w-28')
                        p_slider = ui.slider(min=2, max=6, value=4).classes('flex-grow mx-4')
                        p_label = ui.label('4').classes('font-bold text-blue-600 w-8 text-center')
                    
                    with ui.row().classes('items-center'):
                        ui.icon('memory', color='green')
                        ui.label('Resources:').classes('ml-2 w-28')
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
                                             ui.notify('⚙️ System reconfigured successfully!'))).props('color=primary').classes('custom-button w-full')
            
            # System Status Card
            with ui.card().classes('custom-card'):
                with ui.row().classes('items-center mb-4'):
                    ui.icon('security', size='lg', color='primary')
                    ui.label('System Safety Status').classes('section-title')
                
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
                                with ui.column().classes('scrollable'):
                                    for i, proc in enumerate(sequence):
                                        ui.label(f'{i+1}. {proc}').classes('bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mb-1')
                        else:
                            with ui.column().classes('unsafe-indicator'):
                                ui.icon('warning', size='xl')
                                ui.label('SYSTEM IS UNSAFE').classes('text-lg font-bold mt-2')
                                ui.label('Deadlock may occur!').classes('text-sm opacity-90')
                                ui.separator().classes('my-3')
                                ui.label('⚠️ No safe sequence found').classes('text-sm font-medium')
                
                ui.button('🔍 Check System Safety', on_click=update_status).props('color=primary').classes('custom-button w-full')
            
            # Resource Request Card
            with ui.card().classes('custom-card'):
                with ui.row().classes('items-center mb-4'):
                    ui.icon('add_circle', size='lg', color='primary')
                    ui.label('Resource Request').classes('section-title')
                
                proc_select = ui.select(
                    label='Select Application',
                    options=sim.processes,
                    value=sim.processes[0] if sim.processes else ''
                ).classes('custom-select')
                
                ui.label('Request Resources:').classes('font-medium mb-2')
                req_inputs = []
                with ui.column().classes('space-y-2'):
                    for i, res in enumerate(sim.resources):
                        with ui.row().classes('items-center'):
                            ui.icon('square', color='green')
                            ui.label(f'{res}:').classes('ml-2 w-36')
                            req_inputs.append(ui.number(value=0, min=0, max=5).classes('flex-grow resource-input'))
                
                ui.button('📤 Submit Request', 
                         on_click=lambda: (sim.request_resources(sim.processes.index(proc_select.value), 
                                                               [inp.value for inp in req_inputs]),
                                         refresh(),
                                         update_status())).props('color=secondary').classes('custom-button w-full mt-4')
            
            # Recovery Actions Card
            with ui.card().classes('custom-card'):
                with ui.row().classes('items-center mb-4'):
                    ui.icon('emergency', size='lg', color='red')
                    ui.label('Deadlock Recovery').classes('section-title')
                
                ui.label('Select application to terminate:').classes('font-medium mb-2')
                rec_select = ui.select(
                    options=sim.processes,
                    value=sim.processes[0] if sim.processes else ''
                ).classes('custom-select')
                
                ui.button('💥 Force Terminate', 
                         on_click=lambda: (sim.recover(sim.processes.index(rec_select.value)),
                                         refresh(),
                                         update_status(),
                                         ui.notify(f'⚠️ {rec_select.value} terminated to prevent deadlock'))).props('color=red').classes('custom-button w-full')

        # Right panel - Visualizations
        with ui.column().classes('right-panel'):
            # Matrices Display
            with ui.card().classes('custom-card'):
                with ui.row().classes('items-center mb-4'):
                    ui.icon('table_chart', size='lg', color='primary')
                    ui.label('Resource Allocation Matrices').classes('section-title')
                
                # Create tabs
                with ui.tabs().classes('w-full') as tabs:
                    alloc_tab = ui.tab('📊 Allocated')
                    max_tab = ui.tab('🎯 Maximum Need')
                    need_tab = ui.tab('📝 Current Need')
                    avail_tab = ui.tab('📦 Available')
                    hist_tab = ui.tab('📜 History')
                
                # Tab panels
                with ui.tab_panels(tabs, value=alloc_tab).classes('w-full'):
                    with ui.tab_panel(alloc_tab):
                        alloc_grid = ui.aggrid({
                            'columnDefs': [{'headerName': 'Application', 'field': 'process', 'width': 180}] + 
                                         [{'headerName': res, 'field': f'R{i}', 'width': 100} 
                                          for i, res in enumerate(sim.resources)],
                            'rowData': [],
                            'defaultColDef': {'filter': True, 'sortable': True},
                            'domLayout': 'autoHeight'
                        }).classes('w-full')
                    
                    with ui.tab_panel(max_tab):
                        max_grid = ui.aggrid({
                            'columnDefs': [{'headerName': 'Application', 'field': 'process', 'width': 180}] + 
                                         [{'headerName': res, 'field': f'R{i}', 'width': 100} 
                                          for i, res in enumerate(sim.resources)],
                            'rowData': [],
                            'defaultColDef': {'filter': True, 'sortable': True},
                            'domLayout': 'autoHeight'
                        }).classes('w-full')
                    
                    with ui.tab_panel(need_tab):
                        need_grid = ui.aggrid({
                            'columnDefs': [{'headerName': 'Application', 'field': 'process', 'width': 180}] + 
                                         [{'headerName': res, 'field': f'R{i}', 'width': 100} 
                                          for i, res in enumerate(sim.resources)],
                            'rowData': [],
                            'defaultColDef': {'filter': True, 'sortable': True},
                            'domLayout': 'autoHeight'
                        }).classes('w-full')
                    
                    with ui.tab_panel(avail_tab):
                        avail_grid = ui.aggrid({
                            'columnDefs': [
                                {'headerName': 'Resource', 'field': 'resource', 'width': 180},
                                {'headerName': 'Available Units', 'field': 'count', 'width': 150},
                                {'headerName': 'Status', 'field': 'status', 'width': 120}
                            ],
                            'rowData': [],
                            'domLayout': 'autoHeight'
                        }).classes('w-full')
                    
                    with ui.tab_panel(hist_tab):
                        hist_area = ui.textarea(label='System Events').props('readonly auto-grow').classes('w-full').style('min-height: 200px')
            
            # Visualization Section
            with ui.card().classes('custom-card'):
                with ui.row().classes('items-center mb-4'):
                    ui.icon('hub', size='lg', color='primary')
                    ui.label('Resource Allocation Graph').classes('section-title')
                
                graph_container = ui.column().classes('w-full items-center')
                
                def draw_graph():
                    graph_container.clear()
                    with graph_container:
                        # Processes (Applications)
                        ui.label('Applications').classes('text-lg font-bold mb-3 text-gray-700')
                        with ui.row().classes('cards-grid'):
                            for i, proc in enumerate(sim.processes):
                                need = sim.calculate_need()
                                is_deadlocked = any(need[i][j] > sim.available[j] for j in range(sim.num_resources))
                                
                                card_class = "deadlocked-card" if is_deadlocked else "process-card"
                                with ui.column().classes(card_class):
                                    ui.icon('apps', size='md')
                                    ui.label(proc).classes('text-sm mt-1 truncate max-w-[120px]')
                                    ui.label(f'Allocated: {sim.allocated[i].sum()}').classes('text-xs opacity-80')
                        
                        # Resources
                        ui.label('System Resources').classes('text-lg font-bold mb-3 text-gray-700 mt-6')
                        with ui.row().classes('cards-grid'):
                            for i, res in enumerate(sim.resources):
                                with ui.column().classes('resource-card'):
                                    ui.icon('memory', size='md')
                                    ui.label(res).classes('text-sm mt-1 truncate max-w-[120px]')
                                    ui.label(f'Free: {sim.available[i]}').classes('text-xs opacity-80')
            
            # Algorithm Info
            with ui.expansion('ℹ️ About Banker\'s Algorithm', icon='info').classes('w-full'):
                ui.markdown('''
                ### 🎯 Banker's Algorithm - Deadlock Avoidance
                
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

# Initial refresh
refresh()

# Footer
with ui.card().classes('custom-footer'):
    ui.label('Deadlock Avoidance Simulator | Operating Systems Project | Banker\'s Algorithm Visualization').classes('text-center text-white font-medium')

# Run the app
ui.run(
    title='🎮 Deadlock Simulator', 
    port=8082, 
    reload=False,
    favicon='🔐',
    dark=False
)