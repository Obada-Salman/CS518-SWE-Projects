import pygame
from settings import *
from Player import Player
from NPC import NPC
from score_tracker import ScoreTracker
import game_map
from tiles import Tile
from state_manager import StateManager
import math
import random
import resource_path
from dialogue_cutscene import SequencePlayer
from story_content import RECRUIT_DIALOGUE_BANK
import heapq

class CustomState:
    RESOURCE_POINTS = {
        'water': 20,
        'sunlight': 20,
        'nutrient': 25,
    }

    ENEMY_KILL_POINTS = {
        'carrot': 100,
        'potato': 120,
    }

    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.current_level = 1
        self.score_tracker = getattr(self.state_machine, 'score_tracker', ScoreTracker())
        self.true_width = BASE_WIDTH
        self.true_height = BASE_HEIGHT
        self.internal_surface = pygame.Surface((self.true_width, self.true_height))
        self.tile_size = self.true_height // ROWS

        self.background = pygame.image.load(resource_path.get_resource_path('assets/images/Levels/Caves.png'))
        self.scaled_bg = pygame.transform.scale(self.background, (self.true_width, self.true_height))
        self.door_image = pygame.image.load(resource_path.get_resource_path("assets/images/Misc/door.png"))
        self.lock_image = pygame.image.load(resource_path.get_resource_path("assets/images/Misc/lock_52x68.png"))
        self.door_locked = True

        self.snd_tear_hit = pygame.mixer.Sound(resource_path.get_resource_path('assets/sounds/tear_hit.ogg'))
        self.snd_damage = pygame.mixer.Sound(resource_path.get_resource_path('assets/sounds/damage.ogg'))
        self.snd_collect = pygame.mixer.Sound(resource_path.get_resource_path('assets/sounds/collect.ogg'))
        self.level_cleared = False
        self.scroll = 0
        self.sequence_player = SequencePlayer()
        
    def setup_ui(self):    
        surface = pygame.display.get_surface()
        self.screen_width, self.screen_height = (surface.get_size() if surface else (BASE_WIDTH, BASE_HEIGHT))
        scale_x = self.screen_width / self.true_width
        scale_y = self.screen_height / self.true_height
        self.scale = min(scale_x, scale_y)
        self.scaled_width = int(self.true_width * self.scale)
        self.scaled_height = int(self.true_height * self.scale)
        self.offset_x = (self.screen_width - self.scaled_width) // 2
        self.offset_y = (self.screen_height - self.scaled_height) // 2
        # self.tile_size = self.true_height // ROWS

    def update(self, events):
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.setup_ui()

        if self.sequence_player.active:
            self.sequence_player.process_events(events)
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('pause')
                self.score_tracker.tick()
                return

        # Update Movement and Map Collisions
        self.player.update(self.map, self.tile_size)

        # Scroll with player movement
        half_screen = self.true_width // 2
        self.scroll = self.player.rect.centerx - half_screen
        map_width_px = len(self.map[0]) * self.tile_size

        if self.scroll < 0:
            self.scroll = 0
        if self.scroll > map_width_px - self.true_width:
            self.scroll = map_width_px - self.true_width

        # self.enemy.update(self.map, self.tile_size)

        for enemy in self.enemy_list[:]:
            enemy.update(self.map, self.tile_size)

            # Combat Collision
            # if self.player.rect.colliderect(self.enemy.rect):
            # if self.player.rect.colliderect(enemy.rect):
            if self.mask_collision(self.player, enemy) and enemy.team == 'enemy':
                if self.player.can_damage():
                    enemy.take_damage(1)
                    self.snd_damage.play()
                self.player.take_damage(enemy.damage)

            # Tear Collision
            for tear in self.player.tears[:]:
                # if tear['rect'].colliderect(enemy.rect):
                tear_offset_x = enemy.rect.x - tear['rect'].x
                tear_offset_y = enemy.rect.y - tear['rect'].y
                
                if tear['mask'].overlap(enemy.mask, (tear_offset_x, tear_offset_y)) and enemy.team == 'enemy':
                    enemy.take_damage(1)
                    self.snd_tear_hit.play()
                    self.player.tears.remove(tear)
                
            if not enemy.is_alive():
                self.score_tracker.record_enemy_kill(points=self._enemy_points(enemy))
                self.enemy_list.remove(enemy)

            for ally in self.ally_list:
                if ally.recruited and ally.can_damage() and self.mask_collision(ally, enemy):
                    ally.combat_with(enemy)
                    self.snd_damage.play()
                    
        keys = pygame.key.get_pressed()
        for ally in self.ally_list:
            if not ally.recruited:
                dist = math.hypot(ally.x - self.player.x, ally.y - self.player.y)
                if dist < 100 and keys[pygame.K_e]:
                    self._start_recruitment_dialogue(ally)
                    return
            else:
                # Find closest enemy
                closest_enemy = None
                min_dist = float('inf')
                for enemy in self.enemy_list:
                    dist = math.hypot(ally.x - enemy.x, ally.y - enemy.y)
                    if dist < min_dist:
                        min_dist = dist
                        closest_enemy = enemy
                if closest_enemy and min_dist < 350:
                    # Go towards enemy (allow leading ahead)
                    if ally.x < closest_enemy.x:
                        ally.vx = ally.speed
                        ally.direction = 1
                    elif ally.x > closest_enemy.x:
                        ally.vx = -ally.speed
                        ally.direction = 0
                    else:
                        ally.vx = 0
                    # Jump to reach enemy if needed
                    if ally.on_ground and ally.y > closest_enemy.y + 20:
                        ally.vy = -16.0
                else:
                    # Follow player as scout - allow significant leading ahead (50px)
                    # This lets them scout ahead of player and engage enemies first
                    if ally.x < self.player.x - 50:
                        # Too far behind - catch up faster
                        ally.vx = ally.speed * 1.2  # Speed boost to catch up
                        ally.direction = 1
                    elif ally.x > self.player.x + 50:
                        # Too far ahead - slow down
                        ally.vx = -ally.speed * 0.5
                        ally.direction = 0
                    else:
                        # In formation - move at player speed
                        if ally.x < self.player.x - 10:
                            ally.vx = ally.speed
                            ally.direction = 1
                        elif ally.x > self.player.x + 10:
                            ally.vx = -ally.speed
                            ally.direction = 0
                        else:
                            ally.vx = 0

                if ally.on_ground and ally.y > self.player.y and abs(ally.x - self.player.x) > 30:
                    ally.vy = -16.0
            
            ally.update(self.map, self.tile_size)

        for pot in self.pot_list[:]:
            dist = math.hypot(self.player.x - pot.position[0], self.player.y - pot.position[1])
            sufficient_resources = (self.state_machine.get_water_collected() >= 5 and self.state_machine.get_sunlight_collected() >= 3
                                    and self.state_machine.get_nutrients_collected() >= 2)
            if keys[pygame.K_e] and dist < 100 and sufficient_resources:
                # consume resources
                self.state_machine.add_water(-5)
                self.state_machine.add_sunlight(-3)
                self.state_machine.add_nutrients(-2)
                print(f"Total water collected: {self.state_machine.get_water_collected()}")
                print(f"Total sunlight collected: {self.state_machine.get_sunlight_collected()}")
                print(f"Total nutrients collected: {self.state_machine.get_nutrients_collected()}")

                # plant onion ally
                self.ally_list.append(NPC(pot.position[0], pot.position[1], 34, 34, type='onion', speed=3, team='ally'))
                self.ally_list[-1].recruited = True
                self.pot_list.remove(pot)
                self.snd_collect.play()
                break

        # spikes damage player
        for spike in self.spike_list:
            offset_x = spike.rect.x - self.player.rect.x
            offset_y = spike.rect.y - self.player.rect.y
            spike_mask = pygame.mask.from_surface(spike.image)
            if self.player.mask.overlap(spike_mask, (offset_x, offset_y)) and self.player.can_damage():
                self.player.take_damage(1)
                self.snd_damage.play()
                break

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
                self.score_tracker.record_resource_collected(
                    amount=1,
                    points_per_unit=self.RESOURCE_POINTS.get(c['type'], 10),
                )
                self.collectibles.remove(c)
                self.snd_collect.play()

        if not self.player.is_alive():
            self.__init__(self.state_machine)
            self.state_machine.transition('menu')

        # self.door_locked = self.enemy.is_alive()
        self.door_locked = len(self.enemy_list) > 0

        if not self.door_locked and self.player.rect.colliderect(self.door):
            self.level_cleared = True
            self.score_tracker.finalize_level_completion()
            self.leave()
            
            
            self.level_cleared = False
            self.state_machine.transition('custom_select')

        self.score_tracker.tick()

    def draw(self, surface):
        self.internal_surface.blit(self.scaled_bg, (0, 0))
        
        game_map.draw_map(self.internal_surface, self.map, self.tile_size, self.scroll)
        
        self.internal_surface.blit(self.door_image, (self.door.x - self.scroll, self.door.y))
        
        if self.door_locked:
            self.internal_surface.blit(self.lock_image, (self.door.x - self.scroll, self.door.y))
        
        
        
        for enemy in self.enemy_list:
            enemy.draw(self.internal_surface, self.scroll)

        for ally in self.ally_list:
            ally.draw(self.internal_surface, self.scroll)

        for c in self.collectibles:
            sprite = self.collectible_images[c['type']]
            offset_y = math.sin(pygame.time.get_ticks() * 0.007) * 10
            center_x = c['rect'].centerx - self.scroll
            center_y = c['rect'].centery - 30 + offset_y
            sprite_rect = sprite.get_rect(center=(center_x, center_y))
            self.internal_surface.blit(sprite, sprite_rect)

        for pot in self.pot_list:
            self.internal_surface.blit(pot.image, (pot.position[0] - self.scroll, pot.position[1]))

        for spike in self.spike_list:
            self.internal_surface.blit(spike.image, (spike.position[0] - self.scroll, spike.position[1]))

        self.player.draw(self.internal_surface, self.scroll)
            
        # scales internal surface to fit the window while maintaining aspect ratio
        scaled_display = pygame.transform.scale(self.internal_surface, (self.scaled_width, self.scaled_height))
        # Letterbox
        surface.fill((0, 0, 0)) 
        # scaled game onto the center of the window
        surface.blit(scaled_display, (self.offset_x, self.offset_y))
        self.sequence_player.draw(surface)
        
    def enter(self):
        self.setup_ui()
        self.map = game_map.load_map(self.current_level, "community")
        player_position = game_map.get_tile_position(self.map, "player", self.tile_size, False)        
        door_position = game_map.get_tile_position(self.map, "goal", self.tile_size, False)
        water_positions = game_map.get_tile_position(self.map, "water", self.tile_size, True)
        sunlight_positions = game_map.get_tile_position(self.map, "sunlight", self.tile_size, True)
        nutrient_positions = game_map.get_tile_position(self.map, "nutrient", self.tile_size, True)
        spike_positions = game_map.get_tile_position(self.map, "spike", self.tile_size, True)
        flower_pot_pos = game_map.get_tile_position(self.map, "flower_pot", self.tile_size, True)

        if player_position is None or door_position is None:
            print(f"ERROR: Level {self.current_level} is missing a player spawn or a goal")
            # Fallback: sends user back to custom level select instead of crashing
            self.state_machine.transition('custom_select')
            return
        
        self.player = Player(player_position[0], player_position[1], 34 * 3, 34 * 3)
        self.map[player_position[3]][player_position[2]] = None
        
        self.enemy_list = []
        self.ally_list = []
        self.pot_list = []
        self.spike_list = []

        for character, params in NPC.NPC_CONFIG.items():
            width, height, npc_type, speed, team = params
            positions = game_map.get_tile_position(self.map, character, self.tile_size, True)

            for position in positions:
                npc = NPC(position[0], position[1], width, height, type=npc_type, speed=speed, team=team)

                if team == 'ally':
                    npc.recruited = False
                    self.ally_list.append(npc)
                elif team == 'enemy':
                    self.enemy_list.append(npc)

                self.map[position[3]][position[2]] = None
        
        if self.current_level == 15:
            self.enemy_list.append(FinalBoss(400, 100))

        for pot_pos in flower_pot_pos:
            self.pot_list.append(Tile((pot_pos[0], pot_pos[1]), (55, 59), 'flower_pot'))
            self.map[pot_pos[3]][pot_pos[2]] = None

        # Add spikes
        for spike_pos in spike_positions:
            self.spike_list.append(Tile((spike_pos[0], spike_pos[1]), (self.tile_size, self.tile_size), 'spike'))
            self.map[spike_pos[3]][spike_pos[2]] = None

        self.collectible_sizes = {'water': (45, 53), 'sunlight': (40, 38), 'nutrient': (29, 46)}
        self.sprite_names = {'water': 'water_sprite.png', 'sunlight': 'sun_sprite.png', 'nutrient': 'nutrient_sprite.png'}
        self.collectible_images = {}
        for typ, size in self.collectible_sizes.items():
            img = pygame.image.load(resource_path.get_resource_path(f"assets/images/Misc/{self.sprite_names[typ]}"))
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
        self.score_tracker.start_level(f"custom_level_{self.current_level}")

    def set_level(self, level_number):
        self.current_level = level_number
        
    def leave(self):
        if self.level_cleared and hasattr(self, 'score_tracker'):
            self.score_tracker.submit_current_level()
        if self.level_cleared:
            print(f"Finished Level {self.current_level}")
        else:
            print(f"Exited Level {self.current_level}")

    def _play_level_music(self):
        track = 'SneakyAction.ogg'
        if track and hasattr(self.state_machine, 'sound_manager'):
            self.state_machine.sound_manager.play_music_file(track)
    
    def mask_collision(self, object1, object2):
        offset_x = object2.rect.x - object1.rect.x
        offset_y = object2.rect.y - object1.rect.y
        return object1.mask.overlap(object2.mask, (offset_x, offset_y))

    def _enemy_points(self, enemy):
        return self.ENEMY_KILL_POINTS.get(getattr(enemy, 'type', None), 100)

    def _tile_from_position(self, x, y):
        return int(x // self.tile_size), int(y // self.tile_size)

    def _is_walkable_tile(self, tile_x, tile_y):
        if tile_y < 0 or tile_y >= len(self.map):
            return False
        if tile_x < 0 or tile_x >= len(self.map[0]):
            return False

        tile = self.map[tile_y][tile_x]
        return tile is None or not getattr(tile, 'collision', False)

    def _find_path(self, start, goal):
        if start == goal:
            return [start]

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        closed = set()

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        while open_set:
            _, current = heapq.heappop(open_set)
            if current in closed:
                continue
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            closed.add(current)
            current_x, current_y = current
            for neighbor in (
                (current_x + 1, current_y),
                (current_x - 1, current_y),
                (current_x, current_y + 1),
                (current_x, current_y - 1),
            ):
                if not self._is_walkable_tile(*neighbor) and neighbor != goal:
                    continue

                tentative = g_score[current] + 1
                if tentative >= g_score.get(neighbor, float('inf')):
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative
                priority = tentative + heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))

        return None

    def _select_ally_target(self, ally):
        # Prefer enemies over player, but give priority to nearby threats
        # This allows allies to scout ahead and engage enemies proactively
        if self.enemy_list:
            closest_enemy = min(
                self.enemy_list,
                key=lambda enemy: math.hypot(enemy.rect.centerx - ally.rect.centerx, enemy.rect.centery - ally.rect.centery),
            )
            enemy_dist = math.hypot(closest_enemy.rect.centerx - ally.rect.centerx, closest_enemy.rect.centery - ally.rect.centery)
            # Pursue enemies more aggressively - up to 180px away
            if enemy_dist < 180:
                return closest_enemy
        return self.player

    def _steer_ally_along_path(self, ally, path):
        current_tile = self._tile_from_position(ally.rect.centerx, ally.rect.centery)
        next_tile = path[1]

        next_center_x = next_tile[0] * self.tile_size + self.tile_size / 2
        next_center_y = next_tile[1] * self.tile_size + self.tile_size / 2

        if next_center_x > ally.rect.centerx + 4:
            ally.vx = ally.speed
            ally.direction = 1
        elif next_center_x < ally.rect.centerx - 4:
            ally.vx = -ally.speed
            ally.direction = 0
        else:
            ally.vx = 0

        if next_center_y + (self.tile_size * 0.35) < ally.rect.centery and ally.on_ground:
            ally.vy = -16.0

        # If the path starts with a vertical move, keep the ally aggressive instead of stalling.
        if current_tile[0] == next_tile[0] and abs(next_center_y - ally.rect.centery) > self.tile_size * 0.4:
            ally.vx = 0

    def _steer_ally_directly(self, ally, target):
        # Use dynamic speed based on distance - slower when close, faster when far
        distance = abs(target.rect.centerx - ally.rect.centerx)
        speed_multiplier = min(1.2, 1.0 + (distance / 400))  # Up to 20% speed boost when far
        
        if target.rect.centerx > ally.rect.centerx + 6:
            ally.vx = ally.speed * speed_multiplier
            ally.direction = 1
        elif target.rect.centerx < ally.rect.centerx - 6:
            ally.vx = -ally.speed * speed_multiplier
            ally.direction = 0
        else:
            ally.vx = 0

        if target.rect.centery + 10 < ally.rect.centery and ally.on_ground:
            ally.vy = -16.0

    def _start_recruitment_dialogue(self, ally):
        if ally.recruited:
            return

        bank = list(RECRUIT_DIALOGUE_BANK.get(ally.type, RECRUIT_DIALOGUE_BANK['carrot']))
        random.shuffle(bank)
        dialogue = bank[:4]

        self.sequence_player.start_dialogue(
            dialogue,
            on_complete=lambda: self._complete_recruitment(ally),
        )

    def _complete_recruitment(self, ally):
        if ally.recruited:
            return
        ally.recruited = True
        ally.speed = 5  # Match player speed so they can keep up and scout ahead
        self.snd_collect.play()