import pygame
import math
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        
        # Health and combat
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.layers = 3  # Onion layers
        self.emotion_meter = 0
        self.emotion_max = EMOTION_METER_MAX
        self.is_attacking = False
        self.attack_cooldown = 0
        self.super_attack_ready = False
        self.super_attack_cooldown = 0
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # Create visual representation
        self.image = self.create_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def create_sprite(self):
        """Create the onion visual"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw onion layers
        layer_color = ONION_PURPLE
        num_visible_layers = max(1, (self.health // (self.max_health // self.layers)))
        
        # Draw main body
        pygame.draw.ellipse(surface, layer_color, (5, 15, self.width - 10, self.height - 20))
        
        # Draw layers/rings
        for i in range(num_visible_layers):
            layer_radius = (self.width - 10) // 2 - (i * 3)
            if layer_radius > 5:
                pygame.draw.circle(surface, ONION_LIGHT, 
                                 (self.width // 2, self.height // 2), layer_radius, 2)
        
        # Draw eyes
        eye_offset = 5
        pygame.draw.circle(surface, WHITE, (self.width // 4, self.height // 3), 3)
        pygame.draw.circle(surface, WHITE, (self.width * 3 // 4, self.height // 3), 3)
        pygame.draw.circle(surface, BLACK, (self.width // 4, self.height // 3), 1)
        pygame.draw.circle(surface, BLACK, (self.width * 3 // 4, self.height // 3), 1)
        
        # Draw tears when emotional
        if self.emotion_meter > 50:
            tear_size = min(self.emotion_meter // 20, 3)
            pygame.draw.circle(surface, BLUE, (self.width // 4 - 1, self.height // 3 + 5), tear_size)
            pygame.draw.circle(surface, BLUE, (self.width * 3 // 4 + 1, self.height // 3 + 5), tear_size)
        
        return surface
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        self.vel_x = 0
        
        if keys[pygame.K_a]:
            self.vel_x = -MOVE_SPEED
            self.facing_right = False
        if keys[pygame.K_d]:
            self.vel_x = MOVE_SPEED
            self.facing_right = True
        
        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        
        # Attack (spacebar)
        if keys[pygame.K_SPACE] and self.attack_cooldown == 0:
            self.attack()
        
        # Super attack (shift)
        if keys[pygame.K_LSHIFT] and self.super_attack_ready and self.super_attack_cooldown == 0:
            self.super_attack()
    
    def attack(self):
        """Perform basic attack"""
        self.is_attacking = True
        self.attack_cooldown = 15
    
    def super_attack(self):
        """Perform super attack (emotional discharge)"""
        self.emotion_meter = 0
        self.super_attack_ready = False
        self.super_attack_cooldown = SUPER_ATTACK_COOLDOWN
    
    def take_damage(self, damage, knockback_x=0):
        """Take damage and gain emotion"""
        if not self.invulnerable:
            self.health -= damage
            self.emotion_meter = min(self.emotion_meter + EMOTION_GAIN_ON_HIT, self.emotion_max)
            
            # Check if emotion meter is full
            if self.emotion_meter >= self.emotion_max:
                self.super_attack_ready = True
            
            self.invulnerable = True
            self.invulnerable_timer = 30
            
            # Knockback
            self.vel_x += knockback_x * 2
            
            # Shed layers
            if self.health <= 0:
                self.health = 0
                return True  # Player defeated
        
        return False
    
    def kill_enemy(self, points=1):
        """Called when player kills an enemy"""
        self.emotion_meter = min(self.emotion_meter + EMOTION_GAIN_ON_KILL, self.emotion_max)
        if self.emotion_meter >= self.emotion_max:
            self.super_attack_ready = True
    
    def update(self, platforms, enemies):
        """Update player state"""
        # Apply gravity
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        self.rect.topleft = (self.x, self.y)
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping
                    self.y = platform.rect.bottom
                    self.vel_y = 0
        
        # Boundary collision
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        
        # Falling off screen
        if self.y > SCREEN_HEIGHT:
            self.health = 0
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.is_attacking = False
        
        if self.super_attack_cooldown > 0:
            self.super_attack_cooldown -= 1
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        else:
            self.invulnerable = False
        
        # Update sprite
        self.image = self.create_sprite()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def draw_ui(self, screen, font):
        """Draw player UI"""
        # Health bar
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Health text
        health_text = font.render(f"HP: {int(self.health)}/{int(self.max_health)}", True, WHITE)
        screen.blit(health_text, (bar_x + 5, bar_y - 20))
        
        # Emotion meter
        emotion_y = bar_y + 40
        pygame.draw.rect(screen, YELLOW, (bar_x, emotion_y, bar_width, bar_height))
        emotion_width = int(bar_width * (self.emotion_meter / self.emotion_max))
        pygame.draw.rect(screen, PURPLE, (bar_x, emotion_y, emotion_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, emotion_y, bar_width, bar_height), 2)
        
        # Emotion text
        emotion_text = font.render(f"Emotion: {int(self.emotion_meter)}/{int(self.emotion_max)}", True, WHITE)
        screen.blit(emotion_text, (bar_x + 5, emotion_y - 20))
        
        # Super attack indicator
        if self.super_attack_ready:
            super_text = font.render("SUPER READY (SHIFT)", True, ORANGE)
            screen.blit(super_text, (bar_x, emotion_y + 40))
    
    def get_attack_hitbox(self):
        """Get hitbox for current attack"""
        if self.is_attacking:
            if self.facing_right:
                return pygame.Rect(self.x + self.width, self.y, 30, self.height)
            else:
                return pygame.Rect(self.x - 30, self.y, 30, self.height)
        return None
    
    def get_super_hitbox(self):
        """Get hitbox for super attack"""
        return pygame.Rect(self.x - 100, self.y - 100, self.width + 200, self.height + 200)
