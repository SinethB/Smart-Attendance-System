import cv2
from tkinter import messagebox, Toplevel, Label, Entry, Button
from PIL import Image, ImageTk
from models.face_detection import FaceDetectionModel
from utils.database_handler import DatabaseHandler
import os

class RegistrationWindow:
    def __init__(self, parent):
        self.parent = parent
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        if not self.cap.isOpened():
            print("Error: Camera not accessible")
        else:
            print("Camera initialized successfully")
        
        self.window = Toplevel(self.parent)
        self.window.title("Register Face")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.video_label = Label(self.window)
        self.video_label.pack()
        
        self.user_id_label = Label(self.window, text="User ID:")
        self.user_id_label.pack()
        self.user_id_entry = Entry(self.window)
        self.user_id_entry.pack()
        
        self.name_label = Label(self.window, text="Name:")
        self.name_label.pack()
        self.name_entry = Entry(self.window)
        self.name_entry.pack()
        
        self.register_button = Button(self.window, text="Register", command=self.start_registration)
        self.register_button.pack()
        
        # Initialize face detection model
        self.face_detection = FaceDetectionModel('models/haarcascade_frontalface_default.xml')
        
        # Initialize database handler
        self.db_handler = DatabaseHandler()
        
        self.image_count = 0
        self.max_images = 10  # Number of images to capture per user
        
        self.update_frame()
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Detect faces
            faces = self.face_detection.detect_faces(frame)
            
            # Draw bounding boxes around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Convert the frame to an image format that Tkinter can display
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        
        self.window.after(10, self.update_frame)  # Update the frame every 10 milliseconds

    def start_registration(self):
        self.image_count = 0
        self.capture_images()

    def capture_images(self):
        if self.image_count < self.max_images:
            frame = self.capture_frame()
            if frame is None:
                return
            
            faces = self.face_detection.detect_faces(frame)
            if len(faces) == 0:
                print("No faces detected")
                self.window.after(1000, self.capture_images)  # Retry after 1 second
                return
            
            # Save the image
            user_id = self.user_id_entry.get()
            image_dir = f"data/user_images/{user_id}"
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join(image_dir, f"{user_id}_{self.image_count}.jpg")
            cv2.imwrite(image_path, frame)
            
            self.image_count += 1
            print(f"Captured image {self.image_count}/{self.max_images}")
            
            self.window.after(1000, self.capture_images)  # Capture next image after 1 second
        else:
            self.save_user_data()

    def save_user_data(self):
        user_id = self.user_id_entry.get()
        name = self.name_entry.get()
        image_dir = f"data/user_images/{user_id}"
        image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
        
        self.db_handler.add_user(
            user_id,
            name,
            image_paths,
            []  # Empty embedding for now
        )
        
        messagebox.showinfo("Success", "Face registered successfully!")
        self.window.destroy()

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            return None
        return frame

    def on_closing(self):
        if self.cap.isOpened():
            self.cap.release()
        self.window.destroy()