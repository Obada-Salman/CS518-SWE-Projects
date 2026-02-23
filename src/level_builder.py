import pygame
import game_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN_WIDTH, MARGIN_HEIGHT, SCROLL, SCROLL_SPEED, BLACK, WHITE, ROWS, COLS, HIGHLIGHT_COLOR
import tiles
scaled_tile_size = TILE_SIZE = (SCREEN_HEIGHT - MARGIN_HEIGHT) // ROWS

player_placed = False
goal_placed = False
current_tile_type = ""
current_button = 0
LEVEL = 0
level_type = "Custom"

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

current_tile = button_list[current_button].type

tile_map = game_map.load_map("deafult_map12312312321")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
running = True

while running:
    screen.fill(BLACK)
    game_map.draw_map(screen, tile_map, scaled_tile_size, SCROLL)
    game_map.draw_grid(screen, SCREEN_WIDTH - MARGIN_WIDTH, SCREEN_HEIGHT - MARGIN_HEIGHT, scaled_tile_size, SCROLL)

    # draw margins and buttons
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - MARGIN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - MARGIN_HEIGHT, SCREEN_WIDTH, MARGIN_HEIGHT))

    for button_count, button in enumerate(button_list):
        screen.blit(button.image, button.rect)
        if button.action():
            current_button = button_count
            current_tile = button.type
        
    # highlight tile button
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, button_list[current_button].rect, 3)

    pos= pygame.mouse.get_pos()
    x, y = (pos[0] + SCROLL) // TILE_SIZE, (pos[1] + SCROLL) // TILE_SIZE

    #check to make sure within the map bounds
    if pos[0] < SCREEN_WIDTH - MARGIN_WIDTH and pos[1] < SCREEN_HEIGHT - MARGIN_HEIGHT:
        try:
            tile = getattr(tile_map[y][x], 'type', None)

            # left click place
            if pygame.mouse.get_pressed()[0] == 1:                
                    if player_placed == True and current_tile == "player":
                        pass
                    
                    elif tile != current_tile:
                        if current_tile == "player":
                            player_placed = True
                    
                        tile_map[y][x] = tiles.Tile((x, y), (TILE_SIZE, TILE_SIZE), current_tile)

            # right click remove
            elif pygame.mouse.get_pressed()[2] == 1 and tile != None:
                tile_map[y][x] = None

        except IndexError:
            pass

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Scroll
        if keys[pygame.K_d] and SCROLL < (COLS * TILE_SIZE) - SCREEN_WIDTH:
            SCROLL += 5 * SCROLL_SPEED
        if keys[pygame.K_a] and SCROLL > 0:
            SCROLL -= 5 * SCROLL_SPEED
        
        # Cycle through levels
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and LEVEL < 99:
                LEVEL += 1

            if event.key == pygame.K_LEFT and LEVEL > 1:
                LEVEL -= 1

            tile_map = game_map.load_map(f"levels/{level_type}/{LEVEL}", level_type)

    pygame.display.update()