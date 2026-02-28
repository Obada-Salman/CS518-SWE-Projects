import pygame
import pickle
from settings import ROWS, COLS, WHITE
from Player import Player

def draw_map(screen, tile_map, tile_size, SCROLL):
    for row in tile_map:
        for tile in row:
            
            if tile != None:
                image = tile.image
                x = tile.position[0] * tile_size - SCROLL
                y = tile.position[1] * tile_size

                if isinstance(image, pygame.Surface):
                    image = pygame.transform.scale(image, (tile_size, tile_size))

                if tile.type != "player":

                    screen.blit(image, (x, y))

                elif tile.type == "player":
                    player = Player(x, y, tile_size, tile_size)
                    player.draw(screen)

def draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, tile_size, SCROLL):
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * tile_size), (SCREEN_WIDTH, row * tile_size))
    
    for col in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (col * tile_size - SCROLL, 0), (col * tile_size - SCROLL, SCREEN_HEIGHT))

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