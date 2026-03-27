import pygame
from settings import *
from button import Button

class PauseState:
    def __init__(self, name, state_machine):
        self.name = name
        self.state_machine = state_machine
        self.setup_ui()

    def setup_ui(self):
        surface = pygame.display.get_surface()
        self.screen_width, self.screen_height = surface.get_size() if surface else (BASE_WIDTH, BASE_HEIGHT)
        
        scale_x = self.screen_width / BASE_WIDTH
        scale_y = self.screen_height / BASE_HEIGHT
        
        scale = min(scale_x, scale_y)
        
        btn_width = int(200 * scale)
        btn_height = int(50 * scale)
        btn_spacing = int(50 * scale)
        font_size = max(int(36 * scale), 10)
        btn_font = pygame.font.SysFont(None, font_size)
        
        button_x = (self.screen_width // 2) - (btn_width // 2)
        button_y = (self.screen_height // 2) - int(100 * scale)
        
        self.btn_resume = Button(button_x, button_y, btn_width, btn_height, "Resume", btn_font, BLACK, WHITE)
        self.btn_levels = Button(button_x, button_y + btn_height + btn_spacing, btn_width, btn_height, "Level Select", btn_font, BLACK, WHITE)
        self.btn_menu = Button(button_x, button_y + 2 * (btn_height + btn_spacing), btn_width, btn_height, "Main Menu", btn_font, BLACK, WHITE)
        

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('story')
            
            if self.btn_resume.is_clicked(event):
                self.state_machine.transition('story')
            
            if self.btn_levels.is_clicked(event):
                self.state_machine.transition('level_select')
                
            if self.btn_menu.is_clicked(event):
                self.state_machine.transition('menu')
                
            if event.type == pygame.VIDEORESIZE:
                self.setup_ui()
                if 'story' in self.state_machine.states:
                    self.state_machine.states['story'].setup_ui()

    def draw(self, surface):
        if 'story' in self.state_machine.states:
            self.state_machine.states['story'].draw(surface)
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128)) 
        surface.blit(overlay, (0,0))

        # 2. Draw Pause Text
        title_font = pygame.font.SysFont(None, 80)
        title_text = title_font.render("PAUSED", True, BLACK)
        surface.blit(title_text, (self.screen_width//2 - title_text.get_width()//2, 100))

        self.btn_resume.draw(surface)
        self.btn_levels.draw(surface)
        self.btn_menu.draw(surface)

    def enter(self):
        self.setup_ui()