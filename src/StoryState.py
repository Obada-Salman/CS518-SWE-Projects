import pygame
from settings import *
from button import Button
from Player import Player
from Enemy import Enemy

class StoryState:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.setup_ui()
        self.player = Player(100, self.screen_height - 100, 34 * 3, 34 * 3)
        self.enemy = Enemy(400, self.screen_height - 110, 75, 110)
        
    def setup_ui(self):    
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = BASE_WIDTH, BASE_HEIGHT

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

        self.player.update()
        self.enemy.update()

    def draw(self, surface):
        surface.fill(GREEN)
        text = pygame.font.Font(None, 74).render("Level 1", True, BLACK)
        surface.blit(text, (self.screen_width//2 - text.get_width()//2, 50))
        self.player.draw(surface)
        self.enemy.draw(surface)
        
    def enter(self):
        self.setup_ui()