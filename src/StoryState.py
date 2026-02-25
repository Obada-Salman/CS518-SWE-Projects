import pygame
from settings import *
from button import Button
from Player import Player

class StoryState:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.player = Player(100, SCREEN_HEIGHT, float(747) // 6, float(1024) // 6)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.__init__(self.state_machine)

        self.player.update()

    def draw(self, surface):
        surface.fill(GREEN)
        text = pygame.font.Font(None, 74).render("Level 1", True, BLACK)
        surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))
        self.player.draw(surface)
        
    def enter(self):
        self.__init__(self.state_machine)