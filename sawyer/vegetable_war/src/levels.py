import pygame
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from platforms import Platform, MovingPlatform
from enemies import Enemy, Boss
from constants import *

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.background_color = (34, 139, 34)
        self.player_start_x = 50
        self.player_start_y = 400
        self.resources_needed = {NUTRIENTS: 3, SUNLIGHT: 3, WATER: 3}
        self.boss = None
        self.story = ""
        
        self._create_level()
    
    def _create_level(self):
        """Create level-specific layout"""
        if self.level_num == 1:
            self._create_level_1()
        elif self.level_num == 2:
            self._create_level_2()
        elif self.level_num == 3:
            self._create_level_3()
        else:
            self._create_level_1()
    
    def _create_level_1(self):
        """Level 1: Introduction vs Beans"""
        self.story = "The Beans have invaded! They're competing for nutrients. Stop them!"
        self.background_color = (34, 139, 34)
        
        # Platforms
        self.platforms.add(Platform(0, 600, 200, 100, "normal"))
        self.platforms.add(Platform(250, 500, 200, 100, "normal"))
        self.platforms.add(Platform(500, 550, 200, 100, "normal"))
        self.platforms.add(Platform(750, 480, 200, 100, "normal"))
        self.platforms.add(Platform(1000, 560, 200, 100, "normal"))
        
        # Enemies
        for x in [300, 600, 900]:
            self.enemies.add(Enemy(x, 400, "bean"))
            self.enemies.add(Enemy(x + 100, 380, "bean"))
        
        self.resources_needed = {NUTRIENTS: 5, SUNLIGHT: 0, WATER: 0}
    
    def _create_level_2(self):
        """Level 2: Peas and moving platforms"""
        self.story = "The Peas are lightning fast! Navigate the shifting terrain!"
        self.background_color = (46, 125, 50)
        
        # Platforms with moving sections
        self.platforms.add(Platform(0, 600, 250, 100, "normal"))
        self.platforms.add(MovingPlatform(300, 450, 150, 50, 300, 700, 2))
        self.platforms.add(Platform(750, 550, 200, 100, "normal"))
        self.platforms.add(MovingPlatform(1000, 400, 200, 50, 800, 1100, 2.5))
        
        # Fast Pea enemies
        for x in [400, 700, 1000]:
            self.enemies.add(Enemy(x, 400, "pea"))
            self.enemies.add(Enemy(x + 50, 400, "pea"))
            self.enemies.add(Enemy(x + 100, 400, "pea"))
        
        self.resources_needed = {NUTRIENTS: 3, SUNLIGHT: 5, WATER: 0}
    
    def _create_level_3(self):
        """Level 3: Garlic boss fight"""
        self.story = "A mighty Garlic commander leads the invasion. This is the final battle!"
        self.background_color = (56, 142, 60)
        
        # Boss arena - simple platforms
        self.platforms.add(Platform(0, 600, 300, 100, "normal"))
        self.platforms.add(Platform(450, 500, 300, 100, "normal"))
        self.platforms.add(Platform(900, 600, 300, 100, "normal"))
        
        # Boss
        self.boss = Boss(500, 200, "giant_garlic")
        self.enemies.add(self.boss)
        
        # Support enemies
        self.enemies.add(Enemy(300, 450, "bean"))
        self.enemies.add(Enemy(700, 450, "bean"))
        
        self.resources_needed = {NUTRIENTS: 3, SUNLIGHT: 3, WATER: 5}
    
    def update(self):
        """Update all level entities"""
        for platform in self.platforms:
            if hasattr(platform, 'update'):
                platform.update()
    
    def draw(self, screen):
        """Draw level elements"""
        screen.fill(self.background_color)
        
        for platform in self.platforms:
            platform.draw(screen)
    
    def get_all_platforms(self):
        """Return list of platforms"""
        return list(self.platforms)
    
    def get_all_enemies(self):
        """Return list of enemies"""
        return list(self.enemies)
    
    def check_level_complete(self, resources_collected):
        """Check if level objectives are met"""
        for resource_type, needed in self.resources_needed.items():
            if resources_collected.get(resource_type, 0) < needed:
                return False
        return len(self.enemies) == 0
