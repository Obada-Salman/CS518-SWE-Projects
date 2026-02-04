import pygame
import random
import math
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="bean"):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 35
        self.height = 35
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.enemy_type = enemy_type
        
        # Stats vary by type
        if enemy_type == "bean":
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.speed = 2
            self.color = (139, 69, 19)  # Brown
            self.accent = (205, 92, 0)
        elif enemy_type == "pea":
            self.health = 20
            self.max_health = 20
            self.damage = 8
            self.speed = 4
            self.color = (34, 139, 34)  # Forest green
            self.accent = (50, 205, 50)
        elif enemy_type == "garlic":
            self.health = 40
            self.max_health = 40
            self.damage = 15
            self.speed = 2
            self.color = (255, 255, 255)  # White
            self.accent = (200, 200, 200)
        else:
            self.health = 25
            self.max_health = 25
            self.damage = 10
            self.speed = 3
            self.color = (128, 128, 128)
            self.accent = (160, 160, 160)
        
        # Behavior
        self.direction = random.choice([-1, 1])
        self.facing_right = self.direction > 0
        self.attack_cooldown = 0
        self.patrol_timer = random.randint(60, 120)
        self.attack_range = 60
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.knockback_x = 0
        
        # Create sprite
        self.image = self.create_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def create_sprite(self):
        """Create enemy visual"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw main body
        pygame.draw.circle(surface, self.color, (self.width // 2, self.height // 2), 
                         int(self.width // 2 * (self.health / self.max_health)))
        
        # Draw outline
        pygame.draw.circle(surface, self.accent, (self.width // 2, self.height // 2), 
                         self.width // 2, 2)
        
        # Draw eyes
        eye_y = self.height // 2 - 5
        eye_x_left = self.width // 3
        eye_x_right = self.width * 2 // 3
        
        pygame.draw.circle(surface, WHITE, (eye_x_left, eye_y), 2)
        pygame.draw.circle(surface, WHITE, (eye_x_right, eye_y), 2)
        pygame.draw.circle(surface, BLACK, (eye_x_left, eye_y), 1)
        pygame.draw.circle(surface, BLACK, (eye_x_right, eye_y), 1)
        
        # Draw angry mouth
        pygame.draw.line(surface, BLACK, (eye_x_left - 2, eye_y + 3), 
                        (eye_x_right + 2, eye_y + 3), 2)
        
        return surface
    
    def update(self, platforms, player):
        """Update enemy state"""
        # Apply gravity
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        
        # Knockback handling
        self.vel_x = self.knockback_x
        self.knockback_x *= 0.9
        
        # AI behavior
        dist_to_player = abs(self.x - player.x)
        
        if dist_to_player < self.attack_range:
            # Attack mode
            self.vel_x = 0
            if self.attack_cooldown == 0:
                self.attack_cooldown = 60
        else:
            # Patrol mode
            self.vel_x = self.speed * self.direction
            self.patrol_timer -= 1
            if self.patrol_timer <= 0:
                self.direction *= -1
                self.facing_right = self.direction > 0
                self.patrol_timer = random.randint(60, 120)
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.y = platform.rect.bottom
                    self.vel_y = 0
        
        # Boundary collision
        if self.x < -50 or self.x > SCREEN_WIDTH + 50 or self.y > SCREEN_HEIGHT:
            self.kill()
        
        # Cooldown updates
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        else:
            self.invulnerable = False
        
        # Update sprite
        self.image = self.create_sprite()
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def take_damage(self, damage, knockback_x=0):
        """Take damage from player"""
        if not self.invulnerable:
            self.health -= damage
            self.knockback_x = knockback_x
            self.invulnerable = True
            self.invulnerable_timer = 15
            
            if self.health <= 0:
                return True  # Enemy defeated
        
        return False
    
    def get_attack_hitbox(self):
        """Get hitbox for enemy attack"""
        if self.attack_cooldown == 60:  # Just started attacking
            if self.facing_right:
                return pygame.Rect(self.x + self.width, self.y, 30, self.height)
            else:
                return pygame.Rect(self.x - 30, self.y, 30, self.height)
        return None


class Boss(Enemy):
    def __init__(self, x, y, boss_type="giant_garlic"):
        self.boss_type = boss_type
        super().__init__(x, y, enemy_type="garlic")
        
        # Boss-specific stats
        if boss_type == "giant_garlic":
            self.health = 150
            self.max_health = 150
            self.damage = 20
            self.width = 80
            self.height = 80
            self.color = (255, 255, 220)
            self.accent = (200, 200, 150)
        elif boss_type == "bean_general":
            self.health = 120
            self.max_health = 120
            self.damage = 18
            self.width = 70
            self.height = 70
            self.color = (180, 100, 50)
            self.accent = (220, 140, 80)
        else:
            self.health = 100
            self.max_health = 100
            self.damage = 15
        
        self.attack_range = 150
        self.summon_timer = 0
        self.summon_cooldown = 180
        self.phase = 1
        self.image = self.create_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self, platforms, player):
        """Update boss with special behavior"""
        super().update(platforms, player)
        
        # Phase changes
        if self.health < self.max_health * 0.66:
            self.phase = 2
        if self.health < self.max_health * 0.33:
            self.phase = 3
        
        # Boss summons minions
        self.summon_timer += 1
        if self.summon_timer > self.summon_cooldown:
            self.summon_timer = 0
            self.summon_cooldown = max(120, self.summon_cooldown - 20)
    
    def should_summon(self):
        """Check if boss should summon minions"""
        return self.summon_timer == 0
    
    def get_boss_attack_pattern(self):
        """Get special attack pattern based on phase"""
        if self.phase == 3:
            self.attack_range = 200
            self.speed = 3
        elif self.phase == 2:
            self.attack_range = 150
            self.speed = 2.5
