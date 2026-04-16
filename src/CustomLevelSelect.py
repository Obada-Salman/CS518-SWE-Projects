import pygame
from settings import *
from button import Button

class CustomLevelSelect:
    def __init__(self, name, state_machine):
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        self.name = name
        self.state_machine = state_machine
        self.current_stage = 1
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
        
        GRAY = (150, 150, 150)
        
        self.level_buttons = []
        start_level = (self.current_stage - 1) * 5
        
        for i in range(num_buttons):
            level_num = start_level + i + 1
            x_pos = btn_spacing + i * (btn_width + btn_spacing)
            color = BLACK
            
            btn = Button(x_pos, button_y, btn_width, btn_height, str(level_num), btn_font, color, WHITE)
            self.level_buttons.append((btn, level_num))
        
        arrow_w = int(50 * scale)
        arrow_h = int(50 * scale)
        arrow_y = button_y + (btn_height // 2) - (arrow_h // 2)
        
        self.btn_prev = Button(btn_spacing // 4, arrow_y, arrow_w, arrow_h, "<", btn_font, BLACK, WHITE)
        self.btn_next = Button(self.screen_width - (btn_spacing // 4) - arrow_w, arrow_y, arrow_w, arrow_h, ">", btn_font, BLACK, WHITE)
        
        
        self.btn_back = Button(self.screen_width - btn_width - 10, self.screen_height - int(50 * scale) - 10, btn_width, 50 * scale, "Back", btn_font, BLACK, WHITE)
        
        if self.state_machine.max_unlocked_level <= 5:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu1.png')
        elif self.state_machine.max_unlocked_level <= 10:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu2.png')
        else:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu3.png')
            
        self.scaled_bg = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        
    def update(self, events):
        for event in events:
            for btn, level_num in self.level_buttons:
                if btn.is_clicked(event):
                    self._start_level(level_num)
                    
            if self.current_stage < 3 and self.btn_next.is_clicked(event):
                self.current_stage += 1
                self.setup_ui()
            
            if self.current_stage > 1 and self.btn_prev.is_clicked(event):
                self.current_stage -= 1
                self.setup_ui()
                
            if self.btn_back.is_clicked(event):
                self.state_machine.transition('menu')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

    def _start_level(self, level_number):
        if hasattr(self.state_machine, 'set_custom_level'):
            self.state_machine.set_custom_level(level_number)
        self.state_machine.transition('custom')
    
    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.scaled_bg, (0, 0))
        title_scale = min(self.screen_width / self.BASE_WIDTH, self.screen_height / self.BASE_HEIGHT)
        title_font = pygame.font.Font(None, max(int(74 * title_scale), 20))
        title = title_font.render(f"Custom", True, BLACK)
        
        surface.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(50 * title_scale)))
        
        for btn, _ in self.level_buttons:
            btn.draw(surface)
            
        if self.current_stage > 1:
            self.btn_prev.draw(surface)
        if self.current_stage < 3:
            self.btn_next.draw(surface)
            
        self.btn_back.draw(surface)
    
    def enter(self):
        self.setup_ui()
        
        
        
        