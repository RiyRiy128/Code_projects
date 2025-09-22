import boto3
import json
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QTextEdit, 
                             QLabel, QMessageBox, QSplitter, QDialog, QFormLayout, QLineEdit)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

class StepFunctionsWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    execution_result = pyqtSignal(dict)
    
    def __init__(self, action, **kwargs):
        super().__init__()
        self.action = action
        self.kwargs = kwargs
    
    def run(self):
        try:
            sf_client = boto3.client('stepfunctions')
            
            if self.action == 'list_state_machines':
                state_machines = []
                
                #Get all state machines with pagination
                paginator = sf_client.get_paginator('list_state_machines')
                page_iterator = paginator.paginate()
                
                for page in page_iterator:
                    for sm in page['stateMachines']:
                        state_machines.append({
                            'Name': sm['name'],
                            'Arn': sm['stateMachineArn'],
                            'Type': sm['type'],
                            # list_state_machines doesn't return status, assume ACTIVE
                            'Status': 'ACTIVE',
                            'CreationDate': sm['creationDate']
                        })
                self.finished.emit(state_machines)
                
            elif self.action == 'list_executions':
                sm_arn = self.kwargs['state_machine_arn']
                response = sf_client.list_executions(stateMachineArn=sm_arn, maxResults=20)
                executions = []
                for exec in response['executions']:
                    executions.append({
                        'Name': exec['name'],
                        'Arn': exec['executionArn'],
                        'Status': exec['status'],
                        'StartDate': exec['startDate'],
                        'StopDate': exec.get('stopDate', 'Running')
                    })
                self.finished.emit(executions)
                
            elif self.action == 'start_execution':
                sm_arn = self.kwargs['state_machine_arn']
                execution_name = self.kwargs['execution_name']
                input_data = self.kwargs.get('input', '{}')
                
                response = sf_client.start_execution(
                    stateMachineArn=sm_arn,
                    name=execution_name,
                    input=input_data
                )
                self.execution_result.emit({
                    'action': 'started',
                    'executionArn': response['executionArn'],
                    'startDate': response['startDate']
                })
                
            elif self.action == 'stop_execution':
                execution_arn = self.kwargs['execution_arn']
                response = sf_client.stop_execution(executionArn=execution_arn)
                self.execution_result.emit({
                    'action': 'stopped',
                    'stopDate': response['stopDate']
                })
                
            elif self.action == 'describe_execution':
                execution_arn = self.kwargs['execution_arn']
                response = sf_client.describe_execution(executionArn=execution_arn)
                self.execution_result.emit({
                    'action': 'described',
                    'execution': response
                })
                
        except Exception as e:
            self.error.emit(str(e))

class StartExecutionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start Execution")
        self.setModal(True)
        self.resize(500, 300)
        
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit()
        self.name_input.setText(f"execution-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        
        self.input_text = QTextEdit()
        self.input_text.setPlainText('{}')
        
        layout.addRow("Execution Name:", self.name_input)
        layout.addRow("Input JSON:", self.input_text)
        
        buttons = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.cancel_btn = QPushButton("Cancel")
        
        self.start_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addRow(buttons)

class StepFunctionsManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_state_machine_arn = None
        self.init_ui()
        self.load_state_machines()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.start_execution_btn = QPushButton("Start Execution")
        self.stop_execution_btn = QPushButton("Stop Execution")
        self.describe_execution_btn = QPushButton("Describe Execution")
        self.list_executions_btn = QPushButton("List Executions")
        
        self.refresh_btn.clicked.connect(self.load_state_machines)
        self.start_execution_btn.clicked.connect(self.start_execution)
        self.stop_execution_btn.clicked.connect(self.stop_execution)
        self.describe_execution_btn.clicked.connect(self.describe_execution)
        self.list_executions_btn.clicked.connect(self.list_executions)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.start_execution_btn)
        button_layout.addWidget(self.stop_execution_btn)
        button_layout.addWidget(self.describe_execution_btn)
        button_layout.addWidget(self.list_executions_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        #Create splitter for tables and output
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        #State machines table
        sm_widget = QWidget()
        sm_layout = QVBoxLayout(sm_widget)
        sm_layout.addWidget(QLabel("State Machines:"))
        
        self.sm_table = QTableWidget()
        self.sm_table.setColumnCount(5)
        self.sm_table.setHorizontalHeaderLabels([
            'Name', 'Type', 'Status', 'Creation Date', 'ARN'
        ])
        self.sm_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        sm_layout.addWidget(self.sm_table)
        
        splitter.addWidget(sm_widget)
        
        #Executions table
        exec_widget = QWidget()
        exec_layout = QVBoxLayout(exec_widget)
        exec_layout.addWidget(QLabel("Executions:"))
        
        self.exec_table = QTableWidget()
        self.exec_table.setColumnCount(5)
        self.exec_table.setHorizontalHeaderLabels([
            'Name', 'Status', 'Start Date', 'Stop Date', 'ARN'
        ])
        self.exec_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        exec_layout.addWidget(self.exec_table)
        
        splitter.addWidget(exec_widget)
        
        #Output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setMaximumHeight(200)
        splitter.addWidget(self.output_display)
        
        splitter.setSizes([300, 300, 200])
        layout.addWidget(splitter)
    
    #Helpers to call to certain functionality of the step function Qthread loop
    def load_state_machines(self):
        self.parent.update_status("Loading Step Functions state machines...")
        self.worker = StepFunctionsWorker('list_state_machines')
        self.worker.finished.connect(self.update_sm_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def update_sm_table(self, state_machines):
        self.sm_table.setRowCount(len(state_machines))
        
        for row, sm in enumerate(state_machines):
            self.sm_table.setItem(row, 0, QTableWidgetItem(sm['Name']))
            self.sm_table.setItem(row, 1, QTableWidgetItem(sm['Type']))
            self.sm_table.setItem(row, 2, QTableWidgetItem(sm['Status']))
            self.sm_table.setItem(row, 3, QTableWidgetItem(str(sm['CreationDate'])))
            self.sm_table.setItem(row, 4, QTableWidgetItem(sm['Arn']))
        
        self.parent.update_status(f"Loaded {len(state_machines)} state machines")
    
    def get_selected_state_machine(self):
        current_row = self.sm_table.currentRow()
        if current_row >= 0:
            return {
                'name': self.sm_table.item(current_row, 0).text(),
                'arn': self.sm_table.item(current_row, 4).text()
            }
        return None
    
    def get_selected_execution(self):
        current_row = self.exec_table.currentRow()
        if current_row >= 0:
            return {
                'name': self.exec_table.item(current_row, 0).text(),
                'arn': self.exec_table.item(current_row, 4).text()
            }
        return None
    
    def list_executions(self):
        sm = self.get_selected_state_machine()
        if not sm:
            QMessageBox.warning(self, "No Selection", "Please select a state machine")
            return
        
        self.current_state_machine_arn = sm['arn']
        self.parent.update_status(f"Loading executions for {sm['name']}...")
        
        self.worker = StepFunctionsWorker('list_executions', state_machine_arn=sm['arn'])
        self.worker.finished.connect(self.update_exec_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def update_exec_table(self, executions):
        self.exec_table.setRowCount(len(executions))
        
        for row, exec in enumerate(executions):
            self.exec_table.setItem(row, 0, QTableWidgetItem(exec['Name']))
            self.exec_table.setItem(row, 1, QTableWidgetItem(exec['Status']))
            self.exec_table.setItem(row, 2, QTableWidgetItem(str(exec['StartDate'])))
            self.exec_table.setItem(row, 3, QTableWidgetItem(str(exec['StopDate'])))
            self.exec_table.setItem(row, 4, QTableWidgetItem(exec['Arn']))
        
        self.parent.update_status(f"Loaded {len(executions)} executions")
    
    def start_execution(self):
        sm = self.get_selected_state_machine()
        if not sm:
            QMessageBox.warning(self, "No Selection", "Please select a state machine")
            return
        
        dialog = StartExecutionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            execution_name = dialog.name_input.text().strip()
            input_data = dialog.input_text.toPlainText().strip()
            
            if not execution_name:
                QMessageBox.warning(self, "Invalid Input", "Please enter execution name")
                return
            
            try:
                json.loads(input_data)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Invalid JSON", "Please enter valid JSON input")
                return
            
            self.parent.update_status(f"Starting execution {execution_name}...")
            
            self.worker = StepFunctionsWorker('start_execution', 
                                            state_machine_arn=sm['arn'],
                                            execution_name=execution_name,
                                            input=input_data)
            self.worker.execution_result.connect(self.handle_execution_result)
            self.worker.error.connect(self.show_error)
            self.worker.start()
    
    def stop_execution(self):
        exec = self.get_selected_execution()
        if not exec:
            QMessageBox.warning(self, "No Selection", "Please select an execution")
            return
        
        reply = QMessageBox.question(self, "Confirm Stop", 
                                   f"Are you sure you want to stop execution {exec['name']}?")
        if reply == QMessageBox.StandardButton.Yes:
            self.parent.update_status(f"Stopping execution {exec['name']}...")
            
            self.worker = StepFunctionsWorker('stop_execution', execution_arn=exec['arn'])
            self.worker.execution_result.connect(self.handle_execution_result)
            self.worker.error.connect(self.show_error)
            self.worker.start()
    
    def describe_execution(self):
        exec = self.get_selected_execution()
        if not exec:
            QMessageBox.warning(self, "No Selection", "Please select an execution")
            return
        
        self.parent.update_status(f"Describing execution {exec['name']}...")
        
        self.worker = StepFunctionsWorker('describe_execution', execution_arn=exec['arn'])
        self.worker.execution_result.connect(self.handle_execution_result)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def handle_execution_result(self, result):
        if result['action'] == 'started':
            self.parent.update_status("Execution started successfully")
            self.output_display.setPlainText(f"Started execution: {result['executionArn']}")
            if self.current_state_machine_arn:
                self.list_executions()
        elif result['action'] == 'stopped':
            self.parent.update_status("Execution stopped successfully")
            self.output_display.setPlainText(f"Stopped execution at: {result['stopDate']}")
            if self.current_state_machine_arn:
                self.list_executions()
        elif result['action'] == 'described':
            self.parent.update_status("Execution details retrieved")
            self.output_display.setPlainText(json.dumps(result['execution'], indent=2, default=str))
    
    def show_error(self, error_message):
        self.parent.update_status("Error occurred")
        QMessageBox.critical(self, "Error", f"AWS Error: {error_message}")
        self.output_display.setPlainText(f"Error: {error_message}")