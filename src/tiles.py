import pygame

tile_lookup = {
    # 'grass': {"image": (0, 255, 0), "collision": True},
    'floor': {"image": "assets/images/Levels/cave_floor.png", "collision": True},
    'water': {"image": "assets/images/Misc/water_sprite.png", "collision": True},
    'sunlight': {"image": "assets/images/Misc/sun_sprite.png", "collision": True},
    'nutrient': {"image": "assets/images/Misc/nutrient_sprite.png", "collision": True},
    'carrot': {"image": "assets/images/Characters/carrot_static.png", "collision": False},
    'potato': {"image": "assets/images/Characters/potato_static.png", "collision": False},
    # 'goal': {"image": (128, 128, 128), "collision": True},
    'goal': {"image": "assets/images/Misc/door.png", "collision": False},
    'player': {"image": "assets/images/Characters/onion_static.png", "collision": False}
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
            self.image = pygame.transform.scale(self.image, (int(self.size[0] * 1), int(self.size[1] * 1)))
        elif isinstance(self.image, tuple):
            self.image = pygame.Surface(self.size)
            self.image.fill(self.tile_info["image"])

        self.rect = self.image.get_rect(topleft=self.position)
    
    def __getstate__(self):
        state = self.__dict__.copy()

        state['image'] = self.tile_info["image"]
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)

        if isinstance(self.image, str):
            self.image = pygame.image.load(self.tile_info["image"])
            self.image = pygame.transform.scale(self.image, (int(self.size[0] * 1), int(self.size[1] * 1)))
        elif isinstance(self.image, tuple):
            self.image = pygame.Surface(self.size)
            self.image.fill(self.tile_info["image"])
    
    def get_collision(self):
        return self.collision

    def get_type(self):
        return self.type

class TileButton(Tile):
    def __init__(self, postion, size, type):
        super().__init__(postion, size, type)

        self.clicked = False

    def action(self):
        action = False
        
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action