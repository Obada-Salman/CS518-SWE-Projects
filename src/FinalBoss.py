import pygame
from NPC import NPC
from settings import BASE_HEIGHT, BASE_WIDTH

class FinalBoss(NPC):
    def __init__(self, x, y):
        super().__init__(x, y, 110, 180, type='finalboss', speed=120, team='enemy')

        self.health = 200
        self.max_health = self.health
        self.damage = 4
        self.speed = 120.0
        self.attack_timer = 1.0
        self.attack_cooldown = 1.0
        self.seeds = []
        self.scroll = 0
        self.previous_scroll = 0

    def update(self, game_map, tile_size, scroll, dt):
        super().update(game_map, tile_size, dt)
        self.scroll = scroll
        self.attack_timer -= dt
        if self.attack_timer <= 0:
            self.spawn_seed()
            self.attack_timer = self.attack_cooldown
        
        self.update_seeds(dt)

    def spawn_seed(self):
        seed_width = 16
        seed_height = 16
        seed_x = 400 - self.scroll
        seed_y = 0

        self.seeds.append({
            'rect': pygame.Rect(seed_x, seed_y, seed_width, seed_height),
            'vy': 240,  # px/s
            'damage': 1
        })

    def update_seeds(self, dt):
        scroll_delta = self.scroll - self.previous_scroll
        self.previous_scroll = self.scroll
        
        for seed in self.seeds:
            seed['rect'].x -= scroll_delta
            seed['rect'].y += seed['vy'] * dt
            if seed['rect'].y > BASE_HEIGHT:
                self.seeds.remove(seed)

    def take_damage(self, amount):
        self.health -= amount
    
    def is_alive(self):
        return self.health > 0
    
    def draw(self, surface, scroll):
        self.sprites.draw(surface, self.rect.x - scroll, self.rect.y)
        self.draw_health_bar(surface)
        self.draw_seeds(surface)

    def draw_health_bar(self, surface):
        bar_width = 400
        bar_height = 20
        bar_x = BASE_WIDTH - bar_width - 20
        bar_y = 20
        health_ratio = self.health / self.max_health

        pygame.draw.rect(surface, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x + bar_width - int(bar_width * health_ratio), bar_y, int(bar_width * health_ratio), bar_height))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)

    def draw_seeds(self, surface):
        for seed in self.seeds:
            pygame.draw.rect(surface, (255, 255, 0), seed['rect'])