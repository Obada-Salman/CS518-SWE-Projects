import pygame
from settings import *
from button import Button
from Player import Player

class MainMenuState:
    def __init__ (self, name, state_machine):
        self.name = name
        self.state_machine = state_machine
        # TODO making the buttons dynamic based on screen size
        self.BASE_WIDTH = 800
        self.BASE_HEIGHT = 600
        display_info = pygame.display.Info()
        self.screen_width, self.screen_height = display_info.current_w, display_info.current_h
        scale_x = self.screen_width / self.BASE_WIDTH
        scale_y = self.screen_height / self.BASE_HEIGHT
        btn_width = int(200 * scale_x)
        btn_height = int(50 * scale_y)
        btn_spacing = int(70 * scale_y)
        font_size = max(int(36 * scale_x), 10)
        scale = min(min(scale_x, scale_y), 1.0)
        btn_width = int(200 * scale)
        btn_height = int(50 * scale)
        btn_spacing = int(70 * scale)
        font_size = max(int(36 * scale), 10)
        button_x = (self.screen_width // 2)
        button_y = (self.screen_height // 2) - int(100 * scale)
        btn_font = pygame.font.SysFont(None, font_size)
        
        button_x = (self.screen_width // 2) - (btn_width // 2)
        button_y = (self.screen_height // 2) - int(100 * scale)
        self.story = Button(button_x, button_y, btn_width, btn_height, "Story Mode", btn_font, BLACK, WHITE)
        self.custom = Button(button_x, button_y + btn_spacing, btn_width, btn_height, "Custom Level", btn_font, BLACK, WHITE)
        self.setting = Button(button_x, button_y + btn_spacing * 2, btn_width, btn_height, "Settings", btn_font, BLACK, WHITE)
        self.level_bld = Button(button_x, button_y + btn_spacing * 3, btn_width, btn_height, "Level Builder", btn_font, BLACK, WHITE)
        self.quit = Button(button_x, button_y + btn_spacing * 4, btn_width, btn_height, "Quit", btn_font, RED, WHITE)
        
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
            elif event.type == pygame.VIDEORESIZE:
                self.__init__(self.name, self.state_machine)  
                
    def draw(self, surface):
        surface.fill(WHITE)
        title = pygame.font.Font(None, 74).render("Onions May Cry", True, BLACK)
        surface.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        self.story.draw(surface)
        self.custom.draw(surface)
        self.setting.draw(surface)
        self.level_bld.draw(surface)
        self.quit.draw(surface)
        
    def enter(self):
        self.__init__(self.name, self.state_machine)
        
                