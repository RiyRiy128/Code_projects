import boto3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

class IAMWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, action, **kwargs):
        super().__init__()
        self.action = action
        self.kwargs = kwargs
    

    #List users and roles, policies functionality omitted
    def run(self):
        try:
            iam = boto3.client('iam')
            
            if self.action == 'list_users':
                response = iam.list_users()
                users = []
                for user in response['Users']:
                    users.append({
                        'UserName': user['UserName'],
                        'CreateDate': user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S'),
                        'Arn': user['Arn']
                    })
                self.finished.emit(users)
                
            elif self.action == 'list_roles':
                response = iam.list_roles()
                roles = []
                for role in response['Roles']:
                    roles.append({
                        'RoleName': role['RoleName'],
                        'CreateDate': role['CreateDate'].strftime('%Y-%m-%d %H:%M:%S'),
                        'Arn': role['Arn']
                    })
                self.finished.emit(roles)
                
        except Exception as e:
            self.error.emit(str(e))

class IAMManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.users_btn = QPushButton("List Users")
        self.roles_btn = QPushButton("List Roles")
        self.policies_btn = QPushButton("List Policies")
        
        self.users_btn.clicked.connect(self.load_users)
        self.roles_btn.clicked.connect(self.load_roles)

        #Placeholder for policies, to be possibly implemented, since policies are broad and numerous, not included for simplicity and overload
        self.policies_btn = QPushButton("List Policies")
        self.policies_btn.clicked.connect(self.show_placeholder)
        
        button_layout.addWidget(self.users_btn)
        button_layout.addWidget(self.roles_btn)
        button_layout.addWidget(self.policies_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Name', 'Created', 'ARN'])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
    
    #Fetch users in thread
    def load_users(self):
        self.parent.update_status("Loading IAM users...")
        self.worker = IAMWorker('list_users')
        self.worker.finished.connect(self.update_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    #Fetch roles in thread
    def load_roles(self):
        self.parent.update_status("Loading IAM roles...")
        self.worker = IAMWorker('list_roles')
        self.worker.finished.connect(self.update_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def update_table(self, items):
        self.table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            name_key = 'UserName' if 'UserName' in item else 'RoleName'
            self.table.setItem(row, 0, QTableWidgetItem(item[name_key]))
            self.table.setItem(row, 1, QTableWidgetItem(item['CreateDate']))
            self.table.setItem(row, 2, QTableWidgetItem(item['Arn']))
        
        self.parent.update_status(f"Loaded {len(items)} IAM items")
    
    #Dummy return for yet to be implemented feature such as policies listing
    def show_placeholder(self):
        QMessageBox.information(self, "Feature", "Additional IAM features would be implemented here")
    
    def show_error(self, error_message):
        self.parent.update_status("Error occurred")
        QMessageBox.critical(self, "Error", f"AWS Error: {error_message}")