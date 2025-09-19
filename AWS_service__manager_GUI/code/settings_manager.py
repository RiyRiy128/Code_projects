import boto3
import json
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QLabel, QMessageBox, QFormLayout, 
                             QComboBox, QTextEdit)
from PyQt6.QtCore import QThread, pyqtSignal


#Essentially this is simply the credentials aspect which configured for calling AWS services within the manager
class SettingsManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_current_config()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        #AWS Configuration
        config_layout = QFormLayout()
        
        self.access_key_input = QLineEdit()
        self.secret_key_input = QLineEdit()
        self.secret_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.region_combo = QComboBox()
        self.region_combo.addItems([
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
            'eu-west-1', 'eu-west-2', 'eu-central-1',
            'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1'
        ])
        
        config_layout.addRow("Access Key ID:", self.access_key_input)
        config_layout.addRow("Secret Access Key:", self.secret_key_input)
        config_layout.addRow("Default Region:", self.region_combo)
        
        layout.addLayout(config_layout)
        
        #Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Configuration")
        self.test_btn = QPushButton("Test Connection")
        self.load_btn = QPushButton("Load from AWS CLI")
        
        self.save_btn.clicked.connect(self.save_configuration)
        self.test_btn.clicked.connect(self.test_connection)
        self.load_btn.clicked.connect(self.load_from_aws_cli)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.test_btn)
        button_layout.addWidget(self.load_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        #Current configuration display
        layout.addWidget(QLabel("Current Configuration:"))
        self.config_display = QTextEdit()
        self.config_display.setReadOnly(True)
        self.config_display.setMaximumHeight(200)
        
        layout.addWidget(self.config_display)
        
        layout.addStretch()
    
    def load_current_config(self):
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            
            if credentials:
                config_info = {
                    "Access Key": credentials.access_key[:8] + "..." if credentials.access_key else "Not set",
                    "Secret Key": "***" if credentials.secret_key else "Not set",
                    "Region": session.region_name or "Not set",
                    "Profile": session.profile_name or "default"
                }
                
                self.config_display.setPlainText(json.dumps(config_info, indent=2))
                
                #Update form fields
                if session.region_name:
                    index = self.region_combo.findText(session.region_name)
                    if index >= 0:
                        self.region_combo.setCurrentIndex(index)
            else:
                self.config_display.setPlainText("No AWS credentials configured")
                
        except Exception as e:
            self.config_display.setPlainText(f"Error loading configuration: {str(e)}")
    
    def save_configuration(self):
        access_key = self.access_key_input.text().strip()
        secret_key = self.secret_key_input.text().strip()
        region = self.region_combo.currentText()
        
        if not access_key or not secret_key:
            QMessageBox.warning(self, "Missing Information", 
                              "Please enter both Access Key ID and Secret Access Key")
            return
        
        try:
            #Create AWS credentials directory if it doesn't exist
            aws_dir = os.path.expanduser("~/.aws")
            os.makedirs(aws_dir, exist_ok=True)
            
            #Write credentials file
            credentials_file = os.path.join(aws_dir, "credentials")
            with open(credentials_file, 'w') as f:
                f.write("[default]\n")
                f.write(f"aws_access_key_id = {access_key}\n")
                f.write(f"aws_secret_access_key = {secret_key}\n")
            
            #Write config file
            config_file = os.path.join(aws_dir, "config")
            with open(config_file, 'w') as f:
                f.write("[default]\n")
                f.write(f"region = {region}\n")
            
            QMessageBox.information(self, "Success", "AWS configuration saved successfully")
            self.load_current_config()
            
            #Clear sensitive fields
            self.access_key_input.clear()
            self.secret_key_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")
    
    def test_connection(self):
        try:
            #Test connection by listing S3 buckets
            s3 = boto3.client('s3')
            response = s3.list_buckets()
            
            bucket_count = len(response['Buckets'])
            QMessageBox.information(self, "Connection Test", 
                                  f"✅ Connection successful!\nFound {bucket_count} S3 buckets")
            
        except Exception as e:
            QMessageBox.critical(self, "Connection Test Failed", 
                               f"❌ Connection failed:\n{str(e)}")
    

    #There are some errors on initial load or intermittently when populating clients with credentials
    def load_from_aws_cli(self):
        try:
            #Try to load existing AWS CLI configuration
            aws_config_file = os.path.expanduser("~/.aws/config")
            aws_credentials_file = os.path.expanduser("~/.aws/credentials")
            
            if os.path.exists(aws_config_file) or os.path.exists(aws_credentials_file):
                self.load_current_config()
                QMessageBox.information(self, "Load Configuration", 
                                      "AWS CLI configuration loaded successfully")
            else:
                QMessageBox.warning(self, "No Configuration", 
                                  "No AWS CLI configuration found")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load AWS CLI configuration: {str(e)}")