from utils.abstract_bot import AbstractBot
from utils.moves import Move
from typing import List

class AlwaysCooperateBot(AbstractBot):
    def __init__(self):
        super().__init__()
        self._name = "Always Cooperate Bot"
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return "A bot that always cooperates"
    
    def strategy(self, my_history: List[Move], opponent_history: List[Move], current_round: int, total_rounds: int) -> Move:
        return self.cooperate