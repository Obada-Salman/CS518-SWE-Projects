import pygame
from settings import *
from button import Button
from Player import Player
from Enemy import Enemy
from score_tracker import ScoreTracker
import game_map

class StoryState:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.current_level = 1
        self.score_tracker = getattr(self.state_machine, 'score_tracker', ScoreTracker())
        self.level_music = {
            1: 'story_level_1.ogg',
            2: 'story_level_2.ogg',
            3: 'story_level_3.ogg',
            4: 'story_level_4.ogg',
            5: 'story_level_5.ogg',
        }

        self.background = pygame.image.load('assets/images/Levels/Level1_800x600.png')
        self.door = pygame.image.load("assets/images/Misc/door.png")
        self.lock = pygame.image.load("assets/images/Misc/lock_52x68.png")
        self.door_rect = pygame.Rect(720, 417, 68, 96)
        self.door_locked = True

        self.snd_tear_hit = pygame.mixer.Sound('assets/sounds/tear_hit.ogg')
        self.snd_damage = pygame.mixer.Sound('assets/sounds/damage.ogg')
        
    def setup_ui(self):    
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = BASE_WIDTH, BASE_HEIGHT
        
        self.tile_size = self.screen_height // ROWS
        self.scaled_bg = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

        if self.check_collision(self.player.rect, self.enemy.rect):
            if self.player.can_damage():
                self.enemy.take_damage(1)
                self.snd_damage.play()
            self.player.take_damage(1)

        for tear in self.player.tears:
            if self.check_collision(tear['rect'], self.enemy.rect):
                self.enemy.take_damage(1)
                self.snd_tear_hit.play()
                self.player.tears.remove(tear)

        if not self.player.is_alive():
            self.__init__(self.state_machine)
            self.state_machine.transition('menu')

        if self.enemy.is_alive():
            self.door_locked = True
        else:
            self.door_locked = False

        if not self.door_locked:
            if self.check_collision(self.player.rect, self.door_rect):
                self.__init__(self.state_machine)
                self.state_machine.transition('menu')

        self.player.update()
        self.enemy.update()
        self.score_tracker.tick()

        self.check_map_collision(self.player)
        self.check_map_collision(self.enemy)

    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.scaled_bg, (0, 0))
        text = pygame.font.Font(None, 74).render(f"Level {self.current_level}", True, WHITE)
        surface.blit(text, (self.screen_width//2 - text.get_width()//2, 30))
        
        game_map.draw_map(surface, self.map, self.tile_size, 0)

        score_value = self.score_tracker.snapshot().level_score
        score_text = pygame.font.Font(None, 40).render(f"Score: {score_value}", True, BLACK)
        surface.blit(score_text, (650, 20))

        surface.blit(self.door, (720, 417))
        if self.door_locked:
            surface.blit(self.lock, (727, 437))

        self.player.draw(surface)
        self.enemy.draw(surface)
        
    def enter(self):
        self.setup_ui()
        self.score_tracker.start_level(f"story_{self.current_level}")
        self._play_level_music()

        self.map = game_map.load_map(self.current_level, "story")

        player_position = game_map.get_tile_position(self.map, "player", self.tile_size)
        carrot_position = game_map.get_tile_position(self.map, "carrot", self.tile_size)
        
        self.player = Player(player_position[0], player_position[1], 34 * 3, 34 * 3)
        self.map[player_position[3]][player_position[2]] = None # Remove from map to prevent collisons werid collisions

        self.enemy = Enemy(carrot_position[0], carrot_position[1], 75, 110)
        self.map[carrot_position[3]][carrot_position[2]] = None # Remove from map to prevent collisons werid collisions


    def set_level(self, level_number):
        self.current_level = level_number
        self.score_tracker.start_level(f"story_{self.current_level}")
        self._play_level_music()

    def leave(self):
        self.score_tracker.submit_current_level()

    def _play_level_music(self):
        track = self.level_music.get(self.current_level)
        if not track:
            return

        if hasattr(self.state_machine, 'sound_manager'):
            self.state_machine.sound_manager.play_music_file(track)

    def check_collision(self, rect1, rect2):
        return rect1.colliderect(rect2)

    # check_map_collision and handle_collision proably should be handled by the player and enemy classes, but this is what I got working for now
    def check_map_collision(self, entity):
        # Determine the grid coordinates
        grid_x = entity.rect.centerx // self.tile_size
        grid_y = entity.rect.centery // self.tile_size
        
        # Check a 3x3 area
        for row in range(grid_y - 1, grid_y + 2):
            for col in range(grid_x - 1, grid_x + 2):
                
                # 1. Stay within the map boundaries to avoid "Index Out of Range" errors
                if 0 <= row < len(self.map) and 0 <= col < len(self.map[0]):
                    tile = self.map[row][col]

                    if tile == None:
                        continue
                    
                    elif tile.collision:
                        object_rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                        
                        if entity.rect.colliderect(object_rect):
                            self.handle_collision(entity, object_rect)
    
    # check_map_collision and handle_collision proably should be handled by the player and enemy classes, but this is what I got working for now
    def handle_collision(self, entity, object_rect):
        # Calculate overlap on both axes
        overlap_x = min(entity.rect.right, object_rect.right) - max(entity.rect.left, object_rect.left)
        overlap_y = min(entity.rect.bottom, object_rect.bottom) - max(entity.rect.top, object_rect.top)

        # Snap the entity to the side of the wall it hit
        if overlap_x < overlap_y:
            if entity.rect.centerx < object_rect.centerx:
                entity.rect.right = object_rect.left
            else:
                entity.rect.left = object_rect.right
            if hasattr(entity, "on_wall_hit"):
                entity.on_wall_hit()
            else:
                entity.vx = 0
        else:
            if entity.rect.centery < object_rect.centery:
                entity.rect.bottom = object_rect.top
                entity.vy = 0
                entity.on_ground = True
            else:
                entity.rect.top = object_rect.bottom
                entity.vy = 0
        
        entity.x = entity.rect.x
        entity.y = entity.rect.y