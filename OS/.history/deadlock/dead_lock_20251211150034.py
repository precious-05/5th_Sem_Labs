"""
Deadlock Avoidance and Recovery Simulator
Working Version with Banker's Algorithm
"""

import numpy as np
from nicegui import ui

class DeadlockSimulator:
    def __init__(self):
        self.num_processes = 3
        self.num_resources = 3
        self.initialize_system()
    
    def initialize_system(self, num_processes=None, num_resources=None):
        if num_processes:
            self.num_processes = num_processes
        if num_resources:
            self.num_resources = num_resources
            
        self.processes = [f"P{i}" for i in range(self.num_processes)]
        self.resources = [f"R{i}" for i in range(self.num_resources)]
        
        # Initialize matrices
        self.allocated = np.random.randint(0, 3, (self.num_processes, self.num_resources))
        self.max_need = self.allocated + np.random.randint(1, 4, (self.num_processes, self.num_resources))
        
        # Calculate available resources
        total_allocated = self.allocated.sum(axis=0)
        self.available = total_allocated + np.random.randint(2, 6, self.num_resources)
        
        self.history = [f"Initialized: {self.num_processes} processes, {self.num_resources} resources"]
    
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
                    safe_sequence.append(f"P{i}")
                    break
        
        is_safe = all(finish)
        return is_safe, safe_sequence
    
    def request_resources(self, pid, request):
        if pid < 0 or pid >= self.num_processes:
            return False
        
        need = self.calculate_need()
        
        # Check request validity
        for j in range(self.num_resources):
            if request[j] > need[pid][j]:
                self.history.append(f"P{pid}: Request exceeds max need")
                return False
            if request[j] > self.available[j]:
                self.history.append(f"P{pid}: Insufficient resources")
                return False
        
        # Try allocation
        old_allocated = self.allocated.copy()
        old_available = self.available.copy()
        
        self.allocated[pid] += request
        self.available -= request
        
        is_safe, _ = self.bankers_algorithm()
        
        if is_safe:
            self.history.append(f"P{pid}: Request granted")
            return True
        else:
            self.allocated = old_allocated
            self.available = old_available
            self.history.append(f"P{pid}: Request denied - unsafe")
            return False
    
    def recover(self, pid):
        if 0 <= pid < self.num_processes:
            self.available += self.allocated[pid]
            self.allocated[pid] = 0
            self.max_need[pid] = 0
            self.history.append(f"P{pid} terminated for recovery")
            return True
        return False

# Create simulator
sim = DeadlockSimulator()

# UI Setup
ui.page_title("Deadlock Simulator")

# Header
with ui.header().classes('bg-blue-600 text-white p-4'):
    ui.label('🔒 Deadlock Simulator').classes('text-2xl font-bold')

# Main content
with ui.row().classes('w-full p-4'):
    # Left panel
    with ui.column().classes('w-1/3 space-y-4'):
        # Configuration
        ui.label('⚙️ Configuration').classes('text-xl font-bold')
        
        with ui.card():
            with ui.row().classes('items-center'):
                ui.label('Processes:')
                p_slider = ui.slider(min=2, max=5, value=3)
                p_label = ui.label('3')
            
            with ui.row().classes('items-center'):
                ui.label('Resources:')
                r_slider = ui.slider(min=2, max=5, value=3)
                r_label = ui.label('3')
            
            def update_sliders():
                p_label.text = str(int(p_slider.value))
                r_label.text = str(int(r_slider.value))
            
            p_slider.on('update:model-value', update_sliders)
            r_slider.on('update:model-value', update_sliders)
            
            def reconfigure():
                sim.initialize_system(int(p_slider.value), int(r_slider.value))
                refresh()
                ui.notify('System reconfigured')
            
            ui.button('Apply', on_click=reconfigure)
        
        # System Status
        ui.label('📊 Status').classes('text-xl font-bold')
        
        with ui.card():
            status_text = ui.label('')
            seq_text = ui.label('')
            
            def check_safety():
                safe, seq = sim.bankers_algorithm()
                status_text.text = '✅ SAFE' if safe else '❌ UNSAFE'
                seq_text.text = f'Sequence: {", ".join(seq) if seq else "None"}'
            
            ui.button('Check Safety', on_click=check_safety)
        
        # Resource Request
        ui.label('🔄 Request').classes('text-xl font-bold')
        
        with ui.card():
            proc_select = ui.select(
                options=[f'P{i}' for i in range(sim.num_processes)],
                value='P0'
            )
            
            req_inputs = []
            for i in range(sim.num_resources):
                with ui.row().classes('items-center'):
                    ui.label(f'R{i}:')
                    req_inputs.append(ui.number(value=0, min=0, max=5))
            
            def make_request():
                if proc_select.value:
                    pid = int(proc_select.value[1:])
                    req = [inp.value for inp in req_inputs]
                    sim.request_resources(pid, req)
                    refresh()
            
            ui.button('Submit Request', on_click=make_request)
        
        # Recovery
        ui.label('🛠️ Recovery').classes('text-xl font-bold')
        
        with ui.card():
            rec_select = ui.select(
                options=[f'P{i}' for i in range(sim.num_processes)],
                value='P0'
            )
            
            def terminate():
                if rec_select.value:
                    pid = int(rec_select.value[1:])
                    sim.recover(pid)
                    refresh()
                    ui.notify(f'Terminated {rec_select.value}')
            
            ui.button('Terminate Process', on_click=terminate).props('color=red')
    
    # Right panel
    with ui.column().classes('w-2/3 space-y-4'):
        # Matrices
        ui.label('📈 Matrices').classes('text-xl font-bold')
        
        # Create grids
        with ui.tabs().classes('w-full') as tabs:
            ui.tab('Allocated')
            ui.tab('Max')
            ui.tab('Need')
            ui.tab('Available')
            ui.tab('History')
        
        panels = ui.tab_panels(tabs, value='Allocated').classes('w-full')
        
        with panels:
            # Allocated
            with ui.tab_panel('Allocated'):
                alloc_grid = ui.aggrid({
                    'columnDefs': [{'headerName': '', 'field': 'process'}] + 
                                 [{'headerName': f'R{i}', 'field': f'R{i}'} 
                                  for i in range(sim.num_resources)],
                    'rowData': []
                }).classes('h-48')
            
            # Max
            with ui.tab_panel('Max'):
                max_grid = ui.aggrid({
                    'columnDefs': [{'headerName': '', 'field': 'process'}] + 
                                 [{'headerName': f'R{i}', 'field': f'R{i}'} 
                                  for i in range(sim.num_resources)],
                    'rowData': []
                }).classes('h-48')
            
            # Need
            with ui.tab_panel('Need'):
                need_grid = ui.aggrid({
                    'columnDefs': [{'headerName': '', 'field': 'process'}] + 
                                 [{'headerName': f'R{i}', 'field': f'R{i}'} 
                                  for i in range(sim.num_resources)],
                    'rowData': []
                }).classes('h-48')
            
            # Available
            with ui.tab_panel('Available'):
                avail_grid = ui.aggrid({
                    'columnDefs': [
                        {'headerName': 'Resource', 'field': 'resource'},
                        {'headerName': 'Count', 'field': 'count'}
                    ],
                    'rowData': []
                }).classes('h-48')
            
            # History
            with ui.tab_panel('History'):
                hist_area = ui.textarea(label='Events').classes('h-48').props('readonly')
        
        # Graph Visualization
        ui.label('📊 Graph').classes('text-xl font-bold')
        
        with ui.card():
            graph_container = ui.column().classes('w-full items-center p-4')
            
            def draw_graph():
                graph_container.clear()
                with graph_container:
                    # Processes
                    ui.label('Processes').classes('font-bold')
                    with ui.row().classes('my-2'):
                        for i in range(sim.num_processes):
                            color = 'bg-green-500'
                            need = sim.calculate_need()
                            for j in range(sim.num_resources):
                                if need[i][j] > sim.available[j]:
                                    color = 'bg-red-500'
                                    break
                            ui.label(f'P{i}').classes(f'{color} text-white rounded-full w-10 h-10 flex items-center justify-center mx-1')
                    
                    # Resources
                    ui.label('Resources').classes('font-bold mt-4')
                    with ui.row():
                        for i in range(sim.num_resources):
                            ui.label(f'R{i}').classes('bg-blue-500 text-white rounded-lg w-10 h-10 flex items-center justify-center mx-1')
            
            draw_graph()

# Refresh function
def refresh():
    # Update grids
    alloc_data = []
    for i in range(sim.num_processes):
        row = {'process': f'P{i}'}
        for j in range(sim.num_resources):
            row[f'R{j}'] = int(sim.allocated[i][j])
        alloc_data.append(row)
    alloc_grid.options['rowData'] = alloc_data
    
    max_data = []
    for i in range(sim.num_processes):
        row = {'process': f'P{i}'}
        for j in range(sim.num_resources):
            row[f'R{j}'] = int(sim.max_need[i][j])
        max_data.append(row)
    max_grid.options['rowData'] = max_data
    
    need = sim.calculate_need()
    need_data = []
    for i in range(sim.num_processes):
        row = {'process': f'P{i}'}
        for j in range(sim.num_resources):
            row[f'R{j}'] = int(need[i][j])
        need_data.append(row)
    need_grid.options['rowData'] = need_data
    
    avail_data = [{'resource': f'R{i}', 'count': int(sim.available[i])} 
                 for i in range(sim.num_resources)]
    avail_grid.options['rowData'] = avail_data
    
    # Update history
    hist_area.value = '\n'.join(sim.history[-10:])  # Last 10 entries
    
    # Update dropdowns
    proc_select.options = [f'P{i}' for i in range(sim.num_processes)]
    rec_select.options = [f'P{i}' for i in range(sim.num_processes)]
    
    # Update graph
    draw_graph()
    
    # Check safety
    check_safety()

# Initial refresh
refresh()

# Footer
with ui.footer().classes('bg-gray-100 p-2 text-center'):
    ui.label('Deadlock Simulator | Banker\'s Algorithm | OS Project')

# Run on different port to avoid conflict
ui.run(title='Deadlock Simulator', port=8081, reload=False)