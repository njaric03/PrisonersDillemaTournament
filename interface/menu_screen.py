import tkinter as tk
from tkinter import ttk

class MenuScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Prisoner's Dilemma")
        
        # Configure dark theme
        self.root.configure(bg='#1a1a1a')
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TButton', padding=10, width=30)
        
        # Make window full screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Prisoner's Dilemma Simulator",
                               font=('Helvetica', 24),
                               foreground='white',
                               background='#1a1a1a')
        title_label.pack(pady=20)
        
        # Buttons
        ttk.Button(main_frame, 
                  text="Start Game", 
                  command=self.start_game).pack(pady=10)
        
        ttk.Button(main_frame, 
                  text="Start Tournament", 
                  command=self.start_tournament).pack(pady=10)
        
        ttk.Button(main_frame, 
                  text="Test Against Multiple Opponents", 
                  command=self.test_multiple).pack(pady=10)
        
        ttk.Button(main_frame, 
                  text="Exit", 
                  command=root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self):
        self.clear_window()
        from .game_screen import GameScreen  # Import here instead
        GameScreen(self.root)

    def start_tournament(self):
        self.clear_window()
        from .tournament_screen import TournamentScreen  # Import here instead
        TournamentScreen(self.root)

    def test_multiple(self):
        self.clear_window()
        from .multiple_test_screen import MultipleTestScreen  # Import here instead
        MultipleTestScreen(self.root)
