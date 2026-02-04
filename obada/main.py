import pygame

pygame.init()

resWidth = 800
resHeight = 600
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
player_health = 100

# Load carrot NPC
npc_image = pygame.image.load('obada/carrot.png')
h, w = npc_image.get_size()
npc_sprite = pygame.transform.scale(npc_image, (w // 4, h // 4))
npc = npc_sprite.get_rect(center=(600, 300))
npc_y = float(npc.y)
npc_health = 85

# Load map
map_image = pygame.image.load('obada/map.jpg')

running = True
while running:
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

    if player_health <= 0:
        player.move_ip(-1000, -1000)
    if npc_health <= 0:
        npc.move_ip(-1000, -1000)

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

    # Player movement
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move_ip(-3, 0)
    if key[pygame.K_RIGHT]:
        player.move_ip(3, 0)
    if key[pygame.K_UP] and player.bottom >= resHeight:
        player_vy = -jump_strength
    if key[pygame.K_DOWN]:
        player.move_ip(0, 3)

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

    # Collision with carrot
    if player.colliderect(npc):
        if key[pygame.K_LEFT]:
            player.move_ip(3, 0)
        elif key[pygame.K_RIGHT]:
            player.move_ip(-3, 0)
        elif key[pygame.K_UP]:
            player.move_ip(0, 3)
        elif key[pygame.K_DOWN]:
            player.move_ip(0, -3)
        
        player_y = float(player.y)
        player_health -= 1
        npc_health -= 1

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()