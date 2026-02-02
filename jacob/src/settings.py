import pygame

pygame.init()
display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
MARGIN_WIDTH = 200
MARGIN_HEIGHT = 100
SCROLL = 0
SCROLL_SPEED = 1

ROWS = 20
COLS = 100
TILE_SIZE = (SCREEN_HEIGHT - MARGIN_HEIGHT) // ROWS
# TILE_NUM = len(tile_class.tile_types)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = BLACK

# BUTTON_ROW = 0
# BUTTON_COL = 0
# CURRENT_TILE = 0
# CURRENT_TILE_TYPE = ""

LEVEL = 1

pygame.font.init()
FONT = pygame.font.SysFont("ttf", 50)