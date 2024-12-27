import csv
from datetime import datetime
import os

class CSVLogger:
    def __init__(self, log_path='data/attendance_logs.csv'):
        self.log_path = log_path
        self.ensure_csv_exists()
    
    def ensure_csv_exists(self):
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'User ID', 'Name', 'Emotion'])
    
    def log_attendance(self, user_id, name, emotion):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_id, name, emotion])