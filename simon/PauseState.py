import pygame
from settings import *
from button import Button

class PauseState:
    def __init__(self, manager):
        self.manager = manager
        cx = SCREEN_WIDTH // 2 - 100
        self.btn_resume = Button("Resume", cx, 200, 200, 50, GREEN, DARK_GRAY)
        self.btn_levels = Button("Levels", cx, 270, 200, 50, BLUE, DARK_GRAY)
        self.btn_menu = Button("Main Menu", cx, 340, 200, 50, RED, DARK_GRAY)
        
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.set_alpha(150)
        self.overlay.fill(BLACK)

    def update(self, events):
        target_level = self.manager.last_level if self.manager.last_level else 'menu'
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_resume.check_click():
                    self.manager.set_state(target_level)
                elif self.btn_levels.check_click():
                    self.manager.set_state('level_select')
                elif self.btn_menu.check_click():
                    self.manager.set_state('menu')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.set_state(target_level)

    def draw(self, surface):
        if self.manager.last_level:
            self.manager.states[self.manager.last_level].draw(surface)
        surface.blit(self.overlay, (0,0))
        
        title = pygame.font.Font(None, 74).render("PAUSED", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        self.btn_resume.draw(surface)
        self.btn_levels.draw(surface)
        self.btn_menu.draw(surface)