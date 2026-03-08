import pygame
from settings import *
from button import Button
from Player import Player
from Enemy import Enemy
from score_tracker import ScoreTracker

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
        self.setup_ui()
        self.player = Player(100, self.screen_height, 34 * 3, 34 * 3)
        self.enemy = Enemy(400, self.screen_height, 75, 110)
        
    def setup_ui(self):    
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = BASE_WIDTH, BASE_HEIGHT

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_machine.transition('menu')
            elif event.type == pygame.VIDEORESIZE:
                self.setup_ui()

        if self.check_collision(self.player.rect, self.enemy.rect):
            if self.player.can_damage():
                self.enemy.take_damage(1)
            self.player.take_damage(1)

        for tear in self.player.tears:
            if self.check_collision(tear['rect'], self.enemy.rect):
                self.enemy.take_damage(1)
                self.player.tears.remove(tear)

        if not self.player.is_alive():
            self.__init__(self.state_machine)
            self.state_machine.transition('menu')

        self.player.update()
        self.enemy.update()
        self.score_tracker.tick()

    def draw(self, surface):
        surface.blit(pygame.image.load('assets/images/Levels/Level1_800x600.png'), (0, 0))
        text = pygame.font.Font(None, 74).render(f"Level {self.current_level}", True, WHITE)
        surface.blit(text, (self.screen_width//2 - text.get_width()//2, 30))

        score_value = self.score_tracker.snapshot().level_score
        score_text = pygame.font.Font(None, 40).render(f"Score: {score_value}", True, BLACK)
        surface.blit(score_text, (650, 20))

        self.player.draw(surface)
        self.enemy.draw(surface)
        
    def enter(self):
        self.setup_ui()
        self.score_tracker.start_level(f"story_{self.current_level}")
        self._play_level_music()

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