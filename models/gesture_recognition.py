import tensorflow as tf
import numpy as np
import cv2
import json

class GestureRecognitionModel:
    def __init__(self, model_path, labels_path):
        try:
            # Load the h5 model
            self.model = tf.keras.models.load_model(model_path)
            
            # Load gesture class labels
            with open(labels_path, 'r') as f:
                self.class_labels = json.load(f)
        except Exception as e:
            print(f"Error loading gesture recognition model: {e}")
            self.model = None
            self.class_labels = {}
    
    def recognize_gesture(self, frame):
        if self.model is None:
            return None
        
        # Extract hand region (you might need to implement hand detection)
        hand_image = self._extract_hand(frame)
        
        if hand_image is None:
            return None
        
        # Preprocess hand image
        processed_hand = self._preprocess_hand(hand_image)
        
        # Predict gesture
        predictions = self.model.predict(processed_hand)
        
        # Get top prediction
        top_gesture_index = np.argmax(predictions)
        confidence = predictions[0][top_gesture_index]
        
        # Return gesture label if confidence is high enough
        return self.class_labels.get(str(top_gesture_index), 'Unknown') if confidence > 0.7 else None
    
    def _extract_hand(self, frame):
        # Placeholder for hand extraction
        # This would typically involve:
        # 1. Skin color segmentation
        # 2. Background subtraction
        # 3. Contour detection
        # For now, return a cropped region as an example
        height, width = frame.shape[:2]
        hand_roi = frame[height//2:, width//2:]
        return hand_roi
    
    def _preprocess_hand(self, hand_image):
        # Preprocess hand image for model input
        resized = cv2.resize(hand_image, (64, 64))
        normalized = resized / 255.0
        return np.expand_dims(normalized, axis=0)