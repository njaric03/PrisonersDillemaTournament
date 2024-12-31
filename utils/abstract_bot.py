from abc import ABC, abstractmethod
from utils.moves import Move
from typing import List

class AbstractBot(ABC):
    def __init__(self):
        self.my_history = []
        self.opponent_history = []
        self.total_rounds = 0  # Add this line
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def description(self) -> str:
        return ""  # Default empty description
    
    @abstractmethod
    def strategy(self, opponent_history: List[Move], current_round: int, total_rounds: int) -> Move:
        pass
    
    @property
    def cooperate(self) -> Move:
        return Move.COOPERATE
        
    @property
    def defect(self) -> Move:
        return Move.DEFECT
        
    def make_decision(self) -> Move:  # Remove total_rounds parameter
        """Make a decision based on strategy and history"""
        current_round = len(self.my_history) + 1
        decision = self.strategy(self.opponent_history, current_round, self.total_rounds)
        return decision
        
    def update_history(self, my_move: Move, opponent_move: Move):
        """Update the history of moves"""
        self.my_history.append(my_move)
        self.opponent_history.append(opponent_move)