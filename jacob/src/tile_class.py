import pygame

tile_types = {
    "dirt": {"image": (165, 42, 42), "property": True},
    "grass": {"image": (0, 128, 0), "property": True},
    "water": {"image": (0, 0, 255), "property": True},
    "damage": {"image": (255, 0, 0), "property": False},
    "player": {"image": (128, 0, 128), "property": True},
    "goal": {"image": (128, 128, 128), "property": True}
}

# tile_nums = len(tile_types) REMOVE Unless i find out what this was being used for

class Tile(pygame.sprite.Sprite):
    # """Tile class takes in position -> (x, y) size -> (length, height) tile_type -> 'tile_type'"""
    def __init__(self, position, size, tile_type):
        super().__init__()
        self.tile_type = tile_type
        self.tile_info = tile_types.get(tile_type)
        if self.tile_info == None:
            raise ValueError(f"Invalid tile tyle: {tile_type}\n Try: {list(tile_types.keys())}")

        self.image = pygame.Surface(size)
        self.image.fill(self.tile_info["image"])
        
        self.rect = self.image.get_rect(topleft = position) # Generates tiles at position x, y from top lef



# If sub tile/tile inheretance is used instead
# class Tile(pygame.sprite.Sprite):
#     """Tile class takes in x positions, y position, image"""
#     def __init__(self, x, y, image):
#         super().__init__()
#         self.image = image
#         self.rect = self.image.get_rect(topleft = (x, y)) # Generates tiles at position x, y from top left

#         # Add in properties
#         # proerpity ideas could be ...