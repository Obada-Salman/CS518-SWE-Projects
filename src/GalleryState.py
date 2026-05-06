
import pygame
from settings import *
from button import Button
import resource_path
from story_content import STORY_CUTSCENE_FRAMES
from dialogue_cutscene import SequencePlayer

class GalleryState:
    def __init__(self, name, state_machine):
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        self.name = name
        self.state_machine = state_machine
        self.sequence_player = SequencePlayer()
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


        btn_width = int(120 * scale)
        btn_height = int(120 * scale)
        font_size = max(int(36 * scale), 12)
        btn_font = pygame.font.SysFont(None, font_size)


        GRAY = (150, 150, 150)
        
        self.cutscene_keys = sorted(STORY_CUTSCENE_FRAMES.keys())
        num_buttons = len(self.cutscene_keys)
        max_per_row = 5
        spacing_x = (self.screen_width - (max_per_row * btn_width)) // (max_per_row + 1)
        spacing_y = int(40 * scale)

        start_y = self.screen_height // 3

        self.cutscene_buttons = []

        max_level = getattr(self.state_machine, 'max_unlocked_level', 1)

        for i, level_key in enumerate(self.cutscene_keys):
            row = i // max_per_row
            col = i % max_per_row
            x_pos = spacing_x + col * (btn_width + spacing_x)
            y_pos = start_y + row * (btn_height + spacing_y)
            unlocked = max_level >= level_key
            color = BLACK if unlocked else GRAY

            btn = Button(x_pos, y_pos,btn_width, btn_height,f"{level_key}",btn_font,color,WHITE)
            self.cutscene_buttons.append((btn, level_key))
            
        self.btn_back = Button(self.screen_width - btn_width - 10,self.screen_height - int(50 * scale) - 10,btn_width,int(50 * scale),"Back",btn_font,BLACK,WHITE
                               )
        if self.state_machine.max_unlocked_level <= 5:
            self.background = pygame.image.load(resource_path.get_resource_path('assets/images/Backgrounds/Menu1.png'))
        elif self.state_machine.max_unlocked_level <= 10:
            self.background = pygame.image.load(resource_path.get_resource_path('assets/images/Backgrounds/Menu2.png'))
        else:
            self.background = pygame.image.load(resource_path.get_resource_path('assets/images/Backgrounds/Menu3.png'))
            
        self.scaled_bg = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        
    def update(self, events, dt):
        max_level = getattr(self.state_machine, 'max_unlocked_level', 1)


        for event in events:
            for btn, level_key in self.cutscene_buttons:
                if btn.is_clicked(event) and max_level >= level_key:
                    self._start_cutscene(level_key)
                    
            if self.sequence_player.active:
                self.sequence_player.process_events(events)
                return

            if self.btn_back.is_clicked(event):
                self.state_machine.transition('menu')

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')

            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()
                
    def _start_cutscene(self, level_key):
        max_level = getattr(self.state_machine, 'max_unlocked_level', 1)
        if level_key in STORY_CUTSCENE_FRAMES and level_key <= max_level:
            frames = STORY_CUTSCENE_FRAMES.get(level_key)
            if not frames:
                return

            self.sequence_player.start_cutscene(frames)

    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.scaled_bg, (0, 0))


        title_scale = min(self.screen_width / self.BASE_WIDTH, self.screen_height / self.BASE_HEIGHT)
        title_font = pygame.font.Font(None, max(int(74 * title_scale), 20))


        title = title_font.render("Gallery", True, BLACK)
        surface.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(50 * title_scale)))

        for btn, _ in self.cutscene_buttons:
            btn.draw(surface)

        self.btn_back.draw(surface)
        
        self.sequence_player.draw(surface)


    def enter(self):
        self.setup_ui()




