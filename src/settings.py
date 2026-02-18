import pygame

pygame.init()

display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
MARGIN_WIDTH = 200
MARGIN_HEIGHT = 100
ROWS = 20
COLS = 100
TILE_SIZE = SCREEN_HEIGHT // ROWS
SCROLL = 0
SCROLL_SPEED = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = BLACK