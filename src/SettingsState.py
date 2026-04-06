import pygame
from settings import *
from button import Button

class SettingsState:
    def __init__(self, state_machine):
        self.name = 'settings'
        self.state_machine = state_machine
        self.setup_ui()
        
    def setup_ui(self):
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        
        display_info = pygame.display.Info()
        self.screen_width, self.screen_height = display_info.current_w, display_info.current_h
        
        scale_x = self.screen_width / self.BASE_WIDTH
        scale_y = self.screen_height / self.BASE_HEIGHT
        
        scale = min(scale_x, scale_y) 
        
        btn_width = int(200 * scale)
        btn_height = int(50 * scale)
        btn_spacing = int(70 * scale)
        font_size = max(int(36 * scale), 10)
        btn_font = pygame.font.SysFont(None, font_size)
        
        button_x = (self.screen_width // 2) - (btn_width // 2)
        button_y = (self.screen_height // 2) - int(150 * scale)
        
        self.btn_800 = Button(button_x, button_y, btn_width, btn_height, "800x600", btn_font, BLACK, WHITE)
        self.btn_1280 = Button(button_x, button_y + btn_spacing, btn_width, btn_height, "1280x720", btn_font, BLACK, WHITE)
        self.btn_1920 = Button(button_x, button_y + btn_spacing * 2, btn_width, btn_height, "1920x1080", btn_font, BLACK, WHITE)
        self.btn_full = Button(button_x, button_y + btn_spacing * 3, btn_width, btn_height, "Fullscreen", btn_font, BLACK, WHITE)
        self.btn_back = Button(button_x, button_y + btn_spacing * 4, btn_width, btn_height, "Back", btn_font, BLACK, WHITE)
        if self.state_machine.max_unlocked_level <= 2:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu1.png')
        elif self.state_machine.max_unlocked_level <= 4:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu2.png')
        else:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu3.png')
            
        self.scaled_bg = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def update(self, events):
        for event in events:
            if self.btn_800.is_clicked(event):
                self.change_resolution(800, 600)
            elif self.btn_1280.is_clicked(event):
                self.change_resolution(1280, 720)
            elif self.btn_1920.is_clicked(event):
                self.change_resolution(1920, 1080)
            elif self.btn_full.is_clicked(event):
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.setup_ui()
            elif self.btn_back.is_clicked(event):
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()
                
    def change_resolution(self, width, height):
        pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen_width = width
        self.screen_height = height
        self.setup_ui()
        
    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.scaled_bg, (0, 0))
        
        title_scale = min(self.screen_width / self.BASE_WIDTH, self.screen_height / self.BASE_HEIGHT)
        title_font = pygame.font.Font(None, max(int(74 * title_scale), 20))
        title = title_font.render("Settings", True, BLACK)
        
        surface.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(50 * title_scale)))
        
        self.btn_800.draw(surface)
        self.btn_1280.draw(surface)
        self.btn_1920.draw(surface)
        self.btn_full.draw(surface)
        self.btn_back.draw(surface)
        
    def enter(self):
        self.setup_ui()

#TODO: Add more settings options (e.g. volume, controls)