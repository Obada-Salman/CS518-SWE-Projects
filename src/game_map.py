import pygame
import pickle
from settings import ROWS, COLS, WHITE
from Player import Player
from NPC import NPC
import os
import resource_path

def draw_map(screen, tile_map, tile_size, SCROLL):
    for row in tile_map:
        for tile in row:
            
            if tile != None:
                image = tile.image
                x = tile.position[0] * tile_size - SCROLL
                y = tile.position[1] * tile_size

                if isinstance(image, pygame.Surface):
                    image = pygame.transform.scale(image, (tile_size, tile_size))

                screen.blit(image, (x, y))
                
def draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, tile_size, SCROLL):
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * tile_size), (SCREEN_WIDTH, row * tile_size))
    
    for col in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (col * tile_size - SCROLL, 0), (col * tile_size - SCROLL, SCREEN_HEIGHT))

def save_map(filename, tile_map, level_type="community"):
    # file_path = os.path.join("levels", level_type, f"{filename}.pkl")

    if level_type == "community":
        file_path = resource_path.get_community_level_path()
    elif level_type == "story":
        file_path = resource_path.get_resource_path(f"levels/{level_type}/")
        
    file_path = os.path.join(file_path, f"{filename}.pkl")

    with open(file_path, "wb") as f:
        pickle.dump(tile_map, f)

def load_map(filename, level_type="story"):
    # file_path = os.path.join("levels", level_type, f"{filename}.pkl")
    default_map = [[None]*20 for _ in range(100)] # os.path.join("levels", "default", f"deafult_map.pkl") #TODO change to empty 2x2 matrix of 100x20

    if level_type == "community":
            file_path = resource_path.get_community_level_path()
    elif level_type == "story":
            file_path = resource_path.get_resource_path(f"levels/{level_type}/")
        
    file_path = os.path.join(file_path, f"{filename}.pkl")
    print(file_path)

    try:
        with open(file_path, "rb") as f:
            tile_map = pickle.load(f)
    except TypeError as e:
        print(f"TypeError{e}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        tile_map = default_map

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