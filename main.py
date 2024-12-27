import tkinter as tk
from ui.registration_window import RegistrationWindow
from ui.attendance_window import AttendanceWindow
from ui.styles import UIStyles

class AttendanceSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Facial Recognition Attendance System")
        
        # Set window size and position it in center
        self.root.geometry(UIStyles.MAIN_WINDOW_SIZE)
        self.center_window()
        
        # Make window non-resizable
        self.root.resizable(False, False)
        
        # Set window background color
        self.root.configure(bg=UIStyles.BG_COLOR)
        
        self.setup_main_window()

    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position x and y coordinates
        window_width, window_height = map(int, UIStyles.MAIN_WINDOW_SIZE.split('x'))
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        
        self.root.geometry(f'{window_width}x{window_height}+{position_x}+{position_y}')
        
    def setup_main_window(self):
        # Create main frame
        main_frame = tk.Frame(self.root, bg=UIStyles.BG_COLOR)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Smart Attendance System",
            font=UIStyles.TITLE_FONT,
            bg=UIStyles.BG_COLOR,
            fg=UIStyles.FONT_COLOR
        )
        title_label.pack(pady=(0, 40))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Select an option to proceed",
            font=("Helvetica", 12),
            bg=UIStyles.BG_COLOR,
            fg=UIStyles.FONT_COLOR
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Button Frame
        button_frame = tk.Frame(main_frame, bg=UIStyles.BG_COLOR)
        button_frame.pack()
        
        # Registration Button
        registration_btn = tk.Button(
            button_frame,
            text="Face Registration",
            command=self.open_registration,
            cursor="hand2"  # Changes cursor to hand when hovering
        )
        UIStyles.apply_button_style(registration_btn)
        registration_btn.pack(pady=10)
        
        # Attendance Button
        attendance_btn = tk.Button(
            button_frame,
            text="Mark Attendance",
            command=self.open_attendance,
            cursor="hand2"
        )
        UIStyles.apply_button_style(attendance_btn)
        attendance_btn.pack(pady=10)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=UIStyles.BG_COLOR)
        footer_frame.pack(side='bottom', pady=20)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2024 Face Recognition Attendance System",
            font=("Helvetica", 8),
            bg=UIStyles.BG_COLOR,
            fg=UIStyles.FONT_COLOR
        )
        footer_text.pack()
    
    def open_registration(self):
        RegistrationWindow(self.root)
        
    def open_attendance(self):
        AttendanceWindow(self.root)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AttendanceSystem()
    app.run()