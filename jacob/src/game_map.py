import pygame
from settings import ROWS, COLS, TILE_SIZE, WHITE, BLACK, FONT, SCROLL
import json

def draw_grid(screen_length, screen_height, TILE_SIZE, screen, SCROLL):
    # horzontale lines
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * TILE_SIZE), (screen_length, row * TILE_SIZE))

    # vertical lines
    for col in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (col * TILE_SIZE - SCROLL, 0), (col * TILE_SIZE - SCROLL, screen_height))

def draw_map(tile_map, image_dict, screen, SCROLL):
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile is not None:
                screen.blit(image_dict[tile]["surface"], (x * TILE_SIZE - SCROLL, y * TILE_SIZE))

def draw_text(text, postions, screen):
    text_image = FONT.render(text, True, (BLACK))
    screen.blit(text_image, postions)

def save_map(filename, data):
    try:
        with open(f"levels/{filename}.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error: {e}")

def load_map(filename, tile_map):
    try:
        with open(f"levels/{filename}.json") as f:
            tile_map = json.load(f)
    except FileNotFoundError:
        with open(f"levels/level_default.json") as f:
            tile_map = json.load(f)
    except json.JSONDecoderError:
        print(f"Error: File {tile_map}.json could not load")
    except Exception as e:
        print(f"Error: {e}")

    return tile_map

def check_tile(tile_map, tile_type):
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == tile_type:
                return True

    return False