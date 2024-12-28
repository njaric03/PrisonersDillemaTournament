import tkinter as tk
from tkinter import ttk
from interface.game_ui import GameUI
from interface.menu_screen import MenuScreen

class TournamentScreen:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')  # Add this line
        self.root.title("Tournament Mode")
        self.setup_ui()

    def setup_ui(self):
        # Configure dark theme
        self.root.configure(bg='#1a1a1a')
        self.root.grid_rowconfigure(0, weight=1)  # Add this line
        self.root.grid_columnconfigure(0, weight=1)  # Add this line
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TButton', padding=10, width=30)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.main_frame.grid_rowconfigure(0, weight=0)  # Title
        self.main_frame.grid_rowconfigure(1, weight=0)  # Separator
        self.main_frame.grid_rowconfigure(2, weight=0)  # Description
        self.main_frame.grid_rowconfigure(3, weight=1)  # Content
        self.main_frame.grid_rowconfigure(4, weight=0)  # Back button
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title (moved up)
        title_label = ttk.Label(self.main_frame, 
                              text="Tournament Mode",
                              font=('Helvetica', 24),
                              foreground='white',
                              background='#1a1a1a')
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.grid(row=1, column=0, sticky="ew", pady=10)
        
        # Description
        description = ttk.Label(self.main_frame,
                              text="Select multiple bots to participate in a round-robin tournament. Each bot will play against every other bot.",
                              font=('Helvetica', 12),
                              foreground='white',
                              background='#1a1a1a',
                              wraplength=800)
        description.grid(row=2, column=0, pady=(0, 20))
        
        # Create the tournament UI
        self.game_ui = GameUI(self.main_frame)  # Store as instance variable
        self.game_ui.main_frame.grid(row=3, column=0, sticky="nsew")
        self.game_ui.bot_listbox.configure(selectmode=tk.MULTIPLE)
        self.game_ui.custom_bot_listbox.configure(selectmode=tk.MULTIPLE)  # Set custom bots listbox to MULTIPLE
        
        # Create bottom button frame
        button_frame = ttk.Frame(self.main_frame, style='TFrame')
        button_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        button_frame.grid_columnconfigure(0, weight=0)  # Back button
        button_frame.grid_columnconfigure(1, weight=1)  # Space
        button_frame.grid_columnconfigure(2, weight=0)  # Start button
        
        # Back button on left, no extra width
        ttk.Button(button_frame, 
                  text="Back to Menu",
                  style='TButton',
                  width=15,
                  command=self.back_to_menu).grid(row=0, column=0, padx=5)
        
        # Start button on right, no extra width
        ttk.Button(button_frame,
                  text="Start Tournament",
                  style='TButton',
                  width=15,
                  command=self.start_tournament).grid(row=0, column=2, padx=5)
        
    def start_tournament(self):
        self.game_ui.start_tournament()  # Now using the stored instance

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MenuScreen(self.root)
