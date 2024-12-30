from datetime import datetime
import os
from utils.abstract_bot import AbstractBot
from utils.moves import Move
import importlib.util

class TournamentSimulation:
    def __init__(self):
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.logs_dir, exist_ok=True)

    def load_bot(self, bot_path):
        """Load a bot from a file path."""
        try:
            spec = importlib.util.spec_from_file_location("bot_module", bot_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            for item in dir(module):
                obj = getattr(module, item)
                if isinstance(obj, type) and issubclass(obj, AbstractBot) and obj != AbstractBot:
                    return obj()
            raise ValueError("No valid bot class found in file")
        except Exception as e:
            raise Exception(f"Failed to load bot: {str(e)}")

    def run_all_against_all(self, bot_paths, rounds=100):
        """Conduct a round-robin tournament where each bot plays against each other."""
        timestamp = datetime.now().strftime("%H%M")
        tournament_dir = os.path.join(self.logs_dir, f"{timestamp}_tournament")
        os.makedirs(tournament_dir)

        # Track scores and statistics
        scores = {}
        matches_played = {}
        stats = {
            'mutual_cooperation': 0,
            'mutual_defection': 0,
            'betrayals': {}  # Will track betrayals per bot
        }

        # Run matches between all pairs of bots
        for i, bot1_path in enumerate(bot_paths):
            bot1 = self.load_bot(bot1_path)
            stats['betrayals'][bot1.name] = 0
            
            for j, bot2_path in enumerate(bot_paths[i+1:], i+1):
                bot2 = self.load_bot(bot2_path)
                if j == i: continue  # Skip self-play
                
                if bot2.name not in stats['betrayals']:
                    stats['betrayals'][bot2.name] = 0

                # Initialize scores if needed
                for bot_name in [bot1.name, bot2.name]:
                    scores.setdefault(bot_name, 0)
                    matches_played.setdefault(bot_name, 0)

                # Run match
                match_stats = self._run_match(bot1, bot2, rounds, tournament_dir)
                
                # Update scores and statistics
                scores[bot1.name] += match_stats['scores'][bot1.name]
                scores[bot2.name] += match_stats['scores'][bot2.name]
                matches_played[bot1.name] += 1
                matches_played[bot2.name] += 1
                
                stats['mutual_cooperation'] += match_stats['mutual_cooperation']
                stats['mutual_defection'] += match_stats['mutual_defection']
                stats['betrayals'][bot1.name] += match_stats['betrayals'][bot1.name]
                stats['betrayals'][bot2.name] += match_stats['betrayals'][bot2.name]

        self._write_tournament_summary(tournament_dir, scores, stats, matches_played, rounds)
        return tournament_dir

    def _run_match(self, bot1, bot2, rounds, tournament_dir):
        """Run a single match between two bots and return match statistics."""
        scores = {bot1.name: 0, bot2.name: 0}
        stats = {
            'mutual_cooperation': 0,
            'mutual_defection': 0,
            'betrayals': {bot1.name: 0, bot2.name: 0}
        }
        
        # Reset bot histories at start of match
        bot1.my_history = []
        bot1.opponent_history = []
        bot2.my_history = []
        bot2.opponent_history = []
        
        # Play rounds
        for _ in range(rounds):
            # Get moves using proper AbstractBot interface
            move1 = bot1.make_decision()
            move2 = bot2.make_decision()
            
            # Update both bots' history
            bot1.update_history(move1, move2)
            bot2.update_history(move2, move1)
            
            # Update scores and stats
            if move1 == Move.COOPERATE and move2 == Move.COOPERATE:
                scores[bot1.name] += 3
                scores[bot2.name] += 3
                stats['mutual_cooperation'] += 1
            elif move1 == Move.COOPERATE and move2 == Move.DEFECT:
                scores[bot2.name] += 5
                stats['betrayals'][bot2.name] += 1
            elif move1 == Move.DEFECT and move2 == Move.COOPERATE:
                scores[bot1.name] += 5
                stats['betrayals'][bot1.name] += 1
            else:  # Both defect
                scores[bot1.name] += 1
                scores[bot2.name] += 1
                stats['mutual_defection'] += 1
        
        # Write match results to file
        match_file = os.path.join(tournament_dir, f"{bot1.name}_vs_{bot2.name}.txt")
        with open(match_file, 'w') as f:
            f.write(f"Match: {bot1.name} vs {bot2.name}\n")
            f.write(f"Scores: {bot1.name}: {scores[bot1.name]}, {bot2.name}: {scores[bot2.name]}\n")
            f.write(f"Mutual Cooperation: {stats['mutual_cooperation']}\n")
            f.write(f"Mutual Defection: {stats['mutual_defection']}\n")
            f.write(f"Betrayals by {bot1.name}: {stats['betrayals'][bot1.name]}\n")
            f.write(f"Betrayals by {bot2.name}: {stats['betrayals'][bot2.name]}\n")
        
        return {
            'scores': scores,
            'mutual_cooperation': stats['mutual_cooperation'],
            'mutual_defection': stats['mutual_defection'],
            'betrayals': stats['betrayals']
        }

    def _write_tournament_summary(self, directory, scores, stats, matches_played, rounds_per_match):
        summary_path = os.path.join(directory, "tournament_summary.txt")
        with open(summary_path, 'w') as f:
            f.write("="*50 + "\n")
            f.write("TOURNAMENT SUMMARY\n")
            f.write("="*50 + "\n\n")

            # Leaderboard
            f.write("LEADERBOARD\n")
            f.write("-"*50 + "\n")
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for bot, score in sorted_scores:
                avg_score = score / matches_played[bot]
                f.write(f"{bot}: {score} (avg per match: {avg_score:.1f})\n")

            # Aggregate statistics
            total_matches = sum(matches_played.values()) // 2
            f.write("\n\nAGGREGATE STATISTICS\n")
            f.write("-"*50 + "\n")
            f.write(f"Total Matches: {total_matches}\n")
            f.write(f"Average Mutual Cooperation: {stats['mutual_cooperation']/total_matches:.1f} per match\n")
            f.write(f"Average Mutual Defection: {stats['mutual_defection']/total_matches:.1f} per match\n")
            f.write(f"Average Bot Betrayals: {sum(stats['betrayals'].values())/total_matches:.1f} per match\n")

