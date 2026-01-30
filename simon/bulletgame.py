import pygame
import random
import math

# --- Configuration ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
WORLD_WIDTH, WORLD_HEIGHT = 2000, 2000 
HUD_HEIGHT = 120
FPS = 60

# Colors
SULPHUR_YELLOW = (220, 220, 100)
SOIL_BROWN = (60, 40, 30)
STAGE2_GREEN = (25, 35, 20)
NUTRIENT_GREEN = (50, 255, 50)
OVERSHIELD_BLUE = (100, 200, 255)
WATER_BLUE = (50, 150, 255)
SUN_GOLD = (255, 220, 0)
GARLIC_PURPLE = (180, 100, 255)
BEAN_BRIGHT = (0, 255, 100)
BOSS_PHASE2_COLOR = (100, 50, 120)
WHITE = (255, 255, 255)
UI_BG = (20, 15, 10)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed=14, color=WHITE, reflected=False):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 8)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.reflected = reflected

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not (0 <= self.rect.x <= WORLD_WIDTH and 0 <= self.rect.y <= WORLD_HEIGHT):
            self.kill()

class BeanOrbiter(pygame.sprite.Sprite):
    def __init__(self, player, angle_offset, start_pos):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BEAN_BRIGHT, (15, 15), 12)
        self.rect = self.image.get_rect(center=start_pos)
        self.player = player
        self.angle = angle_offset
        self.dist = 0  # Starts at 0 and grows for a "natural" entry
        self.target_dist = 220
        self.shoot_timer = random.randint(0, 20) 

    def update(self, boss_bullets):
        self.angle += 0.04
        if self.dist < self.target_dist:
            self.dist += 5 # Fly out to orbit
            
        self.rect.centerx = self.player.rect.centerx + math.cos(self.angle) * self.dist
        self.rect.centery = self.player.rect.centery + math.sin(self.angle) * self.dist
        
        self.shoot_timer += 1
        if self.shoot_timer > 60: 
            angle_to_p = math.atan2(self.player.rect.centery - self.rect.centery, 
                                    self.player.rect.centerx - self.rect.centerx)
            
            boss_bullets.add(Projectile(self.rect.centerx, self.rect.centery, angle_to_p, 3, BEAN_BRIGHT))
            self.shoot_timer = 0

class BeanBoss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.display_name = "THE LEGUME OVERLORD"
        self.image = pygame.Surface((160, 100), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (0, 80, 0), (0, 0, 160, 100))
        pygame.draw.ellipse(self.image, BEAN_BRIGHT, (10, 10, 140, 80), 5)
        self.rect = self.image.get_rect(center=(WORLD_WIDTH//2, WORLD_HEIGHT//2 - 400))
        self.health = 3000
        self.max_health = 3000
        self.orbiters = pygame.sprite.Group()
        self.orbiter_count = 0

    def update(self, player, boss_bullets):
        target_y = player.rect.centery - 320
        self.rect.centerx += (player.rect.centerx - self.rect.centerx) * 0.04
        self.rect.centery += (target_y - self.rect.centery) * 0.04

        # Calculate how many orbiters to have SHOULD have (1 base + 1 per 10% health lost)
        health_lost_percent = (self.max_health - self.health) / self.max_health
        required_orbiters = min(5, 1 + int(health_lost_percent * 10))

        if self.orbiter_count < required_orbiters:
            new_angle = self.orbiter_count * (2 * math.pi / 5)
            self.orbiters.add(BeanOrbiter(player, new_angle, self.rect.center))
            self.orbiter_count += 1

        self.orbiters.update(boss_bullets)

class Resource(pygame.sprite.Sprite):
    def __init__(self, x, y, rtype="nutrient"):
        super().__init__()
        self.type = rtype
        self.image = pygame.Surface((12, 12))
        colors = {"nutrient": NUTRIENT_GREEN, "water": WATER_BLUE, "sun": SUN_GOLD}
        self.image.fill(colors.get(rtype, WHITE))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player_rect):
        dx, dy = player_rect.centerx - self.rect.centerx, player_rect.centery - self.rect.centery
        if math.hypot(dx, dy) < 300: 
            self.rect.x += dx * 0.12
            self.rect.y += dy * 0.12

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((34, 139, 34))
        angle = random.uniform(0, 2 * math.pi)
        self.rect = self.image.get_rect(center=(player_pos[0] + math.cos(angle) * 750, 
                                               player_pos[1] + math.sin(angle) * 750))
        self.speed = 2.5

    def update(self, player_pos):
        dx, dy = player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.display_name = "GARLIC INVADER"
        self.image = pygame.Surface((120, 120))
        self.image.fill((220, 220, 200))
        self.rect = self.image.get_rect(center=(WORLD_WIDTH//2, WORLD_HEIGHT//2 - 300))
        self.health = 1500
        self.max_health = 1500
        self.target_pos = [random.randint(200, WORLD_WIDTH-200), random.randint(200, WORLD_HEIGHT-200)]
        self.shoot_timer = 0
        self.phase = 1

    def update(self, player_pos, boss_bullets):
        dx, dy = self.target_pos[0] - self.rect.centerx, self.target_pos[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        move_speed = 3.5 if self.phase == 1 else 5.5
        if dist < 25: self.target_pos = [random.randint(200, WORLD_WIDTH-200), random.randint(200, WORLD_HEIGHT-200)]
        else:
            self.rect.x += (dx / dist) * move_speed
            self.rect.y += (dy / dist) * move_speed

        if self.phase == 1 and self.health <= self.max_health * 0.33:
            self.phase = 2
            self.display_name = "VAMPIRE GARLIC (PHASE 2)"
            self.health = self.max_health
            self.image.fill(BOSS_PHASE2_COLOR)

        self.shoot_timer += 1
        fire_rate = 80 if self.phase == 1 else 60
        if self.shoot_timer >= fire_rate:
            angle = math.atan2(player_pos[1] - self.rect.centery, player_pos[0] - self.rect.centerx)
            if self.phase == 1: boss_bullets.add(Projectile(self.rect.centerx, self.rect.centery, angle, 7, GARLIC_PURPLE))
            else:
                for off in [-0.3, 0, 0.3]: boss_bullets.add(Projectile(self.rect.centerx, self.rect.centery, angle + off, 8, GARLIC_PURPLE))
            self.shoot_timer = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.layers = 3
        self.max_layers = 5 
        self.health_in_layer = 100
        self.super_meter = 0
        self.rect = pygame.Rect(WORLD_WIDTH//2, WORLD_HEIGHT//2, 60, 60)
        self.move_speed = 5
        self.aim_angle = 0
        self.melee_cooldown = 0
        self.swing_timer = 0 
        self.parry_active = 0 
        self.beam_timer = 0 

    def update(self, keys, mouse_pos, camera_offset):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += 1
        if dx != 0 or dy != 0:
            dist = math.hypot(dx, dy)
            self.rect.x += (dx / dist) * self.move_speed
            self.rect.y += (dy / dist) * self.move_speed
        
        ax, ay = mouse_pos[0] + camera_offset[0], mouse_pos[1] + camera_offset[1]
        self.aim_angle = math.atan2(ay - self.rect.centery, ax - self.rect.centerx)
        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))
        if self.melee_cooldown > 0: self.melee_cooldown -= 1
        if self.swing_timer > 0: self.swing_timer -= 1
        if self.parry_active > 0: self.parry_active -= 1
        if self.beam_timer > 0: self.beam_timer -= 1

    def take_damage(self, amount):
        if self.health_in_layer > 100: self.health_in_layer = 100; return False
        self.health_in_layer -= amount
        if self.health_in_layer <= 0:
            if self.layers > 1:
                self.layers -= 1; self.health_in_layer = 100; self.rect.inflate_ip(-10, -10); return False
            return True
        return False

    def heal(self):
        self.health_in_layer += 10
        if self.health_in_layer >= 200 and self.layers < self.max_layers:
            self.layers += 1; self.health_in_layer = 100; self.rect.inflate_ip(10, 10)
        elif self.health_in_layer > 200: self.health_in_layer = 200

    def draw(self, surface, offset):
        dr = self.rect.move(-offset[0], -offset[1])
        if self.beam_timer > 0:
            end_x, end_y = dr.centerx + math.cos(self.aim_angle) * 1000, dr.centery + math.sin(self.aim_angle) * 1000
            pygame.draw.line(surface, SUN_GOLD, dr.center, (end_x, end_y), 50)
            pygame.draw.line(surface, WHITE, dr.center, (end_x, end_y), 20)
        color = (255, 255, 200) if self.health_in_layer <= 100 else (180, 255, 180)
        pygame.draw.ellipse(surface, color, dr)
        if self.parry_active > 0: pygame.draw.ellipse(surface, WHITE, dr.inflate(25, 25), 4)
        if self.health_in_layer > 100: pygame.draw.ellipse(surface, OVERSHIELD_BLUE, dr, 4)
        if self.swing_timer > 0:
            arc_surf = pygame.Surface((240, 240), pygame.SRCALPHA)
            pygame.draw.arc(arc_surf, (255, 255, 255, 180), (0, 0, 240, 240), -self.aim_angle-0.8, -self.aim_angle+0.8, 20)
            surface.blit(arc_surf, (dr.centerx - 120, dr.centery - 120))
        ex, ey = dr.centerx + math.cos(self.aim_angle) * 15, dr.centery + math.sin(self.aim_angle) * 15
        pygame.draw.circle(surface, (0,0,0), (int(ex-6), int(ey-4)), 4)
        pygame.draw.circle(surface, (0,0,0), (int(ex+6), int(ey-4)), 4)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20, bold=True)
    big_font = pygame.font.SysFont("Arial", 48, bold=True)
    
    player = Player()
    bullets, enemies, resources, boss_group, boss_bullets = [pygame.sprite.Group() for _ in range(5)]
    game_state = "PLAYING"
    current_stage, boss_spawned = 1, False
    
    running = True
    while running:
        cam_x, cam_y = max(0, min(player.rect.centerx - 400, 1200)), max(0, min(player.rect.centery - 400, 1200))
        offset, mouse_pos = (cam_x, cam_y), pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_z, pygame.K_e] and player.beam_timer <= 0:
                        bullets.add(Projectile(player.rect.centerx, player.rect.centery, player.aim_angle))
                    if event.key == pygame.K_x and player.super_meter >= 100: player.beam_timer = 60; player.super_meter = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and player.melee_cooldown <= 0:
                        player.swing_timer = 8; player.melee_cooldown = 25 
                        for e in enemies:
                            if math.hypot(e.rect.centerx-player.rect.centerx, e.rect.centery-player.rect.centery) < 145:
                                e.kill(); resources.add(Resource(e.rect.centerx, e.rect.centery, random.choices(["nutrient", "sun", "water"], [0.6, 0.2, 0.2])[0]))
                        for b in boss_group:
                            if math.hypot(b.rect.centerx-player.rect.centerx, b.rect.centery-player.rect.centery) < 180: b.health -= 50
                    if event.button == 3: player.parry_active = 12
            elif game_state == "UPGRADE" and event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[0] < 266: player.max_layers = 7
                elif mouse_pos[0] < 532: player.move_speed += 2
                else: player.super_meter = 100
                current_stage, game_state = 2, "PLAYING"

        if game_state == "PLAYING":
            screen.fill(SOIL_BROWN if current_stage == 1 else STAGE2_GREEN)
            spawn_chance = 0.05 if current_stage == 1 else 0.1
            if len(enemies) < (20 if current_stage == 1 else 40) and random.random() < spawn_chance: enemies.add(Enemy(player.rect.center))
            
            if not boss_spawned:
                if current_stage == 1 and player.layers >= 5: boss_group.add(Boss()); boss_spawned = True
                elif current_stage == 2 and player.layers >= 5: boss_group.add(BeanBoss()); boss_spawned = True

            player.update(pygame.key.get_pressed(), mouse_pos, offset)
            bullets.update(); boss_bullets.update(); resources.update(player.rect)
            for e in enemies: e.update(player.rect.center)
            for b in boss_group:
                if isinstance(b, Boss): b.update(player.rect.center, boss_bullets)
                else: 
                    b.update(player, boss_bullets)
                    for orb in b.orbiters: screen.blit(orb.image, orb.rect.move(-offset[0], -offset[1]))

            if player.beam_timer > 0:
                for e in enemies:
                    if abs((math.atan2(e.rect.centery-player.rect.centery, e.rect.centerx-player.rect.centerx) - player.aim_angle + math.pi) % (2*math.pi) - math.pi) < 0.15: e.kill()
                for b in boss_group: b.health -= 15

            for bb in boss_bullets:
                if player.rect.colliderect(bb.rect):
                    if player.parry_active > 0: bb.vx *= -2.5; bb.vy *= -2.5; bb.reflected = True; player.super_meter = min(100, player.super_meter + 15); player.parry_active = 0
                    else: 
                        if player.take_damage(20): running = False
                        bb.kill()
                if bb.reflected:
                    for b in boss_group:
                        if b.rect.colliderect(bb.rect): b.health -= 120; bb.kill()

            for b in bullets:
                e_hits = pygame.sprite.spritecollide(b, enemies, True)
                for h in e_hits:
                    resources.add(Resource(h.rect.centerx, h.rect.centery, random.choices(["nutrient", "sun", "water"], [0.7, 0.15, 0.15])[0]))
                    player.super_meter = min(100, player.super_meter + 5)
                b_hits = pygame.sprite.spritecollide(b, boss_group, False)
                if e_hits or b_hits:
                    b.kill()
                    for h in b_hits:
                        h.health -= 25
                        if h.health <= 0: h.kill(); boss_spawned = False; game_state = "UPGRADE" if current_stage == 1 else "WON"

            for r in pygame.sprite.spritecollide(player, resources, True):
                if r.type == "nutrient": player.heal()
                elif r.type == "sun": player.super_meter = min(100, player.super_meter + 20)
                elif r.type == "water": player.move_speed = min(12, player.move_speed + 0.5)

            if pygame.sprite.spritecollide(player, enemies, True):
                if player.take_damage(25): running = False

            for group in [resources, enemies, bullets, boss_bullets, boss_group]:
                for s in group: screen.blit(s.image, s.rect.move(-offset[0], -offset[1]))
            player.draw(screen, offset)

            # --- HUD ---
            pygame.draw.rect(screen, UI_BG, (0, 680, 800, 120))
            pygame.draw.rect(screen, (60, 20, 20), (30, 710, 300, 30))
            hp_w, sh_w = (min(player.health_in_layer, 100)/100)*300, (max(0, player.health_in_layer-100)/100)*300
            pygame.draw.rect(screen, (50, 220, 50), (30, 710, hp_w, 30))
            if sh_w > 0: pygame.draw.rect(screen, OVERSHIELD_BLUE, (30, 710, sh_w, 30))
            screen.blit(font.render(f"LAYER HEALTH: {int(player.health_in_layer)}%", True, WHITE), (40, 715))
            pygame.draw.rect(screen, (40, 40, 40), (30, 755, 300, 20))
            pygame.draw.rect(screen, SULPHUR_YELLOW, (30, 755, player.super_meter * 3, 20))
            screen.blit(font.render(f"EMOTION METER (X): {int(player.super_meter)}%", True, WHITE), (40, 755))
            screen.blit(font.render(f"LAYERS: {player.layers} / {player.max_layers}", True, WHITE), (380, 710))
            screen.blit(font.render(f"MOVE SPEED: {round(player.move_speed, 1)}", True, WATER_BLUE), (380, 735))
            
            if boss_spawned:
                for b in boss_group:
                    pygame.draw.rect(screen, (30, 30, 30), (200, 20, 400, 25))
                    pygame.draw.rect(screen, WHITE, (200, 20, (b.health/b.max_health)*400, 25))
                    screen.blit(font.render(b.display_name, True, WHITE), (300, 50))

        elif game_state == "UPGRADE":
            screen.fill((20, 20, 40))
            screen.blit(big_font.render("GARLIC DEFEATED!", True, SUN_GOLD), (180, 100))
            pygame.draw.rect(screen, (50, 0, 0), (0, 300, 266, 300))
            pygame.draw.rect(screen, (0, 50, 0), (266, 300, 266, 300))
            pygame.draw.rect(screen, (0, 0, 50), (532, 300, 266, 300))
            screen.blit(font.render("MAX LAYERS -> 7", True, WHITE), (50, 450))
            screen.blit(font.render("+2 SPEED BOOST", True, WHITE), (330, 450))
            screen.blit(font.render("REFILL SUPER", True, WHITE), (600, 450))
        elif game_state == "WON":
            screen.fill((0, 0, 0)); screen.blit(big_font.render("GARDEN SECURED!", True, NUTRIENT_GREEN), (200, 350))
        pygame.display.flip(); clock.tick(FPS)
    pygame.quit()

main()