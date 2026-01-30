import pygame

pygame.init()

resWidth = 800
resHeight = 600
screen = pygame.display.set_mode((resWidth, resHeight))

FPS = 120
clock = pygame.time.Clock()

# Load player
player_image = pygame.image.load('obada/player.png')
h, w = player_image.get_size()
player_sprite = pygame.transform.scale(player_image, (w // 16, h // 16))
player = player_sprite.get_rect(center=(400, 300))
player_health = 100

# Load carrot NPC
npc_image = pygame.image.load('obada/carrot.png')
h, w = npc_image.get_size()
npc_sprite = pygame.transform.scale(npc_image, (w // 4, h // 4))
npc = npc_sprite.get_rect(center=(600, 300))
npc_health = 85

# Load map
map_image = pygame.image.load('obada/map.jpg')

running = True
while running:
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
        player.move_ip(-1, 0)
    elif key[pygame.K_RIGHT]:
        player.move_ip(1, 0)
    elif key[pygame.K_UP]:
        player.move_ip(0, -1)
    elif key[pygame.K_DOWN]:
        player.move_ip(0, 1)

    # Collision with screen borders
    if player.left < 0:
        player.left = 0
    if player.right > resWidth:
        player.right = resWidth
    if player.top < 0:
        player.top = 0
    if player.bottom > resHeight:
        player.bottom = resHeight

    # Collision with carrot
    if player.colliderect(npc):
        if key[pygame.K_LEFT]:
            player.move_ip(1, 0)
        elif key[pygame.K_RIGHT]:
            player.move_ip(-1, 0)
        elif key[pygame.K_UP]:
            player.move_ip(0, 1)
        elif key[pygame.K_DOWN]:
            player.move_ip(0, -1)
        
        # Decrease health when colliding
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