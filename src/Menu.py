import pygame
from settings import *
from button import Button
from Player import Player

class MainMenuState:
    def __init__(self, name, state_machine):
        self.name = name
        self.state_machine = state_machine
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        self.setup_ui()
        
    def setup_ui(self):
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = self.BASE_WIDTH, self.BASE_HEIGHT
            
        scale_x = self.screen_width / self.BASE_WIDTH
        scale_y = self.screen_height / self.BASE_HEIGHT
        
        scale = min(scale_x, scale_y)
        
        btn_width = int(200 * scale)
        btn_height = int(50 * scale)
        btn_spacing = int(70 * scale)
        font_size = max(int(36 * scale), 10)
        btn_font = pygame.font.SysFont(None, font_size)
        
        button_x = (self.screen_width // 2) - (btn_width // 2)
        button_y = (self.screen_height // 2) - int(100 * scale)
        self.story = Button(button_x, button_y, btn_width, btn_height, "Story Mode", btn_font, BLACK, WHITE)
        self.custom = Button(button_x, button_y + btn_spacing, btn_width, btn_height, "Custom Level", btn_font, BLACK, WHITE)
        self.setting = Button(button_x, button_y + btn_spacing * 2, btn_width, btn_height, "Settings", btn_font, BLACK, WHITE)
        self.level_bld = Button(button_x, button_y + btn_spacing * 3, btn_width, btn_height, "Level Builder", btn_font, BLACK, WHITE)
        self.quit = Button(button_x, button_y + btn_spacing * 4, btn_width, btn_height, "Quit", btn_font, RED, WHITE)

        self.username_font = pygame.font.SysFont(None, max(int(32 * scale), 14))
        input_width = int(320 * scale)
        input_height = int(44 * scale)
        input_x = (self.screen_width // 2) - (input_width // 2)
        input_y = max(110, button_y - int(80 * scale))
        self.username_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        self.username_active = False
        if not hasattr(self, "username_input"):
            existing = getattr(getattr(self.state_machine, "score_tracker", None), "username", "player1")
            self.username_input = self._normalize_username(existing)
        
        if self.state_machine.max_unlocked_level <= 5:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu1.png')
        elif self.state_machine.max_unlocked_level <= 10:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu2.png')
        else:
            self.background = pygame.image.load('assets/images/Backgrounds/Menu3.png')
            
        self.scaled_bg = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.username_active = self.username_rect.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and self.username_active:
                if event.key == pygame.K_RETURN:
                    self._apply_username()
                    self.username_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.username_input = self.username_input[:-1]
                else:
                    typed = event.unicode
                    if typed and typed.isprintable() and len(self.username_input) < 32:
                        self.username_input += typed

            if self.story.is_clicked(event):
                self._apply_username()
                self.state_machine.transition('level_select')
            elif self.custom.is_clicked(event):
                self.state_machine.transition('custom_select')
            elif self.setting.is_clicked(event):
                self.state_machine.transition('settings')
            elif self.level_bld.is_clicked(event):
                self.state_machine.transition('level_builder')
            elif self.quit.is_clicked(event):
                self.state_machine.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.__init__(self.name, self.state_machine)  
                
    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.scaled_bg, (0, 0))
        title = pygame.font.Font(None, 74).render("Onions May Cry", True, BLACK)
        surface.blit(title, (self.screen_width//2 - title.get_width()//2, 50))

        label = self.username_font.render("Player Name", True, BLACK)
        surface.blit(label, (self.username_rect.x, self.username_rect.y - 24))
        border_color = RED if self.username_active else BLACK
        pygame.draw.rect(surface, WHITE, self.username_rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.username_rect, 2, border_radius=8)
        shown_name = self.username_input if self.username_input else "player1"
        name_text = self.username_font.render(shown_name, True, BLACK)
        surface.blit(name_text, (self.username_rect.x + 10, self.username_rect.y + 10))

        self.story.draw(surface)
        self.custom.draw(surface)
        self.setting.draw(surface)
        self.level_bld.draw(surface)
        self.quit.draw(surface)
        
    def enter(self):
        self.__init__(self.name, self.state_machine)

    def _normalize_username(self, username):
        normalized = (username or "").strip()
        if not normalized:
            normalized = "player1"
        return normalized[:32]

    def _apply_username(self):
        if hasattr(self.state_machine, "set_player_username"):
            self.username_input = self.state_machine.set_player_username(self.username_input)
        else:
            self.username_input = self._normalize_username(self.username_input)
        
                