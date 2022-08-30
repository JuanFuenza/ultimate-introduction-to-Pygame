import pygame

# Init pygame
pygame.init()

# Display surface
width = 800
height = 400
ds = pygame.display.set_mode((width, height))
pygame.display.set_caption("Runner")

# fonts
test_font = pygame.font.Font("assets/font/Pixeltype.ttf", 50)

# load surfaces
# sky
sky_image = pygame.image.load("assets/graphics/Sky.png").convert()
# ground
ground_image = pygame.image.load("assets/graphics/ground.png").convert()

# texts
score_surf = test_font.render("Hello World!", False, (64,64,64))
score_rect = score_surf.get_rect(center = (width//2, 50))

# snail enemy
snail_surface = pygame.image.load("assets/graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (800, 300))

# player surface
player_surf = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# fps and clock
FPS = 60
clock = pygame.time.Clock()

# set game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
            if event.key == pygame.K_SPACE:
                player_gravity = -20

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20

    # bg
    ds.blit(sky_image, (0,0))
    ds.blit(ground_image, (0,300))

    # text
    pygame.draw.rect(ds, "#c0e8ec",score_rect)
    pygame.draw.rect(ds, "#c0e8ec",score_rect,10)
    ds.blit(score_surf, score_rect)

    # blit player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
    ds.blit(player_surf, player_rect)

    # snail blit and movement
    ds.blit(snail_surface, snail_rect)
    snail_rect.x -= 4
    if snail_rect.x < -75: 
        snail_rect.x = 900

    # update display
    pygame.display.update()

    # set fps
    clock.tick(FPS)

# end the game
pygame.quit()