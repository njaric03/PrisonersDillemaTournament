import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import importlib.util
from utils.abstract_bot import AbstractBot
from simulation.simulate_tournament import TournamentSimulation
from simulation.simulate_games import PrisonersDilemmaSimulation

class GameUI:
    def __init__(self, parent):
        self.parent = parent
        
        # Initialize variables first
        self.available_bots = self.load_bots()
        self.filename_to_display = {}
        self.game_button = None
        self.tournament_button = None
        self.player2_path = None
        self.player2_entry = None
        
        # Configure parent frame to expand
        parent.grid_rowconfigure(1, weight=1)  # Changed from 0 to 1 to match the content row
        parent.grid_columnconfigure(0, weight=1)
        
        # Configure dark theme
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabelframe', background='#1a1a1a', foreground='white')
        style.configure('TLabelframe.Label', background='#1a1a1a', foreground='white')
        style.configure('TLabel', background='#1a1a1a', foreground='white')
        style.configure('TRadiobutton', background='#1a1a1a', foreground='white')
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(parent, padding="20", style='TFrame')  # Made it instance variable
        self.main_frame.grid(row=1, column=0, sticky="nsew")  # Changed row from 0 to 1
        
        # Configure all grid weights for vertical expansion
        self.main_frame.grid_rowconfigure(0, weight=1)  # Main content row
        self.main_frame.grid_columnconfigure(0, weight=1)  # Left frame
        self.main_frame.grid_columnconfigure(1, weight=2)  # Center space
        self.main_frame.grid_columnconfigure(2, weight=1)  # Right frame

        # Left and right frames need vertical expansion
        left_frame = ttk.LabelFrame(self.main_frame, text="Player 1", padding="10")
        right_frame = ttk.LabelFrame(self.main_frame, text="Player 2", padding="10")
        
        # Make frames expand vertically
        left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)
        
        # Configure vertical expansion for frames
        left_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        # Left frame content (Player 1)
        ttk.Label(left_frame, text="Select Bot File:").pack(pady=5)
        self.player1_path = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.player1_path, width=50).pack(pady=5)
        ttk.Button(left_frame, text="Browse", command=self.browse_file).pack(pady=5)

        # Right frame content (Player 2)
        ttk.Label(right_frame, text="Available Bots:", font=('Helvetica', 10, 'bold')).pack(pady=(5,2))
        
        # Single listbox with scrollbar for all bots
        listbox_frame = ttk.Frame(right_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        
        self.bot_listbox = tk.Listbox(listbox_frame, width=47, height=12)
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.bot_listbox.yview)
        self.bot_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.bot_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_bot_dropdown()
        
        # Create tooltip
        self.tooltip = None
        self.tooltip_id = None  # For managing hide delay
        self.current_item = -1  # Track current item under mouse
        
        # Bind mouse events
        self.bot_listbox.bind('<Motion>', self.schedule_tooltip)
        self.bot_listbox.bind('<Leave>', self.schedule_hide_tooltip)
        
        # Add bot button frame (removed description label)
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="Add Custom Bot", command=self.add_custom_bot).pack(padx=5)

        # Remove old buttons and entry
        self.game_button = None
        self.tournament_button = None
        self.player2_path = None
        self.player2_entry = None

    def add_custom_bot(self):
        filepath = filedialog.askopenfilename(
            title="Select Bot File",
            filetypes=(("Python files", "*.py"), ("All files", "*.*"))
        )
        if filepath:
            try:
                # Try to load the bot to verify it's valid
                spec = importlib.util.spec_from_file_location("custom_bot", filepath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find the bot class
                bot_class = None
                for item in dir(module):
                    obj = getattr(module, item)
                    if isinstance(obj, type) and issubclass(obj, AbstractBot) and obj != AbstractBot:
                        bot_class = obj
                        break
                
                if bot_class:
                    bot_instance = bot_class()
                    display_name = f"{bot_instance.name} (Custom)"
                    self.filename_to_display[display_name] = filepath
                    self.bot_listbox.insert(tk.END, display_name)
                else:
                    messagebox.showerror("Error", "No valid bot class found in file")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load bot: {str(e)}")

    def get_selected_bots(self):
        """Get selected bots (both built-in and custom)"""
        bots = []
        for idx in self.bot_listbox.curselection():
            bot_name = self.bot_listbox.get(idx)
            filepath = self.filename_to_display.get(bot_name)
            if "(Custom)" in bot_name:
                bots.append(filepath)  # Custom bot - use full path
            else:
                # Built-in bot - construct path
                bots.append(os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    'bots',
                    filepath
                ))
        return bots

    def browse_file2(self):
        filename = filedialog.askopenfilename(
            title="Select Bot File",
            filetypes=(("Python files", "*.py"), ("All files", "*.*"))
        )
        if filename:
            self.player2_path.set(filename)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Bot File",
            filetypes=(("Python files", "*.py"), ("All files", "*.*"))
        )
        if filename:
            self.player1_path.set(filename)

    def load_bots(self):
        """Dynamically load bot classes from the bots directory"""
        bots = {}
        bots_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'bots'))
        
        if not os.path.exists(bots_dir):
            os.makedirs(bots_dir)
            print(f"Created bots directory at: {bots_dir}")
            return bots
            
        print(f"Loading bots from: {bots_dir}")
        for filename in os.listdir(bots_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                filepath = os.path.normpath(os.path.join(bots_dir, filename))
                try:
                    print(f"Attempting to load bot from: {filepath}")
                    spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find the bot class in the module
                    for item in dir(module):
                        obj = getattr(module, item)
                        if isinstance(obj, type) and issubclass(obj, AbstractBot) and obj != AbstractBot:
                            bot_instance = obj()
                            bots[filename] = bot_instance
                            print(f"Successfully loaded bot: {bot_instance.name} from {filename}")
                            break
                except Exception as e:
                    print(f"Error loading bot {filename}: {str(e)}")
                    
        return bots

    def update_bot_dropdown(self):
        """Update listbox with bot names"""
        self.bot_listbox.delete(0, tk.END)
        self.filename_to_display = {}
        
        for filename, bot in self.available_bots.items():
            display_name = bot.name
            self.filename_to_display[display_name] = filename
            self.bot_listbox.insert(tk.END, display_name)

    def schedule_tooltip(self, event):
        # Get the item under cursor
        index = self.bot_listbox.nearest(event.y)
        
        # If mouse is over a different item or no tooltip exists
        if index >= 0 and (index != self.current_item or not self.tooltip):
            self.current_item = index
            
            # Cancel any pending hide operations
            if self.tooltip_id:
                self.bot_listbox.after_cancel(self.tooltip_id)
                self.tooltip_id = None
            
            # Show tooltip immediately
            self.show_bot_description(event)

    def schedule_hide_tooltip(self, event):
        # Schedule hiding with a delay
        if self.tooltip_id:
            self.bot_listbox.after_cancel(self.tooltip_id)
        self.tooltip_id = self.bot_listbox.after(500, self.hide_bot_description)  # 500ms delay

    def show_bot_description(self, event):
        # Get the item under cursor
        index = self.bot_listbox.nearest(event.y)
        if index >= 0:
            bot_name = self.bot_listbox.get(index)
            filename = self.filename_to_display.get(bot_name)
            
            # Get description
            description = ""
            if "(Custom)" in bot_name:
                try:
                    spec = importlib.util.spec_from_file_location("custom_bot", filename)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for item in dir(module):
                        obj = getattr(module, item)
                        if isinstance(obj, type) and issubclass(obj, AbstractBot) and obj != AbstractBot:
                            description = obj().description
                            break
                except:
                    description = "Custom bot"
            elif filename in self.available_bots:
                description = self.available_bots[filename].description
            
            # Create or update tooltip
            if description:
                if self.tooltip:
                    self.tooltip.destroy()
                x = self.bot_listbox.winfo_rootx() - 205
                y = self.bot_listbox.winfo_rooty() + event.y
                self.tooltip = tk.Toplevel(self.bot_listbox)
                self.tooltip.wm_overrideredirect(True)
                self.tooltip.wm_geometry(f"+{x}+{y}")
                
                # Add some padding around the text
                frame = ttk.Frame(self.tooltip, style='TFrame')
                frame.pack(fill=tk.BOTH, expand=True)
                
                label = ttk.Label(frame, text=description,
                                background='#2a2a2a', foreground='white',
                                wraplength=200, padding=5)
                label.pack(fill=tk.BOTH, expand=True)

    def hide_bot_description(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        self.current_item = -1
        self.tooltip_id = None

    def start_games(self):
        """Pairwise run, final results in Games_summary.txt."""
        player1_bot = self.player1_path.get()
        if not player1_bot:
            tk.messagebox.showerror("Error", "Please select Player 1 bot")
            return

        opponents = self.get_selected_bots()
        if not opponents:
            tk.messagebox.showerror("Error", "Please select at least one opponent")
            return

        try:
            simulation = PrisonersDilemmaSimulation(player1_bot)
            simulation.run_games(opponents, 100)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Simulation failed: {str(e)}")

    def start_tournament(self):
        """Round-robin tournament, results in Tournament_summary.txt."""
        player1_bot = self.player1_path.get()
        if not player1_bot:
            tk.messagebox.showerror("Error", "Please select Player 1 bot")
            return

        try:
            simulation = TournamentSimulation(player1_bot)
            player1_name = simulation.bot1.name
            
            bot_paths = [player1_bot]
            
            selected_bots = self.get_selected_bots()
            if not selected_bots:
                tk.messagebox.showerror("Error", "Please select at least one opponent")
                return
                
            for bot_path in selected_bots:
                temp_sim = TournamentSimulation(bot_path)
                if temp_sim.bot1.name == player1_name:
                    tk.messagebox.showerror("Error", "Player 1 bot cannot be the same as an opponent bot")
                    return
                bot_paths.append(bot_path)

            simulation.run_all_against_all(bot_paths, 100)
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Tournament failed: {str(e)}")
