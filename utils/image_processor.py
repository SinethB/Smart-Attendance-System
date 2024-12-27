import cv2
import numpy as np

class ImageProcessor:
    @staticmethod
    def preprocess_for_face_detection(image):
        # Resize and normalize image for face detection model
        resized = cv2.resize(image, (224, 224))
        normalized = resized / 255.0
        return np.expand_dims(normalized, axis=0)
    
    @staticmethod
    def preprocess_for_face_recognition(image):
        # Resize and normalize for face recognition model
        resized = cv2.resize(image, (160, 160))
        normalized = resized / 255.0
        return np.expand_dims(normalized, axis=0)
    
    @staticmethod
    def preprocess_for_gesture(image):
        # Resize and normalize for gesture recognition
        resized = cv2.resize(image, (64, 64))
        normalized = resized / 255.0
        return np.expand_dims(normalized, axis=0)
    
    @staticmethod
    def crop_face(image, face_location):
        # Crop face from image based on detected location
        x, y, w, h = face_location
        return image[y:y+h, x:x+w]