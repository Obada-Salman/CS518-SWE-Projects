import pygame

class Tile_Button():
    def __init__(self, position, tile_type, image, scale = 1):
        length = 50 # temp
        height = 50 # temp
        self.tile_type = tile_type
        self.position = position
        
        if isinstance(image, tuple):
            self.image = pygame.Surface((length, height))
            self.image.fill(image)
        elif isinstance(image, str):
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (int(length * scale), int(height * scale)))

        self.rect = self.image.get_rect(topleft = self.position) # Generates tiles at postion x, y from top lef
        
        self.clicked = False

    def action(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = False
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action

class Button():
    def __init__(self, position, length, height, image, scale = 1):
        self.position = position
        
        # self.image = pygame.transform.scale(image, (int(length * scale), int(height * scale)))
        # self.image = pygame.Surface((length, height))
        # self.image.fill(image)
        
        if isinstance(image, tuple):
            self.image = pygame.Surface((length, height))
            self.image.fill(image)
        elif isinstance(image, str):
            self.image = pygame.image.load(image)
        
        self.rect = self.image.get_rect(topleft = self.position) # Generates tiles at postion x, y from top lef
        
        self.clicked = False

    def action(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = False
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action