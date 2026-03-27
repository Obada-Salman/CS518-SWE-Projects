import pygame
from settings import *
from SpriteHandler import SpriteHandler

class Enemy:
    def __init__(self, x, y, width, height, type='enemy_carrot', speed=3):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.type = type
        self.speed = speed
        self.health = 8
        self.vx = -self.speed
        self.vy = 0.0
        self.gravity = 0.8
        self.on_ground = False
        self.direction = 0 
        self.state = 1 
        self.sprites = SpriteHandler("assets/images/Characters/Carrot_75x110.png", type=self.type)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def check_map_collision(self, game_map, tile_size, axis):
        start_col = int(self.rect.left // tile_size)
        end_col = int(self.rect.right // tile_size)
        start_row = int(self.rect.top // tile_size)
        end_row = int(self.rect.bottom // tile_size)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if 0 <= row < len(game_map) and 0 <= col < len(game_map[0]):
                    tile = game_map[row][col]
                    if tile and tile.collision:
                        tile_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                        if self.rect.colliderect(tile_rect):
                            if axis == 'x':
                                if self.vx > 0: self.rect.right = tile_rect.left
                                else: self.rect.left = tile_rect.right
                                self.x = float(self.rect.x)
                                self.vx *= -1
                                self.direction = 1 if self.vx > 0 else 0
                                return # Exit after first wall hit to prevent double-bounce
                            elif axis == 'y':
                                if self.vy > 0:
                                    self.rect.bottom = tile_rect.top
                                    self.y = float(self.rect.y)
                                    self.vy = 0
                                    self.on_ground = True
                                elif self.vy < 0:
                                    self.rect.top = tile_rect.bottom
                                    self.y = float(self.rect.y)
                                    self.vy = 0

    def update(self, game_map, tile_size):
        # Move X
        self.x += self.vx
        self.rect.x = int(round(self.x))
        self.check_map_collision(game_map, tile_size, 'x')

        # Move Y
        self.vy += self.gravity
        self.y += self.vy
        self.rect.y = int(round(self.y))
        self.on_ground = False
        self.check_map_collision(game_map, tile_size, 'y')

        self.sprites.update(direction=self.direction, state=self.state)
        
        if self.health <= 0:
            self.x, self.y = -1000, -1000
            self.rect.topleft = (int(self.x), int(self.y))

    def take_damage(self, amount):
        self.health -= amount
    
    def is_alive(self):
        return self.health > 0
    
    
    def draw(self, surface):
        self.sprites.draw(surface, self.rect.x, self.rect.y)