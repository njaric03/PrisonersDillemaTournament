from utils.abstract_bot import AbstractBot
from utils.moves import Move
from typing import List

class YourBot(AbstractBot):
    """
    Implementacija vašeg bota. Implementirajte svoju strategiju ovde.
    Nasleđuje AbstractBot koji pruža:
    - my_history: Lista vaših prethodnih poteza
    - opponent_history: Lista protivnikovih prethodnih poteza
    - cooperate: Move.COOPERATE (C)
    - defect: Move.DEFECT (D)
    """
    
    @property
    def name(self) -> str:
        """Vraća ime vašeg bota, nije neophodno da bude isto kao ime ekipe"""
        return "Moj bot"
    
    @property
    def description(self) -> str:
        """Vraća opis strategije vašeg bota, ne morate popunjavati"""
        return ""
    
    def strategy(self, my_history: List[Move], opponent_history: List[Move],
            current_round: int, total_rounds: int) -> Move:
        """
        Implementirajte svoju strategiju ovde.
        
        Argumenti:
            my_history: Lista vaših prethodnih poteza
            opponent_history: Lista protivnikovih prethodnih poteza
            current_round: Trenutni broj runde (počinje od 1)
            total_rounds: Ukupan broj rundi u igri
            
        Vraća:
            Move.COOPERATE ili Move.DEFECT
        """
        # Implementacija vaše strategije ovde
        # Primer: Uvek sarađuj
        return self.cooperate
