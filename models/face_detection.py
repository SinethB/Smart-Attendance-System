import cv2
import numpy as np

class FaceDetectionModel:
    def __init__(self, cascade_path):
        try:
            # Load the Haar cascade classifier
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            if self.face_cascade.empty():
                raise ValueError("Failed to load Haar Cascade")
        except Exception as e:
            print(f"Error loading face cascade: {e}")
            self.face_cascade = None
    
    def detect_faces(self, frame):
        if self.face_cascade is None:
            return []
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces