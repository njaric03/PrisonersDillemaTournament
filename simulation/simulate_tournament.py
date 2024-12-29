from datetime import datetime
import os
from .simulate_games import PrisonersDilemmaSimulation
from utils.moves import Move

class TournamentSimulation(PrisonersDilemmaSimulation):
    def __init__(self, bot1_path):  # Add bot1_path parameter
        super().__init__(bot1_path)  # Pass bot1_path to parent
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.logs_dir, exist_ok=True)

    def run_all_against_all(self, bot_paths, rounds=100):
        """
        Conduct a round-robin where each bot plays against each other.
        """
        timestamp = datetime.now().strftime("%H%M")
        tournament_dir = os.path.join(self.logs_dir, f"{timestamp}_tournament")
        os.makedirs(tournament_dir)

        # Create subdirectories for logs
        player_dir = os.path.join(tournament_dir, "player_games")
        others_dir = os.path.join(tournament_dir, "other_games")
        os.makedirs(player_dir)
        os.makedirs(others_dir)

        # Track scores and statistics
        scores = {}
        matches_played_by = {}
        all_stats = {
            'mutual_cooperation': 0,
            'mutual_defection': 0,
            'bot1_betrayals': 0,
            'opponent_betrayals': 0
        }

        # Store the player's bot name for comparison
        player_bot_name = self.bot1.name
        
        # Run matches between all pairs of bots
        for i, bot1_path in enumerate(bot_paths):
            bot1 = self.load_bot(bot1_path)
            for bot2_path in bot_paths[i+1:]:  # Start from i+1 to avoid duplicate matches
                bot2 = self.load_bot(bot2_path)
                
                # Initialize scores if needed
                scores.setdefault(bot1.name, 0)
                scores.setdefault(bot2.name, 0)
                matches_played_by.setdefault(bot1.name, 0)
                matches_played_by.setdefault(bot2.name, 0)

                # Determine log directory by comparing with player's bot name
                is_player_game = (bot1.name == player_bot_name or bot2.name == player_bot_name)
                log_dir = player_dir if is_player_game else others_dir

                # Run match
                self.bot1 = bot1
                self.bot2 = bot2
                self.history1 = []
                self.history2 = []
                self.scores = {bot1.name: 0, bot2.name: 0}

                stats = self._run_match(rounds, log_dir, bot2.name)

                # Update scores and statistics
                scores[bot1.name] += self.scores[bot1.name]
                scores[bot2.name] += self.scores[bot2.name]
                matches_played_by[bot1.name] += 1
                matches_played_by[bot2.name] += 1

                for key in all_stats:
                    all_stats[key] += stats[key]

        self._write_tournament_summary(tournament_dir, scores, all_stats, matches_played_by, rounds)
        print(f"Tournament complete. Results saved to {tournament_dir}")

    def _write_tournament_summary(self, directory, scores, stats, matches_played_by, rounds_per_match):
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
                avg_score = score / matches_played_by[bot]
                f.write(f"{bot}: {score} (avg per match: {avg_score:.1f})\n")

            # Aggregate statistics
            total_matches = sum(matches_played_by.values()) // 2
            f.write("\n\nAGGREGATE STATISTICS\n")
            f.write("-"*50 + "\n")
            f.write(f"Total Matches: {total_matches}\n")
            f.write(f"Average Mutual Cooperation: {stats['mutual_cooperation']/total_matches:.1f} per match\n")
            f.write(f"Average Mutual Defection: {stats['mutual_defection']/total_matches:.1f} per match\n")
            f.write(f"Average Bot Betrayals: {stats['bot1_betrayals']/total_matches:.1f} per match\n")
            f.write(f"Average Opponent Betrayals: {stats['opponent_betrayals']/total_matches:.1f} per match\n")

