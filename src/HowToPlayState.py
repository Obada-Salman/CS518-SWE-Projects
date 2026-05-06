import pygame
from settings import *
from button import Button

class HowToPlayState:
    def __init__(self, state_machine):
        self.name = 'how_to_play'
        self.state_machine = state_machine
        self.setup_ui()

    def setup_ui(self):
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = BASE_WIDTH, BASE_HEIGHT

        self.scale = min(self.screen_width / BASE_WIDTH, self.screen_height / BASE_HEIGHT)
        font_size = max(int(28 * self.scale), 14)
        btn_font = pygame.font.SysFont(None, max(int(34 * self.scale), 16))

        button_width = int(180 * self.scale)
        button_height = int(50 * self.scale)
        button_x = (self.screen_width - button_width) // 2
        button_y = self.screen_height - button_height - int(40 * self.scale)

        self.btn_back = Button(button_x, button_y, button_width, button_height, "Back", btn_font, BLACK, WHITE)
        self.title_font = pygame.font.Font(None, max(int(64 * self.scale), 24))
        self.text_font = pygame.font.SysFont(None, font_size)
        self.heading_font = pygame.font.SysFont(None, font_size, bold=True)
        self.heading_titles = {"Story", "Controls", "Objective", "Level Builder"}

        self.content_padding = int(20 * self.scale)
        content_top = int(150 * self.scale)
        content_bottom = self.btn_back.rect.top - int(20 * self.scale)
        self.content_rect = pygame.Rect(
            int(80 * self.scale),
            content_top,
            self.screen_width - int(160 * self.scale),
            max(0, content_bottom - content_top),
        )

        self.instructions = [
            "Story",
            "In the once peaceful and fruitful Saladlands, a corrupt king named Pumpking",
            "has taken over and converted other vegetables into soulless and emotionless",
            "workers. Onions, being the emotional vegetables they are, were left to rot",
            "underground. You play as the only surviving onion, and your goal is to defeat",
            "Pumpking and restore the Saladlands. You will face some non-corrupt vegetables",
            "on your way who are willing to join your cause, and you can collect resources",
            "such as sunlight, water, and nutrients to plant onions when possible and help",
            "grow your endangered species.",
            "",
            "Controls",
            "Arrow keys to move.",
            "Space or Up arrow to jump.",
            "X to shoot tears.",
            "ESC to pause the game.",
            "",
            "Objective",
            "Defeat all enemies within each level and go through the exit door to progress to the next level.",
            "Allies are stationary and marked with a gray circle. When nearby, press E to recruit them and they",
            "will help you fight enemies. The circle will turn green and reflect the ally's health.",
            "When nearby flowerpots, press E to plant onion allies given you have enough resources. Each onion",
            "costs 5 sunlight, 5 water, and 5 nutrients to plant.",
            "",
            "Level Builder",
            "Left click to place objects, right click to remove objects.",
            "A and D to scroll left and right.",
            "Left/right arrows to cycle through levels."
        ]
        self.scroll_offset = 0
        self.scroll_speed = max(int(40 * self.scale), 10)
        self._update_scroll_limits()

    def _update_scroll_limits(self):
        line_height = self.text_font.get_height() + int(8 * self.scale)
        content_height = len(self.instructions) * line_height
        visible_height = max(0, self.content_rect.height - self.content_padding * 2)
        self.max_scroll = max(0, content_height - visible_height)
        self.scroll_offset = min(max(self.scroll_offset, 0), self.max_scroll)

    def update(self, events, dt):
        for event in events:
            if self.btn_back.is_clicked(event):
                self.state_machine.transition('menu')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y * self.scroll_speed
                self.scroll_offset = min(max(self.scroll_offset, 0), self.max_scroll)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
                amount = 1 if event.button == 4 else -1
                self.scroll_offset -= amount * self.scroll_speed
                self.scroll_offset = min(max(self.scroll_offset, 0), self.max_scroll)
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

    def draw(self, surface):
        surface.fill(WHITE)
        title = self.title_font.render("How to Play", True, BLACK)
        surface.blit(title, (self.screen_width // 2 - title.get_width() // 2, int(50 * self.scale)))

        pygame.draw.rect(surface, (245, 245, 245), self.content_rect, border_radius=14)
        pygame.draw.rect(surface, BLACK, self.content_rect, 2, border_radius=14)

        line_height = self.text_font.get_height() + int(8 * self.scale)
        x_text = self.content_rect.x + self.content_padding
        y_start = self.content_rect.y + self.content_padding
        previous_clip = surface.get_clip()
        surface.set_clip(self.content_rect)
        for index, line in enumerate(self.instructions):
            if line.strip():
                font = self.heading_font if line in self.heading_titles else self.text_font
                rendered = font.render(line, True, BLACK)
                line_y = y_start + index * line_height - self.scroll_offset
                if line_y + line_height < self.content_rect.y or line_y > self.content_rect.bottom:
                    continue
                center_x = self.content_rect.x + (self.content_rect.width - rendered.get_width()) // 2
                surface.blit(rendered, (center_x, line_y))
        surface.set_clip(previous_clip)

        self.btn_back.draw(surface)

    def enter(self):
        self.setup_ui()
