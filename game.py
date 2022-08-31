import pygame
from random import randint
def display_score():
    """
    Display score in screen
    returns: int
    """
    current_time = (pygame.time.get_ticks()//1000) - start_time
    score_surf = test_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    ds.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300:
                ds.blit(snail_surface, obstacle_rect)
            else:
                ds.blit(fly_surf, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

# Init pygame
pygame.init()

# Display surface
width = 800
height = 400
ds = pygame.display.set_mode((width, height))
pygame.display.set_caption("Runner")
game_active = False
start_time = 0
score = 0

# fonts
test_font = pygame.font.Font("assets/font/Pixeltype.ttf", 50)

# load surfaces
# sky
sky_image = pygame.image.load("assets/graphics/Sky.png").convert()
# ground
ground_image = pygame.image.load("assets/graphics/ground.png").convert()

# texts
game_over_surf = test_font.render("Pixel Runner!", False, (64,64,64))
game_over_rect = game_over_surf.get_rect(center = (width//2 + 10, 60))
press_space_surf = test_font.render("Press space to run", False, (64,64,64))
press_space_rect = press_space_surf.get_rect(center = (width//2, 350))
# score_surf = test_font.render("Hello World!", False, (64,64,64))
# score_rect = score_surf.get_rect(center = (width//2, 50))

# enemies
snail_surface = pygame.image.load("assets/graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (800, 300))

fly_surf = pygame.image.load("assets/graphics/fly/fly1.png").convert_alpha()

obstacle_rect_list = []

# player surface
player_surf = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# game over menu
player_stand = pygame.image.load("assets/graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (width//2,200))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# fps and clock
FPS = 60
clock = pygame.time.Clock()

# set game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_active:
            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.x = 800
                    start_time = pygame.time.get_ticks()//1000
        
        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1300), 300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900, 1300), 210)))

    # playing the game
    if game_active:
        # bg
        ds.blit(sky_image, (0,0))
        ds.blit(ground_image, (0,300))

        # text
        score = display_score()
        # pygame.draw.rect(ds, "#c0e8ec",score_rect)
        # pygame.draw.rect(ds, "#c0e8ec",score_rect,10)
        # ds.blit(score_surf, score_rect)

        # blit player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        ds.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)

        # snail blit and movement
        # ds.blit(snail_surface, snail_rect)
        # snail_rect.x -= 4
        # if snail_rect.x < -75: 
        #     snail_rect.x = 900

        # ends the game if collition to enemy
        if snail_rect.colliderect(player_rect):
            game_active = False

    # game over menu
    else:
        ds.fill((94,129,162))
        ds.blit(player_stand, player_stand_rect)
        ds.blit(game_over_surf, game_over_rect)
        score_message = test_font.render(f'Your score: {score}', False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400,320))
        obstacle_rect_list = []
        player_rect.midbottom = (80, 300)

        if score == 0:
            ds.blit(press_space_surf, press_space_rect)
        else:
            ds.blit(score_message, score_message_rect)


    # update display
    pygame.display.update()
    # set fps
    clock.tick(FPS)

# end the game
pygame.quit()