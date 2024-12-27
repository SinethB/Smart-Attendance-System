import tensorflow as tf
import numpy as np
import json
import cv2

class FaceRecognitionModel:
    def __init__(self, model_path, users_path):
        try:
            # Load the h5 model
            self.model = tf.keras.models.load_model(model_path)
            
            # Load registered users
            with open(users_path, 'r') as f:
                self.registered_users = json.load(f)
        except Exception as e:
            print(f"Error loading face recognition model: {e}")
            self.model = None
            self.registered_users = {}
    
    def recognize_face(self, face_image):
        if self.model is None:
            return None
        
        # Preprocess the face image
        processed_face = self._preprocess_face(face_image)
        
        # Generate embedding for the input face
        face_embedding = self._extract_embedding(processed_face)
        
        # Match with registered users
        return self._match_user(face_embedding)
    
    def _preprocess_face(self, face_image):
        # Resize and normalize face image
        resized = cv2.resize(face_image, (160, 160))
        normalized = resized / 255.0
        return np.expand_dims(normalized, axis=0)
    
    def _extract_embedding(self, processed_face):
        # Use the model to generate face embedding
        return self.model.predict(processed_face)[0]
    
    def _match_user(self, input_embedding):
        # Compare input embedding with registered user embeddings
        best_match = None
        best_distance = float('inf')
        
        for user_id, user_data in self.registered_users.items():
            # Compare embeddings (assuming user_data has 'embedding')
            registered_embedding = np.array(user_data.get('face_embedding', []))
            
            # Calculate cosine similarity or euclidean distance
            distance = np.linalg.norm(input_embedding - registered_embedding)
            
            if distance < best_distance and distance < 0.6:  # Threshold can be adjusted
                best_distance = distance
                best_match = {
                    'id': user_id,
                    'name': user_data.get('name', 'Unknown'),
                    **user_data
                }
        
        return best_match