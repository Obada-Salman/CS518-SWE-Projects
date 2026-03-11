import pygame
from SpriteHandler import *
from settings import *
from configs import *

class Player:
    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        # self.screen_width = BASE_WIDTH 
        # self.screen_height = BASE_HEIGHT - 80
        self.speed = 5
        self.health = 5

        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.6
        self.jump_strength = -16.0
        self.on_ground = False

        self.direction = 1  # Right = 1, Left = 0
        self.state = 0      # Idle = 0, Walk = 1, Jump/Fall = 2
        self.invincible = False
        self.time_since_hit = 0
        self.visible = True
        self.invincibility_time = 2000 # milliseconds

        self.sprites = SpriteHandler("assets/images/Characters/Onion_34x34.png", type='player', scale=3, anim_time=7)
        self.tear = pygame.image.load("assets/images/Misc/tear_34x34.png")
        self.health_image = pygame.image.load('assets/images/Misc/health_50x50.png')
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.tear_rect = self.tear.get_rect()
        self.tears = [] # list to hold active tears
        self.x_pressed_last_frame = False  # used so that holding down X doesn't shoot tears every frame

    def handle_input(self):
        key = pygame.key.get_pressed()
        self.vx = 0.0
        if key[pygame.K_LEFT]:
            self.vx = -self.speed
            self.direction = 0
            if self.on_ground:
                self.state = 1
            else:
                self.state = 2
        elif key[pygame.K_RIGHT]:
            self.vx = self.speed
            self.direction = 1
            if self.on_ground:
                self.state = 1
            else:
                self.state = 2
        else:
            if self.on_ground:
                self.state = 0

        if (key[pygame.K_UP] or key[pygame.K_SPACE]) and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False
            self.state = 2

        # shoot tear only on X press, not hold
        x_pressed_now = key[pygame.K_x]
        if x_pressed_now and not self.x_pressed_last_frame:
            self.shoot_tear()
        self.x_pressed_last_frame = x_pressed_now

    # def apply_physics(self):
    #     self.x += self.vx
    #     self.vy += self.gravity
    #     self.y += self.vy

        # floor = self.screen_height - self.height
        # if self.y >= floor:
        #     self.y = floor
        #     self.vy = 0.0
        #     self.on_ground = True

        # if self.x < 0:
        #     self.x = 0
        # if self.x + self.width > self.screen_width:
        #     self.x = self.screen_width - self.width

    def shoot_tear(self):
        self.tear_rect = self.tear.get_rect(center=self.rect.center)
        self.tears.append({'rect': self.tear_rect, 'direction': self.direction, 'speed': 10})

    def update(self):
        self.handle_input()

        # self.apply_physics()
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for tear in self.tears:
            if tear['direction'] == 1:
                tear['rect'].x += tear['speed']
            else:
                tear['rect'].x -= tear['speed']

            # if tear['rect'].right < 0 or tear['rect'].left > self.screen_width:
            #     self.tears.remove(tear)

        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.time_since_hit < self.invincibility_time:
                self.visible = not self.visible
            else:
                self.visible = True
                self.invincible = False

        self.sprites.update(self.direction, self.state)

    def take_damage(self, amount):
        now = pygame.time.get_ticks()
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.time_since_hit = now
        elif now - self.time_since_hit > self.invincibility_time:
            self.invincible = False

    def can_damage(self):
        return not self.invincible
    
    def is_alive(self):
        return self.health > 0

    def draw(self, surface):
        if self.visible:
            self.sprites.draw(surface, int(self.x), int(self.y))
        for tear in self.tears:
            surface.blit(self.tear, tear['rect'])
        surface.blit(self.health_image, (10, 10))
        surface.blit(pygame.font.SysFont(None, 40).render(f"x {self.health}", True, (255, 255, 255)), (60, 20))