import pygame
import game_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN_WIDTH, MARGIN_HEIGHT, SCROLL, SCROLL_SPEED, BLACK, WHITE, ROWS
scaled_tile_size = TILE_SIZE = (SCREEN_HEIGHT - MARGIN_HEIGHT) // ROWS

player_placed = False
goal_placed = False

current_tile = ""

tile_map = game_map.load_map("src/tiles2.pkl")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
running = True

while running:
    screen.fill(BLACK)
    game_map.draw_map(screen, tile_map, scaled_tile_size, SCROLL)
    game_map.draw_grid(screen, SCREEN_WIDTH - MARGIN_WIDTH, SCREEN_HEIGHT - MARGIN_HEIGHT, scaled_tile_size, SCROLL)

    # draw margins and buttons
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - MARGIN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - MARGIN_HEIGHT, SCREEN_WIDTH, MARGIN_HEIGHT))

    # TODO: add buttons

    pygame.display.update()