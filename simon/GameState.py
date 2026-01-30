import pygame
from settings import *

class GameState:
    def __init__(self, manager):
        self.manager = manager
        self.player_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]

    def enter(self):
        print(f"Entering Level {self.manager.game_data.get('current_level', 1)}")

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.set_state('pause')

        
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_LEFT]: self.player_pos[0] -= speed
        if keys[pygame.K_RIGHT]: self.player_pos[0] += speed
        if keys[pygame.K_UP]: self.player_pos[1] -= speed
        if keys[pygame.K_DOWN]: self.player_pos[1] += speed

    def draw(self, surface):
        surface.fill(BLACK)
        
       
        current_level = self.manager.game_data.get('current_level', 1)
        font = pygame.font.Font(None, 48)
        level_text = font.render(f"Playing Level {current_level}", True, WHITE)
        surface.blit(level_text, (20, 20))
        
        help_text = pygame.font.Font(None, 24).render("Use Arrows to Move, ESC to Pause", True, GRAY)
        surface.blit(help_text, (20, 60))

        pygame.draw.circle(surface, BLUE, (int(self.player_pos[0]), int(self.player_pos[1])), 20)