import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.width = float(747) // 6
        self.height = float(1024) // 6
        self.speed = 5

        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.6
        self.jump_strength = -16.0
        self.on_ground = False

    def handle_input(self):
        key = pygame.key.get_pressed()
        self.vx = 0.0
        if key[pygame.K_LEFT]:
            self.vx = -self.speed
        if key[pygame.K_RIGHT]:
            self.vx = self.speed
        if (key[pygame.K_UP] or key[pygame.K_SPACE]) and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False

    def apply_physics(self):
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

        floor = SCREEN_HEIGHT - self.height
        if self.y >= floor:
            self.y = floor
            self.vy = 0.0
            self.on_ground = True

        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width

    def update(self):
        self.handle_input()
        self.apply_physics()

    def draw(self, surface):
        sprite = pygame.image.load("assets/images/player.png")
        sprite = pygame.transform.scale(sprite, (self.width, self.height))
        surface.blit(sprite, (self.x, self.y))