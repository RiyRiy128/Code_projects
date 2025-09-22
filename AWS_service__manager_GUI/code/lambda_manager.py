import boto3
import json
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QTextEdit, 
                             QLabel, QMessageBox, QSplitter, QComboBox, QGroupBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

class LambdaWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    log_result = pyqtSignal(str)
    account_settings = pyqtSignal(dict)
    
    def __init__(self, action, **kwargs):
        super().__init__()
        self.action = action
        self.kwargs = kwargs
    

    #Logs functionality omitted here as mentioned below
    def run(self):
        try:
            lambda_client = boto3.client('lambda')
            cloudwatch = boto3.client('cloudwatch')
            
            if self.action == 'list_functions':
                functions = []
                
                #Get all functions with pagination
                paginator = lambda_client.get_paginator('list_functions')
                page_iterator = paginator.paginate()
                
                #Get metrics for all functions
                end_time = datetime.utcnow()
                start_time = end_time - timedelta(minutes=5)
                
                for page in page_iterator:
                    for func in page['Functions']:
                        function_name = func['FunctionName']
                        
                        #Get concurrent executions
                        try:
                            concurrent_response = cloudwatch.get_metric_statistics(
                                Namespace='AWS/Lambda',
                                MetricName='ConcurrentExecutions',
                                Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                                StartTime=start_time,
                                EndTime=end_time,
                                Period=300,
                                Statistics=['Maximum']
                            )
                            concurrent_executions = max([dp['Maximum'] for dp in concurrent_response['Datapoints']], default=0)
                        except:
                            concurrent_executions = 0
                        
                        #Get invocations in last 5 minutes
                        try:
                            invocation_response = cloudwatch.get_metric_statistics(
                                Namespace='AWS/Lambda',
                                MetricName='Invocations',
                                Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                                StartTime=start_time,
                                EndTime=end_time,
                                Period=300,
                                Statistics=['Sum']
                            )
                            invocations = sum([dp['Sum'] for dp in invocation_response['Datapoints']])
                        except:
                            invocations = 0
                        
                        functions.append({
                            'FunctionName': function_name,
                            'Runtime': func.get('Runtime', 'Container'),
                            'Handler': func.get('Handler', 'N/A'),
                            'CodeSize': self.format_size(func['CodeSize']),
                            'LastModified': func['LastModified'],
                            'ConcurrentExecutions': int(concurrent_executions),
                            'Invocations5Min': int(invocations)
                        })
                
                self.finished.emit(functions)
                
            elif self.action == 'get_account_settings':
                try:
                    settings = lambda_client.get_account_settings()
                    self.account_settings.emit(settings['AccountLimit'])
                except Exception as e:
                    self.account_settings.emit({'Error': str(e)})
            elif self.action == 'invoke_function':
                function_name = self.kwargs['function_name']
                payload = self.kwargs.get('payload', '{}')
                
                response = lambda_client.invoke(
                    FunctionName=function_name,
                    Payload=payload
                )
                
                result = {
                    'StatusCode': response['StatusCode'],
                    'Payload': response['Payload'].read().decode('utf-8'),
                    'LogResult': response.get('LogResult', '')
                }
                
                self.log_result.emit(json.dumps(result, indent=2))
                self.finished.emit([])
                
            elif self.action == 'get_function':
                function_name = self.kwargs['function_name']
                response = lambda_client.get_function(FunctionName=function_name)
                
                function_info = {
                    'Configuration': response['Configuration'],
                    'Code': response['Code']
                }
                
                self.log_result.emit(json.dumps(function_info, indent=2, default=str))
                self.finished.emit([])
                
        except Exception as e:
            self.error.emit(str(e))
    
    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"

class LambdaManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_functions()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        #Account settings group
        settings_group = QGroupBox("Account Settings")
        settings_layout = QHBoxLayout(settings_group)
        self.settings_label = QLabel("Loading account settings...")
        settings_layout.addWidget(self.settings_label)
        layout.addWidget(settings_group)
        
        #Control buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.invoke_btn = QPushButton("Invoke Function")
        self.get_info_btn = QPushButton("Get Function Info")
        self.view_logs_btn = QPushButton("View Logs")
        
        self.refresh_btn.clicked.connect(self.load_functions)
        self.invoke_btn.clicked.connect(self.invoke_function)
        self.get_info_btn.clicked.connect(self.get_function_info)
        self.view_logs_btn.clicked.connect(self.view_logs)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.invoke_btn)
        button_layout.addWidget(self.get_info_btn)
        button_layout.addWidget(self.view_logs_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        #Create splitter for table and output
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        #Function table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'Function Name', 'Runtime', 'Handler', 'Code Size', 'Last Modified', 'Active Concurrency', 'Invocations (5min)'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        splitter.addWidget(self.table)
        
        #Output area
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        #Payload input for invocation
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(QLabel("Payload:"))
        self.payload_input = QTextEdit()
        self.payload_input.setMaximumHeight(100)
        self.payload_input.setPlainText('{"key": "value"}')
        payload_layout.addWidget(self.payload_input)
        
        output_layout.addLayout(payload_layout)
        
        #Output display
        output_layout.addWidget(QLabel("Output:"))
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        output_layout.addWidget(self.output_display)
        
        splitter.addWidget(output_widget)
        splitter.setSizes([400, 300])
        
        layout.addWidget(splitter)
    
    #load functions on thread
    def load_functions(self):
        self.parent.update_status("Loading Lambda functions...")
        self.worker = LambdaWorker('list_functions')
        self.worker.finished.connect(self.update_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
        
        #Load account settings on thread
        self.settings_worker = LambdaWorker('get_account_settings')
        self.settings_worker.account_settings.connect(self.update_account_settings)
        self.settings_worker.start()
    
    #Populate results
    def update_table(self, functions):
        self.table.setRowCount(len(functions))
        
        for row, func in enumerate(functions):
            self.table.setItem(row, 0, QTableWidgetItem(func['FunctionName']))
            self.table.setItem(row, 1, QTableWidgetItem(func['Runtime']))
            self.table.setItem(row, 2, QTableWidgetItem(func['Handler']))
            self.table.setItem(row, 3, QTableWidgetItem(func['CodeSize']))
            self.table.setItem(row, 4, QTableWidgetItem(str(func['LastModified'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(func['ConcurrentExecutions'])))
            self.table.setItem(row, 6, QTableWidgetItem(str(func['Invocations5Min'])))
        
        self.parent.update_status(f"Loaded {len(functions)} Lambda functions")
    
    #Call to populate Lambda account settings
    def update_account_settings(self, settings):
        if 'Error' in settings:
            self.settings_label.setText(f"Error loading settings: {settings['Error']}")
        else:
            concurrent_limit = settings.get('ConcurrentExecutions', 'N/A')
            code_size_limit = settings.get('TotalCodeSize', 'N/A')
            unreserved_concurrent = settings.get('UnreservedConcurrentExecutions', 'N/A')
            self.settings_label.setText(
                f"Concurrent Executions: {concurrent_limit} | "
                f"Total Code Size: {code_size_limit} bytes | "
                f"Unreserved Concurrent: {unreserved_concurrent}"
            )
    

    def get_selected_function(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            return self.table.item(current_row, 0).text()
        return None
    
    #Call invoke function on thread 
    def invoke_function(self):
        function_name = self.get_selected_function()
        if not function_name:
            QMessageBox.warning(self, "No Selection", "Please select a function")
            return
        
        payload = self.payload_input.toPlainText()
        
        #Validate JSON payload
        try:
            json.loads(payload)
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Invalid JSON", "Please enter valid JSON payload")
            return
        
        self.parent.update_status(f"Invoking function {function_name}...")
        self.output_display.clear()
        
        self.worker = LambdaWorker('invoke_function', 
                                 function_name=function_name, 
                                 payload=payload)
        self.worker.finished.connect(lambda: self.parent.update_status("Function invoked successfully"))
        self.worker.log_result.connect(self.display_output)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    #Fetch function details on thread
    def get_function_info(self):
        function_name = self.get_selected_function()
        if not function_name:
            QMessageBox.warning(self, "No Selection", "Please select a function")
            return
        
        self.parent.update_status(f"Getting info for {function_name}...")
        self.output_display.clear()
        
        self.worker = LambdaWorker('get_function', function_name=function_name)
        self.worker.finished.connect(lambda: self.parent.update_status("Function info retrieved"))
        self.worker.log_result.connect(self.display_output)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    

    #Logs place holder call. Since load times can be vast as is with loading functions, omitting logs for simplicity and overload
    def view_logs(self):
        function_name = self.get_selected_function()
        if not function_name:
            QMessageBox.warning(self, "No Selection", "Please select a function")
            return
        
        # Placeholder for CloudWatch logs integration
        QMessageBox.information(self, "View Logs", 
                              f"CloudWatch logs integration for {function_name} would be implemented here, but for simplicity and load times I am omitting it")
    
    def display_output(self, output):
        self.output_display.setPlainText(output)
    
    def show_error(self, error_message):
        self.parent.update_status("Error occurred")
        QMessageBox.critical(self, "Error", f"AWS Error: {error_message}")
        self.output_display.setPlainText(f"Error: {error_message}")