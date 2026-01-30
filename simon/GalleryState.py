import pygame
from settings import *
from button import Button

class GalleryState:
    def __init__(self, manager):
        self.manager = manager
        
        self.btn_back = Button("Back", SCREEN_WIDTH//2 - 100, 500, 200, 50, RED, DARK_GRAY)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_back.check_click():
                    self.manager.set_state('menu')

    def draw(self, surface):
        surface.fill((30, 30, 60)) 
        
        title = pygame.font.Font(None, 60).render("Gallery", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        
        
        self.btn_back.draw(surface)