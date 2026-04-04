import pygame
from settings import *
from SpriteHandler import SpriteHandler

class Enemy:
    ENEMY_TYPES = {
        'enemy_carrot': {
            'speed': 3,
            'health': 8,
            'sprite': 'assets/images/Characters/Carrot_75x110.png'
        },
        'enemy_potato': {
            'speed': 2,
            'health': 5,
            'sprite': 'assets/images/Characters/Potato_83x94.png'
        }
    }

    def __init__(self, x, y, width, height, type='enemy_carrot', speed=None):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.type = type
        
        enemy_config = self.ENEMY_TYPES.get(type, self.ENEMY_TYPES['enemy_carrot'])
        
        self.speed = speed if speed is not None else enemy_config['speed']
        self.health = enemy_config['health']
        self.max_health = self.health
        sprite_path = enemy_config['sprite']
        
        self.vx = -self.speed
        self.vy = 0.0
        self.gravity = 0.8
        self.on_ground = False
        self.direction = 0 
        self.state = 1 
        self.sprites = SpriteHandler(sprite_path, type=self.type)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.mask = pygame.mask.from_surface(self.sprites.get_current_frame())


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

        # current_frame = self.sprites.get_current_frame()
        # self.mask = pygame.mask.from_surface(current_frame)
        
        if self.health <= 0:
            self.x, self.y = -1000, -1000
            self.rect.topleft = (int(self.x), int(self.y))

    def take_damage(self, amount):
        self.health -= amount
    
    def is_alive(self):
        return self.health > 0
    
    
    def draw(self, surface):
        self.sprites.draw(surface, self.rect.x, self.rect.y)
    
    def check_map_collision(self, game_map, tile_size, axis):
        # Calculate exactly which tiles we are overlapping
        start_col = int(self.rect.left // tile_size)
        end_col = int((self.rect.right - 1) // tile_size)
        start_row = int(self.rect.top // tile_size)
        end_row = int((self.rect.bottom - 1) // tile_size)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if 0 <= row < len(game_map) and 0 <= col < len(game_map[0]):
                    tile = game_map[row][col]
                    
                    # Check if tile exists and has collision
                    if tile and tile.collision:
                        tile_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                        tile_mask = pygame.mask.Mask((tile_size, tile_size), fill=True)
                        
                        offset_x = tile_rect.x - self.rect.x
                        offset_y = tile_rect.y - self.rect.y

                        if self.mask.overlap(tile_mask, (offset_x, offset_y)):
                            if axis == 'x':
                                if self.mask.overlap(tile_mask, (offset_x, offset_y)):
                                    self.vx *= -1
                                    self.direction = 1 if self.vx > 0 else 0
                                
                                return

                            elif axis == 'y':
                                if self.vy > 0:  # Falling
                                    while self.mask.overlap(tile_mask, (offset_x, offset_y)):
                                        self.rect.y -= 1
                                        self.y = float(self.rect.y)
                                        offset_y = tile_rect.y - self.rect.y

                                    self.on_ground = True
                                
                                elif self.vy < 0:  # Jumping/Up
                                    while self.mask.overlap(tile_mask, (offset_x, offset_y)):
                                        self.rect.y += 1
                                        self.y = float(self.rect.y)
                                        offset_y = tile_rect.y - self.rect.y
                                
                                self.vy = 0
                                return