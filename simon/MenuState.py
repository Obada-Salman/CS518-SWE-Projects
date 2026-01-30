import pygame
import sys
from settings import *
from button import Button

class MainMenuState:
    def __init__(self, manager):
        self.manager = manager
        cx = SCREEN_WIDTH // 2 - 100
        self.btn_play = Button("Play", cx, 150, 200, 50, BLUE, DARK_GRAY)
        self.btn_levels = Button("Levels", cx, 220, 200, 50, BLUE, DARK_GRAY)
        self.btn_gallery = Button("Gallery", cx, 290, 200, 50, BLUE, DARK_GRAY)
        self.btn_quit = Button("Quit", cx, 360, 200, 50, RED, DARK_GRAY)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_play.check_click():
                    if self.manager.last_level:
                        self.manager.set_state(self.manager.last_level)
                    else:
                        self.manager.set_state('level_one')
                elif self.btn_levels.check_click():
                    self.manager.set_state('level_select')
                elif self.btn_gallery.check_click():
                    self.manager.set_state('gallery')
                elif self.btn_quit.check_click():
                    pygame.quit()
                    sys.exit()

    def draw(self, surface):
        surface.fill(DARK_GRAY)
        title = pygame.font.Font(None, 74).render("Main Menu", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        self.btn_play.draw(surface)
        self.btn_levels.draw(surface)
        self.btn_gallery.draw(surface)
        self.btn_quit.draw(surface)