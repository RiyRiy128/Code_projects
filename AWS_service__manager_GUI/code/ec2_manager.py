import boto3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QComboBox, 
                             QLineEdit, QLabel, QMessageBox, QDialog, QFormLayout)
from PyQt6.QtCore import QThread, pyqtSignal
import json


#EC2 client ran on the QT
class EC2Worker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, action, **kwargs):
        super().__init__()
        self.action = action
        self.kwargs = kwargs
    
    def run(self):
        try:
            ec2 = boto3.client('ec2')
            
            if self.action == 'list_instances':
                response = ec2.describe_instances()
                instances = []
                for reservation in response['Reservations']:
                    for instance in reservation['Instances']:
                        instances.append({
                            'InstanceId': instance['InstanceId'],
                            'State': instance['State']['Name'],
                            'InstanceType': instance['InstanceType'],
                            'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                            'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A')
                        })
                self.finished.emit(instances)
                
            elif self.action == 'start_instance':
                ec2.start_instances(InstanceIds=[self.kwargs['instance_id']])
                self.finished.emit([])
                
            elif self.action == 'stop_instance':
                ec2.stop_instances(InstanceIds=[self.kwargs['instance_id']])
                self.finished.emit([])
                
            elif self.action == 'terminate_instance':
                ec2.terminate_instances(InstanceIds=[self.kwargs['instance_id']])
                self.finished.emit([])
                
        except Exception as e:
            self.error.emit(str(e))


#Launches an instance of an AMI
class LaunchInstanceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Launch EC2 Instance")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QFormLayout(self)
        

        #These are all dummy functions/inputs for selection to simulate possibly launching an instance from the service manager
        self.ami_input = QLineEdit("Some ami would be used here")
        self.instance_type = QComboBox()
        self.instance_type.addItems(['t2.micro', 't2.small', 't2.medium', 't3.micro', 't3.small'])
        self.key_name = QLineEdit()
        self.security_group = QLineEdit("default")
        
        layout.addRow("AMI:", self.ami_input)
        layout.addRow("Instance Type:", self.instance_type)
        layout.addRow("Key Pair Name:", self.key_name)
        layout.addRow("Security Group:", self.security_group)
        
        buttons = QHBoxLayout()
        self.launch_btn = QPushButton("Launch")
        self.cancel_btn = QPushButton("Cancel")
        
        self.launch_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(self.launch_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addRow(buttons)

class EC2Manager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_instances()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.launch_btn = QPushButton("Launch Instance")
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.terminate_btn = QPushButton("Terminate")
        
        self.refresh_btn.clicked.connect(self.load_instances)
        self.launch_btn.clicked.connect(self.launch_instance)
        self.start_btn.clicked.connect(self.start_instance)
        self.stop_btn.clicked.connect(self.stop_instance)
        self.terminate_btn.clicked.connect(self.terminate_instance)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.launch_btn)
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.terminate_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Instance table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'Instance ID', 'State', 'Type', 'Public IP', 'Private IP'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
    
    #Fetches instances from AWS and updates the table with the results
    
    def load_instances(self):
        self.parent.update_status("Loading EC2 instances...")
        self.worker = EC2Worker('list_instances')
        self.worker.finished.connect(self.update_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    
    def show_error(self, error):
        QMessageBox.critical(self, "Error", error)

    #Updates the table with the given instances
    def update_table(self, instances):
        self.table.setRowCount(len(instances))
        
        for row, instance in enumerate(instances):
            self.table.setItem(row, 0, QTableWidgetItem(instance['InstanceId']))
            self.table.setItem(row, 1, QTableWidgetItem(instance['State']))
            self.table.setItem(row, 2, QTableWidgetItem(instance['InstanceType']))
            self.table.setItem(row, 3, QTableWidgetItem(instance['PublicIpAddress']))
            self.table.setItem(row, 4, QTableWidgetItem(instance['PrivateIpAddress']))
        
        self.parent.update_status(f"Loaded {len(instances)} EC2 instances")
    
    def get_selected_instance(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            return self.table.item(current_row, 0).text()
        return None
    
    #Dummy placeholder helper function for launching instance
    def launch_instance(self):
        dialog = LaunchInstanceDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # In a real implementation, you would launch the instance here
            QMessageBox.information(self, "Launch Instance", 
                                  "Instance launch would be done here, but since this is a highly configurable operation, will be omitting this for simplicity")
    
    #Start instance function
    def start_instance(self):
        instance_id = self.get_selected_instance()
        if not instance_id:
            QMessageBox.warning(self, "No Selection", "Please select an instance")
            return
        
        self.parent.update_status(f"Starting instance {instance_id}...")
        self.worker = EC2Worker('start_instance', instance_id=instance_id)
        self.worker.finished.connect(lambda: self.instance_action_complete("started"))
        self.worker.error.connect(self.show_error)
        self.worker.start()

    #Stop instance function
    def stop_instance(self):
        instance_id = self.get_selected_instance()
        if not instance_id:
            QMessageBox.warning(self, "No Selection", "Please select an instance")
            return
        
        self.parent.update_status(f"Stopping instance {instance_id}...")
        self.worker = EC2Worker('stop_instance', instance_id=instance_id)
        self.worker.finished.connect(lambda: self.instance_action_complete("stopped"))
        self.worker.error.connect(self.show_error)
        self.worker.start()

    #Terminate selected instance function
    def terminate_instance(self):
        instance_id = self.get_selected_instance()
        if not instance_id:
            QMessageBox.warning(self, "No Selection", "Please select an instance")
            return
        
        reply = QMessageBox.question(self, "Confirm Termination", 
                                   f"Are you sure you want to terminate {instance_id}?")
        if reply == QMessageBox.StandardButton.Yes:
            self.parent.update_status(f"Terminating instance {instance_id}...")
            self.worker = EC2Worker('terminate_instance', instance_id=instance_id)
            self.worker.finished.connect(lambda: self.instance_action_complete("terminated"))
            self.worker.error.connect(self.show_error)
            self.worker.start()
    #Returns status update for operation
    def instance_action_complete(self, action):
        self.parent.update_status(f"Instance {action} successfully")
        self.load_instances()  # Refresh the list
    
    def show_error(self, error_message):
        self.parent.update_status("Error occurred")
        QMessageBox.critical(self, "Error", f"AWS Error: {error_message}")