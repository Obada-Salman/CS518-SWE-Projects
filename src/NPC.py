import pygame
from settings import *
from SpriteHandler import SpriteHandler
import resource_path

class NPC:
    NPC_TYPES = {
        'carrot': {
            'speed': 3,
            'health': 8,
            'scale': 1,
            'sprite': 'assets/images/Characters/Carrot_75x110.png'
        },
        'potato': {
            'speed': 2,
            'health': 5,
            'scale': 1,
            'sprite': 'assets/images/Characters/Potato_83x94.png'
        },
        'onion': {
            'speed': 2,
            'health': 5,
            'scale': 2,
            'sprite': 'assets/images/Characters/Onion_34x34.png'
        },
        'tomato': {
            'speed': 7,
            'health': 3,
            'scale': 0.6,
            'sprite': 'assets/images/Characters/Tomato_94x190.png'
        }
    }

    NPC_CONFIG = {
        'carrot': (75, 110, 'carrot', 3, 'enemy'),
        'potato': (83, 94, 'potato', 3, 'enemy'),
        'tomato': (94, 190, 'tomato', 3, 'enemy'),
        'carrot_ally': (75, 110, 'carrot', 0, 'ally'),
        'potato_ally': (83, 94, 'potato', 0, 'ally'),
        'tomato_ally': (94, 190, 'tomato', 0, 'ally'),
    }

    def __init__(self, x, y, width, height, type='carrot', speed=None):
        self.x = float(x)
        self.y = float(y)
        
        npc_config = self.NPC_TYPES.get(type, self.NPC_TYPES['carrot'])
        self.type = type
        self.team = 'enemy'
        self.recruited = False
        self.width = width * npc_config['scale']
        self.height = height * npc_config['scale']
        
        
        self.speed = speed if speed is not None else npc_config['speed']
        self.health = npc_config['health']
        self.max_health = self.health
        sprite_path = npc_config['sprite']
        
        self.vx = -self.speed
        self.vy = 0.0
        self.gravity = 0.8
        self.on_ground = False
        self.direction = 0 
        self.state = 0 
        self.moving = False
        self.jumping = False
        self.sprites = SpriteHandler(resource_path.get_resource_path(sprite_path), type=self.type, scale=npc_config['scale'])
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.mask_frame = self.sprites.get_current_frame()
        self.mask_frame = pygame.transform.flip(self.mask_frame, True, False)
        self.mask = pygame.mask.from_surface(self.mask_frame)

        # ally hit properties
        self.invincible = False
        self.time_since_hit = 0
        self.visible = True
        self.invincibility_time = 2000

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
        
        # Set animation flags
        self.moving = abs(self.vx) > 0.1
        if self.vy < 0:
            self.jumping = True
        elif self.on_ground:
            self.jumping = False

        # Make allies briefly invincible after getting hit
        if self.team == 'ally' and self.invincible:
            now = pygame.time.get_ticks()
            if now - self.time_since_hit < self.invincibility_time:
                self.visible = not self.visible
            else:
                self.visible, self.invincible = True, False
        
        # Animation states
        if self.jumping:
            self.state = 2
        elif self.moving:
            self.state = 1
        else: # idle
            self.state = 0
        
        self.sprites.update(direction=self.direction, state=self.state)

        # current_frame = self.sprites.get_current_frame()
        # self.mask = pygame.mask.from_surface(current_frame)
        
        if self.health <= 0:
            self.x, self.y = -1000, -1000
            self.rect.topleft = (int(self.x), int(self.y))

    def take_damage(self, amount):
        if self.team == 'ally' and not self.invincible:
            self.health -= amount
            self.invincible = True
            self.time_since_hit = pygame.time.get_ticks()
        elif self.team == 'enemy':
            self.health -= amount

    def can_damage(self):
        if self.team == 'ally':
            return not self.invincible
        return True

    def is_alive(self):
        return self.health > 0

    def draw(self, surface, scroll):
        if self.team == 'ally' and self.visible:
            self.sprites.draw(surface, self.rect.x - scroll, self.rect.y)
        elif self.team == 'enemy':
            self.sprites.draw(surface, self.rect.x - scroll, self.rect.y)

        if self.team == 'ally':
            if not self.recruited:
                # draw gray circle above ally
                pygame.draw.circle(surface, (128, 128, 128), (self.rect.centerx - scroll, self.rect.top - 20), 10)
            else:
                # draw green circle that gradually turns to red as health decreases
                health_ratio = 0.0 if self.max_health <= 0 else self.health / self.max_health
                health_ratio = max(0.0, min(1.0, health_ratio))
                red = max(0, min(255, int(255 * (1 - health_ratio))))
                green = max(0, min(255, int(255 * health_ratio)))
                pygame.draw.circle(surface, (red, green, 0), (self.rect.centerx - scroll, self.rect.top - 20), 10)

    def check_map_collision(self, game_map, tile_size, axis):
        map_width = len(game_map[0]) * tile_size
        map_height = len(game_map) * tile_size

        mask_rects = self.mask.get_bounding_rects()
        if not mask_rects:
            return
        
        mask_bounding_rect = mask_rects[0]
        
        if axis == 'x':
            # Left Edge current position + mask offset
            if self.rect.x + mask_bounding_rect.left < 0:
                self.rect.x = -mask_bounding_rect.left
                self.x = float(self.rect.x)

                self.vx *= -1
                self.direction = 1 if self.vx > 0 else 0
                self.mask_frame = pygame.transform.flip(self.mask_frame, True, False)
                self.mask = pygame.mask.from_surface(self.mask_frame)

                return
                
            # Right Edge current position + mask width
            elif self.rect.x + mask_bounding_rect.right > map_width:
                self.rect.x = map_width - mask_bounding_rect.right
                self.x = float(self.rect.x)
        
                self.vx *= -1
                self.direction = 1 if self.vx > 0 else 0
                self.mask_frame = pygame.transform.flip(self.mask_frame, True, False)
                self.mask = pygame.mask.from_surface(self.mask_frame)

                return

        elif axis == 'y':
            # Bottom Edge
            if self.rect.y + mask_bounding_rect.bottom > map_height:
                self.health = 0

        start_col = int(self.rect.left // tile_size)
        end_col = int((self.rect.right - 1) // tile_size)
        start_row = int(self.rect.top // tile_size)
        end_row = int((self.rect.bottom - 1) // tile_size)

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if 0 <= row < len(game_map) and 0 <= col < len(game_map[0]):
                    tile = game_map[row][col]
                    
                    if tile and tile.collision:
                        tile_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                        tile_mask = pygame.mask.Mask((tile_size, tile_size), fill=True)
                        
                        offset_x = tile_rect.x - self.rect.x
                        offset_y = tile_rect.y - self.rect.y

                        if self.mask.overlap(tile_mask, (offset_x, offset_y)):
                            if axis == 'x':
                                # When colliding on X, just flip velocity and stay there.
                                # Don't adjust Y at all.
                                self.vx *= -1
                                self.direction = 1 if self.vx > 0 else 0
                                self.mask_frame = pygame.transform.flip(self.mask_frame, True, False)
                                self.mask = pygame.mask.from_surface(self.mask_frame)
                                
                                # Optional: Push out of the wall slightly to prevent sticking
                                if self.vx > 0: self.rect.left = tile_rect.right
                                else: self.rect.right = tile_rect.left
                                self.x = float(self.rect.x)
                                return

                            elif axis == 'y':
                                # Only adjust Y if we aren't moving horizontally into a wall
                                if self.vy > 0:  # Falling
                                    self.rect.bottom = tile_rect.top
                                    self.on_ground = True
                                elif self.vy < 0:  # Jumping Up
                                    self.rect.top = tile_rect.bottom
                                
                                self.y = float(self.rect.y)
                                self.vy = 0
                                return