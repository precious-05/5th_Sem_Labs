"""
Deadlock Avoidance and Recovery Simulator
A GUI-based educational tool using NiceGUI
Simplified and working version
"""

import numpy as np
from nicegui import ui

class DeadlockSimulator:
    def __init__(self):
        self.num_processes = 3
        self.num_resources = 3
        self.initialize_system()
    
    def initialize_system(self, num_processes=None, num_resources=None):
        """Initialize the system with given number of processes and resources"""
        if num_processes:
            self.num_processes = num_processes
        if num_resources:
            self.num_resources = num_resources
            
        self.processes = [f"P{i}" for i in range(self.num_processes)]
        self.resources = [f"R{i}" for i in range(self.num_resources)]
        
        # Initialize matrices
        self.allocated = []
        self.max_need = []
        self.available = []
        self.history = []
        
        # Create random initial state
        for i in range(self.num_processes):
            allocated_row = []
            max_row = []
            for j in range(self.num_resources):
                alloc = np.random.randint(0, 3)
                allocated_row.append(alloc)
                max_row.append(alloc + np.random.randint(1, 4))
            self.allocated.append(allocated_row)
            self.max_need.append(max_row)
        
        # Calculate available resources
        self.available = [0] * self.num_resources
        for j in range(self.num_resources):
            total_allocated = sum(self.allocated[i][j] for i in range(self.num_processes))
            self.available[j] = total_allocated + np.random.randint(2, 6)
        
        self.history.append(f"System initialized with {self.num_processes} processes and {self.num_resources} resources")
    
    def calculate_need(self):
        """Calculate the need matrix (max - allocated)"""
        need = []
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                row.append(self.max_need[i][j] - self.allocated[i][j])
            need.append(row)
        return need
    
    def bankers_algorithm(self):
        """Banker's algorithm for deadlock avoidance"""
        need = self.calculate_need()
        work = self.available.copy()
        finish = [False] * self.num_processes
        
        safe_sequence = []
        count = 0
        
        while count < self.num_processes:
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if need[i] <= work
                    can_allocate = True
                    for j in range(self.num_resources):
                        if need[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        # Process can complete
                        for j in range(self.num_resources):
                            work[j] += self.allocated[i][j]
                        finish[i] = True
                        safe_sequence.append(self.processes[i])
                        found = True
                        count += 1
            
            if not found:
                break
        
        is_safe = all(finish)
        return is_safe, safe_sequence
    
    def detect_deadlock(self):
        """Detect which processes are deadlocked"""
        deadlocked = []
        is_safe, _ = self.bankers_algorithm()
        
        if not is_safe:
            # Simplified: mark all processes that can't immediately get resources
            need = self.calculate_need()
            for i in range(self.num_processes):
                can_proceed = True
                for j in range(self.num_resources):
                    if need[i][j] > self.available[j]:
                        can_proceed = False
                        break
                if not can_proceed:
                    deadlocked.append(i)
        
        return deadlocked
    
    def request_resources(self, process_idx, request):
        """Process requests resources"""
        if process_idx < 0 or process_idx >= self.num_processes:
            return False
        
        need = self.calculate_need()
        
        # Check request validity
        for j in range(self.num_resources):
            if request[j] > need[process_idx][j]:
                self.history.append(f"Error: P{process_idx} requested more than max need")
                return False
            
            if request[j] > self.available[j]:
                self.history.append(f"P{process_idx} must wait - insufficient resources")
                return False
        
        # Try allocation temporarily
        old_allocated = [row.copy() for row in self.allocated]
        old_available = self.available.copy()
        
        # Apply request
        for j in range(self.num_resources):
            self.allocated[process_idx][j] += request[j]
            self.available[j] -= request[j]
        
        # Check safety
        is_safe, _ = self.bankers_algorithm()
        
        if is_safe:
            self.history.append(f"Request granted to P{process_idx}")
            return True
        else:
            # Revert changes
            self.allocated = old_allocated
            self.available = old_available
            self.history.append(f"Request denied to P{process_idx} - unsafe state")
            return False
    
    def recover_by_termination(self, process_idx):
        """Recover from deadlock by terminating a process"""
        if 0 <= process_idx < self.num_processes:
            # Free resources
            for j in range(self.num_resources):
                self.available[j] += self.allocated[process_idx][j]
                self.allocated[process_idx][j] = 0
                self.max_need[process_idx][j] = 0
            
            self.history.append(f"P{process_idx} terminated for recovery")
            return True
        return False

# Create simulator instance
simulator = DeadlockSimulator()

# UI Setup
ui.page_title("Deadlock Simulator")

# Header
with ui.header().classes('bg-blue-600 text-white'):
    ui.label('🔒 Deadlock Avoidance & Recovery Simulator').classes('text-2xl font-bold')

# Main layout
with ui.row().classes('w-full h-screen'):
    # Left panel - Controls
    with ui.column().classes('w-1/3 p-4 bg-gray-100 h-full'):
        # System Configuration
        ui.label('⚙️ System Configuration').classes('text-xl font-bold mb-4')
        
        with ui.card():
            ui.label('Setup Parameters')
            with ui.row().classes('items-center'):
                ui.label('Processes:')
                process_slider = ui.slider(min=2, max=5, value=3)
                process_label = ui.label('3')
            
            with ui.row().classes('items-center'):
                ui.label('Resources:')
                resource_slider = ui.slider(min=2, max=5, value=3)
                resource_label = ui.label('3')
            
            def update_sliders():
                process_label.text = str(int(process_slider.value))
                resource_label.text = str(int(resource_slider.value))
            
            process_slider.on('update:model-value', update_sliders)
            resource_slider.on('update:model-value', update_sliders)
            
            def apply_config():
                simulator.initialize_system(int(process_slider.value), int(resource_slider.value))
                refresh_ui()
                ui.notify('System reconfigured!')
            
            ui.button('Apply Configuration', on_click=apply_config)
        
        # System Status
        ui.label('📊 System Status').classes('text-xl font-bold mt-6 mb-4')
        
        with ui.card():
            status_label = ui.label('')
            sequence_label = ui.label('')
            
            def check_status():
                is_safe, sequence = simulator.bankers_algorithm()
                if is_safe:
                    status_label.text = '✅ System is SAFE'
                    sequence_label.text = f'Safe sequence: {" → ".join(sequence)}'
                else:
                    status_label.text = '❌ System is UNSAFE'
                    sequence_label.text = 'Deadlock possible!'
            
            ui.button('Check System State', on_click=check_status)
        
        # Resource Request
        ui.label('🔄 Request Resources').classes('text-xl font-bold mt-6 mb-4')
        
        with ui.card():
            process_select = ui.select(
                options=[f'P{i}' for i in range(simulator.num_processes)],
                value='P0'
            )
            
            request_inputs = []
            for i in range(simulator.num_resources):
                with ui.row().classes('items-center'):
                    ui.label(f'R{i}:')
                    request_inputs.append(ui.number(value=0, min=0, max=5))
            
            def submit_request():
                if process_select.value:
                    pid = int(process_select.value[1:])
                    request = [inp.value for inp in request_inputs]
                    success = simulator.request_resources(pid, request)
                    refresh_ui()
            
            ui.button('Submit Request', on_click=submit_request)
        
        # Recovery Actions
        ui.label('🛠️ Recovery Actions').classes('text-xl font-bold mt-6 mb-4')
        
        with ui.card():
            deadlock_label = ui.label('')
            
            def detect_deadlock():
                deadlocked = simulator.detect_deadlock()
                if deadlocked:
                    deadlock_label.text = f'Deadlocked: {", ".join([f"P{i}" for i in deadlocked])}'
                else:
                    deadlock_label.text = 'No deadlock detected'
            
            ui.button('Detect Deadlock', on_click=detect_deadlock)
            
            recovery_select = ui.select(
                options=[f'P{i}' for i in range(simulator.num_processes)],
                value='P0'
            )
            
            def terminate_process():
                if recovery_select.value:
                    pid = int(recovery_select.value[1:])
                    simulator.recover_by_termination(pid)
                    refresh_ui()
                    ui.notify(f'Process {recovery_select.value} terminated')
            
            ui.button('Terminate Process', on_click=terminate_process).props('color=red')
    
    # Right panel - Matrices
    with ui.column().classes('w-2/3 p-4 h-full'):
        ui.label('📈 System Matrices').classes('text-xl font-bold mb-4')
        
        # Create tabs for different matrices
        tabs = ui.tabs().classes('w-full')
        with tabs:
            ui.tab('Allocated')
            ui.tab('Max Need')
            ui.tab('Need')
            ui.tab('Available')
            ui.tab('History')
        
        tab_panels = ui.tab_panels(tabs, value='Allocated').classes('w-full')
        
        # Allocated Matrix
        with tab_panels:
            with ui.tab_panel('Allocated'):
                allocated_grid = ui.aggrid({
                    'columnDefs': [{'headerName': 'Process', 'field': 'process'}] + 
                                 [{'headerName': f'R{i}', 'field': f'R{i}'} for i in range(simulator.num_resources)],
                    'rowData': []
                }).classes('h-64')
            
            # Max Need Matrix
            with ui.tab_panel('Max Need'):
                max_grid = ui.aggrid({
                    'columnDefs': [{'headerName': 'Process', 'field': 'process'}] + 
                                 [{'headerName': f'R{i}', 'field': f'R{i}'} for i in range(simulator.num_resources)],
                    'rowData': []
                }).classes('h-64')
            
            # Need Matrix
            with ui.tab_panel('Need'):
                need_grid = ui.aggrid({
                    'columnDefs': [{'headerName': 'Process', 'field': 'process'}] + 
                                 [{'headerName': f'R{i}', 'field': f'R{i}'} for i in range(simulator.num_resources)],
                    'rowData': []
                }).classes('h-64')
            
            # Available Resources
            with ui.tab_panel('Available'):
                available_grid = ui.aggrid({
                    'columnDefs': [
                        {'headerName': 'Resource', 'field': 'resource'},
                        {'headerName': 'Available', 'field': 'available'}
                    ],
                    'rowData': []
                }).classes('h-64')
            
            # History
            with ui.tab_panel('History'):
                history_area = ui.textarea(label='System Events').classes('h-64').props('readonly')
        
        # Visualization
        ui.label('📊 Process-Resource Graph').classes('text-xl font-bold mt-6 mb-4')
        
        with ui.card():
            graph_container = ui.column().classes('w-full items-center p-4')
            
            def update_graph():
                graph_container.clear()
                with graph_container:
                    # Processes
                    ui.label('Processes').classes('font-bold mb-2')
                    with ui.row().classes('mb-4'):
                        for i in range(simulator.num_processes):
                            deadlocked = simulator.detect_deadlock()
                            color = 'bg-red-500' if i in deadlocked else 'bg-green-500'
                            ui.label(f'P{i}').classes(f'{color} text-white rounded-full w-12 h-12 flex items-center justify-center mx-1')
                    
                    # Resources
                    ui.label('Resources').classes('font-bold mb-2')
                    with ui.row():
                        for i in range(simulator.num_resources):
                            ui.label(f'R{i}').classes('bg-blue-500 text-white rounded-lg w-12 h-12 flex items-center justify-center mx-1')
            
            update_graph()
        
        # Algorithm Explanation
        with ui.expansion('ℹ️ About Banker\'s Algorithm'):
            ui.markdown('''
            ### Banker's Algorithm for Deadlock Avoidance
            
            **Steps:**
            1. Calculate **Need = Max - Allocated**
            2. Check if **Need ≤ Available** for any process
            3. If yes, assume it completes and free its resources
            4. Repeat until all processes complete
            
            **Safe State:** All processes can complete in some order
            **Unsafe State:** Deadlock possible
            **Recovery:** Terminate processes or preempt resources
            ''')

# Function to refresh UI elements
def refresh_ui():
    # Update matrices
    allocated_data = []
    for i in range(simulator.num_processes):
        row = {'process': f'P{i}'}
        for j in range(simulator.num_resources):
            row[f'R{j}'] = simulator.allocated[i][j]
        allocated_data.append(row)
    allocated_grid.options['rowData'] = allocated_data
    
    max_data = []
    for i in range(simulator.num_processes):
        row = {'process': f'P{i}'}
        for j in range(simulator.num_resources):
            row[f'R{j}'] = simulator.max_need[i][j]
        max_data.append(row)
    max_grid.options['rowData'] = max_data
    
    need = simulator.calculate_need()
    need_data = []
    for i in range(simulator.num_processes):
        row = {'process': f'P{i}'}
        for j in range(simulator.num_resources):
            row[f'R{j}'] = need[i][j]
        need_data.append(row)
    need_grid.options['rowData'] = need_data
    
    available_data = [{'resource': f'R{i}', 'available': simulator.available[i]} 
                     for i in range(simulator.num_resources)]
    available_grid.options['rowData'] = available_data
    
    # Update history
    history_area.value = '\n'.join(simulator.history)
    
    # Update dropdowns
    process_select.options = [f'P{i}' for i in range(simulator.num_processes)]
    recovery_select.options = [f'P{i}' for i in range(simulator.num_processes)]
    
    # Update graph
    update_graph()
    
    # Check status
    check_status()

# Initial UI refresh
refresh_ui()

# Footer
with ui.footer().classes('bg-gray-800 text-white p-4'):
    ui.label('Deadlock Simulator | OS Project | Banker\'s Algorithm').classes('text-center w-full')

# Run the app
ui.run(title='Deadlock Simulator', port=8080, reload=False)