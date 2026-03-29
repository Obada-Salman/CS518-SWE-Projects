import pygame
from SpriteHandler import *
from settings import *

class Player:
    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        
        self.speed = 5
        self.health = 5
        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.8  # Slightly increased for snappier feel
        self.jump_strength = -16.0
        self.on_ground = False
        self.moving = False

        self.direction = 1 
        self.state = 0 
        self.invincible = False
        self.time_since_hit = 0
        self.visible = True
        self.invincibility_time = 2000

        self.sprites = SpriteHandler("assets/images/Characters/Onion_34x34.png", type='player', scale=3, anim_time=7)
        self.tear = pygame.image.load("assets/images/Misc/tear_34x34.png")
        self.health_image = pygame.image.load('assets/images/Misc/health_50x50.png')
        self.tears = [] 
        self.x_pressed_last_frame = False 

        self.snd_tear_shoot = pygame.mixer.Sound('assets/sounds/tear_shoot.ogg')
        self.snd_jump = pygame.mixer.Sound('assets/sounds/jump.ogg')

        self.mask = pygame.mask.from_surface(self.sprites.get_current_frame())

    def handle_input(self):
        key = pygame.key.get_pressed()
        
        self.vx = 0.0
        self.moving = False

        if key[pygame.K_LEFT]:
            self.vx = -self.speed
            self.direction = 0
            self.moving = True
        elif key[pygame.K_RIGHT]:
            self.vx = self.speed
            self.direction = 1
            self.moving = True

        if (key[pygame.K_UP] or key[pygame.K_SPACE]) and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False
            self.snd_jump.play()

        x_pressed_now = key[pygame.K_x]
        if x_pressed_now and not self.x_pressed_last_frame:
            self.shoot_tear()
        self.x_pressed_last_frame = x_pressed_now

    def shoot_tear(self):
        tear_surface = self.tear
        tear_rect = self.tear.get_rect(center=self.rect.center)
        tear_mask = pygame.mask.from_surface(tear_surface)

        self.tears.append({'rect': tear_rect, 'direction': self.direction, 'speed': 10, 'mask': tear_mask})
        self.snd_tear_shoot.play()


    def update(self, game_map, tile_size):
        self.handle_input()
        self.on_ground = False

        # Move X
        self.x += self.vx
        self.rect.x = int(self.x)
        self.check_map_collision(game_map, tile_size, 'x')

        # Move Y
        if not self.on_ground:
            self.vy += self.gravity
            if self.vy > 14:
                self.vy = 14
        else:
            self.vy = 0
        
        
        self.y += self.vy
        self.rect.y = int(self.y)
        self.check_map_collision(game_map, tile_size, 'y')

        # Cleanup: sync tears and invincibility
        for tear in self.tears[:]:
            tear['rect'].x += tear['speed'] if tear['direction'] == 1 else -tear['speed']

        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.time_since_hit < self.invincibility_time:
                self.visible = not self.visible
            else:
                self.visible, self.invincible = True, False

        # Animation states
        if not self.on_ground:
            self.state = 2
        elif self.moving and abs(self.vx) > 0.1:
            self.state = 1
        else:
            self.state = 0

        self.sprites.update(self.direction, self.state)
        
        current_frame = self.sprites.get_current_frame()
        self.mask = pygame.mask.from_surface(current_frame)

    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.time_since_hit = pygame.time.get_ticks()

    def can_damage(self):
        return not self.invincible
    
    def is_alive(self):
        return self.health > 0

    def draw(self, surface):
        if self.visible:
            self.sprites.draw(surface, self.rect.x, self.rect.y)
        
        for tear in self.tears:
            surface.blit(self.tear, tear['rect'])
        surface.blit(self.health_image, (10, 10))
        surface.blit(pygame.font.SysFont(None, 40).render(f"x {self.health}", True, (255, 255, 255)), (60, 20))
    
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
                    if tile and tile.collision:
                        
                        tile_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)                        
                        tile_mask = pygame.mask.Mask((tile_size, tile_size), fill=True)
                        offset_x = tile_rect.x - self.rect.x
                        offset_y = tile_rect.y - self.rect.y

                        if self.mask.overlap(tile_mask, (offset_x, offset_y)):
                            if axis == 'x':
                                if self.vx > 0:  # moving right
                                    while self.mask.overlap(tile_mask, (offset_x, offset_y)):
                                        self.rect.x -= 1
                                        self.x = float(self.rect.x)
                                        offset_x = tile_rect.x - self.rect.x

                                elif self.vx < 0:  # moving left
                                    while self.mask.overlap(tile_mask, (offset_x, offset_y)):
                                        self.rect.x += 1
                                        self.x = float(self.rect.x)
                                        offset_x = tile_rect.x - self.rect.x

                                self.vx = 0
                                return

                            elif axis == 'y':
                                if self.vy > 0:  # falling
                                    while self.mask.overlap(tile_mask, (offset_x, offset_y)):
                                        self.rect.y -= 1
                                        self.y = float(self.rect.y)
                                        offset_y = tile_rect.y - self.rect.y
                                    
                                    self.on_ground = True
                                
                                elif self.vy < 0:
                                    while self.mask.overlap(tile_mask, (offset_x, offset_y)):
                                        self.rect.y += 1
                                        self.y = float(self.rect.y)
                                        offset_y = tile_rect.y - self.rect.y
                            
                                self.vy = 0

                            return