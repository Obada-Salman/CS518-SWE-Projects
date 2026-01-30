import pygame
from settings import *
from button import Button

class LevelSelectState:
    def __init__(self, manager):
        self.manager = manager
        cx = SCREEN_WIDTH // 2 - 100
        
        self.btn_lvl1 = Button("Level 1", cx, 150, 200, 50, GREEN, DARK_GRAY)
        self.btn_lvl2 = Button("Level 2", cx, 220, 200, 50, GREEN, DARK_GRAY)
        self.btn_lvl3 = Button("Level 3", cx, 290, 200, 50, GREEN, DARK_GRAY)
        
        self.btn_back = Button("Back to Menu", cx, 400, 200, 50, RED, DARK_GRAY)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_lvl1.check_click():
                    self.manager.set_state('level_one')
                elif self.btn_lvl2.check_click():
                    self.manager.set_state('level_two')
                elif self.btn_lvl3.check_click():
                    self.manager.set_state('level_three')
                elif self.btn_back.check_click():
                    self.manager.set_state('menu')

    def draw(self, surface):
        surface.fill(DARK_GRAY)
        
        title = pygame.font.Font(None, 60).render("Select Level", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        self.btn_lvl1.draw(surface)
        self.btn_lvl2.draw(surface)
        self.btn_lvl3.draw(surface)
        self.btn_back.draw(surface)