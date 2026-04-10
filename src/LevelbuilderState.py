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
        self.btn_font = pygame.font.SysFont(None, 25)
        self.scroll = SCROLL
        self.scroll_speed = SCROLL_SPEED
        self.message_text = ""
        self.message_timer = 0
        self.message_color = BLACK

        self.tile_map = game_map.load_map(self.LEVEL, self.level_type)

        self.setup_ui()

    def setup_ui(self):
        setting_state = self.state_machine.states['settings']
        self.screen_width = setting_state.screen_width
        self.screen_height = setting_state.screen_height
        self.tile_size = (self.screen_height - self.margin_height) // ROWS
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        
        scale_x = self.screen_width / self.BASE_WIDTH
        scale_y = self.screen_height / self.BASE_HEIGHT
        scale = min(scale_x, scale_y)
        self.btn_width = int(100 * scale)
        self.btn_height = int(30 * scale)

        self.save_button = Button(
            self.screen_width // 2, self.screen_height - (self.margin_height // 2),
            self.btn_width, self.btn_height, "Save", self.btn_font, BLACK, BLACK, WHITE, WHITE, False
        )

        self.back_button = Button(
            (self.screen_width // 2) + 200, self.screen_height - (self.margin_height // 2),
            self.btn_width, self.btn_height, "Exit", self.btn_font, BLACK, BLACK, WHITE, WHITE, False
        )
        
        self.level_type_button = Button(
            (self.screen_width // 2) - 200, self.screen_height - (self.margin_height // 2),
            self.btn_width, self.btn_height, self.level_type, self.btn_font, BLACK, BLACK, WHITE, WHITE, False
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
        self.player_placed = game_map.check_tile(self.tile_map, "player")
        self.goal_placed = game_map.check_tile(self.tile_map, "goal")

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
                    self.tile_map = game_map.load_map(self.LEVEL, self.level_type)

                if event.key == pygame.K_LEFT and self.LEVEL > 1:
                    self.LEVEL -= 1
                    self.tile_map = game_map.load_map(self.LEVEL, self.level_type)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
        
            if self.save_button.is_clicked(event):
                if self.player_placed == False or self.goal_placed == False:
                    self.message_text = "Missing Player and/or Goal"
                    self.message_color = (200, 0, 0)
                else:
                    game_map.save_map(self.LEVEL, self.tile_map, self.level_type)
                    self.message_text = f"Level {self.LEVEL} Saved"
                    self.message_color = (0, 150, 0)

                self.message_timer = pygame.time.get_ticks() + 2000

            if self.level_type_button.is_clicked(event):
                if self.level_type == "community":
                    self.level_type = "story"
                    self.level_type_button.text = "Story"
                else:
                    self.level_type = "community"
                    self.level_type_button.text = "Community"

                self.level_type_button = Button(
                    (self.screen_width // 2) - 200, self.screen_height - (self.margin_height // 2),
                    self.btn_width, self.btn_height, self.level_type, self.btn_font, BLACK, BLACK, WHITE, WHITE, False
                )
            
                self.tile_map = game_map.load_map(self.LEVEL, self.level_type)
                    

            if self.back_button.is_clicked(event):
                self.state_machine.transition('menu')
   
        for button_count, button in enumerate(self.button_list):
            if button.action():
                self.current_button = button_count
                self.current_tile = button.type
        
        pos = pygame.mouse.get_pos()
        x, y = (pos[0] + self.scroll) // self.tile_size, (pos[1]) // self.tile_size

        #check to make sure within the map bounds
        if pos[0] < self.screen_width - self.margin_width and pos[1] < self.screen_height - self.margin_height:
            try:
                tile = getattr(self.tile_map[y][x], 'type', None)

                # left click place
                if pygame.mouse.get_pressed()[0] == 1:                
                        if self.player_placed == True and self.current_tile == "player":
                            pass

                        elif self.goal_placed == True and self.current_tile == "goal":
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
        self.level_type_button.draw(surface)
        text_surface = self.btn_font.render(f"Level: {self.LEVEL}", True, BLACK)
        surface.blit(text_surface, (50, (self.screen_height - self.margin_height + 50)))

        if pygame.time.get_ticks() < self.message_timer:
            msg_surf = self.btn_font.render(self.message_text, True, self.message_color)
            # Position it near the save button or top of screen
            msg_rect = msg_surf.get_rect(center=(self.screen_width // 2, self.screen_height - self.margin_height - 30))
            surface.blit(msg_surf, msg_rect)
    
    def enter(self):
        self.setup_ui()