import pygame
from pygame.sprite import Sprite
from pathlib import Path
import sys

class Alien(Sprite):
    def __init__(self, sw_game):
        # Initialise the alien and set the starting position
        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings

        # Determine the correct path for the image file
        if hasattr(sys, '_MEIPASS'):
            # If running from the bundled executable
            base_path = Path(sys._MEIPASS)
        else:
            # If running from the script directly
            base_path = Path.cwd()

        # Load the alien image and set rect
        alien_image_path = base_path / "space_wars" / 'images' / 'alien3.bmp'
        self.image = pygame.image.load(str(alien_image_path))
        self.rect = self.image.get_rect()

        # Start each alien by top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return True if alien at edge of screen
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        # Move aliens to the right
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
