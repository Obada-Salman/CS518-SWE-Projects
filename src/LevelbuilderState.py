import pygame
import tiles
from settings import MARGIN_HEIGHT, MARGIN_WIDTH, ROWS
import game_map
from button import Button

class LevelBuilderState:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.name = "level_builder"

        SCREEN_WIDTH = self.state_machine.screen_width
        SCREEN_HEIGHT = self.state_machine.screen_height
        print(SCREEN_WIDTH, SCREEN_HEIGHT)

        scaled_tile_size = TILE_SIZE = (SCREEN_HEIGHT - MARGIN_HEIGHT) // ROWS

        self.player_placed = False
        self.goal_placed = False
        self.current_tile_type = ""
        self.current_button = 0
        self.LEVEL = 1
        self.level_type = "community"

        self.button_list = []
        button_col = 0
        button_row = 0
        for tile in tiles.tile_lookup:
            self.button_list.append(
                tiles.TileButton(
                    ((SCREEN_WIDTH - MARGIN_WIDTH + (50 * button_col) + 50, 75 * button_row + 50)),
                    (scaled_tile_size, scaled_tile_size),
                    tile
                )
            )
            button_col += 1
            if button_col == 2:
                button_col = 0
                button_row += 1
        
        self.current_tile = self.button_list[self.current_button].type

        tile_map = game_map.load_map("deafult_map")