from pygame.font import Font
import sys
from pathlib import Path
import os

class Settings:
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (0,0,51)
        # Ship settings
        self.ship_limit = 3
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (102,255,255)
        self.bullets_allowed = 3
        # Alien settings
        self.fleet_drop_speed = 10
        # How quickly the game speeds up
        self.speed_up_scale = 1.2
        self.score_scale = 1.5
        # Font
        if getattr(sys, '_MEIPASS', False):
            font_path = os.path.join(sys._MEIPASS, 'fonts', 'PressStart2P-Regular.ttf')
        else:
            font_path = str(next(Path.cwd().rglob('PressStart2P-Regular.ttf'), None))
        self.pixel_font = Font(font_path, 28)

        self.initialise_dynamic_settings()
    
    def initialise_dynamic_settings(self):
        # Initialising the settings that can change
        self.ship_speed = 2.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.2
        
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        # Increasing the speeds
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.fleet_drop_speed += 1

        self.alien_points = int(self.alien_points * self.score_scale)
    
    def increase_alien_speed(self):
        self.alien_speed *= self.speed_up_scale