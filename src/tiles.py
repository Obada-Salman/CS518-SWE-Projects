import pygame

tile_lookup = {
    'grass': {"image": (0, 255, 0), "collision": True},
    'water': {"image": "assets/images/water_sprite.png", "collision": True},
    'sunlight': {"image": "assets/images/sunlight_sprite.png", "collision": True},
    'resources': {"image": "assets/images/resources_sprite.png", "collision": True},
    'enemy': {"image": (255, 0, 0), "collision": False},
    'goal': {"image": (128, 128, 128), "collision": True},
    'player': {"image": (128, 0, 128), "collision": True}
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, postion, size, type):
        super().__init__()

        self.type = type
        self.tile_info = tile_lookup.get(type)

        if self.tile_info == None:
            raise ValueError(f"Invalid tile tyle: {tile_lookup}\n Try: {list(tile_lookup.keys())}")

        self.image = self.tile_info["image"]
        self.collision = self.tile_info["collision"]
        self.position = postion
        self.size = size

        if isinstance(self.image, str):
            self.image = pygame.image.load(self.tile_info["image"])
            self.image = pygame.transform.scale(self.image, (int(50 * 1), int(50 * 1)))
        elif isinstance(self.image, tuple):
            self.image = pygame.Surface(self.size)
            self.image.fill(self.tile_info["image"])
    
    def __getstate__(self):
        state = self.__dict__.copy()

        state['image'] = self.tile_info["image"]
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)

        if isinstance(self.image, str):
            self.image = pygame.image.load(self.tile_info["image"])
            self.image = pygame.transform.scale(self.image, (int(50 * 1), int(50 * 1)))
        elif isinstance(self.image, tuple):
            self.image = pygame.Surface(self.size)
            self.image.fill(self.tile_info["image"])
    
    def get_collision(self):
        return self.collision

    def get_type(self):
        return self.type