# Prisoner's Dilemma Tournament Simulator

A desktop application for running Prisoner's Dilemma tournaments with customizable bots. Perfect for educational purposes, hackathons, and exploring game theory concepts through practical simulations.

## Overview

This Python-based tournament simulator brings the classic Prisoner's Dilemma to life, allowing users to:
- Run tournaments between pre-programmed bots
- Create and test custom bot strategies
- Visualize tournament results and game statistics
- Explore different approaches to game theory

## Features

🎮 **Interactive Tournament System**
- Multiple round support
- Real-time scoring and statistics
- Tournament bracket visualization
- Detailed match history tracking

🤖 **Bot Management**
- Easy-to-use bot creation interface
- Pre-built strategy templates
- Custom bot implementation support
- Strategy testing environment

📊 **Analysis Tools**
- Performance metrics tracking
- Strategy effectiveness analysis
- Head-to-head comparison tools
- Tournament history logging and export

## Technologies

- Python 3.8+
- Tkinter (GUI Framework)

## Getting Started

### Prerequisites
```bash
# Python 3.8 or higher required
python --version

# Install Tkinter if not included in your Python distribution
pip install tk
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/prisoners-dilemma-tournament.git

# Navigate to project directory
cd prisoners-dilemma-tournament

# Run the application
python main.py
```

## Creating Custom Bots

Create your own bot by implementing the `AbstractBot` class:

```python
from utils.abstract_bot import AbstractBot
from moves import Move

class MyCustomBot(AbstractBot):
    def name(self) -> str:
        return "CustomBot"

    @property
    def description(self) -> str:
        return "My custom strategy implementation"

    def strategy(self, opponent_history: List[Move]) -> Move:
        # Implement your strategy here
        return Move.COOPERATE
```

## Built-in Strategies

The simulator includes several pre-implemented bots:

- **Always Cooperate**: Consistently chooses cooperation
- **Always Betray**: Consistently chooses betrayal
- **Tit for Tat**: Mirrors the opponent's previous move
- **Random**: Makes random decisions each round
- **Grudger**: Cooperates until betrayed, then always betrays


## Topics

`game-theory` `python` `simulation` `tournament` `prisoners-dilemma` `educational` `bot` `strategy` `tkinter` `desktop-application`
