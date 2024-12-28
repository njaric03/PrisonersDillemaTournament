import tkinter as tk
from tkinter import ttk
from interface.game_ui import GameUI  # Changed from relative to absolute import
from interface.menu_screen import MenuScreen  # Changed from relative to absolute import

class GameScreen:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')  # Add this line
        self.root.title("Single Game Mode")
        self.setup_ui()

    def setup_ui(self):
        # Configure dark theme
        self.root.configure(bg='#1a1a1a')
        
        # Ensure window maximizes properly
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TButton', padding=10, width=30)
        
        # Create main frame with full expansion
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure main frame grid weights
        self.main_frame.grid_rowconfigure(0, weight=0)  # Title
        self.main_frame.grid_rowconfigure(1, weight=0)  # Separator
        self.main_frame.grid_rowconfigure(2, weight=0)  # Description
        self.main_frame.grid_rowconfigure(3, weight=1)  # Content
        self.main_frame.grid_rowconfigure(4, weight=0)  # Back button
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title (moved up one row)
        title_label = ttk.Label(self.main_frame, 
                              text="Single Game Mode",
                              font=('Helvetica', 24),
                              foreground='white',
                              background='#1a1a1a')
        title_label.grid(row=0, column=0, pady=(0, 5))  # Reduced bottom padding
        
        # Separator
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.grid(row=1, column=0, sticky="ew", pady=5)  # Reduced padding
        
        # Description
        description = ttk.Label(self.main_frame,
                              text="Test your bot against a single opponent. Select your bot and choose who to play against.",
                              font=('Helvetica', 12),
                              foreground='white',
                              background='#1a1a1a',
                              wraplength=800)
        description.grid(row=2, column=0, pady=(5, 10))  # Adjusted padding
        
        # Create the game UI (moved up one row)
        self.game_ui = GameUI(self.main_frame)  # Store as instance variable
        self.game_ui.main_frame.grid(row=3, column=0, sticky="nsew")
        self.game_ui.bot_listbox.configure(selectmode=tk.SINGLE)
        # Removed game_ui button configuration
        
        # Create bottom button frame (in row 4)
        button_frame = ttk.Frame(self.main_frame, style='TFrame')
        button_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        button_frame.grid_columnconfigure(0, weight=0)  # Back button
        button_frame.grid_columnconfigure(1, weight=1)  # Space
        button_frame.grid_columnconfigure(2, weight=0)  # Start button
        
        # Back button on left, no extra width
        ttk.Button(button_frame, 
                  text="Back to Menu",
                  style='TButton',
                  width=15,  # Fixed width
                  command=self.back_to_menu).grid(row=0, column=0, padx=5)
        
        # Start button on right, no extra width
        ttk.Button(button_frame,
                  text="Start Game",
                  style='TButton',
                  width=15,  # Fixed width
                  command=self.start_game).grid(row=0, column=2, padx=5)

    def start_game(self):
        self.game_ui.start_games()  # Now using the stored instance

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MenuScreen(self.root)
