import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, sw_game):
        # Create a bullet object at the ships current position
        super().__init__()
        self.screen = sw_game.screen
        self.settings = sw_game.settings
        self.colour = self.settings.bullet_colour

        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = sw_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        # Move bullet up screen
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw bullet on screen
        pygame.draw.rect(self.screen, self.colour, self.rect)
