
from utils.abstract_bot import AbstractBot
from utils.moves import Move
from typing import List

class GrudgeBot(AbstractBot):
    def __init__(self):
        self.been_betrayed = False
    
    @property
    def name(self) -> str:
        return "Grudge Bot"
    
    @property
    def description(self) -> str:
        return "A bot that never forgives betrayal"
    
    def strategy(self, opponent_history: List[Move]) -> Move:
        if not opponent_history:
            return self.cooperate
            
        if not self.been_betrayed and opponent_history[-1] == Move.DEFECT:
            self.been_betrayed = True
            
        return self.defect if self.been_betrayed else self.cooperate