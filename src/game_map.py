import pygame
import pickle
from settings import ROWS, COLS, WHITE, TILE_SIZE
from Player import Player


def draw_map(screen, tile_map, TILE_SIZE, SCROLL):
    for row in tile_map:
        for tile in row:
            
            if tile != None:
                image = tile.image
                x = tile.position[0] * TILE_SIZE - SCROLL
                y = tile.position[1] * TILE_SIZE

                if tile.type != "player":
                    screen.blit(image, (x, y))

                elif tile.type == "player":
                    player = Player(x, y, TILE_SIZE, TILE_SIZE)
                    player.draw(screen)


def draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, scaled_TILE_SIZE, SCROLL):
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * scaled_TILE_SIZE), (SCREEN_WIDTH, row * scaled_TILE_SIZE))
    
    for col in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (col * scaled_TILE_SIZE - SCROLL, 0), (col * scaled_TILE_SIZE - SCROLL, SCREEN_HEIGHT))

def save_map(filename, tile_map, level_type="community"):
        with open(f"levels/{level_type}/{filename}.pkl", "wb") as f:
            pickle.dump(tile_map, f)

def load_map(filename, level_type="story"):
    try:
        with open(f"levels/{level_type}/{filename}.pkl", "rb") as f:
            tile_map = pickle.load(f)
    except FileNotFoundError:
        with open(f"levels/default/deafult_map.pkl", "rb") as f:
            tile_map = pickle.load(f)

    
    return tile_map