import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("assets/graphics/player/player_walk_2.png").convert_alpha()

        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("assets/graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("assets/audio/jump.mp3")
        self.jump_sound.set_volume(0.05)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        """
        Animate the player when jumps or when is walking
        return: None
        """
        if self.rect.bottom < 300:
            # jump
            self.image = self.player_jump
        else:
            # walk
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load("assets/graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("assets/graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210

        else:
            snail_1 = pygame.image.load("assets/graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("assets/graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1400), y_pos))


    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


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

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
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
bg_music = pygame.mixer.Sound("assets/audio/music.wav")
bg_music.set_volume(0.03)
bg_music.play(loops = -1)


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

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
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() // 1000)

    # playing the game
    if game_active:
        # bg
        ds.blit(sky_image, (0,0))
        ds.blit(ground_image, (0,300))

        # text
        score = display_score()
        # Player
        player.draw(ds)
        player.update()

        # Obstacle
        obstacle_group.draw(ds)
        obstacle_group.update()

        # collision
        game_active = collision_sprite()

    # game over menu
    else:
        ds.fill((94,129,162))
        ds.blit(player_stand, player_stand_rect)
        ds.blit(game_over_surf, game_over_rect)
        score_message = test_font.render(f'Your score: {score}', False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400,320))

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