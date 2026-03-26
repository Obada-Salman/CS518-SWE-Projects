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
        self.door = pygame.image.load("assets/images/Misc/door.png")
        self.lock = pygame.image.load("assets/images/Misc/lock_52x68.png")
        self.door_rect = pygame.Rect(720, 417, 68, 96)
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
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

        # Update Movement and Map Collisions
        self.player.update(self.map, self.tile_size)
        self.enemy.update(self.map, self.tile_size)

        # Combat Collision
        if self.player.rect.colliderect(self.enemy.rect):
            if self.player.can_damage():
                self.enemy.take_damage(1)
                self.snd_damage.play()
            self.player.take_damage(1)

        # Tear Collision
        for tear in self.player.tears[:]:
            if tear['rect'].colliderect(self.enemy.rect):
                self.enemy.take_damage(1)
                self.snd_tear_hit.play()
                self.player.tears.remove(tear)

        if not self.player.is_alive():
            self.__init__(self.state_machine)
            self.state_machine.transition('menu')

        self.door_locked = self.enemy.is_alive()
        if not self.door_locked and self.player.rect.colliderect(self.door_rect):
            self.__init__(self.state_machine)
            self.state_machine.transition('menu')

        self.score_tracker.tick()

    def draw(self, surface):
        surface.blit(self.scaled_bg, (0, 0))
        game_map.draw_map(surface, self.map, self.tile_size, 0)
        surface.blit(self.door, (720, 417))
        if self.door_locked: surface.blit(self.lock, (727, 437))
        self.player.draw(surface)
        self.enemy.draw(surface)
        
    def enter(self):
        self.setup_ui()
        self.map = game_map.load_map(self.current_level, "story")
        p_pos = game_map.get_tile_position(self.map, "player", self.tile_size)
        e_pos = game_map.get_tile_position(self.map, "carrot", self.tile_size)
        
        self.player = Player(p_pos[0], p_pos[1], 34 * 3, 34 * 3)
        self.enemy = Enemy(e_pos[0], e_pos[1], 75, 110)
        
        self.map[p_pos[3]][p_pos[2]] = None 
        self.map[e_pos[3]][e_pos[2]] = None 
        self._play_level_music()

    def _play_level_music(self):
        track = self.level_music.get(self.current_level)
        if track and hasattr(self.state_machine, 'sound_manager'):
            self.state_machine.sound_manager.play_music_file(track)