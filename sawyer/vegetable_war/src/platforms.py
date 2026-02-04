import pygame
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="normal"):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform_type = platform_type
        
        self.image = self.create_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def create_sprite(self):
        """Create platform visual"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.platform_type == "normal":
            # Brown dirt platform
            pygame.draw.rect(surface, (139, 69, 19), (0, 0, self.width, self.height))
            # Texture
            for i in range(0, self.width, 10):
                pygame.draw.line(surface, (101, 50, 15), (i, 0), (i, self.height), 1)
        
        elif self.platform_type == "moving":
            # Gray moving platform
            pygame.draw.rect(surface, LIGHT_GRAY, (0, 0, self.width, self.height))
            pygame.draw.rect(surface, WHITE, (0, 0, self.width, self.height), 2)
        
        elif self.platform_type == "breakable":
            # Cracked platform
            pygame.draw.rect(surface, (210, 180, 140), (0, 0, self.width, self.height))
            pygame.draw.line(surface, BLACK, (0, self.height // 2), (self.width, self.height // 2), 2)
        
        elif self.platform_type == "water":
            # Water platform
            pygame.draw.rect(surface, BLUE, (0, 0, self.width, self.height))
            # Wave effect
            for i in range(0, self.width, 15):
                pygame.draw.arc(surface, (0, 150, 255), (i, -5, 20, 10), 0, 3.14, 2)
        
        return surface
    
    def update(self):
        """Update platform (for moving platforms)"""
        pass
    
    def draw(self, screen):
        """Draw platform"""
        screen.blit(self.image, (self.x, self.y))


class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, start_x, end_x, speed):
        super().__init__(x, y, width, height, "moving")
        self.start_x = start_x
        self.end_x = end_x
        self.speed = speed
        self.direction = 1
    
    def update(self):
        """Move platform back and forth"""
        self.x += self.speed * self.direction
        
        if self.x <= self.start_x or self.x >= self.end_x:
            self.direction *= -1
        
        self.rect.x = self.x


class BreakablePlatform(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "breakable")
        self.health = 1
        self.is_broken = False
    
    def take_damage(self):
        """Break platform"""
        self.health -= 1
        if self.health <= 0:
            self.is_broken = True
            self.kill()
