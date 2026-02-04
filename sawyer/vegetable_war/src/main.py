import pygame
import sys
import os
import random

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import *
from player import Player
from enemies import Enemy, Boss
from platforms import Platform
from levels import Level
from story import StoryManager
from audio import init_sound_manager, get_sound_manager
from effects import ParticleSystem, ScreenShake, FloatingTextManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Onions May Cry - The Vegetable War")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        self.huge_font = pygame.font.Font(None, 72)
        
        # Initialize sound
        self.sound_manager = init_sound_manager()
        
        # Start playing background music
        self.sound_manager.play_music()
        
        # Visual effects
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.floating_text = FloatingTextManager()
        
        # Game state
        self.state = STATE_MENU
        self.current_level_num = 1
        self.current_level = None
        self.player = None
        self.resources_collected = {NUTRIENTS: 0, SUNLIGHT: 0, WATER: 0}
        
        # Story and cutscenes
        self.story_manager = StoryManager()
        
        # Start with intro
        self.show_menu()
    
    def show_menu(self):
        """Show main menu"""
        self.state = STATE_MENU
        menu_running = True
        
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu_running = False
            
            self.screen.fill(DARK_GRAY)
            
            # Title
            title = self.huge_font.render("ONIONS MAY CRY", True, ONION_PURPLE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = self.large_font.render("The Vegetable War", True, ORANGE)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 180))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Description
            desc_lines = [
                "You are an onion, guardian of the garden.",
                "Invaders seek the nutrients, water, and sunlight that sustain you.",
                "",
                "GAMEPLAY:",
                "A/D - Move     W - Jump     SPACE - Attack     SHIFT - Super Attack",
                "",
                "Your EMOTION METER fills as you battle.",
                "When it's full, use SHIFT for a devastating attack!",
                "",
                "Shed your layers, but never surrender!",
                "",
                "PRESS SPACE TO BEGIN"
            ]
            
            y_pos = 280
            for line in desc_lines:
                if line:
                    text = self.font.render(line, True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                    self.screen.blit(text, text_rect)
                y_pos += 30
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Start intro cutscene
        self.story_manager.start_cutscene("intro")
        self.state = STATE_CUTSCENE
    
    def start_level(self, level_num):
        """Start a new level"""
        self.current_level_num = level_num
        self.current_level = Level(level_num)
        self.player = Player(self.current_level.player_start_x, 
                           self.current_level.player_start_y)
        self.resources_collected = {NUTRIENTS: 0, SUNLIGHT: 0, WATER: 0}
        
        # Clear previous effects
        self.particle_system.clear()
        self.floating_text.texts.clear()
        
        # Show level intro cutscene
        cutscene_keys = {
            1: "level1_intro",
            2: "level2_intro",
            3: "level3_intro"
        }
        if level_num in cutscene_keys:
            self.story_manager.start_cutscene(cutscene_keys[level_num])
            self.state = STATE_CUTSCENE
        else:
            self.state = STATE_PLAYING
    
    def handle_input(self):
        """Handle user input"""
        keys = pygame.key.get_pressed()
        
        if self.state == STATE_PLAYING:
            self.player.handle_input(keys)
        elif self.state == STATE_CUTSCENE:
            self.story_manager.update(keys)
    
    def update(self):
        """Update game state"""
        if self.state == STATE_PLAYING:
            # Update player
            self.player.update(self.current_level.platforms, 
                             self.current_level.enemies)
            
            # Update enemies
            for enemy in self.current_level.enemies:
                enemy.update(self.current_level.platforms, self.player)
            
            # Check collisions with player attack
            if self.player.is_attacking:
                attack_hitbox = self.player.get_attack_hitbox()
                if attack_hitbox:
                    damage = 15
                    for enemy in self.current_level.enemies:
                        if attack_hitbox.colliderect(enemy.rect):
                            knockback = 5 if self.player.facing_right else -5
                            if enemy.take_damage(damage, knockback):
                                self.current_level.enemies.remove(enemy)
                                self.player.kill_enemy()
                                self.resources_collected[NUTRIENTS] += 1
                                self.sound_manager.play_sound('hit')
                                # Effects
                                self.particle_system.emit_hit(enemy.x + enemy.width // 2, 
                                                             enemy.y + enemy.height // 2, 8, YELLOW)
                                self.floating_text.add_text(enemy.x, enemy.y - 20, "HIT!", YELLOW)
                            else:
                                # Hit but not killed
                                self.particle_system.emit_hit(enemy.x + enemy.width // 2,
                                                             enemy.y + enemy.height // 2, 4, ORANGE)
            
            # Check collision with super attack
            if self.player.super_attack_cooldown > 0 and self.player.super_attack_cooldown < 5:
                super_hitbox = self.player.get_super_hitbox()
                self.particle_system.emit_super_effect(self.player.x + self.player.width // 2,
                                                      self.player.y + self.player.height // 2)
                self.screen_shake.start()
                for enemy in list(self.current_level.enemies):
                    if super_hitbox.colliderect(enemy.rect):
                        if enemy.take_damage(SUPER_ATTACK_DAMAGE, 10):
                            self.current_level.enemies.remove(enemy)
                            self.player.kill_enemy(2)
                            self.resources_collected[NUTRIENTS] += 2
                            self.floating_text.add_text(enemy.x, enemy.y - 20, "ELIMINATED!", ORANGE)
            
            # Check collisions with enemy attacks
            for enemy in self.current_level.enemies:
                enemy_attack = enemy.get_attack_hitbox()
                if enemy_attack and self.player.rect.colliderect(enemy_attack):
                    knockback = 5 if enemy.facing_right else -5
                    if self.player.take_damage(enemy.damage, knockback):
                        self.story_manager.start_cutscene("gameover")
                        self.state = STATE_CUTSCENE
            
            # Check if boss should summon
            if self.current_level.boss:
                if self.current_level.boss.should_summon():
                    if random.random() > 0.3:
                        new_enemy = Enemy(self.current_level.boss.x, self.current_level.boss.y, "bean")
                        self.current_level.enemies.add(new_enemy)
            
            # Update level
            self.current_level.update()
            
            # Update effects
            self.particle_system.update()
            self.floating_text.update()
            self.screen_shake.update()
            
            # Check level complete
            if len(self.current_level.enemies) == 0:
                self.state = STATE_LEVEL_COMPLETE
                
                # Show level outro
                outro_keys = {
                    1: "level1_outro",
                    2: "level2_outro",
                }
                if self.current_level_num in outro_keys:
                    self.story_manager.start_cutscene(outro_keys[self.current_level_num])
                    self.state = STATE_CUTSCENE
                elif self.current_level_num == 3:
                    self.story_manager.start_cutscene("victory")
                    self.state = STATE_CUTSCENE
        
        elif self.state == STATE_CUTSCENE:
            keys = pygame.key.get_pressed()
            self.story_manager.update(keys)
            if not self.story_manager.is_cutscene_playing():
                # Determine what cutscene just finished
                cutscene_key = self.story_manager.last_cutscene_key
                
                if cutscene_key == "gameover":
                    self.show_menu()  # Game over - go back to menu
                elif cutscene_key == "victory":
                    self.state = STATE_MENU  # Victory - back to menu
                elif cutscene_key == "intro":
                    # Start level 1 after main intro cutscene
                    self.start_level(1)
                elif cutscene_key in ["level1_intro", "level2_intro", "level3_intro"]:
                    # Level intro finished, go to gameplay
                    self.state = STATE_PLAYING
                elif cutscene_key in ["level1_outro", "level2_outro"]:
                    # Level outro finished, go to next level
                    self.start_level(self.current_level_num + 1)
                else:
                    self.state = STATE_PLAYING
        
        elif self.state == STATE_GAME_OVER:
            # This state is deprecated, handled by STATE_CUTSCENE now
            pass
    
    def draw(self):
        """Draw game"""
        if self.state == STATE_MENU:
            # Draw menu
            self.story_manager.draw(self.screen, self.font, self.large_font)
        
        elif self.state == STATE_CUTSCENE:
            # Draw level background if in a level cutscene
            if self.current_level:
                self.current_level.draw(self.screen)
                
                # Draw platforms
                for platform in self.current_level.platforms:
                    self.screen.blit(platform.image, (platform.x, platform.y))
                
                # Draw enemies
                for enemy in self.current_level.enemies:
                    self.screen.blit(enemy.image, enemy.rect)
                
                # Draw player
                self.screen.blit(self.player.image, self.player.rect)
            
            # Draw cutscene overlay on top
            self.story_manager.draw(self.screen, self.font, self.large_font)
        
        elif self.state in [STATE_PLAYING, STATE_GAME_OVER, STATE_LEVEL_COMPLETE]:
            # Get screen shake offset
            shake_offset = self.screen_shake.get_offset()
            
            # Draw level
            self.current_level.draw(self.screen)
            
            # Draw platforms
            for platform in self.current_level.platforms:
                pos = (int(platform.x + shake_offset[0]), int(platform.y + shake_offset[1]))
                self.screen.blit(platform.image, pos)
            
            # Draw enemies
            for enemy in self.current_level.enemies:
                pos = (int(enemy.x + shake_offset[0]), int(enemy.y + shake_offset[1]))
                self.screen.blit(enemy.image, pos)
                
                # Draw enemy health bar
                health_bar_width = 30
                health_bar_height = 5
                health_width = int(health_bar_width * (enemy.health / enemy.max_health))
                bar_x = int(enemy.x + shake_offset[0])
                bar_y = int(enemy.y - 10 + shake_offset[1])
                pygame.draw.rect(self.screen, RED, (bar_x, bar_y, health_bar_width, health_bar_height))
                pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, health_width, health_bar_height))
            
            # Draw player
            player_pos = (int(self.player.x + shake_offset[0]), int(self.player.y + shake_offset[1]))
            self.screen.blit(self.player.image, player_pos)
            
            # Draw attack hitbox (debug)
            if self.player.is_attacking:
                attack_box = self.player.get_attack_hitbox()
                if attack_box:
                    rect = pygame.Rect(attack_box.x + shake_offset[0], attack_box.y + shake_offset[1],
                                      attack_box.width, attack_box.height)
                    pygame.draw.rect(self.screen, YELLOW, rect, 2)
            
            # Draw particles and effects
            self.particle_system.draw(self.screen)
            self.floating_text.draw(self.screen, self.font)
            
            # Draw UI
            self.player.draw_ui(self.screen, self.font)
            
            # Draw resources collected
            resource_y = 80
            for resource_type, name in enumerate(RESOURCE_NAMES):
                count = self.resources_collected.get(resource_type, 0)
                needed = self.current_level.resources_needed.get(resource_type, 0)
                text = self.font.render(f"{name}: {count}/{needed}", True, WHITE)
                self.screen.blit(text, (10, resource_y))
                resource_y += 25
            
            # Draw level info
            level_text = self.font.render(f"Stage {self.current_level_num}", True, ORANGE)
            self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
