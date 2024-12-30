import importlib.util
from utils.abstract_bot import AbstractBot
from utils.moves import Move
from datetime import datetime
import os

class PrisonersDilemmaSimulation:
    def __init__(self, bot1_path):
        self.bot1 = self.load_bot(bot1_path)
        
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def load_bot(self, path):
        """Load a bot from a file path"""
        try:
            spec = importlib.util.spec_from_file_location("bot_module", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            for item in dir(module):
                obj = getattr(module, item)
                if isinstance(obj, type) and issubclass(obj, AbstractBot) and obj != AbstractBot:
                    return obj()
            raise ValueError("No valid bot class found in file")
        except Exception as e:
            raise Exception(f"Error loading bot from {path}: {e}")

    def calculate_score(self, move1: Move, move2: Move):
        """Calculate scores based on moves"""
        if move1 == Move.COOPERATE and move2 == Move.COOPERATE:
            return 3, 3
        elif move1 == Move.COOPERATE and move2 == Move.DEFECT:
            return 0, 5
        elif move1 == Move.DEFECT and move2 == Move.COOPERATE:
            return 5, 0
        else:  # both defect
            return 1, 1

    def run_games(self, opponent_paths, rounds=100):
        """Run games against multiple opponents."""
        timestamp = datetime.now().strftime("%H%M")
        games_dir = os.path.join(self.logs_dir, f"{timestamp}_{self.bot1.name}_games")
        os.makedirs(games_dir)

        all_stats = []
        for opponent_path in opponent_paths:
            # Load opponent bot
            opponent = self.load_bot(opponent_path)
            
            # Run the match and collect stats
            match_stats = self._run_match(opponent, rounds, games_dir)
            all_stats.append({
                'opponent': opponent.name,
                'stats': match_stats
            })

        # Write summary of all games
        self._write_games_summary(games_dir, all_stats)
        print(f"Games complete. Results saved to {games_dir}")

    def _run_match(self, opponent, rounds, tournament_dir):
        stats = {
            'mutual_cooperation': 0,
            'mutual_defection': 0,
            'bot1_betrayals': 0,
            'opponent_betrayals': 0,
            'scores': {self.bot1.name: 0, opponent.name: 0}
        }

        timestamp = datetime.now().strftime("%H%M")
        log_filename = f"{timestamp}_vs_{opponent.name}.txt"
        log_path = os.path.join(tournament_dir, log_filename)

        output_lines = []
        output_lines.extend([
            "="*50,
            f"MATCH RESULTS - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"Bot 1: {self.bot1.name}",
            f"Bot 2: {opponent.name}",
            "="*50,
            ""
        ])

        output_lines.extend([
            "ROUND HISTORY:",
            f"{'Round':^6} | {'Bot 1':^10} | {'Bot 2':^10} | {'Score':^12}",
            "-"*42
        ])

        for round_num in range(rounds):
            move1 = self.bot1.strategy([])
            move2 = opponent.strategy([])

            score1, score2 = self.calculate_score(move1, move2)
            stats['scores'][self.bot1.name] += score1
            stats['scores'][opponent.name] += score2

            if move1 == Move.COOPERATE and move2 == Move.COOPERATE:
                stats['mutual_cooperation'] += 1
            elif move1 == Move.DEFECT and move2 == Move.DEFECT:
                stats['mutual_defection'] += 1
            elif move1 == Move.DEFECT and move2 == Move.COOPERATE:
                stats['bot1_betrayals'] += 1
            else:
                stats['opponent_betrayals'] += 1

            output_lines.append(f"{round_num+1:^6} | {move1.name:^10} | {move2.name:^10} | {score1:^5}-{score2:^5}")

        scores_section = [
            "SCORES:",
            "-"*50,
            f"{self.bot1.name}: {stats['scores'][self.bot1.name]}",
            f"{opponent.name}: {stats['scores'][opponent.name]}",
            "-"*50,
            ""
        ]
        output_lines[6:6] = scores_section

        output_lines.extend([
            "\nMATCH STATISTICS:",
            "-"*50,
            f"Total Rounds: {rounds}",
            f"Mutual Cooperation: {stats['mutual_cooperation']} ({stats['mutual_cooperation']/rounds*100:.1f}%)",
            f"Mutual Defection: {stats['mutual_defection']} ({stats['mutual_defection']/rounds*100:.1f}%)",
            f"Bot 1 Betrayals: {stats['bot1_betrayals']} ({stats['bot1_betrayals']/rounds*100:.1f}%)",
            f"Opponent Betrayals: {stats['opponent_betrayals']} ({stats['opponent_betrayals']/rounds*100:.1f}%)",
            "",
            "FINAL SCORES:",
            "-"*50,
            f"{self.bot1.name}: {stats['scores'][self.bot1.name]}",
            f"{opponent.name}: {stats['scores'][opponent.name]}",
            "="*50
        ])

        with open(log_path, 'w') as log_file:
            log_file.write('\n'.join(output_lines))

        return stats

    def _write_games_summary(self, directory, all_stats):
        """Write a summary of all games played."""
        summary_path = os.path.join(directory, "games_summary.txt")
        with open(summary_path, 'w') as f:
            f.write("="*50 + "\n")
            f.write(f"MULTIPLE GAMES SUMMARY\n")
            f.write(f"Player: {self.bot1.name}\n")
            f.write("="*50 + "\n\n")

            for stat in all_stats:
                opponent = stat['opponent']
                stats = stat['stats']
                f.write(f"Against {opponent}:\n")
                f.write("-"*30 + "\n")
                f.write(f"Score: {stats['scores'][self.bot1.name]}\n")
                f.write(f"Mutual Cooperation: {stats['mutual_cooperation']}\n")
                f.write(f"Mutual Defection: {stats['mutual_defection']}\n")
                f.write(f"Times Betrayed: {stats['opponent_betrayals']}\n")
                f.write(f"Times Betrayed Opponent: {stats['bot1_betrayals']}\n\n")

            # Overall statistics
            f.write("\nOVERALL STATISTICS\n")
            f.write("-"*30 + "\n")
            total_games = len(all_stats)
            total_score = sum(s['stats']['scores'][self.bot1.name] for s in all_stats)
            avg_score = total_score / total_games
            f.write(f"Total Games: {total_games}\n")
            f.write(f"Total Score: {total_score}\n")
            f.write(f"Average Score: {avg_score:.1f}\n")
