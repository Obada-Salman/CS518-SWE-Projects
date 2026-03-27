import pygame
from settings import *
from Player import Player
from Enemy import Enemy
from score_tracker import ScoreTracker
import game_map

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
            if self.player.rect.colliderect(enemy.rect):
                if self.player.can_damage():
                    enemy.take_damage(1)
                    self.snd_damage.play()
                self.player.take_damage(1)

            # Tear Collision
            for tear in self.player.tears[:]:
                if tear['rect'].colliderect(enemy.rect):
                    enemy.take_damage(1)
                    self.snd_tear_hit.play()
                    self.player.tears.remove(tear)

            if not enemy.is_alive():
                self.enemy_list.remove(enemy)

        if not self.player.is_alive():
            self.__init__(self.state_machine)
            self.state_machine.transition('menu')

        # self.door_locked = self.enemy.is_alive()
        self.door_locked = len(self.enemy_list) > 0

        if not self.door_locked:
            if self.check_collision(self.player.rect, self.door_rect):
                if self.current_level == self.state_machine.max_unlocked_level and self.current_level < 5:
                    self.state_machine.max_unlocked_level += 1
                if self.current_level < 5:
                    self.leave()
                    self.current_level += 1
                    self.enter() 
                else:
                    self.leave()
                    self.state_machine.transition('level_select')

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
        
    def enter(self):
        self.setup_ui()
        self.map = game_map.load_map(self.current_level, "story")
        player_position = game_map.get_tile_position(self.map, "player", self.tile_size, False)        
        enemy_positions = game_map.get_tile_position(self.map, "carrot", self.tile_size, True)
        door_position = game_map.get_tile_position(self.map, "goal", self.tile_size, False)
        
        if player_position is None or carrot_position is None:
            print(f"Error: Map for level {self.current_level} isnt integrated properly. Missing player or carrot position. Returning to level select.")
            self.state_machine.transition('level_select')
            return
        
        self.player = Player(player_position[0], player_position[1], 34 * 3, 34 * 3)
        self.map[player_position[3]][player_position[2]] = None
        
        self.enemy_list = []
        for enemy_position in enemy_positions:
            self.enemy_list.append(Enemy(enemy_position[0], enemy_position[1], 75, 110))
        
            self.map[enemy_position[3]][enemy_position[2]] = None
        
        self.door = pygame.Rect(door_position[0], door_position[1], self.tile_size, self.tile_size)
        self.map[door_position[3]][door_position[2]] = None
        self.door_image = pygame.transform.smoothscale(self.door_image, (self.tile_size, self.tile_size))
        self.lock_image = pygame.transform.smoothscale(self.lock_image, (self.tile_size, self.tile_size))

        self._play_level_music()

    def _play_level_music(self):
        track = self.level_music.get(self.current_level)
        if track and hasattr(self.state_machine, 'sound_manager'):
            self.state_machine.sound_manager.play_music_file(track)