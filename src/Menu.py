import pygame
from settings import *
from button import Button
from Player import Player

class MainMenuState:
    def __init__ (self, name, state_machine):
        self.name = name
        self.state_machine = state_machine
        # TODO making the buttons dynamic based on screen size
        button_x = (SCREEN_WIDTH) // 2 - 100
        self.story = Button(button_x, 200, 200, 50, "Story Mode", pygame.font.SysFont(None, 36), BLACK, WHITE)
        self.custom = Button(button_x, 270, 200, 50, "Custom Level", pygame.font.SysFont(None, 36), BLACK, WHITE)
        self.setting = Button(button_x, 340, 200, 50, "Settings", pygame.font.SysFont(None, 36), BLACK, WHITE)
        self.level_bld = Button(button_x, 410, 200, 50, "Level Builder", pygame.font.SysFont(None, 36), BLACK, WHITE)
        self.quit = Button(button_x, 480, 200, 50, "Quit", pygame.font.SysFont(None, 36), RED, (255, 255, 255))
        
    def update(self, events):
        for event in events:
            if self.story.is_clicked(event):
                self.state_machine.transition('story')
            elif self.custom.is_clicked(event):
                self.state_machine.transition('custom')
            elif self.setting.is_clicked(event):
                self.state_machine.transition('settings')
            elif self.level_bld.is_clicked(event):
                self.state_machine.transition('level_bld')
            elif self.quit.is_clicked(event):
                self.state_machine.quit()
                
    def draw(self, surface):
        surface.fill(WHITE)
        title = pygame.font.Font(None, 74).render("Main Menu", True, BLACK)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        self.story.draw(surface)
        self.custom.draw(surface)
        self.setting.draw(surface)
        self.level_bld.draw(surface)
        self.quit.draw(surface)
                
class StoryState:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.player = Player(100, SCREEN_HEIGHT)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')

        self.player.update()

    def draw(self, surface):
        surface.fill(GREEN)
        text = pygame.font.Font(None, 74).render("Level 1", True, BLACK)
        surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))
        self.player.draw(surface)