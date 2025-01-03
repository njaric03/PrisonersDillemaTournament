import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import time

class TournamentVisualizer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        # Sort dataframe by Average in descending order
        self.df = self.df.sort_values('Average', ascending=False)
        self.current_index = 0  # Start from first (bottom) row
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Tournament Results")
        self.root.state('zoomed')
        
        # Create and configure tree widget
        self.tree = ttk.Treeview(self.root, style='Custom.Treeview')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Configure style for larger rows and font
        style = ttk.Style()
        style.configure('Custom.Treeview', 
                       rowheight=150,  # Increased from 120
                       font=('Arial', 28))  # Increased from 20
        style.configure('Custom.Treeview.Heading',
                       font=('Arial', 32, 'bold'))  # Increased from 24
        
        # Configure columns
        self.tree['columns'] = ['Bot', 'Average']
        self.tree.column('#0', width=0, stretch=False)
        
        for col in ['Bot', 'Average']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=400)
        
        # Configure medal and hidden styles
        self.tree.tag_configure('gold', background='#FFD700', font=('Arial', 32, 'bold'))  # Increased from 24
        self.tree.tag_configure('silver', background='#E6E8FA', font=('Arial', 30, 'bold'))  # Increased from 22
        self.tree.tag_configure('bronze', background='#CD7F32', font=('Arial', 28, 'bold'))  # Increased from 20
        self.tree.tag_configure('hidden', background='white', foreground='white')
        
        # Load all rows initially as hidden
        self.load_hidden_rows()
        
        # Bind spacebar to reveal next row
        self.root.bind('<space>', self.reveal_next)

    def load_hidden_rows(self):
        """Load all rows initially but hide them"""
        # Load in descending order (best scores first)
        for index in range(len(self.df)):
            row = self.df.iloc[index]
            values = [row['Bot'], row['Average']]
            self.tree.insert('', 'end', values=values, tags=('hidden',))

    def reveal_next(self, event):
        """Reveal next row when spacebar is pressed"""
        if self.current_index < len(self.df):
            # Get all items and reveal from bottom
            items = self.tree.get_children()
            item_to_reveal = items[-(self.current_index + 1)]  # Start from bottom
            
            # Apply appropriate medal tag
            if self.current_index == len(self.df) - 1:  # First place (revealed last)
                self.tree.item(item_to_reveal, tags=('gold',))
            elif self.current_index == len(self.df) - 2:  # Second place
                self.tree.item(item_to_reveal, tags=('silver',))
            elif self.current_index == len(self.df) - 3:  # Third place
                self.tree.item(item_to_reveal, tags=('bronze',))
            else:
                self.tree.item(item_to_reveal, tags=())
            
            self.current_index += 1

    def show(self):
        self.root.mainloop()
