import pygame

pygame.init()

display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
MARGIN_WIDTH = 200
MARGIN_HEIGHT = 100
ROWS = 20
COLS = 100
TILE_SIZE = SCREEN_HEIGHT // ROWS
SCROLL = 0
SCROLL_SPEED = 1

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (20, 200, 20)
RED = (200, 20, 20)
HIGHLIGHT_COLOR = BLACK