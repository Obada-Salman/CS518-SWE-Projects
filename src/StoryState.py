import pygame
from settings import *
from Player import Player
from Enemy import Enemy
from score_tracker import ScoreTracker
import game_map
from tiles import Tile
from state_manager import StateManager
import math

class StoryState:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.current_level = 1
        self.score_tracker = getattr(self.state_machine, 'score_tracker', ScoreTracker())
        self.level_music = {1: 'story_level_1.ogg', 2: 'story_level_2.ogg', 3: 'story_level_3.ogg'}

        self.background = pygame.image.load('assets/images/Levels/Level1_800x600.png')
        self.door_image = pygame.image.load("assets/images/Misc/door.png")
        self.lock_image = pygame.image.load("assets/images/Misc/lock_52x68.png")
        self.door_locked = True

        self.snd_tear_hit = pygame.mixer.Sound('assets/sounds/tear_hit.ogg')
        self.snd_damage = pygame.mixer.Sound('assets/sounds/damage.ogg')
        self.level_cleared = False
        
    def setup_ui(self):    
        surface = pygame.display.get_surface()
        self.screen_width, self.screen_height = (surface.get_size() if surface else (BASE_WIDTH, BASE_HEIGHT))
        self.tile_size = self.screen_height // ROWS
        self.scaled_bg = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('pause')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

        # Update Movement and Map Collisions
        self.player.update(self.map, self.tile_size)
        # self.enemy.update(self.map, self.tile_size)

        for enemy in self.enemy_list:
            enemy.update(self.map, self.tile_size)

            # Combat Collision
            # if self.player.rect.colliderect(self.enemy.rect):
            # if self.player.rect.colliderect(enemy.rect):
            if self.mask_collision(self.player, enemy):
                if self.player.can_damage():
                    enemy.take_damage(1)
                    self.snd_damage.play()
                self.player.take_damage(1)

            # Tear Collision
            for tear in self.player.tears[:]:
                # if tear['rect'].colliderect(enemy.rect):
                tear_offset_x = enemy.rect.x - tear['rect'].x
                tear_offset_y = enemy.rect.y - tear['rect'].y
                
                if tear['mask'].overlap(enemy.mask, (tear_offset_x, tear_offset_y)):
                    enemy.take_damage(1)
                    self.snd_tear_hit.play()
                    self.player.tears.remove(tear)
                
            if not enemy.is_alive():
                self.enemy_list.remove(enemy)

        for c in self.collectibles[:]:
            if self.player.rect.colliderect(c['rect']):
                if c['type'] == 'water':
                    self.state_machine.add_water(1)
                    print(f"Total water collected: {self.state_machine.get_water_collected()}")
                elif c['type'] == 'sunlight':
                    self.state_machine.add_sunlight(1)
                    print(f"Total sunlight collected: {self.state_machine.get_sunlight_collected()}")
                elif c['type'] == 'nutrient':
                    self.state_machine.add_nutrients(1)
                    print(f"Total nutrients collected: {self.state_machine.get_nutrients_collected()}")
                self.collectibles.remove(c)
                pygame.mixer.Sound('assets/sounds/collect.ogg').play()

        if not self.player.is_alive():
            self.__init__(self.state_machine)
            self.state_machine.transition('menu')

        # self.door_locked = self.enemy.is_alive()
        self.door_locked = len(self.enemy_list) > 0

        if not self.door_locked and self.player.rect.colliderect(self.door):
            if self.current_level == self.state_machine.max_unlocked_level and self.current_level < 5:
                self.state_machine.max_unlocked_level += 1
                self.level_cleared = True
                self.leave()
                self.current_level += 1
                self.level_cleared = False
                if self.state_machine.current_state == 'story' and hasattr(self.state_machine.current_state, 'set_level'):
                    self.state_machine.current_state.set_level(self.current_level)
                self.enter()

        self.score_tracker.tick()

    def draw(self, surface):
        surface.blit(self.scaled_bg, (0, 0))
        
        game_map.draw_map(surface, self.map, self.tile_size, 0)
        
        surface.blit(self.door_image, self.door.topleft)
        
        if self.door_locked:
            surface.blit(self.lock_image, self.door.topleft)
        
        self.player.draw(surface)
        
        # self.enemy.draw(surface)
        for enemy in self.enemy_list:
            enemy.draw(surface)

        for c in self.collectibles:
            sprite = self.collectible_images[c['type']]
            offset_y = math.sin(pygame.time.get_ticks() * 0.007) * 10
            center_x = c['rect'].centerx
            center_y = c['rect'].centery - 30 + offset_y
            sprite_rect = sprite.get_rect(center=(center_x, center_y))
            surface.blit(sprite, sprite_rect)
        
    def enter(self):
        self.setup_ui()
        self.map = game_map.load_map(self.current_level, "story")
        player_position = game_map.get_tile_position(self.map, "player", self.tile_size, False)        
        carrot_positions = game_map.get_tile_position(self.map, "carrot", self.tile_size, True)
        potato_positions = game_map.get_tile_position(self.map, "potato", self.tile_size, True)
        door_position = game_map.get_tile_position(self.map, "goal", self.tile_size, False)
        water_positions = game_map.get_tile_position(self.map, "water", self.tile_size, True)
        sunlight_positions = game_map.get_tile_position(self.map, "sunlight", self.tile_size, True)
        nutrient_positions = game_map.get_tile_position(self.map, "nutrient", self.tile_size, True)
        
        if player_position is None or door_position is None:
            print(f"ERROR: Level {self.current_level} is missing a player spawn or a goal")
            # Fallback: sends user back to level select instead of crashing
            self.state_machine.transition('level_select')
            return
        
        self.player = Player(player_position[0], player_position[1], 34 * 3, 34 * 3)
        self.map[player_position[3]][player_position[2]] = None
        
        self.enemy_list = []
        # Add carrots
        for enemy_position in carrot_positions:
            self.enemy_list.append(Enemy(enemy_position[0], enemy_position[1], 75, 110, type='enemy_carrot'))
            self.map[enemy_position[3]][enemy_position[2]] = None
        
        # Add potatoes
        for enemy_position in potato_positions:
            self.enemy_list.append(Enemy(enemy_position[0], enemy_position[1], 83, 94, type='enemy_potato'))
            self.map[enemy_position[3]][enemy_position[2]] = None
        
        self.collectible_sizes = {'water': (45, 53), 'sunlight': (40, 38), 'nutrient': (29, 46)}
        self.sprite_names = {'water': 'water_sprite.png', 'sunlight': 'sun_sprite.png', 'nutrient': 'nutrient_sprite.png'}
        self.collectible_images = {}
        for typ, size in self.collectible_sizes.items():
            img = pygame.image.load(f"assets/images/Misc/{self.sprite_names[typ]}")
            self.collectible_images[typ] = img # pygame.transform.smoothscale(img, size)

        self.collectibles = []
        for w in water_positions:
            size = self.collectible_sizes['water']
            rect = pygame.Rect(w[0], w[1], *size)
            self.collectibles.append({'type': 'water', 'rect': rect})
            self.map[w[3]][w[2]] = None
        for s in sunlight_positions:
            size = self.collectible_sizes['sunlight']
            rect = pygame.Rect(s[0], s[1], *size)
            self.collectibles.append({'type': 'sunlight', 'rect': rect})
            self.map[s[3]][s[2]] = None
        for n in nutrient_positions:
            size = self.collectible_sizes['nutrient']
            rect = pygame.Rect(n[0], n[1], *size)
            self.collectibles.append({'type': 'nutrient', 'rect': rect})
            self.map[n[3]][n[2]] = None

        self.door = pygame.Rect(door_position[0], door_position[1], self.tile_size, self.tile_size)
        self.map[door_position[3]][door_position[2]] = None
        self.door_image = pygame.transform.smoothscale(self.door_image, (self.tile_size, self.tile_size))
        self.lock_image = pygame.transform.smoothscale(self.lock_image, (self.tile_size, self.tile_size))

        self._play_level_music()

    def set_level(self, level_number):
        self.current_level = level_number
        
    def leave(self):
        if hasattr(self, 'score_tracker'):
            self.score_tracker.submit_current_level()
        if self.level_cleared:
            print(f"Finished Level {self.current_level}")
        else:
            print(f"Exited Level {self.current_level}")

    def _play_level_music(self):
        track = self.level_music.get(self.current_level)
        if track and hasattr(self.state_machine, 'sound_manager'):
            self.state_machine.sound_manager.play_music_file(track)
    
    def mask_collision(self, object1, object2):
        offset_x = object2.rect.x - object1.rect.x
        offset_y = object2.rect.y - object1.rect.y
        return object1.mask.overlap(object2.mask, (offset_x, offset_y))