from pathlib import Path
import sys

class GameStats:
    """Track statistics for Space Wars."""
    def __init__(self, sw_game):
        """Initialize statistics."""
        self.sw_game = sw_game
        self.settings = sw_game.settings
        self.reset_stats()

        # Determine the correct path for the high_score.txt file
        if hasattr(sys, '_MEIPASS'):
            # If running from the bundled executable
            base_path = Path(sys._MEIPASS)
        else:
            # If running from the script directly
            base_path = Path.cwd()

        # Set the path for high_score.txt
        self.high_score_path = base_path / "space_wars" / 'high_score.txt'

        # Load the high score
        self.high_score = self.read_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def read_high_score(self):
        """Read high score from file, handling empty or invalid content."""
        try:
            with open(self.high_score_path, "r") as file:
                score = file.read().strip()
                if score:
                    return int(score)
                else:
                    return 0
        except (FileNotFoundError, ValueError):
            return 0
        
    def write_high_score(self):
        """Write the high score to a file."""
        with open(self.high_score_path, "w") as file:
            file.write(str(self.high_score))

    def reset_speeds(self):
        """Reset the aliens and stars speeds to the current level's speed."""
        current_speed_factor = 1.2**self.level

        # Reset aliens' speed to current level speed
        self.settings.alien_speed = current_speed_factor

        # Reset stars' speed to match the alien's speed scaling
        self.sw_game.stars.star_speed = current_speed_factor
