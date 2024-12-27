import json
import os

class DatabaseHandler:
    def __init__(self, db_path='data/registered_users.json'):
        self.db_path = db_path
        self.users = self.load_users()
    
    def load_users(self):
        if not os.path.exists(self.db_path):
            return {}
        
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def save_users(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def add_user(self, user_id, name, image_path, face_embedding):
        self.users[user_id] = {
            'name': name,
            'image_path': image_path,
            'face_embedding': face_embedding
        }
        self.save_users()
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def user_exists(self, user_id):
        return user_id in self.users