"""
Deadlock Avoidance and Recovery Simulator
A GUI-based educational tool using NiceGUI
"""

import numpy as np
from nicegui import ui
import time
from typing import List, Dict, Tuple, Optional

class DeadlockSimulator:
    def __init__(self):
        self.processes = []
        self.resources = []
        self.allocated = []
        self.max_need = []
        self.available = []
        self.request = []
        self.safe_sequence = []
        self.history = []
        # Add these attributes to fix the binding error
        self.num_processes = 3
        self.num_resources = 3
        
    def initialize_system(self, num_processes: int = None, num_resources: int = None):
        """Initialize the system with given number of processes and resources"""
        if num_processes is not None:
            self.num_processes = num_processes
        if num_resources is not None:
            self.num_resources = num_resources
            
        self.processes = [f"P{i}" for i in range(self.num_processes)]
        self.resources = [f"R{i}" for i in range(self.num_resources)]
        
        # Initialize matrices with zeros
        self.allocated = [[0 for _ in range(self.num_resources)] for _ in range(self.num_processes)]
        self.max_need = [[0 for _ in range(self.num_resources)] for _ in range(self.num_processes)]
        self.request = [[0 for _ in range(self.num_resources)] for _ in range(self.num_processes)]
        self.available = [0 for _ in range(self.num_resources)]
        
        # Set some initial values for demonstration
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                self.allocated[i][j] = np.random.randint(0, 3)
                self.max_need[i][j] = self.allocated[i][j] + np.random.randint(0, 3)
        
        # Initialize available resources
        for j in range(self.num_resources):
            total_allocated = sum(self.allocated[i][j] for i in range(self.num_processes))
            self.available[j] = total_allocated + np.random.randint(1, 5)
        
        self.safe_sequence = []
        self.history.append(f"System initialized with {self.num_processes} processes and {self.num_resources} resources")
    
    def calculate_need(self) -> List[List[int]]:
        """Calculate the need matrix (max - allocated)"""
        need = []
        for i in range(len(self.processes)):
            row = []
            for j in range(len(self.resources)):
                row.append(self.max_need[i][j] - self.allocated[i][j])
            need.append(row)
        return need
    
    def bankers_algorithm(self) -> Tuple[bool, List[str]]:
        """Banker's algorithm for deadlock avoidance"""
        need = self.calculate_need()
        work = self.available.copy()
        finish = [False] * len(self.processes)
        
        safe_sequence = []
        count = 0
        
        while count < len(self.processes):
            found = False
            for i in range(len(self.processes)):
                if not finish[i]:
                    # Check if need[i] <= work
                    if all(need[i][j] <= work[j] for j in range(len(self.resources))):
                        # Process can complete
                        for j in range(len(self.resources)):
                            work[j] += self.allocated[i][j]
                        finish[i] = True
                        safe_sequence.append(self.processes[i])
                        found = True
                        count += 1
            
            if not found:
                break
        
        is_safe = all(finish)
        return is_safe, safe_sequence
    
    def is_deadlock(self) -> bool:
        """Check if the system is in deadlock"""
        is_safe, _ = self.bankers_algorithm()
        return not is_safe
    
    def recovery_preemptive(self, process_index: int) -> bool:
        """Recover from deadlock using process termination"""
        if process_index < 0 or process_index >= len(self.processes):
            return False
        
        # Free resources of terminated process
        for j in range(len(self.resources)):
            self.available[j] += self.allocated[process_index][j]
            self.allocated[process_index][j] = 0
            self.max_need[process_index][j] = 0
        
        self.history.append(f"Process {self.processes[process_index]} terminated for recovery")
        return True
    
    def detect_deadlock(self) -> List[int]:
        """Detect deadlock using resource allocation graph algorithm"""
        # Simplified detection for display purposes
        need = self.calculate_need()
        work = self.available.copy()
        finish = [False] * len(self.processes)
        
        # Mark processes that can finish
        for i in range(len(self.processes)):
            if all(need[i][j] == 0 for j in range(len(self.resources))):
                finish[i] = True
        
        # Try to find processes that can finish
        changed = True
        while changed:
            changed = False
            for i in range(len(self.processes)):
                if not finish[i]:
                    if all(need[i][j] <= work[j] for j in range(len(self.resources))):
                        for j in range(len(self.resources)):
                            work[j] += self.allocated[i][j]
                        finish[i] = True
                        changed = True
        
        # Processes that cannot finish are in deadlock
        deadlocked = []
        for i in range(len(self.processes)):
            if not finish[i]:
                deadlocked.append(i)
        
        return deadlocked
    
    def request_resources(self, process_index: int, request_vector: List[int]) -> bool:
        """Process requests resources"""
        if process_index < 0 or process_index >= len(self.processes):
            return False
            
        need = self.calculate_need()
        
        # Check if request <= need
        if not all(request_vector[j] <= need[process_index][j] for j in range(len(self.resources))):
            self.history.append(f"Error: Process {self.processes[process_index]} requested more than its maximum claim")
            return False
        
        # Check if request <= available
        if not all(request_vector[j] <= self.available[j] for j in range(len(self.resources))):
            self.history.append(f"Process {self.processes[process_index]} must wait (insufficient resources)")
            return False
        
        # Try to allocate resources temporarily
        temp_available = self.available.copy()
        temp_allocated = [row.copy() for row in self.allocated]
        
        for j in range(len(self.resources)):
            temp_available[j] -= request_vector[j]
            temp_allocated[process_index][j] += request_vector[j]
        
        # Save current state and apply temporary changes
        original_available = self.available.copy()
        original_allocated = [row.copy() for row in self.allocated]
        
        self.available = temp_available
        self.allocated = temp_allocated
        
        # Check if the new state is safe
        is_safe, _ = self.bankers_algorithm()
        
        # Restore original state
        self.available = original_available
        self.allocated = original_allocated
        
        if is_safe:
            # Actually allocate the resources
            for j in range(len(self.resources)):
                self.available[j] -= request_vector[j]
                self.allocated[process_index][j] += request_vector[j]
            
            self.history.append(f"Resources allocated to Process {self.processes[process_index]}")
            return True
        else:
            self.history.append(f"Request denied: Allocation would lead to unsafe state")
            return False

# Create the simulator instance
simulator = DeadlockSimulator()

# Initialize with default values
simulator.initialize_system()

# Create the UI
ui.colors(primary='#3B82F6', secondary='#10B981', accent='#8B5CF6')
ui.page_title("Deadlock Simulator")

with ui.header(elevated=True).style('background-color: #3B82F6').classes('items-center justify-between'):
    ui.label('🔒 Deadlock Avoidance & Recovery Simulator').style('font-size: 1.5rem; font-weight: bold; color: white')
    
    with ui.row():
        ui.button('Reset System', on_click=lambda: simulator.initialize_system()).props('flat color=white')
        ui.button('Help', on_click=lambda: ui.notify('This simulator demonstrates deadlock avoidance using Banker\'s Algorithm and recovery techniques')).props('flat color=white')

# Main content
with ui.row().classes('w-full'):
    # Left panel - Controls and Information
    with ui.column().classes('w-1/3 p-4'):
        ui.label('⚙️ System Configuration').style('font-size: 1.2rem; font-weight: bold')
        
        with ui.card().tight():
            with ui.card_section():
                ui.label('Setup Parameters')
                
                with ui.row().classes('items-center'):
                    ui.label('Processes:')
                    process_slider = ui.slider(min=2, max=5, value=3)
                    process_value = ui.label('3')
                    
                with ui.row().classes('items-center'):
                    ui.label('Resources:')
                    resource_slider = ui.slider(min=2, max=5, value=3)
                    resource_value = ui.label('3')
                
                def update_slider_values():
                    process_value.set_text(str(int(process_slider.value)))
                    resource_value.set_text(str(int(resource_slider.value)))
                
                process_slider.on('update:model-value', update_slider_values)
                resource_slider.on('update:model-value', update_slider_values)
                
                def apply_config():
                    simulator.initialize_system(int(process_slider.value), int(resource_slider.value))
                    refresh_display()
                    ui.notify(f'System reconfigured with {process_slider.value} processes and {resource_slider.value} resources')
                
                ui.button('Apply Configuration', on_click=apply_config).props('flat')
        
        with ui.card().tight():
            with ui.card_section():
                ui.label('📊 System Status')
                
                status_label = ui.label('Checking...')
                sequence_label = ui.label('')
                
                def update_status():
                    is_safe, sequence = simulator.bankers_algorithm()
                    if is_safe:
                        status_label.set_text('✅ System is in SAFE state')
                        sequence_label.set_text(f'Safe sequence: {", ".join(sequence)}')
                    else:
                        status_label.set_text('❌ System is in UNSAFE state (Deadlock possible)')
                        sequence_label.set_text('No safe sequence exists')
                
                ui.button('Check System State', on_click=update_status)
        
        with ui.card().tight():
            with ui.card_section():
                ui.label('🔄 Request Resources')
                
                process_select = ui.select(
                    options=[f'P{i}' for i in range(len(simulator.processes))],
                    label='Select Process'
                ).classes('w-full')
                
                request_inputs = []
                with ui.column().classes('w-full'):
                    for i, res in enumerate(simulator.resources):
                        with ui.row().classes('items-center justify-between w-full'):
                            ui.label(f'{res}:')
                            request_inputs.append(ui.number(value=0, min=0, max=5).classes('w-20'))
                
                def make_request():
                    if not process_select.value:
                        ui.notify('Please select a process first!', type='warning')
                        return
                        
                    process_idx = int(process_select.value[1:])
                    request_vector = [inp.value for inp in request_inputs]
                    success = simulator.request_resources(process_idx, request_vector)
                    
                    if success:
                        ui.notify('Request granted!', type='positive')
                    else:
                        ui.notify('Request denied!', type='warning')
                    
                    update_status()
                    refresh_display()
                
                ui.button('Submit Request', on_click=make_request)
        
        with ui.card().tight():
            with ui.card_section():
                ui.label('🛠️ Recovery Actions')
                
                deadlocked_list = ui.label('Click "Detect Deadlock" to check')
                
                def detect_and_display():
                    deadlocked = simulator.detect_deadlock()
                    if deadlocked:
                        deadlocked_list.set_text(f'Deadlocked processes: {", ".join([simulator.processes[i] for i in deadlocked])}')
                    else:
                        deadlocked_list.set_text('No deadlock detected')
                
                ui.button('Detect Deadlock', on_click=detect_and_display)
                
                recovery_select = ui.select(
                    options=[f'P{i}' for i in range(len(simulator.processes))],
                    label='Select Process to Terminate'
                ).classes('w-full')
                
                def recover_deadlock():
                    if not recovery_select.value:
                        ui.notify('Please select a process first!', type='warning')
                        return
                        
                    process_idx = int(recovery_select.value[1:])
                    success = simulator.recovery_preemptive(process_idx)
                    
                    if success:
                        ui.notify(f'Process {simulator.processes[process_idx]} terminated for recovery', type='info')
                        detect_and_display()
                        update_status()
                        refresh_display()
                
                ui.button('Terminate Process (Recovery)', on_click=recover_deadlock).props('color=red')
    
    # Right panel - Matrices and History
    with ui.column().classes('w-2/3 p-4'):
        ui.label('📈 System Matrices').style('font-size: 1.2rem; font-weight: bold')
        
        matrices_tabs = ui.tabs([
            'Allocated Matrix', 
            'Max Need Matrix', 
            'Need Matrix', 
            'Available Resources',
            'System History'
        ]).classes('w-full')
        
        with ui.tab_panels(matrices_tabs, value='Allocated Matrix').classes('w-full'):
            # Allocated Matrix
            with ui.tab_panel('Allocated Matrix'):
                allocated_table = ui.table({
                    'columnDefs': [{'headerName': 'Process', 'field': 'process'}] + 
                                 [{'headerName': res, 'field': res} for res in simulator.resources],
                    'rowData': []
                }).classes('w-full h-64')
            
            # Max Need Matrix
            with ui.tab_panel('Max Need Matrix'):
                max_table = ui.table({
                    'columnDefs': [{'headerName': 'Process', 'field': 'process'}] + 
                                 [{'headerName': res, 'field': res} for res in simulator.resources],
                    'rowData': []
                }).classes('w-full h-64')
            
            # Need Matrix
            with ui.tab_panel('Need Matrix'):
                need_table = ui.table({
                    'columnDefs': [{'headerName': 'Process', 'field': 'process'}] + 
                                 [{'headerName': res, 'field': res} for res in simulator.resources],
                    'rowData': []
                }).classes('w-full h-64')
            
            # Available Resources
            with ui.tab_panel('Available Resources'):
                available_table = ui.table({
                    'columnDefs': [{'headerName': 'Resource', 'field': 'resource'},
                                 {'headerName': 'Available', 'field': 'available'}],
                    'rowData': []
                }).classes('w-full h-64')
            
            # System History
            with ui.tab_panel('System History'):
                history_text = ui.textarea(label='System Events', value='').classes('w-full h-64').props('readonly')
                
                def clear_history():
                    simulator.history = ['History cleared']
                    history_text.value = '\n'.join(simulator.history)
                
                ui.button('Clear History', on_click=clear_history)
        
        # Algorithm Explanation
        with ui.expansion('ℹ️ Algorithm Explanation', icon='info').classes('w-full mt-4'):
            ui.markdown('''
            ## Banker's Algorithm for Deadlock Avoidance
            
            **Steps:**
            1. **Need Calculation**: Need = Max - Allocated
            2. **Safety Check**: 
               - Find a process whose Need ≤ Available
               - Add its allocated resources to Available
               - Mark it as finished
               - Repeat until all processes are finished
            
            **Recovery Methods:**
            - **Process Termination**: Kill one or more processes
            - **Resource Preemption**: Take resources from processes
            
            **Key Concepts:**
            - **Safe State**: Exists at least one safe sequence
            - **Unsafe State**: May lead to deadlock
            - **Deadlock**: Circular waiting for resources
            ''').classes('p-4')
        
        # Visualization
        with ui.card().tight().classes('w-full mt-4'):
            with ui.card_section():
                ui.label('📊 Resource Allocation Graph')
                
                # Simple visualization
                graph_container = ui.column().classes('w-full items-center')
                
                def update_graph():
                    graph_container.clear()
                    with graph_container:
                        with ui.row().classes('justify-center items-center w-full'):
                            with ui.column().classes('items-center'):
                                ui.label('Processes').style('font-weight: bold')
                                for i, p in enumerate(simulator.processes):
                                    deadlocked = simulator.detect_deadlock()
                                    color = "#EF4444" if i in deadlocked else "#10B981"
                                    ui.label(p).style(f'background-color: {color}; color: white; padding: 8px; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin: 5px')
                            
                            ui.label('⇄').style('font-size: 2rem; margin: 0 20px')
                            
                            with ui.column().classes('items-center'):
                                ui.label('Resources').style('font-weight: bold')
                                for i, r in enumerate(simulator.resources):
                                    ui.label(r).style('background-color: #3B82F6; color: white; padding: 8px; border-radius: 4px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin: 5px')

# Function to refresh all displays
def refresh_display():
    # Update allocated matrix
    allocated_data = []
    for i, process in enumerate(simulator.processes):
        row = {'process': process}
        for j, res in enumerate(simulator.resources):
            row[res] = simulator.allocated[i][j]
        allocated_data.append(row)
    allocated_table.options['rowData'] = allocated_data
    allocated_table.update()
    
    # Update max need matrix
    max_data = []
    for i, process in enumerate(simulator.processes):
        row = {'process': process}
        for j, res in enumerate(simulator.resources):
            row[res] = simulator.max_need[i][j]
        max_data.append(row)
    max_table.options['rowData'] = max_data
    max_table.update()
    
    # Update need matrix
    need = simulator.calculate_need()
    need_data = []
    for i, process in enumerate(simulator.processes):
        row = {'process': process}
        for j, res in enumerate(simulator.resources):
            row[res] = need[i][j]
        need_data.append(row)
    need_table.options['rowData'] = need_data
    need_table.update()
    
    # Update available resources
    available_data = []
    for i, res in enumerate(simulator.resources):
        available_data.append({'resource': res, 'available': simulator.available[i]})
    available_table.options['rowData'] = available_data
    available_table.update()
    
    # Update history
    history_text.value = '\n'.join(simulator.history)
    
    # Update dropdown options
    process_select.options = [f'P{i}' for i in range(len(simulator.processes))]
    recovery_select.options = [f'P{i}' for i in range(len(simulator.processes))]
    
    # Update request inputs
    # Clear and recreate request inputs
    # (This part is handled by the refresh function)
    
    # Update status
    update_status()
    detect_and_display()
    update_graph()

# Initialize displays
refresh_display()

# Footer
with ui.footer().style('background-color: #F3F4F6'):
    with ui.row().classes('w-full justify-center'):
        ui.label('Deadlock Simulator | Created with NiceGUI | OS Project').style('color: #6B7280')

# Start the application
ui.run(title='Deadlock Simulator', dark=False, reload=False, port=8080)