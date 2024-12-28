import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import importlib.util
from utils.abstract_bot import AbstractBot
from simulation.simulate_tournament import TournamentSimulation
from simulation.simulate_games import PrisonersDilemmaSimulation

class PrisonersDilemmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Prisoner's Dilemma Simulator")
        
        # Configure dark theme
        self.root.configure(bg='#1a1a1a')  # Darker background
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabelframe', background='#1a1a1a', foreground='white')
        style.configure('TLabelframe.Label', background='#1a1a1a', foreground='white')
        style.configure('TLabel', background='#1a1a1a', foreground='white')
        # Removed custom button styling
        style.configure('TRadiobutton', background='#1a1a1a', foreground='white')
        
        # Make window full screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for side-anchored frames
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)  # Left frame
        main_frame.grid_columnconfigure(1, weight=3)  # Center space
        main_frame.grid_columnconfigure(2, weight=0)  # Right frame
        main_frame.grid_rowconfigure(0, weight=1)

        # Create left and right frames
        left_frame = ttk.LabelFrame(main_frame, text="Player 1", padding="10")
        right_frame = ttk.LabelFrame(main_frame, text="Player 2", padding="10")

        # Anchor frames to sides
        left_frame.grid(row=0, column=0, sticky="nsw", padx=20)
        right_frame.grid(row=0, column=2, sticky="nse", padx=20)

        # Left frame content (Player 1)
        ttk.Label(left_frame, text="Select Bot File:").pack(pady=5)
        self.player1_path = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.player1_path, width=50).pack(pady=5)
        ttk.Button(left_frame, text="Browse", command=self.browse_file).pack(pady=5)

        # Right frame content (Player 2)
        # Radio buttons for selection type
        self.player2_choice = tk.StringVar(value="existing")
        ttk.Radiobutton(right_frame, text="Choose Existing Bot", 
                       variable=self.player2_choice, value="existing",
                       command=self.toggle_player2_choice).pack(pady=5)
        ttk.Radiobutton(right_frame, text="Custom Bot", 
                       variable=self.player2_choice, value="custom",
                       command=self.toggle_player2_choice).pack(pady=5)

        # Load bots and create listbox
        self.available_bots = self.load_bots()
        self.filename_to_display = {}  # Move this here as class property

        # Replace Combobox with Listbox for multiple selection
        self.bot_listbox = tk.Listbox(right_frame, width=47, selectmode=tk.MULTIPLE)
        self.bot_listbox.pack(pady=5)
        self.update_bot_dropdown()  # Call this immediately after creating listbox
        self.bot_listbox.bind('<<ListboxSelect>>', self.update_bot_description)

        # Bot description label (remove duplicate)
        self.bot_description = ttk.Label(right_frame, text="", wraplength=300)
        self.bot_description.pack(pady=10)

        # Custom bot file selection
        self.player2_path = tk.StringVar()
        self.player2_entry = ttk.Entry(right_frame, textvariable=self.player2_path, width=50)
        self.player2_button = ttk.Button(right_frame, text="Browse", command=self.browse_file2)
        # Initially hidden
        
        # Replace single "Start Simulation" with two buttons:
        ttk.Button(main_frame, text="Start Games", 
                   command=self.start_games).grid(row=1, column=0, 
                                                   columnspan=3, pady=10)
        ttk.Button(main_frame, text="Start Tournament",
                   command=self.start_tournament).grid(row=2, column=0,
                                                       columnspan=3, pady=10)

    def toggle_player2_choice(self):
        if self.player2_choice.get() == "existing":
            self.bot_listbox.pack(pady=5)
            self.player2_entry.pack_forget()
            self.player2_button.pack_forget()
        else:
            self.bot_listbox.pack_forget()
            self.player2_entry.pack(pady=5)
            self.player2_button.pack(pady=5)

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
        bots_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), 'bots'))
        
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

    def update_bot_description(self, event=None):
        """Update description based on selected bot"""
        selection = self.bot_listbox.curselection()
        if selection:
            selected_bot = self.bot_listbox.get(selection[0])
            filename = self.filename_to_display.get(selected_bot)
            if filename in self.available_bots:
                description = self.available_bots[filename].description
                self.bot_description.config(text=description)

    def start_games(self):
        """Pairwise run, final results in Games_summary.txt."""
        player1_bot = self.player1_path.get()
        if not player1_bot:
            tk.messagebox.showerror("Error", "Please select Player 1 bot")
            return
        try:
            if self.player2_choice.get() == "existing":
                selected_indices = self.bot_listbox.curselection()
                if not selected_indices:
                    tk.messagebox.showerror("Error", "Please select at least one opponent")
                    return
                opponents = []
                for idx in selected_indices:
                    bot_name = self.bot_listbox.get(idx)
                    bot_path = os.path.join(
                        os.path.dirname(__file__),
                        'bots',
                        self.filename_to_display.get(bot_name)
                    )
                    opponents.append(bot_path)
            else:
                opponents = [self.player2_path.get()]
                if not opponents[0]:
                    tk.messagebox.showerror("Error", "Please select opponent bot")
                    return

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
            # Load player's bot first to get its name
            simulation = TournamentSimulation(player1_bot)
            player1_name = simulation.bot1.name
            
            # Collect all bot paths
            bot_paths = [player1_bot]  # Start with player1's bot
            
            if self.player2_choice.get() == "existing":
                selected_indices = self.bot_listbox.curselection()
                if not selected_indices:
                    tk.messagebox.showerror("Error", "Please select at least one opponent")
                    return
                    
                for idx in selected_indices:
                    bot_name = self.bot_listbox.get(idx)
                    if bot_name == player1_name:
                        tk.messagebox.showerror("Error", "Player 1 bot cannot be the same as an opponent bot")
                        return
                    bot_path = os.path.join(
                        os.path.dirname(__file__),
                        'bots',
                        self.filename_to_display.get(bot_name)
                    )
                    bot_paths.append(bot_path)
            else:
                opponent_path = self.player2_path.get()
                if not opponent_path:
                    tk.messagebox.showerror("Error", "Please select opponent bot")
                    return
                # Load opponent bot to check name
                temp_sim = TournamentSimulation(opponent_path)
                if temp_sim.bot1.name == player1_name:
                    tk.messagebox.showerror("Error", "Player 1 bot cannot be the same as an opponent bot")
                    return
                bot_paths.append(opponent_path)

            simulation.run_all_against_all(bot_paths, 100)
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Tournament failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')  # For Windows
    app = PrisonersDilemmaGUI(root)
    root.mainloop()  # Remove duplicate mainloop call