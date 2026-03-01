import pygame
from settings import *
from SpriteHandler import SpriteHandler
from configs import *

class Enemy:
    def __init__(self, x, y, width, height, type='enemy_carrot', speed=5):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.type = type
        self.speed = speed
        self.screen_width = BASE_WIDTH
        self.screen_height = BASE_HEIGHT

        self.vx = -self.speed
        self.vy = 0.0
        self.gravity = 0.6
        self.on_ground = False

        self.direction = 1 if self.vx > 0 else 0 # Right = 1, Left = 0
        self.state = 1 # Idle = 0, Walk = 1, Jump/Fall = 2

        # For now, just use the carrot sprite sheet. We can add more modularity later once we have more enemy types.
        self.sprites = SpriteHandler("assets/images/Carrot_75x110.png", type=self.type)

        self.enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def apply_physics(self):
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

        floor = self.screen_height - self.height
        if self.y >= floor:
            self.y = floor
            self.vy = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        # simple movement for now: just bounce back and forth between edges
        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)
        if self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width
            self.vx = -abs(self.vx)

        self.direction = 1 if self.vx > 0 else 0
        self.state = 1 if self.vx != 0 else 0

    def update(self):
        self.apply_physics()
        self.enemy_rect.topleft = (self.x, self.y)
        self.sprites.update(direction=self.direction, state=self.state)

    def draw(self, surface):
        self.sprites.draw(surface, int(self.x), int(self.y))