import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color=(255, 255, 255), text_hover_color=(0, 0, 0), action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = color
        self.hover_color = hover_color
        self.text_hover_color = text_hover_color
        self.text_color = text_color
        
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            bg = self.hover_color
            text_color = self.text_hover_color
        else:
            bg = self.bg_color
            text_color = self.text_color
        
        pygame.draw.rect(surface, bg, self.rect, border_radius=12)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=12) 
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
            return True
        return False