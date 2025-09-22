import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                             QVBoxLayout, QWidget, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ec2_manager import EC2Manager
from s3_manager import S3Manager
from lambda_manager import LambdaManager
from iam_manager import IAMManager
from cloudformation_manager import CloudFormationManager
from stepfunctions_manager import StepFunctionsManager
from settings_manager import SettingsManager

class AWSCLIGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AWS desktop service manager")
        self.setGeometry(100, 100, 1200, 800)
        
        #Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        #Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        #Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        #Initialize managers
        self.init_tabs()
        
        #Apply styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #0078d4;
            }
        """)
    
    #Start service tabs
    def init_tabs(self):
        
        #EC2 Management
        self.ec2_manager = EC2Manager(self)
        self.tabs.addTab(self.ec2_manager, "EC2")
        
        #S3 Management
        self.s3_manager = S3Manager(self)
        self.tabs.addTab(self.s3_manager, "S3")
        
        #Lambda Management
        self.lambda_manager = LambdaManager(self)
        self.tabs.addTab(self.lambda_manager, "Lambda")
        
        #IAM Management
        self.iam_manager = IAMManager(self)
        self.tabs.addTab(self.iam_manager, "IAM")
        
        #CloudFormation Management
        self.cf_manager = CloudFormationManager(self)
        self.tabs.addTab(self.cf_manager, "CloudFormation")
        
        #Step Functions Management
        self.sf_manager = StepFunctionsManager(self)
        self.tabs.addTab(self.sf_manager, "Step Functions")
        
        #Settings
        self.settings_manager = SettingsManager(self)
        self.tabs.addTab(self.settings_manager, "Settings")
    
    def update_status(self, message):
        self.status_bar.showMessage(message)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AWS CLI GUI")
    
    window = AWSCLIGui()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()