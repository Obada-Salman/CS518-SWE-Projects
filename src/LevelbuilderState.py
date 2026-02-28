import pygame
import tiles
from settings import *
import game_map
from button import Button

class LevelBuilderState:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.name = "level_builder"

        # Variables
        self.player_placed = False
        self.goal_placed = False
        self.LEVEL = 1
        self.level_type = "community"
        self.margin_height = 100
        self.margin_width = 200
        self.btn_font = pygame.font.SysFont(None, 50)
        self.scroll = SCROLL
        self.scroll_speed = SCROLL_SPEED
        
        self.tile_map = game_map.load_map("deafult_map")

        self.setup_ui()

    def setup_ui(self):
        setting_state = self.state_machine.states['settings']
        self.screen_width = setting_state.screen_width
        self.screen_height = setting_state.screen_height
        self.tile_size = (self.screen_height - self.margin_height) // ROWS

        self.save_button = Button(
            self.screen_width // 2, self.screen_height - (self.margin_height // 2),
            100, 50, "Save", self.btn_font, BLACK, BLACK, WHITE, WHITE, False
        )

        self.back_button = Button(
            (self.screen_width // 2) + 250, self.screen_height - (self.margin_height // 2),
            100, 50, "Exit", self.btn_font, BLACK, BLACK, WHITE, WHITE, False
        )

        self.current_tile_type = ""
        self.button_list = []
        button_col = 0
        button_row = 0
        
        for tile in tiles.tile_lookup:
            self.button_list.append(
                tiles.TileButton(
                    ((self.screen_width - self.margin_width + (50 * button_col) + 50, 75 * button_row + 50)),
                    (self.tile_size, self.tile_size),
                    tile
                )
            )
        
            button_col += 1
            if button_col == 2:
                button_col = 0
                button_row += 1
        
        self.current_button = 0
        self.current_tile = self.button_list[self.current_button].type

    def update(self, events):
        keys = pygame.key.get_pressed()

        # scroll
        if keys[pygame.K_d] and self.scroll < (COLS * self.tile_size) - self.screen_width:
            self.scroll += 5 * self.scroll_speed
        if keys[pygame.K_a] and self.scroll > 0:
            self.scroll -= 5 * self.scroll_speed
        
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.setup_ui()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.LEVEL < 99:
                    self.LEVEL += 1

                if event.key == pygame.K_LEFT and self.LEVEL > 1:
                    self.LEVEL -= 1

                self.tile_map = game_map.load_map(self.LEVEL, self.level_type)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
        
            if self.save_button.is_clicked(event):
                game_map.save_map(self.LEVEL, self.tile_map, "community")

            if self.back_button.is_clicked(event):
                self.state_machine.transition('menu')
   
        for button_count, button in enumerate(self.button_list):
            if button.action():
                self.current_button = button_count
                self.current_tile = button.type
        
        pos = pygame.mouse.get_pos()
        x, y = (pos[0] + self.scroll) // self.tile_size, (pos[1] + self.scroll) // self.tile_size

        #check to make sure within the map bounds
        if pos[0] < self.screen_width - self.margin_width and pos[1] < self.screen_height - self.margin_height:
            try:
                tile = getattr(self.tile_map[y][x], 'type', None)

                # left click place
                if pygame.mouse.get_pressed()[0] == 1:                
                        if self.player_placed == True and self.current_tile == "player":
                            pass
                        
                        elif tile != self.current_tile:
                            if self.current_tile == "player":
                                self.player_placed = True
                        
                            self.tile_map[y][x] = tiles.Tile((x, y), (self.tile_size, self.tile_size), self.current_tile)

                # right click remove
                elif pygame.mouse.get_pressed()[2] == 1 and tile != None:
                    self.tile_map[y][x] = None

            except IndexError:
                pass

    def draw(self, surface):
        surface.fill(BLACK)

        game_map.draw_map(surface, self.tile_map, self.tile_size, self.scroll)
        game_map.draw_grid(surface, self.screen_width - self.margin_width, self.screen_height - self.margin_height, self.tile_size, self.scroll)

        # draw margins
        pygame.draw.rect(surface, WHITE, (self.screen_width - self.margin_width, 0, self.screen_width, self.screen_height))
        pygame.draw.rect(surface, WHITE, (0, self.screen_height - self.margin_height, self.screen_width, self.margin_height))
     
        # draw buttons
        for button in self.button_list:
            surface.blit(button.image, button.rect)
        
        # highlight tile button
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, self.button_list[self.current_button].rect, 3)

        # save, and exit button, and text
        self.save_button.draw(surface)
        self.back_button.draw(surface)
        text_surface = self.btn_font.render(f"Level: {self.LEVEL}", True, BLACK)
        surface.blit(text_surface, (50, (self.screen_height - self.margin_height + 50)))
    
    def enter(self):
        self.setup_ui()