import pygame
import time


pygame.init()

resWidth = 1280
resHeight = 720
screen = pygame.display.set_mode((resWidth, resHeight))

FPS = 120
gravity = 0.3
jump_strength = 12
player_vy = 0.0
npc_vy = 0.0
clock = pygame.time.Clock()

# Load player
player_image = pygame.image.load('obada/player.png')
h, w = player_image.get_size()
player_sprite = pygame.transform.scale(player_image, (w // 16, h // 16))
player = player_sprite.get_rect(center=(400, 300))
player_y = float(player.y)
player_y_prev = player_y
player_health = 100

# Load carrot NPC
npc_image = pygame.image.load('obada/carrot.png')
h, w = npc_image.get_size()
npc_sprite = pygame.transform.scale(npc_image, (w // 4, h // 4))
npc = npc_sprite.get_rect(center=(600, 300))
npc_y = float(npc.y)
npc_health = 100

# Load map
map_image = pygame.image.load('obada/map.png')

# Load platforms
platform_image = pygame.image.load('obada/platform.png')
platform_sprite = pygame.transform.scale(platform_image, (467 // 1.5, 188 // 1.5))
platform1 = platform_sprite.get_rect(topleft=(200, 200))
platform2 = platform_sprite.get_rect(topleft=(650, 350))
platform3 = platform_sprite.get_rect(topleft=(100, 500))

# Load tear
tear_image = pygame.image.load('obada/tear.png')
tear_sprite = pygame.transform.scale(tear_image, (16, 16))
projectiles = []
last_direction = 1  # 1 for right, -1 for left
x_pressed_last_frame = False

# Load door and lock
door_image = pygame.image.load('obada/door.png')
lock_image = pygame.image.load('obada/lock.png')
door_sprite = pygame.transform.scale(door_image, (64, 96))
lock_sprite = pygame.transform.scale(lock_image, (64, 64))
door = door_sprite.get_rect(topleft=(10, 10))

# Jump sound
jump_sound = pygame.mixer.Sound('obada/jump.mp3')

# Shoot sound
shoot_sound = pygame.mixer.Sound('obada/shoot.mp3')

game_won = False
running = True

while running and not game_won:
    # Store previous positions
    player_y_prev = player_y
    npc_y_prev = npc_y
    
    player_vy += gravity
    player_y += player_vy
    npc_vy += gravity
    npc_y += npc_vy

    if player_y + player.height >= resHeight:
        player_y = resHeight - player.height
        player_vy = 0.0
    player.y = int(player_y)

    if npc_y + npc.height >= resHeight:
        npc_y = resHeight - npc.height
        npc_vy = 0.0
    npc.y = int(npc_y)

    screen.blit(map_image, (0, 0))
    screen.blit(platform_sprite, platform1)
    screen.blit(platform_sprite, platform2)
    screen.blit(platform_sprite, platform3)
    
    # Draw door and lock
    screen.blit(door_sprite, door)
    if npc_health > 0:
        lock_rect = lock_sprite.get_rect(center=(door.centerx, door.top + 45))
        screen.blit(lock_sprite, lock_rect)

    # Update and draw projectiles
    for proj in projectiles[:]:
        proj['rect'].x += proj['vx']
        screen.blit(tear_sprite, proj['rect'])
        
        # Remove projectiles that go off screen
        if proj['rect'].left > resWidth:
            projectiles.remove(proj)

    if player_health <= 0:
        player.move_ip(1000, 1000)
    if npc_health <= 0:
        npc.move_ip(1000, 1000)

    if player_health > 0:
        screen.blit(player_sprite, player)
    if npc_health > 0:
        screen.blit(npc_sprite, npc)

    # Draw health bars
    bar_width = 40
    bar_height = 5
    
    if player_health > 0:
        player_bar_rect = pygame.Rect(player.centerx - bar_width // 2, player.top - 10, bar_width, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), player_bar_rect)
        player_health_width = int(bar_width * (player_health / 100))
        pygame.draw.rect(screen, (0, 255, 0), (player.centerx - bar_width // 2, player.top - 10, player_health_width, bar_height))
    
    if npc_health > 0:
        npc_bar_rect = pygame.Rect(npc.centerx - bar_width // 2, npc.top - 10, bar_width, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), npc_bar_rect)
        npc_health_width = int(bar_width * (npc_health / 100))
        pygame.draw.rect(screen, (0, 255, 0), (npc.centerx - bar_width // 2, npc.top - 10, npc_health_width, bar_height))

    # Check if player is on ground or platform
    on_ground = player.bottom >= resHeight
    platforms = [platform1, platform2, platform3]
    
    for plat in platforms:
        if player.colliderect(plat) and player_vy >= 0:
            on_ground = True
            break
    
    # Player movement with arrow keys
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move_ip(-3, 0)
        last_direction = -1
    if key[pygame.K_RIGHT]:
        player.move_ip(3, 0)
        last_direction = 1
    if key[pygame.K_UP] and on_ground:
        player_vy = -jump_strength
        jump_sound.play()
    if key[pygame.K_DOWN]:
        player.move_ip(0, 3)
    
    # Shoot tears when pressing X
    if key[pygame.K_x] and not x_pressed_last_frame:
        tear_rect = tear_sprite.get_rect(center=player.center)
        projectiles.append({'rect': tear_rect, 'vx': 8 * last_direction})
        shoot_sound.play()
    
    x_pressed_last_frame = key[pygame.K_x]

    # Collision with screen borders
    if player.left < 0:
        player.left = 0
    if player.right > resWidth:
        player.right = resWidth
    if player.top < 0:
        player.top = 0
    if player.bottom > resHeight:
        player.bottom = resHeight

    player_y = float(player.y)

    if npc.left < 0:
        npc.left = 0
    if npc.right > resWidth:
        npc.right = resWidth
    if npc.top < 0:
        npc.top = 0
    if npc.bottom > resHeight:
        npc.bottom = resHeight

    npc_y = float(npc.y)

    # Collision with platforms
    for plat in platforms:
        if player.colliderect(plat) and player_vy > 0:
            if player_y_prev + player.height <= plat.top:
                player.bottom = plat.top
                player_vy = 0.0
                player_y = float(player.y)
        
        if npc.colliderect(plat) and npc_vy > 0:
            if npc_y_prev + npc.height <= plat.top:
                npc.bottom = plat.top
                npc_vy = 0.0
                npc_y = float(npc.y)

    # Collision with carrot
    if player.colliderect(npc):
        if key[pygame.K_LEFT]:
            player.move_ip(3, 0)
        if key[pygame.K_RIGHT]:
            player.move_ip(-3, 0)
        if key[pygame.K_UP]:
            player.move_ip(0, 3)
        if key[pygame.K_DOWN]:
            player.move_ip(0, -3)
        
        player_y = float(player.y)
        player_health -= 1
        npc_health -= 1

    # Projectile collision with carrot
    for proj in projectiles[:]:
        if proj['rect'].colliderect(npc):
            npc_health -= 10
            projectiles.remove(proj)

    # NPC moves towards player
    if npc_health > 0:
        dx = player.centerx - npc.centerx
        dy = player.centery - npc.centery
        
        if not npc.colliderect(player) and (abs(dx) > abs(dy)):
            if dx > 0:
                npc.move_ip(1, 0)
            else:
                npc.move_ip(-1, 0)
        else:
            if dy > 0:
                npc.move_ip(0, 1)
            else:
                npc.move_ip(0, -1)
    
    # When carrot dies and player reaches door, game is won
    if npc_health <= 0 and player.colliderect(door):
        game_won = True
        # Display win screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 72)
        win_text = font.render("YOU WIN!", True, (255, 255, 0))
        win_rect = win_text.get_rect(center=(resWidth // 2, resHeight // 2))
        screen.blit(win_text, win_rect)
        pygame.display.update()
        time.sleep(3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()