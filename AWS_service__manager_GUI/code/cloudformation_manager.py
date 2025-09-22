import boto3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

class CloudFormationWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, action, **kwargs):
        super().__init__()
        self.action = action
        self.kwargs = kwargs
    
    def run(self):
        try:
            cf = boto3.client('cloudformation')
            
            if self.action == 'list_stacks':
                response = cf.list_stacks(
                    StackStatusFilter=[
                        'CREATE_COMPLETE', 'UPDATE_COMPLETE', 'DELETE_FAILED',
                        'CREATE_FAILED', 'UPDATE_FAILED', 'ROLLBACK_COMPLETE'
                    ]
                )
                stacks = []
                for stack in response['StackSummaries']:
                    stacks.append({
                        'StackName': stack['StackName'],
                        'StackStatus': stack['StackStatus'],
                        'CreationTime': stack['CreationTime'].strftime('%Y-%m-%d %H:%M:%S')
                    })
                self.finished.emit(stacks)
                
        except Exception as e:
            self.error.emit(str(e))

class CloudFormationManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_stacks()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh Stacks")
        self.create_btn = QPushButton("Create Stack")
        self.update_btn = QPushButton("Update Stack")
        self.delete_btn = QPushButton("Delete Stack")
        
        self.refresh_btn.clicked.connect(self.load_stacks)

        #For the above listed buttons, placeholder output returned as this functionality is not added for simplicity and overload
        self.create_btn.clicked.connect(self.show_placeholder)
        self.update_btn.clicked.connect(self.show_placeholder)
        self.delete_btn.clicked.connect(self.show_placeholder)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Stack table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Stack Name', 'Status', 'Created'])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
    
    def load_stacks(self):
        self.parent.update_status("Loading CloudFormation stacks...")
        self.worker = CloudFormationWorker('list_stacks')
        self.worker.finished.connect(self.update_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    #Populate results of stacks
    def update_table(self, stacks):
        self.table.setRowCount(len(stacks))
        
        for row, stack in enumerate(stacks):
            self.table.setItem(row, 0, QTableWidgetItem(stack['StackName']))
            self.table.setItem(row, 1, QTableWidgetItem(stack['StackStatus']))
            self.table.setItem(row, 2, QTableWidgetItem(stack['CreationTime']))
        
        self.parent.update_status(f"Loaded {len(stacks)} CloudFormation stacks")
    
    
    #Return dummy response for placeholder functions 
    def show_placeholder(self):
        QMessageBox.information(self, "Feature", "CloudFormation management features would be implemented here")
    
    def show_error(self, error_message):
        self.parent.update_status("Error occurred")
        QMessageBox.critical(self, "Error", f"AWS Error: {error_message}")