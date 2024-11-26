import pygame
from pygame.sprite import Sprite
from pathlib import Path
import sys

class Ship(Sprite):
    def __init__(self, sw_game):
        super().__init__()

        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.screen_rect = sw_game.screen.get_rect()

        # Determine the correct path for the image file
        if hasattr(sys, '_MEIPASS'):
            # If running from the bundled executable
            base_path = Path(sys._MEIPASS)
        else:
            # If running from the script directly
            base_path = Path.cwd()

        # Load the ship image and get its rect
        ship_image_path = base_path / "space_wars" / 'images' / 'ship3.bmp'
        self.image = pygame.image.load(str(ship_image_path))
        self.rect = self.image.get_rect()

        # Starting location of the ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's position
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def centre_ship(self):
        """Center the ship at the bottom of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
