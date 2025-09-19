import boto3
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLineEdit, 
                             QLabel, QMessageBox, QFileDialog, QProgressBar)
from PyQt6.QtCore import QThread, pyqtSignal

class S3Worker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, action, **kwargs):
        super().__init__()
        self.action = action
        self.kwargs = kwargs
    
    def run(self):
        try:
            s3 = boto3.client('s3')
            
            if self.action == 'list_buckets':
                response = s3.list_buckets()
                buckets = []
                for bucket in response['Buckets']:
                    buckets.append({
                        'Name': bucket['Name'],
                        'CreationDate': bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')
                    })
                self.finished.emit(buckets)
                
            elif self.action == 'list_objects':
                bucket_name = self.kwargs['bucket_name']
                response = s3.list_objects_v2(Bucket=bucket_name)
                objects = []
                for obj in response.get('Contents', []):
                    objects.append({
                        'Key': obj['Key'],
                        'Size': self.format_size(obj['Size']),
                        'LastModified': obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
                    })
                self.finished.emit(objects)
                
            elif self.action == 'create_bucket':
                bucket_name = self.kwargs['bucket_name']
                s3.create_bucket(Bucket=bucket_name)
                self.finished.emit([])
                
            elif self.action == 'delete_bucket':
                bucket_name = self.kwargs['bucket_name']
                s3.delete_bucket(Bucket=bucket_name)
                self.finished.emit([])
                
            elif self.action == 'upload_file':
                bucket_name = self.kwargs['bucket_name']
                file_path = self.kwargs['file_path']
                key = self.kwargs['key']
                
                file_size = os.path.getsize(file_path)
                uploaded = 0
                
                def upload_callback(bytes_transferred):
                    nonlocal uploaded
                    uploaded += bytes_transferred
                    progress = int((uploaded / file_size) * 100)
                    self.progress.emit(progress)
                
                s3.upload_file(file_path, bucket_name, key, Callback=upload_callback)
                self.finished.emit([])
                
            elif self.action == 'download_file':
                bucket_name = self.kwargs['bucket_name']
                object_key = self.kwargs['object_key']
                file_path = self.kwargs['file_path']
                s3.download_file(bucket_name, object_key, file_path)
                self.finished.emit([])
                
            elif self.action == 'delete_object':
                bucket_name = self.kwargs['bucket_name']
                object_key = self.kwargs['object_key']
                s3.delete_object(Bucket=bucket_name, Key=object_key)
                self.finished.emit([])
                
        except Exception as e:
            self.error.emit(str(e))
    
    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"

class S3Manager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_bucket = None
        self.init_ui()
        self.load_buckets()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Bucket controls
        bucket_layout = QHBoxLayout()
        
        bucket_layout.addWidget(QLabel("Buckets:"))
        self.refresh_buckets_btn = QPushButton("Refresh Buckets")
        self.create_bucket_btn = QPushButton("Create Bucket")
        self.delete_bucket_btn = QPushButton("Delete Bucket")
        
        self.refresh_buckets_btn.clicked.connect(self.load_buckets)
        self.create_bucket_btn.clicked.connect(self.create_bucket)
        self.delete_bucket_btn.clicked.connect(self.delete_bucket)
        
        bucket_layout.addWidget(self.refresh_buckets_btn)
        bucket_layout.addWidget(self.create_bucket_btn)
        bucket_layout.addWidget(self.delete_bucket_btn)
        bucket_layout.addStretch()
        
        layout.addLayout(bucket_layout)
        
        # Bucket table
        self.bucket_table = QTableWidget()
        self.bucket_table.setColumnCount(2)
        self.bucket_table.setHorizontalHeaderLabels(['Bucket Name', 'Creation Date'])
        self.bucket_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bucket_table.itemSelectionChanged.connect(self.bucket_selected)
        self.bucket_table.setMaximumHeight(200)
        
        layout.addWidget(self.bucket_table)
        
        # Object controls
        object_layout = QHBoxLayout()
        
        self.current_bucket_label = QLabel("Select a bucket to view objects")
        self.upload_btn = QPushButton("Upload File")
        self.download_btn = QPushButton("Download File")
        self.delete_object_btn = QPushButton("Delete Object")
        
        self.upload_btn.clicked.connect(self.upload_file)
        self.download_btn.clicked.connect(self.download_file)
        self.delete_object_btn.clicked.connect(self.delete_object)
        
        object_layout.addWidget(self.current_bucket_label)
        object_layout.addStretch()
        object_layout.addWidget(self.upload_btn)
        object_layout.addWidget(self.download_btn)
        object_layout.addWidget(self.delete_object_btn)
        
        layout.addLayout(object_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Object table
        self.object_table = QTableWidget()
        self.object_table.setColumnCount(3)
        self.object_table.setHorizontalHeaderLabels(['Object Key', 'Size', 'Last Modified'])
        self.object_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.object_table)
    
    def load_buckets(self):
        self.parent.update_status("Loading S3 buckets...")
        self.worker = S3Worker('list_buckets')
        self.worker.finished.connect(self.update_bucket_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def update_bucket_table(self, buckets):
        self.bucket_table.setRowCount(len(buckets))
        
        for row, bucket in enumerate(buckets):
            self.bucket_table.setItem(row, 0, QTableWidgetItem(bucket['Name']))
            self.bucket_table.setItem(row, 1, QTableWidgetItem(bucket['CreationDate']))
        
        self.parent.update_status(f"Loaded {len(buckets)} S3 buckets")
    
    def bucket_selected(self):
        current_row = self.bucket_table.currentRow()
        if current_row >= 0:
            bucket_name = self.bucket_table.item(current_row, 0).text()
            self.current_bucket = bucket_name
            self.current_bucket_label.setText(f"Bucket: {bucket_name}")
            self.load_objects()
    
    def load_objects(self):
        if not self.current_bucket:
            return
        
        self.parent.update_status(f"Loading objects from {self.current_bucket}...")
        self.worker = S3Worker('list_objects', bucket_name=self.current_bucket)
        self.worker.finished.connect(self.update_object_table)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def update_object_table(self, objects):
        self.object_table.setRowCount(len(objects))
        
        for row, obj in enumerate(objects):
            self.object_table.setItem(row, 0, QTableWidgetItem(obj['Key']))
            self.object_table.setItem(row, 1, QTableWidgetItem(obj['Size']))
            self.object_table.setItem(row, 2, QTableWidgetItem(obj['LastModified']))
        
        self.parent.update_status(f"Loaded {len(objects)} objects from {self.current_bucket}")
    
    def create_bucket(self):
        bucket_name, ok = QLineEdit().getText(self, "Create Bucket", "Bucket name:")
        if ok and bucket_name:
            self.parent.update_status(f"Creating bucket {bucket_name}...")
            self.worker = S3Worker('create_bucket', bucket_name=bucket_name)
            self.worker.finished.connect(lambda: self.bucket_action_complete("created"))
            self.worker.error.connect(self.show_error)
            self.worker.start()
    
    def delete_bucket(self):
        current_row = self.bucket_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a bucket")
            return
        
        bucket_name = self.bucket_table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                   f"Are you sure you want to delete bucket '{bucket_name}'?")
        
        if reply == QMessageBox.StandardButton.Yes:
            self.parent.update_status(f"Deleting bucket {bucket_name}...")
            self.worker = S3Worker('delete_bucket', bucket_name=bucket_name)
            self.worker.finished.connect(lambda: self.bucket_action_complete("deleted"))
            self.worker.error.connect(self.show_error)
            self.worker.start()
    
    def upload_file(self):
        if not self.current_bucket:
            QMessageBox.warning(self, "No Bucket", "Please select a bucket first")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if file_path:
            key = os.path.basename(file_path)
            
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.parent.update_status(f"Uploading {key} to {self.current_bucket}...")
            self.worker = S3Worker('upload_file', 
                                 bucket_name=self.current_bucket, 
                                 file_path=file_path, 
                                 key=key)
            self.worker.finished.connect(self.upload_complete)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.error.connect(self.show_error)
            self.worker.start()


    def delete_complete(self):
        self.progress_bar.setVisible(False)
        self.parent.update_status("Deletion completed successfully")
        self.load_objects()  # Refresh object list        
    
    def upload_complete(self):
        self.progress_bar.setVisible(False)
        self.parent.update_status("Upload completed successfully")
        self.load_objects()  # Refresh object list
    
    def download_complete(self):
        self.progress_bar.setVisible(False)
        self.parent.update_status("Download completed successfully")

        #Refresh the object list
        self.load_objects()  


    def download_file(self):

        if not self.current_bucket:
            QMessageBox.warning(self, "No Bucket", "Please select a bucket first")
            return
        current_row = self.object_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an object")
            return
        object_key = self.object_table.item(current_row, 0).text()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", object_key)
        if file_path:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)

            self.parent.update_status(f"Downloading {object_key} from {self.current_bucket}...")
            self.worker = S3Worker('download_file',
                                   bucket_name=self.current_bucket,
                                   object_key=object_key,
                                   file_path=file_path)
            self.worker.finished.connect(self.download_complete)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.error.connect(self.show_error)
            self.worker.start()
    
    def delete_object(self):
        if not self.current_bucket:
            QMessageBox.warning(self, "No Bucket", "Please select a bucket first")
            return
        current_row = self.object_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an object")
            return
        object_key = self.object_table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirm Deletion",f"Are you sure you want to delete '{object_key}'?")
        if reply == QMessageBox.StandardButton.Yes:
            self.parent.update_status(f"Deleting {object_key} from {self.current_bucket}...")
            self.worker = S3Worker('delete_object',
                                   bucket_name=self.current_bucket,
                                   object_key=object_key)
            self.worker.finished.connect(self.delete_complete)
            self.worker.error.connect(self.show_error)
            self.worker.start()
        else:
            self.parent.update_status("Deletion cancelled")
                
        
    
    def bucket_action_complete(self, action):
        self.parent.update_status(f"Bucket {action} successfully")
        self.load_buckets()  # Refresh bucket list
    
    def show_error(self, error_message):
        self.parent.update_status("Error occurred")
        QMessageBox.critical(self, "Error", f"AWS Error: {error_message}")