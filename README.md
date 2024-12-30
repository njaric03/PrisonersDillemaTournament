# Prisoner's Dilemma Tournament App

This is a simple Desktop app designed to simulate tournaments for the classic Prisoner's Dilemma game, making it perfect for small hackathons or tournament-style competitions! You can pit predefined bots against each other or create your own bot to compete in the game. The app is built with Python and Tkinter, so it's easy to use and expand.
## What's It About?

The Prisoner's Dilemma is a classic game theory scenario where two players choose whether to cooperate or betray. It mirrors the Split or Steal dilemma, commonly seen in social and economic models. Your decision affects both your outcome and your opponent’s. In this app, each bot competes in multiple rounds, and the tournament results are calculated by summing the outcomes of each round for all games. The bot with the highest total score across all rounds wins, emphasizing the balance between cooperation, betrayal, and retaliation—an ideal showcase of strategic decision-making in game theory.
## Getting Started

### Requirements

- **Python 3.8+** (comes with Tkinter pre-installed in most cases)
- If you’re using a stripped-down Python version, install Tkinter with:
```bash
  pip install tk
```



## Running the App
### Clone the repo:
```bash
git clone https://github.com/your-username/prisoners-dilemma-tournament.git
cd prisoners-dilemma-tournament
```

### Launch the app:
```bash
python main.py
```



## How to Make Your Own Bot
Bots are built by inheriting from the AbstractBot class. Here's the structure to follow:

```python
from utils.abstract_bot import AbstractBot
from typing import List
from moves import Move  # Enum with "COOPERATE" and "DEFECT"

class HAL9000Bot(AbstractBot):
    def name(self) -> str:
        return "HAL9000"

    @property
    def description(self) -> str:
        return "Cooperates unless betrayed. If betrayed, will retaliate."

    def strategy(self, opponent_history: List[Move]) -> Move:
        # HAL 9000 cooperates unless betrayed in the last round.
        # If betrayed, it retaliates in the next round.
        if opponent_history and opponent_history[-1] == Move.BETRAY:
            return Move.BETRAY
        return Move.COOPERATE
```

### Steps:
Add your bot file (e.g., hal9000_bot.py) to the bots directory.

Your bot must:

- Have a name method: Return your bot's name.
- Optionally override description: A short description of your bot.
- Implement strategy: Define how your bot decides to cooperate or betray based on the opponent's history.


## Predefined Bots
The app comes with several built-in bots:

- AlwaysCooperateBot: Always cooperates.
- AlwaysBetrayBot: Always betrays.
- TitForTatBot: Mirrors the opponent's last move.
- RandomBot: Makes random decisions.
- You can battle these or test your own bot against them.
