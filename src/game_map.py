import pygame
import pickle
from settings import ROWS, COLS, WHITE
from Player import Player
from Enemy import Enemy
import os

def draw_map(screen, tile_map, tile_size, SCROLL):
    for row in tile_map:
        for tile in row:
            
            if tile != None:
                image = tile.image
                x = tile.position[0] * tile_size - SCROLL
                y = tile.position[1] * tile_size

                if isinstance(image, pygame.Surface):
                    image = pygame.transform.scale(image, (tile_size, tile_size))

                # if tile.type != "player" and tile.type != "carrot":

                screen.blit(image, (x, y))

                # elif tile.type == "player":
                #     player = Player(x, y, tile_size, tile_size)
                #     player.draw(screen)
                
                # elif tile.type == "carrot":
                #     player = Enemy(x, y, tile_size, tile_size)
                #     player.draw(screen)
                
def draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, tile_size, SCROLL):
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * tile_size), (SCREEN_WIDTH, row * tile_size))
    
    for col in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (col * tile_size - SCROLL, 0), (col * tile_size - SCROLL, SCREEN_HEIGHT))

def save_map(filename, tile_map, level_type="community"):
        file_path = os.path.join("levels", level_type, f"{filename}.pkl")

        with open(file_path, "wb") as f:
            pickle.dump(tile_map, f)

def load_map(filename, level_type="story"):
    file_path = os.path.join("levels", level_type, f"{filename}.pkl")
    default_path = os.path.join("levels", "default", f"deafult_map.pkl")

    try:
        with open(file_path, "rb") as f:
            tile_map = pickle.load(f)
    except FileNotFoundError:
        with open(default_path, "rb") as f:
            tile_map = pickle.load(f)

    return tile_map

def check_tile(tile_map, tile_type):
    for row in tile_map:
        for tile in row:
            if tile != None:
                if tile.type == tile_type:
                    return True

    return False

def get_tile_position(tile_map, tile_type, tile_size, find_all=False):
    results = []
    
    for row in tile_map:
            for tile in row:
                if tile and tile.type == tile_type:
                    
                    # Returns (x, y, tile_size_x, tile_size_y) pixel coordinates
                    positions = (tile.position[0] * tile_size, tile.position[1] * tile_size, tile.position[0], tile.position[1])

                    if not find_all:
                        return positions
                    
                    results.append(positions)

    return results if find_all else None