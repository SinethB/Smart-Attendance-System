import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np

from PIL import Image, ImageTk  

from utils.database_handler import DatabaseHandler
from utils.csv_logger import CSVLogger
from utils.image_processor import ImageProcessor
from ui.styles import UIStyles

# Import custom models
from models.face_detection import FaceDetectionModel
from models.face_recognition import FaceRecognitionModel
from models.gesture_recognition import GestureRecognitionModel
from models.emotion_detection import EmotionDetectionModel

class AttendanceWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Attendance Marking")
        
        # Initialize models and utilities
        self.db_handler = DatabaseHandler()
        self.csv_logger = CSVLogger()
        
        # self.face_detection_model = FaceDetectionModel('models/face_detection_model.h5')
        # Change this line in __init__
        self.face_detection_model = FaceDetectionModel('models/haarcascade_frontalface_default.xml')
        self.face_recognition_model = FaceRecognitionModel('models/face_recognition_model.h5', 'data/registered_users.json')
        self.gesture_recognition_model = GestureRecognitionModel('models/gesture_recognition_model.keras', 'models/gesture_class_labels.json')
        self.emotion_detection_model = EmotionDetectionModel('models/emotion_recognition_model.h5', 'models/emotion_labels.json')
        
        # State tracking
        self.current_state = 'WAIT_FACE'
        self.detected_user = None
        
        # Setup UI
        self.setup_ui()
        
        # Camera setup
        self.capture = cv2.VideoCapture(0)
        
    def setup_ui(self):
        # Status Display
        self.status_label = tk.Label(self.window, text="Waiting for Face Detection", font=("Arial", 16))
        self.status_label.pack()
        
        # Camera Preview
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()
        
        # Start attendance process
        self.window.after(100, self.attendance_process)
    
    def attendance_process(self):
        ret, frame = self.capture.read()
        if not ret:
            return
        
        # State machine for attendance
        if self.current_state == 'WAIT_FACE':
            self.wait_for_face(frame)
        elif self.current_state == 'WAIT_GESTURE':
            self.wait_for_gesture(frame)
        elif self.current_state == 'CONFIRM_USER':
            self.confirm_user(frame)
        
        self.window.after(100, self.attendance_process)
    
    def wait_for_face(self, frame):
        # Detect faces
        faces = self.face_detection_model.detect_faces(frame)
        
        if len(faces) > 0:
            # Take first detected face
            face_coords = faces[0]  # (x, y, w, h)
            face_image = self.face_detection_model.crop_face(frame, face_coords)
            
            # Draw rectangle around face
            (x, y, w, h) = face_coords
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Recognize face
            recognized_user = self.face_recognition_model.recognize_face(face_image)
            
            if recognized_user:
                self.detected_user = recognized_user
                self.current_state = 'WAIT_GESTURE'
                self.status_label.config(text=f"Detected: {recognized_user['name']}. Waiting for 'Five' Gesture")
            else:
                self.status_label.config(text="Unknown Face Detected")
        
        self.update_canvas(frame)
    
    def wait_for_gesture(self, frame):
        # Detect hand gestures
        gesture = self.gesture_recognition_model.recognize_gesture(frame)
        
        if gesture == 'Five':
            # Show user details
            self.current_state = 'CONFIRM_USER'
            self.status_label.config(text=f"Confirm User: {self.detected_user['name']}")
        
        self.update_canvas(frame)
    
    def confirm_user(self, frame):
        # Wait for confirmation gestures
        gesture = self.gesture_recognition_model.recognize_gesture(frame)
        
        if gesture == 'ThumbsUp':
            # Mark attendance
            emotion = self.emotion_detection_model.detect_emotion(frame)
            self.csv_logger.log_attendance(
                self.detected_user['id'], 
                self.detected_user['name'], 
                emotion
            )
            messagebox.showinfo("Success", f"Attendance marked for {self.detected_user['name']}")
            self.reset_attendance_process()
        
        elif gesture == 'ThumbsDown':
            # Reject and restart
            self.reset_attendance_process()
        
        elif gesture == 'Fist':
            # Exit to initial state
            self.reset_attendance_process()
        
        self.update_canvas(frame)
    
    def reset_attendance_process(self):
        self.current_state = 'WAIT_FACE'
        self.detected_user = None
        self.status_label.config(text="Waiting for Face Detection")
    
    def update_canvas(self, frame):
        # Convert frame for Tkinter display
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)