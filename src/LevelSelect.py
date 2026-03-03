import pygame
from settings import *
from button import Button

class LevelSelectState:
    def __init__(self, name, state_machine):
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        self.name = name
        self.state_machine = state_machine
        self.setup_ui()
        
    def setup_ui(self):
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = BASE_WIDTH, BASE_HEIGHT
            
        scale_x = self.screen_width / BASE_WIDTH
        scale_y = self.screen_height / BASE_HEIGHT
        
        scale = min(scale_x, scale_y)
        
        btn_width = int(100 * scale)
        btn_height = int(100 * scale)
        font_size = max(int(36 * scale), 10)
        btn_font = pygame.font.SysFont(None, font_size)
        num_buttons = 5
        total_button_width = num_buttons * btn_width
        total_empty_space = self.screen_width - total_button_width
        btn_spacing = total_empty_space // (num_buttons + 1)
        button_y = (self.screen_height // 3) - (btn_height // 2)
        
        
        button_x = (self.screen_width // 5) - int(150 * scale)
       
        
        self.btn_1 = Button(btn_spacing, button_y, btn_width, btn_height, "1", btn_font, BLACK, WHITE)
        self.btn_2 = Button(btn_spacing + 1 * (btn_width + btn_spacing), button_y, btn_width, btn_height, "2", btn_font, BLACK, WHITE)
        self.btn_3 = Button(btn_spacing + 2 * (btn_width + btn_spacing), button_y, btn_width, btn_height, "3", btn_font, BLACK, WHITE)
        self.btn_4 = Button(btn_spacing + 3 * (btn_width + btn_spacing), button_y, btn_width, btn_height, "4", btn_font, BLACK, WHITE)
        self.btn_5 = Button(btn_spacing + 4 * (btn_width + btn_spacing), button_y, btn_width, btn_height, "5", btn_font, BLACK, WHITE)
        self.btn_back = Button(self.screen_width - btn_width - 10, self.screen_height - int(50 * scale) - 10, btn_width, 50 * scale, "Back", btn_font, BLACK, WHITE)
        
    def update(self, events):
        for event in events:
            if self.btn_1.is_clicked(event):
                self._start_level(1)
            elif self.btn_2.is_clicked(event):
                self._start_level(2)
            elif self.btn_3.is_clicked(event):
                self._start_level(3)
            elif self.btn_4.is_clicked(event):
                self._start_level(4)
            elif self.btn_5.is_clicked(event):
                self._start_level(5)
            elif self.btn_back.is_clicked(event):
                self.state_machine.transition('menu')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

    def _start_level(self, level_number):
        if hasattr(self.state_machine, 'set_story_level'):
            self.state_machine.set_story_level(level_number)
        self.state_machine.transition('story')
    
    def draw(self, surface):
        surface.fill(WHITE)
        
        title_scale = min(self.screen_width / self.BASE_WIDTH, self.screen_height / self.BASE_HEIGHT)
        title_font = pygame.font.Font(None, max(int(74 * title_scale), 20))
        title = title_font.render("Stage Select", True, BLACK)
        
        surface.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(50 * title_scale)))
        
        self.btn_1.draw(surface)
        self.btn_2.draw(surface)
        self.btn_3.draw(surface)
        self.btn_4.draw(surface)
        self.btn_5.draw(surface)
        self.btn_back.draw(surface)
    
    def enter(self):
        self.setup_ui()
        
        
        
        