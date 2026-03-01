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
        self.screen_width = BASE_WIDTH 
        self.screen_height = BASE_HEIGHT
        self.speed = 5

        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.6
        self.jump_strength = -16.0
        self.on_ground = False

        self.direction = 1  # Right = 1, Left = 0
        self.state = 0      # Idle = 0, Walk = 1, Jump/Fall = 2

        self.sprites = SpriteHandler("assets/images/Onion_34x34.png", type='player', scale=3, anim_time=7)
        self.tear = pygame.image.load("assets/images/tear_34x34.png")
        self.player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
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

    def apply_physics(self):
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

        floor = self.screen_height - self.height
        if self.y >= floor:
            self.y = floor
            self.vy = 0.0
            self.on_ground = True

        if self.x < 0:
            self.x = 0
        if self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width

    def shoot_tear(self):
        tear_rect = self.tear.get_rect(center=self.player_rect.center)
        self.tears.append({'rect': tear_rect, 'direction': self.direction, 'speed': 10})

    def update(self):
        self.handle_input()
        self.apply_physics()
        self.player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for tear in self.tears:
            if tear['direction'] == 1:
                tear['rect'].x += tear['speed']
            else:
                tear['rect'].x -= tear['speed']

            if tear['rect'].right < 0 or tear['rect'].left > self.screen_width:
                self.tears.remove(tear)

        self.sprites.update(self.direction, self.state)

    def draw(self, surface):
        self.sprites.draw(surface, int(self.x), int(self.y))
        for tear in self.tears:
            surface.blit(self.tear, tear['rect'])