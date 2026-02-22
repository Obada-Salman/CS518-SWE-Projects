import pygame
import game_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN_WIDTH, MARGIN_HEIGHT, SCROLL, SCROLL_SPEED, BLACK, WHITE, ROWS, HIGHLIGHT_COLOR
import tiles
scaled_tile_size = TILE_SIZE = (SCREEN_HEIGHT - MARGIN_HEIGHT) // ROWS

player_placed = False
goal_placed = False
current_tile_type = ""
current_button = 0

button_list = []
button_col = 0
button_row = 0
for tile in tiles.tile_lookup:
    button_list.append(
        tiles.TileButton(
            ((SCREEN_WIDTH - MARGIN_WIDTH + (50 * button_col) + 50, 75 * button_row + 50)),
            (scaled_tile_size, scaled_tile_size),
            tile
        )
    )
    button_col += 1
    if button_col == 2:
        button_col = 0
        button_row += 1
    
tile_map = game_map.load_map("tiles2", "community")
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
    for button_count, button in enumerate(button_list):
        screen.blit(button.image, button.rect)
        if button.action():
            current_button = button_count
            current_tile_type = button.type
        
    # highlight tile button
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, button_list[current_button].rect, 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()