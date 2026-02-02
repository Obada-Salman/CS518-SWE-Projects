import pygame
import tile_class
import button_class
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN_WIDTH, MARGIN_HEIGHT, TILE_SIZE, ROWS, COLS, LEVEL, SCROLL, SCROLL_SPEED, WHITE, BLACK, HIGHLIGHT_COLOR
import game_map

image_dict = {}
for tile, attributes in tile_class.tile_types.items():
    image = attributes["image"]
    # TODO For when image path is used
    # image = pygame.image.load(attributes["image"])
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(image)
    image_dict[tile] = {"image": image, "surface": surface}


# Setup buttons
save_button = button_class.Button((SCREEN_WIDTH // 2, SCREEN_HEIGHT - (MARGIN_HEIGHT // 2)), 100, 50, (250, 200, 100))

button_list = []
button_row = 0
button_col = 0
current_tile = 0
current_tile_type = ""
for tile, image in image_dict.items():

    tile_button = button_class.Tile_Button((SCREEN_WIDTH - MARGIN_WIDTH + (50 * button_col) + 50, 75 * button_row + 50), tile, image['image'])
    button_list.append(tile_button)
    button_col += 1
    if button_col == 2:
        button_row += 1
        button_col = 0

current_tile_type = button_list[0].tile_type

tile_map = []
tile_map = game_map.load_map(f"level_{LEVEL}", tile_map)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

running = True

while running:   
    screen.fill(BLACK)
    game_map.draw_map(tile_map, image_dict, screen, SCROLL)
    game_map.draw_grid(SCREEN_WIDTH - MARGIN_WIDTH, SCREEN_HEIGHT - MARGIN_HEIGHT, TILE_SIZE, screen, SCROLL)

    # draw margins and buttons
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - MARGIN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - MARGIN_HEIGHT, SCREEN_WIDTH, MARGIN_HEIGHT))

    # Draw buttons then chose button
    for button_count, i in enumerate(button_list):
        screen.blit(i.image, i.rect)
        if i.action():
            current_tile = button_count
            current_tile_type = i.tile_type
    
    # highlight selected tile
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, button_list[current_tile].rect, 3)

    game_map.draw_text(f"Level: {LEVEL}", (50, SCREEN_HEIGHT - MARGIN_HEIGHT + 50), screen)

    screen.blit(save_button.image, save_button.rect)
    game_map.draw_text(f"SAVE", (save_button.rect), screen)
    if save_button.action():
        game_map.save_map(f"level_{LEVEL}", tile_map)

    pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (0, 0, 0), (pos[0], pos[1]), 10)
    pygame.draw.circle(screen, (255, 255, 255), (pos[0], pos[1]), 7)
    
    # Add tiles
    x, y = (pos[0] + SCROLL) // TILE_SIZE, (pos[1]) // TILE_SIZE

    # check bounds to only place tiles in map
    if pos[0] < SCREEN_WIDTH - MARGIN_WIDTH and pos[1] < SCREEN_HEIGHT - MARGIN_HEIGHT:

        # Left click add tile
        if pygame.mouse.get_pressed()[0] == 1:
            try:
                if tile_map[y][x] != current_tile_type:
                    tile_map[y][x] = current_tile_type
            except IndexError:
                pass
    
        # Right click remove tile
        elif pygame.mouse.get_pressed()[2] == 1:
            tile_map[y][x] = None

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
                tile_map = game_map.load_map(f"level_{LEVEL}", tile_map)

            if event.key == pygame.K_LEFT and LEVEL > 1:
                LEVEL -= 1
                tile_map = game_map.load_map(f"level_{LEVEL}", tile_map)

    pygame.display.update()