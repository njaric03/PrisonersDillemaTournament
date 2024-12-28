from abc import ABC, abstractmethod
from utils.moves import Move
from typing import List

class AbstractBot(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def description(self) -> str:
        return ""  # Default empty description
    
    @abstractmethod
    def strategy(self, opponent_history: List[Move]) -> Move:
        pass
    
    @property
    def cooperate(self) -> Move:
        return Move.COOPERATE
        
    @property
    def defect(self) -> Move:
        return Move.DEFECT