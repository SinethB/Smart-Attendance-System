import tensorflow as tf
import numpy as np
import cv2
import json

class EmotionDetectionModel:
    def __init__(self, model_path, labels_path):
        try:
            # Load the h5 model
            self.model = tf.keras.models.load_model(model_path)
            
            # Load emotion labels
            with open(labels_path, 'r') as f:
                self.emotion_labels = json.load(f)
        except Exception as e:
            print(f"Error loading emotion detection model: {e}")
            self.model = None
            self.emotion_labels = {}
    
    def detect_emotion(self, face_image):
        if self.model is None:
            return 'Unknown'
        
        # Preprocess face image
        processed_face = self._preprocess_face(face_image)
        
        # Predict emotion
        predictions = self.model.predict(processed_face)
        
        # Get top emotion
        top_emotion_index = np.argmax(predictions)
        confidence = predictions[0][top_emotion_index]
        
        # Return emotion label if confidence is high enough
        return self.emotion_labels.get(str(top_emotion_index), 'Unknown') if confidence > 0.6 else 'Neutral'
    
    def _preprocess_face(self, face_image):
        # Preprocess face image for emotion detection
        # Convert to grayscale
        if len(face_image.shape) == 3:
            grayscale = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        else:
            grayscale = face_image
        
        # Resize to model's expected input size
        resized = cv2.resize(grayscale, (48, 48))
        
        # Normalize
        normalized = resized / 255.0
        
        # Reshape for model input
        return np.expand_dims(np.expand_dims(normalized, axis=0), axis=-1)