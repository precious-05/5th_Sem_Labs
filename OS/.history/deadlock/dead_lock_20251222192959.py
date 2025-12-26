"""
Deadlock Avoidance and Recovery Simulator
100% Working Version - Fixed Table Syntax
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
        self.allocated = np.random.randint(0, 3, (self.num_processes, self.num_resources), dtype=np.int32)
        self.max_need = self.allocated + np.random.randint(1, 4, (self.num_processes, self.num_resources), dtype=np.int32)
        
        # Calculate available resources
        total_allocated = self.allocated.sum(axis=0)
        self.available = total_allocated + np.random.randint(2, 6, self.num_resources, dtype=np.int32)
        
        self.history = [f"✅ System initialized with {self.num_processes} processes and {self.num_resources} resources"]
        self.safe_sequence = []
    
    def calculate_need(self):
        return np.subtract(self.max_need, self.allocated)
    
    def bankers_algorithm(self):
        need = self.calculate_need()
        work = self.available.copy()
        finish = [False] * self.num_processes
        
        safe_sequence = []
        count = 0
        
        for _ in range(self.num_processes):
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    can_allocate = True
                    for j in range(self.num_resources):
                        if need[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        work += self.allocated[i]
                        finish[i] = True
                        safe_sequence.append(self.processes[i])
                        found = True
                        count += 1
                        break
            
            if not found:
                break
        
        is_safe = all(finish)
        self.safe_sequence = safe_sequence
        return is_safe, safe_sequence
    
    def request_resources(self, pid, request):
        if pid < 0 or pid >= self.num_processes:
            return False
        
        request_array = np.array(request, dtype=np.int32)
        need = self.calculate_need()
        
        # Check request validity
        for j in range(self.num_resources):
            if request_array[j] > need[pid][j]:
                self.history.append(f"❌ {self.processes[pid]}: Request ({request_array[j]}) exceeds maximum need ({need[pid][j]}) for {self.resources[j]}")
                return False
            if request_array[j] > self.available[j]:
                self.history.append(f"⏳ {self.processes[pid]}: Waiting for {self.resources[j]} (Requested: {request_array[j]}, Available: {self.available[j]})")
                return False
        
        # Try allocation temporarily
        old_allocated = self.allocated.copy()
        old_available = self.available.copy()
        
        self.allocated[pid] = self.allocated[pid] + request_array
        self.available = self.available - request_array
        
        is_safe, _ = self.bankers_algorithm()
        
        if is_safe:
            self.history.append(f"✅ {self.processes[pid]}: Request granted ({request_array})")
            return True
        else:
            self.allocated = old_allocated
            self.available = old_available
            self.history.append(f"⚠️ {self.processes[pid]}: Request denied - would lead to unsafe state")
            return False
    
    def recover(self, pid):
        if 0 <= pid < self.num_processes:
            self.available = self.available + self.allocated[pid]
            freed_resources = int(self.allocated[pid].sum())
            self.history.append(f"🔄 {self.processes[pid]} terminated. Resources freed: {freed_resources} units")
            self.allocated[pid] = np.zeros(self.num_resources, dtype=np.int32)
            self.max_need[pid] = np.zeros(self.num_resources, dtype=np.int32)
            return True
        return False

# Create simulator instance
simulator = DeadlockSimulator()

# Custom CSS
css = '''
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}

.header-card {
    background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 16px;
    padding: 25px 30px;
    margin-bottom: 20px;
    text-align: center;
    color: white;
}

.content-wrapper {
    display: flex;
    gap: 20px;
    width: 100%;
    margin-bottom: 20px;
}

.left-panel {
    flex: 0 0 380px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-width: 0;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.button {
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.safe-status {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 15px;
}

.unsafe-status {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 15px;
}

.process-card {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    min-width: 120px;
}

.resource-card {
    background: linear-gradient(135deg, #10b981 0%, #047857 100%);
    color: white;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    min-width: 120px;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.deadlocked {
    animation: pulse 2s infinite;
}

.table-container {
    height: 250px;
    overflow: auto;
}

.history-textarea {
    height: 250px;
    font-family: monospace;
}
'''

ui.add_head_html(f'<style>{css}</style>')

# Create UI elements
ui.page_title("Deadlock Simulator")

with ui.column().classes('container'):
    # Header
    with ui.card().classes('header-card'):
        ui.label('🔐 Deadlock Avoidance Simulator').classes('text-2xl font-bold')
        ui.label('Banker\'s Algorithm with Real Applications').classes('text-lg opacity-90')
        
        with ui.row().classes('gap-2 mt-4'):
            ui.button('Reset System', 
                     on_click=lambda: (simulator.initialize_system(), refresh_ui())).props('flat color=white')
            ui.button('Help', 
                     on_click=lambda: ui.notify('1. Click "Check Safety" first\n2. Make small requests (0-1)\n3. Try to cause deadlock\n4. Use recovery if needed')).props('flat color=white')
    
    # Main content
    with ui.row().classes('content-wrapper'):
        # Left panel - Controls
        with ui.column().classes('left-panel'):
            # Configuration Card
            with ui.card().classes('card'):
                ui.label('⚙️ Configuration').classes('text-xl font-bold mb-4')
                
                with ui.row().classes('items-center mb-4'):
                    ui.label('Applications:')
                    p_slider = ui.slider(min=2, max=6, value=4).classes('flex-grow')
                    p_label = ui.label('4').classes('ml-2 font-bold w-8')
                
                with ui.row().classes('items-center mb-4'):
                    ui.label('Resources:')
                    r_slider = ui.slider(min=2, max=4, value=3).classes('flex-grow')
                    r_label = ui.label('3').classes('ml-2 font-bold w-8')
                
                def apply_config():
                    simulator.initialize_system(int(p_slider.value), int(r_slider.value))
                    refresh_ui()
                    ui.notify('✅ System configured!')
                
                ui.button('Apply Configuration', on_click=apply_config).props('color=primary').classes('w-full')
            
            # Status Card
            with ui.card().classes('card'):
                ui.label('📊 System Status').classes('text-xl font-bold mb-4')
                
                # Status display area
                status_area = ui.column()
                
                def check_safety():
                    status_area.clear()
                    with status_area:
                        is_safe, sequence = simulator.bankers_algorithm()
                        if is_safe:
                            with ui.column().classes('safe-status'):
                                ui.icon('check_circle', size='xl')
                                ui.label('SYSTEM IS SAFE').classes('text-lg font-bold mt-2')
                                ui.label('No deadlock possible').classes('text-sm')
                                if sequence:
                                    ui.separator().classes('my-3')
                                    ui.label('Safe Sequence:').classes('text-sm font-bold')
                                    for i, proc in enumerate(sequence):
                                        ui.label(f'{i+1}. {proc}').classes('bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm my-1')
                        else:
                            with ui.column().classes('unsafe-status'):
                                ui.icon('warning', size='xl')
                                ui.label('SYSTEM IS UNSAFE').classes('text-lg font-bold mt-2')
                                ui.label('Deadlock may occur!').classes('text-sm')
                
                ui.button('Check System Safety', on_click=check_safety).props('color=primary').classes('w-full')
            
            # Request Card
            with ui.card().classes('card'):
                ui.label('🔄 Request Resources').classes('text-xl font-bold mb-4')
                
                process_select = ui.select(
                    label='Select Application',
                    options=simulator.processes,
                    value=simulator.processes[0] if simulator.processes else ''
                ).classes('w-full mb-4')
                
                ui.label('Request Amounts (0-2 recommended):').classes('font-medium mb-2')
                request_inputs = []
                for i, res in enumerate(simulator.resources):
                    with ui.row().classes('items-center mb-2'):
                        ui.label(f'{res}:').classes('w-32')
                        request_inputs.append(ui.number(value=0, min=0, max=3).classes('ml-2 flex-grow'))
                
                def submit_request():
                    if not process_select.value:
                        ui.notify('Please select an application!', type='warning')
                        return
                    
                    pid = simulator.processes.index(process_select.value)
                    request = [inp.value for inp in request_inputs]
                    
                    success = simulator.request_resources(pid, request)
                    
                    if success:
                        ui.notify('✅ Request granted!', type='positive')
                    else:
                        ui.notify('⚠️ Request denied', type='warning')
                    
                    refresh_ui()
                    check_safety()
                    
                    # Reset inputs
                    for inp in request_inputs:
                        inp.value = 0
                
                ui.button('Submit Request', on_click=submit_request).props('color=secondary').classes('w-full')
            
            # Recovery Card
            with ui.card().classes('card'):
                ui.label('🛠️ Recovery').classes('text-xl font-bold mb-4')
                
                recovery_select = ui.select(
                    label='Select Application to Terminate',
                    options=simulator.processes,
                    value=simulator.processes[0] if simulator.processes else ''
                ).classes('w-full mb-4')
                
                def terminate_process():
                    if not recovery_select.value:
                        ui.notify('Please select an application!', type='warning')
                        return
                    
                    pid = simulator.processes.index(recovery_select.value)
                    simulator.recover(pid)
                    ui.notify(f'✅ {recovery_select.value} terminated', type='positive')
                    refresh_ui()
                    check_safety()
                
                ui.button('Force Terminate', on_click=terminate_process).props('color=red').classes('w-full')
        
        # Right panel - Visualizations
        with ui.column().classes('right-panel'):
            # Matrices Card
            with ui.card().classes('card'):
                ui.label('📈 Resource Matrices').classes('text-xl font-bold mb-4')
                
                # Create tabs
                tabs = ui.tabs().classes('w-full')
                with tabs:
                    tab1 = ui.tab('Allocated')
                    tab2 = ui.tab('Maximum')
                    tab3 = ui.tab('Need')
                    tab4 = ui.tab('Available')
                    tab5 = ui.tab('History')
                
                panels = ui.tab_panels(tabs, value=tab1).classes('w-full')
                
                with panels:
                    # Allocated matrix
                    with ui.tab_panel(tab1):
                        allocated_container = ui.column().classes('table-container')
                    
                    # Maximum matrix
                    with ui.tab_panel(tab2):
                        max_container = ui.column().classes('table-container')
                    
                    # Need matrix
                    with ui.tab_panel(tab3):
                        need_container = ui.column().classes('table-container')
                    
                    # Available resources
                    with ui.tab_panel(tab4):
                        available_container = ui.column().classes('table-container')
                    
                    # History
                    with ui.tab_panel(tab5):
                        history_area = ui.textarea(label='System Events').props('readonly').classes('history-textarea w-full')
            
            # Visualization Card
            with ui.card().classes('card'):
                ui.label('📊 Process-Resource Graph').classes('text-xl font-bold mb-4')
                
                graph_area = ui.column()
                
                def update_graph():
                    graph_area.clear()
                    with graph_area:
                        # Processes
                        ui.label('Applications').classes('font-bold mb-2')
                        with ui.row().classes('flex-wrap gap-2 mb-4'):
                            for i, proc in enumerate(simulator.processes):
                                need = simulator.calculate_need()
                                is_deadlocked = any(need[i][j] > simulator.available[j] for j in range(simulator.num_resources))
                                
                                card_class = "process-card deadlocked" if is_deadlocked else "process-card"
                                with ui.column().classes(card_class):
                                    ui.label(proc.split()[0]).classes('font-medium')
                                    ui.label(f'Alloc: {int(simulator.allocated[i].sum())}').classes('text-xs')
                        
                        # Resources
                        ui.label('Resources').classes('font-bold mb-2')
                        with ui.row().classes('flex-wrap gap-2'):
                            for i, res in enumerate(simulator.resources):
                                with ui.column().classes('resource-card'):
                                    ui.label(res.split()[0]).classes('font-medium')
                                    ui.label(f'Free: {int(simulator.available[i])}').classes('text-xs')

# Function to create table
def create_table(container, data, columns):
    container.clear()
    with container:
        # Create headers
        with ui.row().classes('bg-gray-100 p-2 rounded-t-lg font-bold'):
            for col in columns:
                ui.label(col).classes('w-32 px-2')
        
        # Create rows
        for row in data:
            with ui.row().classes('border-b py-2 hover:bg-gray-50'):
                for value in row:
                    ui.label(str(value)).classes('w-32 px-2')

# Refresh function
def refresh_ui():
    # Update allocated matrix
    alloc_data = []
    for i, proc in enumerate(simulator.processes):
        row = [proc] + [int(simulator.allocated[i][j]) for j in range(simulator.num_resources)]
        alloc_data.append(row)
    create_table(allocated_container, alloc_data, ['Application'] + simulator.resources)
    
    # Update max matrix
    max_data = []
    for i, proc in enumerate(simulator.processes):
        row = [proc] + [int(simulator.max_need[i][j]) for j in range(simulator.num_resources)]
        max_data.append(row)
    create_table(max_container, max_data, ['Application'] + simulator.resources)
    
    # Update need matrix
    need = simulator.calculate_need()
    need_data = []
    for i, proc in enumerate(simulator.processes):
        row = [proc] + [int(need[i][j]) for j in range(simulator.num_resources)]
        need_data.append(row)
    create_table(need_container, need_data, ['Application'] + simulator.resources)
    
    # Update available resources
    avail_data = []
    for i, res in enumerate(simulator.resources):
        avail_data.append([res, int(simulator.available[i])])
    create_table(available_container, avail_data, ['Resource', 'Available'])
    
    # Update history
    history_area.value = '\n'.join(simulator.history[-15:])
    
    # Update dropdowns
    process_select.options = simulator.processes
    recovery_select.options = simulator.processes
    if simulator.processes:
        process_select.value = simulator.processes[0]
        recovery_select.value = simulator.processes[0]
    
    # Update graph
    update_graph()

# Initialize the UI
refresh_ui()

# Footer
with ui.card().classes('card mt-4'):
    ui.label('Deadlock Simulator | Banker\'s Algorithm | OS Project').classes('text-center')

# Run the app
ui.run(
    title='Deadlock Simulator',
    port=8082,
    reload=False,
    dark=False
)