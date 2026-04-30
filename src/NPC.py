import pygame
from settings import *
from SpriteHandler import SpriteHandler
import resource_path

class NPC:
    NPC_TYPES = {
        'carrot': {
            'speed': 180.0,
            'health': 5,
            'damage': 1,
            'scale': 1,
            'sprite': 'assets/images/Characters/Carrot_75x110.png'
        },
        'potato': {
            'speed': 120.0,
            'health': 7,
            'damage': 1,
            'scale': 1,
            'sprite': 'assets/images/Characters/Potato_83x94.png'
        },
        'onion': {
            'speed': 250.0,
            'health': 5,
            'damage': 1,
            'scale': 2,
            'sprite': 'assets/images/Characters/Onion_34x34.png'
        },
        'tomato': {
            'speed': 420.0,
            'health': 3,
            'damage': 1,
            'scale': 0.6,
            'sprite': 'assets/images/Characters/Tomato_94x190.png'
        },
        'bokchoy': {
            'speed': 300.0,
            'health': 5,
            'damage': 2,
            'scale': 0.6,
            'sprite': 'assets/images/Characters/BokChoy_94x184.png'
        },
        'pumpkin': {
            'speed': 270.0,
            'health': 12,
            'damage': 3,
            'scale': 0.6,
            'sprite': 'assets/images/Characters/Pumpkin_94x177.png'
        },
        'broccoli': {
            'speed': 540.0,
            'health': 6,
            'damage': 1,
            'scale': 0.6,
            'sprite': 'assets/images/Characters/Broccoli_101x178.png'
        },
        'finalboss': {
            'speed': 120.0,
            'health': 200,
            'damage': 4,
            'scale': 2,
            'sprite': 'assets/images/Characters/FinalBoss_110x180.png'
        }
    }

    NPC_CONFIG = {
        'carrot': (75, 110, 'carrot', 180.0, 'enemy'),
        'potato': (83, 94, 'potato', 120.0, 'enemy'),
        'tomato': (94, 190, 'tomato', 420.0, 'enemy'),
        'bokchoy': (94, 184, 'bokchoy', 300.0, 'enemy'),
        'pumpkin': (94, 177, 'pumpkin', 270.0, 'enemy'),
        'broccoli': (101, 178, 'broccoli', 540.0, 'enemy'),
        'carrot_ally': (75, 110, 'carrot', 0, 'ally'),
        'potato_ally': (83, 94, 'potato', 0, 'ally'),
        'tomato_ally': (94, 190, 'tomato', 0, 'ally'),
        'bokchoy_ally': (94, 184, 'bokchoy', 0, 'ally'),
        'pumpkin_ally': (94, 177, 'pumpkin', 0, 'ally'),
        'broccoli_ally': (101, 178, 'broccoli', 0, 'ally'),
        'finalboss': (110, 180, 'finalboss', 120.0, 'enemy')
    }

    def __init__(self, x, y, width, height, type='carrot', speed=None, team='enemy'):
        self.x = float(x)
        self.y = float(y)
        
        npc_config = self.NPC_TYPES.get(type, self.NPC_TYPES['carrot'])
        self.type = type
        self.team = team
        self.recruited = False
        self.width = width * npc_config['scale']
        self.height = height * npc_config['scale']
        
        
        self.speed = speed if speed is not None else npc_config['speed']
        self.health = npc_config['health']
        self.damage = npc_config.get('damage', 1)
        self.max_health = self.health
        sprite_path = npc_config['sprite']
        
        self.vx = -self.speed
        self.vy = 0.0
        self.gravity = 2880.0  # px/s^2
        self.on_ground = False
        self.on_wall = False  # Track if touching a wall
        self.wall_direction = 0  # 0=left, 1=right
        self.wall_jump_cooldown = 0  # Prevent rapid wall jumps
        self.stuck_timer = 0  # Track how long ally has been barely moving
        self.last_x = 0  # Track position to detect stuck state
        self.direction = 0 
        self.state = 0 
        self.moving = False
        self.jumping = False
        self.sprites = SpriteHandler(resource_path.get_resource_path(sprite_path), type=self.type, scale=npc_config['scale'])
        self.mask_frame = self.sprites.get_current_frame()
        self.mask_frame = pygame.transform.flip(self.mask_frame, True, False)
        self.mask = pygame.mask.from_surface(self.mask_frame)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        mask_rects = self.mask.get_bounding_rects()
        visible_pixels = mask_rects[0]
        self.bottom_offset = self.rect.height - visible_pixels.bottom
        self.top_offset = visible_pixels.top
        self.left_offset = visible_pixels.left
        self.right_offset = self.rect.width - visible_pixels.right
        
        # ally hit properties
        self.invincible = False
        self.time_since_hit = 0
        self.visible = True
        self.invincibility_time = 2000

    def update(self, game_map, tile_size, dt):
        # Move X
        self.on_wall = False  # Reset wall flag each frame
        self.x += self.vx * dt
        self.rect.x = int(round(self.x))
        self.check_map_collision(game_map, tile_size, 'x')

        # Move Y
        self.vy += self.gravity * dt
        self.y += self.vy * dt
        self.rect.y = int(round(self.y))
        self.on_ground = False
        self.check_map_collision(game_map, tile_size, 'y')
        
        # Wall jump logic - automatically jump off walls to unstick
        if self.wall_jump_cooldown > 0:
            self.wall_jump_cooldown -= dt
        
        # If stuck on a wall, perform wall jump (aggressive corner escape)
        # Trigger when on wall, even if on ground (corner case)
        if self.on_wall and self.wall_jump_cooldown <= 0:
            self.perform_wall_jump()
        
        # Emergency jump if stuck in terrain (not moving despite trying)
        # Track movement to detect stuck state
        movement_distance = abs(self.x - self.last_x)
        if self.vx != 0 and movement_distance < 0.5 and self.wall_jump_cooldown <= 0:
            # Not moving despite trying to move
            self.stuck_timer += dt
            if self.stuck_timer > 0.33:  # Stuck for 0.33 seconds
                if self.on_ground:
                    self.vy = -840.0  # Emergency jump
                    self.stuck_timer = 0
                    self.wall_jump_cooldown = 0.25  # 0.25 seconds
        else:
            self.stuck_timer = 0  # Reset if moving
        
        self.last_x = self.x  # Store position for next frame
        
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
        
        self.sprites.update(dt, direction=self.direction, state=self.state)

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

    def combat_with(self, opponent):
        """
        Health-based combat system: whoever has higher health wins.
        The opponent takes damage, winner takes reduced damage or none.
        """
        if self.health <= 0 or opponent.health <= 0:
            return
        
        # Determine winner based on health
        health_diff = self.health - opponent.health
        
        if health_diff > 0:  # Self is healthier, wins the combat
            # Opponent takes full damage, winner takes minimal damage
            opponent.take_damage(self.damage)
            if self.team == 'ally' and not self.invincible:
                self.health -= max(1, self.damage // 2)  # Reduced damage for winner
                self.invincible = True
                self.time_since_hit = pygame.time.get_ticks()
            elif self.team == 'enemy':
                self.health -= max(1, self.damage // 2)  # Reduced damage for winner
        elif health_diff < 0:  # Opponent is healthier, they win
            # Self takes full damage, opponent takes minimal damage
            self.take_damage(opponent.damage)
            if opponent.team == 'ally' and not opponent.invincible:
                opponent.health -= max(1, opponent.damage // 2)  # Reduced damage for winner
                opponent.invincible = True
                opponent.time_since_hit = pygame.time.get_ticks()
            elif opponent.team == 'enemy':
                opponent.health -= max(1, opponent.damage // 2)  # Reduced damage for winner
        else:  # Equal health - both take full damage
            self.take_damage(opponent.damage)
            opponent.take_damage(self.damage)

    def perform_wall_jump(self):
        """Jump off the wall to unstick and continue following player."""
        # Jump up and away from the wall
        self.vy = -840.0  # Strong upward velocity
        # Push away from wall
        self.vx = self.speed if self.wall_direction == 0 else -self.speed
        self.direction = 1 if self.vx > 0 else 0
        self.wall_jump_cooldown = 0.25  # 0.25 seconds
        self.on_wall = False

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

        # DBUGGING for hoitboxes do not remove
        # pygame.draw.rect(surface, (255, 0, 0), (self.rect.x - scroll, self.rect.y, self.rect.width, self.rect.height), 1)

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
            # if self.rect.y + mask_bounding_rect.bottom > map_height:
            if self.rect.y + mask_bounding_rect.top > map_height + tile_size:
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
                                
                                # Detect wall collision for wall jump
                                # wall_direction: 0=hit left wall, 1=hit right wall
                                if offset_x > 0:  # Hit left wall (tile is to the right)
                                    self.on_wall = True
                                    self.wall_direction = 1
                                else:  # Hit right wall (tile is to the left)
                                    self.on_wall = True
                                    self.wall_direction = 0
                                
                                # Optional: Push out of the wall slightly to prevent sticking
                                if self.vx > 0: self.rect.left = tile_rect.right - self.left_offset
                                else: self.rect.right = tile_rect.left + self.right_offset
                                self.x = float(self.rect.x)

                                self.mask_frame = pygame.transform.flip(self.mask_frame, True, False)
                                self.mask = pygame.mask.from_surface(self.mask_frame)
                                mask_rects = self.mask.get_bounding_rects()
                                self.left_offset = mask_rects[0].left
                                self.right_offset = self.rect.width - mask_rects[0].right
                                
                                return

                            elif axis == 'y':
                                # Only adjust Y if we aren't moving horizontally into a wall
                                if self.vy > 0:  # Falling
                                    self.rect.bottom = tile_rect.top + self.bottom_offset
                                    self.on_ground = True
                                    self.on_wall = False  # Reset wall flag when on ground
                                elif self.vy < 0:  # Jumping Up
                                    self.rect.top = tile_rect.bottom - self.top_offset
                                
                                self.y = float(self.rect.y)
                                self.vy = 0
                                return