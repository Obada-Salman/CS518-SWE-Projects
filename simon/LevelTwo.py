import pygame
from settings import *

class LevelTwo:
    def __init__(self, manager):
        self.manager = manager
        self.player_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]
        self.speed = 5

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.last_level = 'level_two'
                    self.manager.set_state('pause')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.player_pos[0] -= self.speed
        if keys[pygame.K_RIGHT]: self.player_pos[0] += self.speed
        if keys[pygame.K_UP]:    self.player_pos[1] -= self.speed
        if keys[pygame.K_DOWN]:  self.player_pos[1] += self.speed

    def draw(self, surface):
        surface.fill((0, 0, 50))
        font = pygame.font.Font(None, 48)
        text = font.render("Level Two", True, WHITE)
        surface.blit(text, (20, 20))
        pygame.draw.circle(surface, BLUE, (int(self.player_pos[0]), int(self.player_pos[1])), 20)