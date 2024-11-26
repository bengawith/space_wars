import sys
import os
from time import sleep
import pygame
from pathlib import Path

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from stars import Stars


class SpaceWars:
    def __init__(self):
        # Initialising the game and creating resources
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self._load_sounds()

        # Set to full screen mode or windowed mode for testing
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Space Wars")
        
        if getattr(sys, '_MEIPASS', False):
            font_path = os.path.join(sys._MEIPASS, 'fonts', 'PressStart2P-Regular.ttf')
        else:
            font_path = str(next(Path.cwd().rglob('PressStart2P-Regular.ttf'), None))

        self.game_font = font_path

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = Stars(self.screen, self.settings)

        self.game_active = False
        self.paused = False
        self.mute = False
        self.start_screen = True
        self.game_over = False

        self.processed_columns = set()

        self._create_fleet()

        self.play_button = Button(self, "Play")
        

    def run_game(self):
        """Main game loop."""
        while True:
            # Checking keyboard and mouse events
            self._check_events()

            if self.game_active and not self.paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.stars.update_stars()

            self._update_screen()
            self.clock.tick(60)
    

    def _load_sounds(self):
       """Load all sound effects and music."""
       
       if hasattr(sys, '_MEIPASS'):
           # If running from the bundled executable
           base_path = Path(sys._MEIPASS)
       else:
           # If running from the script directly
           base_path = Path.cwd()
       # Load sounds with correct path resolution
       bullet = base_path  / "space_wars" / "sounds" / "bullet.wav"
       alien_hit = base_path / "space_wars" / "sounds" / "alien_hit.wav"
       ship_hit = base_path / "space_wars" / "sounds" / "ship_hit.wav"
       game_over = base_path / "space_wars" / "sounds" / "game_over.ogg"
       play = base_path / "space_wars" / "sounds" / "play.wav"
       background_music = base_path / "space_wars" / "sounds" / "background_music.wav"
       
       # Set paths
       self.bullet_sound = pygame.mixer.Sound(str(bullet))
       self.alien_hit_sound = pygame.mixer.Sound(str(alien_hit))
       self.ship_hit_sound = pygame.mixer.Sound(str(ship_hit))
       self.game_over_sound = pygame.mixer.Sound(str(game_over))
       self.play_sound = pygame.mixer.Sound(str(play))
       # Load background music
       pygame.mixer.music.load(str(background_music))
       
    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _start_game(self):
        if self.game_over:
            self.game_over_sound.stop()
            self.game_over = False
        if self.start_screen:
            self.start_screen = False

        self.play_sound.play()
        self.settings.initialise_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.game_active = True
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

        self.processed_columns.clear()
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        
        self.ship.centre_ship()
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            if self.start_screen:
                self._start_game()
                self.start_screen = False
            elif not self.game_active:
                self._start_game()

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RETURN:
            self._start_game()
        elif event.key == pygame.K_p:
            self._toggle_pause()
            if not self.mute:    
                self._toggle_mute()
            else:
                self._toggle_mute()
        elif event.key == pygame.K_m:
            self._toggle_mute()
        elif event.key == pygame.K_q:
            self.stats.write_high_score()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _toggle_pause(self):
        """Toggle the paused state."""
        if self.game_active:
            # Toggle the paused state
            self.paused = not self.paused 

    def _toggle_mute(self):
        """Toggle the mute state."""
        self.mute = not self.mute  # Toggle the mute state
    
        if self.mute:
            # Mute both background music and sound effects
            pygame.mixer.music.set_volume(0)  # Mute music
            self.bullet_sound.set_volume(0)  # Mute sound effects
            self.alien_hit_sound.set_volume(0)
            self.ship_hit_sound.set_volume(0)
            self.game_over_sound.set_volume(0)
            self.play_sound.set_volume(0)
        else:
            # Unmute both background music and sound effects
            pygame.mixer.music.set_volume(0.75)  # Restore music volume
            self.bullet_sound.set_volume(1)  # Restore sound effects volume
            self.alien_hit_sound.set_volume(1)
            self.ship_hit_sound.set_volume(1)
            self.game_over_sound.set_volume(1)
            self.play_sound.set_volume(1)
  

    def _fire_bullet(self):
        """Fire a bullet if limit not reached."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            # Play bullet firing sound
            self.bullet_sound.play()

    def _update_bullets(self):
        """Update position of bullets and remove old bullets."""
        self.bullets.update()
        # Remove bullets that have disappeared off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_collisions()

    def _check_collisions(self):
        """Check for any bullets that hit aliens and remove both."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():    
                self.stats.score += self.settings.alien_points * len(aliens)
                self.alien_hit_sound.play()
                self._check_outer_columns()

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.settings.increase_alien_speed()
            self.stars.increase_speed(1.2)
            self.sb.check_high_score()
            self.stats.level += 1
            self.processed_columns.clear()
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to ship being hit by alien."""

        self.ship_hit_sound.play()

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Empty bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.centre_ship()

            # Pause
            sleep(1.5)
        else:
            self.game_active = False
            self.game_over = True
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if fleet is at edge and update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create a fleet of aliens and reset column destruction flags."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        self.alien_columns = {}

        current_x, current_y = alien_width, alien_height * 2
        column_index = 0
        while current_y < (self.settings.screen_height - 4 * alien_height):
            column_index = 0
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                if column_index not in self.alien_columns:
                    self.alien_columns[column_index] = []
                self.alien_columns[column_index].append(self.aliens.sprites()[-1])
                current_x += 2 * alien_width
                column_index += 1

            current_x = alien_width
            current_y += 2 * alien_height

        # Reset the column destruction flags
        self.left_column_destroyed = False
        self.right_column_destroyed = False

        self.stats.reset_speeds()

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_outer_columns(self):
        """Check if the outermost columns are destroyed and increase speed accordingly."""
        if not self.aliens:
            return

        # Get the current leftmost and rightmost column indices
        leftmost_column = min(self.alien_columns.keys())
        rightmost_column = max(self.alien_columns.keys())

        # Check if all aliens in the leftmost or rightmost column are destroyed
        leftmost_column_destroyed = all(alien not in self.aliens for alien in self.alien_columns[leftmost_column])
        rightmost_column_destroyed = all(alien not in self.aliens for alien in self.alien_columns[rightmost_column])

        # Increase speed if the leftmost column is destroyed and hasn't already been handled
        if leftmost_column_destroyed and leftmost_column not in self.processed_columns:
            self.settings.increase_alien_speed()
            self.stars.increase_speed(1.2)
            del self.alien_columns[leftmost_column]  # Remove destroyed column
            self.processed_columns.add(leftmost_column)  # Mark this column as processed

        # Increase speed if the rightmost column is destroyed and hasn't already been handled
        if rightmost_column_destroyed and rightmost_column not in self.processed_columns:
            self.settings.increase_alien_speed()
            self.stars.increase_speed(1.2)
            del self.alien_columns[rightmost_column]  # Remove destroyed column
            self.processed_columns.add(rightmost_column)  # Mark this column as processed

    
    def _start_screen(self):
        """Display the start screen with a translucent overlay."""
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(180)
        overlay.fill(self.settings.bg_colour) 
        self.screen.blit(overlay, (0, 0))

        font_big = pygame.font.Font(self.game_font, 80)
        font_small = pygame.font.Font(self.game_font, 40)
        font_tiny = pygame.font.SysFont(None, 24)

        welcome_text = font_small.render("Welcome to...", True, (255, 255, 255))
        game_title = font_big.render("Space Wars", True, (170, 250, 50))
        instructions_text = font_tiny.render("Press: 'left key' to go left, 'right key' to go right, 'space' to shoot, 'enter' or click PLAY to start, 'p' to pause, 'q' to quit, 'm' to mute", True, (155, 255, 255))

        welcome_rect = welcome_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 150))
        title_rect = game_title.get_rect(center=self.screen.get_rect().center)
        instructions_rect = instructions_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().bottom - 20))

        self.screen.blit(welcome_text, welcome_rect)
        self.screen.blit(game_title, title_rect)
        self.screen.blit(instructions_text, instructions_rect)

        self.play_button.set_position(self.screen.get_rect().centerx, title_rect.bottom + 50)
        self.play_button.draw_button()
    
    def _draw_pause_overlay(self):
        """Draw a translucent overlay and a pause symbol when the game is paused."""
        # Create a translucent grey overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(128)  # Set transparency (0 fully transparent, 255 fully opaque)
        overlay.fill((100, 100, 100))  # Fill with grey color
        self.screen.blit(overlay, (0, 0))

        # Draw pause symbol (e.g., two vertical bars)
        pause_font = pygame.font.Font(self.game_font, 50)
        pause_text = pause_font.render("||", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(pause_text, pause_rect)

    def _game_over(self):
        """Display the game over message and the final score."""
        # Stop background music and play game over sound
        pygame.mixer.music.stop()
        self.game_over_sound.play()

        # Create overlay for game over message
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))
        self.screen.blit(overlay, (0, 0))

        game_over_font = pygame.font.Font(self.game_font, 80)
        # Use the font for game over text
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 100))

        # Display final score in font
        final_score_text = self.settings.pixel_font.render(f"Final Score: {self.stats.score:,}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(self.screen.get_rect().center))

        # Draw the Game Over text and final score
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, final_score_rect)

        # Adjust the "Play Again" button position below the final score
        self.play_button.set_position(self.screen.get_rect().centerx, final_score_rect.bottom + 50)  # Place below score
        self.play_button.draw_button()

    def _draw_mute_overlay(self):
        """Draw a translucent mute text when the game is muted."""
        mute_font = pygame.font.Font(self.game_font, 24)
        mute_text = mute_font.render("MUTED", True, (255, 255, 255))

        mute_surface = pygame.Surface(mute_text.get_size(), pygame.SRCALPHA)

        mute_surface.blit(mute_text, (0,0))

        mute_surface.set_alpha(128)

        # Get the rectangle for positioning
        mute_rect = mute_surface.get_rect()
        mute_rect.topright = (self.screen.get_rect().right - 120, 20)

        # Blit the translucent mute surface onto the screen
        self.screen.blit(mute_surface, mute_rect)


    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_colour)
        self.stars.draw_stars()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()
        if self.start_screen:
            self._start_screen()
        # Draw play button if game inactive
        if not self.game_active and not self.game_over:
            self.play_button.draw_button()
        # Draw pause overlay
        if self.paused:
            self._draw_pause_overlay()
        if self.mute:
            self._draw_mute_overlay()
        if self.game_over:
            self._game_over()
        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == "__main__":
    sw = SpaceWars()
    sw.run_game()