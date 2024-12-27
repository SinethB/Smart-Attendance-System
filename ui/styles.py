class UIStyles:
    # Color scheme
    PRIMARY_COLOR = "#2196F3"    # Blue
    SECONDARY_COLOR = "#1976D2"  # Darker Blue
    BG_COLOR = "#F5F5F5"        # Light Gray
    TEXT_COLOR = "#FFFFFF"       # White
    FONT_COLOR = "#333333"       # Dark Gray
    
    # Fonts
    TITLE_FONT = ("Helvetica", 24, "bold")
    BUTTON_FONT = ("Helvetica", 14)
    
    # Window sizes
    MAIN_WINDOW_SIZE = "800x600"
    
    # Button styles
    BUTTON_STYLE = {
        'font': BUTTON_FONT,
        'bg': PRIMARY_COLOR,
        'fg': TEXT_COLOR,
        'activebackground': SECONDARY_COLOR,
        'activeforeground': TEXT_COLOR,
        'padx': 30,
        'pady': 15,
        'relief': 'flat',
        'borderwidth': 0
    }
    
    @classmethod
    def apply_button_style(cls, button):
        button.config(**cls.BUTTON_STYLE)
        
        # Add hover effect
        button.bind('<Enter>', lambda e: button.config(bg=cls.SECONDARY_COLOR))
        button.bind('<Leave>', lambda e: button.config(bg=cls.PRIMARY_COLOR))