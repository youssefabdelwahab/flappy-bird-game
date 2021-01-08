import pygame
import sys
import random
tower_list = []
def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 500))
    screen.blit(floor_surface, (floor_x_position + 1000, 500))

def create_tower():
    bottom_random_tower_pos = random.choice(tower_height)
    upper_random_tower_pos = random.choice(tower_height)
    bottom_tower = tower_surface.get_rect(midtop= (2000 ,bottom_random_tower_pos ))
    upper_tower =  tower_surface.get_rect(midbottom= (2000 ,bottom_random_tower_pos -125))
    return bottom_tower , upper_tower

def move_tower(towers):
    for tower in towers:
        tower.centerx -= 4
    exsisting_towers = [ tower for tower in towers if tower.right >-50]
    return exsisting_towers
#
def draw_tower(towers):
    for tower in towers:
        if tower.bottom >= 600:
            screen.blit(tower_surface ,tower )
        else:
            flip_tower = pygame.transform.flip(tower_surface, False , True)
            screen.blit(flip_tower, tower)
def collision_detector(towers):
    for tower in towers:
        if bird_rect.colliderect(tower):
            collision_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 500:
        collision_sound.play()
        can_score = True
        return False
    return True

def rotate_bird(bird):
    new_flappy_bird = pygame.transform.rotozoom(bird , -bird_movement*3, 1)
    return new_flappy_bird

def bird_animation():
    new_bird =  bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird , new_bird_rect

def writing_score():
    score_surface = game_font.render(str(int(score)), True,(255,255,255))
    score_rect = score_surface.get_rect(center = (500,50))
    screen.blit(score_surface, score_rect)

def score_check():
    global score, can_score
    if tower_list:
        for tower in tower_list:
            if tower.centerx == 100  and can_score:
                point_sound.play()
                score += 1
                can_score = False
            if tower.centerx < 0:
                can_score = True

def displaying_score(game_state):

    if game_state == 'initial_game':
        score_surface = game_font.render(str(int(score)), True , (255,255,255))
        score_rect = score_surface.get_rect(center =(500 , 50))
        screen.blit(score_surface , score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (500 , 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (500 , 475))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score , high_score):
    if score > high_score:
        high_score = score
    return high_score




pygame.init()
game_font = pygame.font.Font('assets/04B_19.TTF',40)
gravity = 0.20
bird_movement = 0
tower_height =[200 , 250 ,350, 400 , 450]
screen = pygame.display.set_mode((1000 , 600))
clock = pygame.time.Clock()
can_score = True
score = 0
high_score = 0
levels = [2 , 20 , 30 , 40 , 50 , 60 , 70 , 80 , 90 , 100]
background_surface = pygame.image.load("assets/background-day.png").convert()
background_surface = pygame.transform.scale(background_surface , (1000 ,600))

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface , (1000 , 200))
floor_x_position = 0

flappy_bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
flappy_bird_downflap = pygame.transform.scale(flappy_bird_downflap ,(40,30))
flappy_bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
flappy_bird_midflap = pygame.transform.scale(flappy_bird_midflap, (40,30))
flappy_bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
flappy_bird_upflap = pygame.transform.scale(flappy_bird_upflap, (40 , 30))
bird_list = [flappy_bird_downflap, flappy_bird_midflap, flappy_bird_upflap]
bird_index = 0
bird_surface = bird_list[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 200))
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (200 , 300))
game_over_rect = game_over_surface.get_rect(center = (500 , 275))
flapp_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
collision_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('sound/sfx_point.wav')
BIRDFLAP = pygame.USEREVENT +1
pygame.time.set_timer(BIRDFLAP, 200)
i = 0


# flappy_bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
# flappy_bird_surface = pygame.transform.scale(flappy_bird_surface,(40,30))
# flappy_bird_rect = flappy_bird_surface.get_rect(center = (100, 200))

tower_surface = pygame.image.load("assets/pipe-green.png").convert_alpha()
tower_surface = pygame.transform.scale(tower_surface, (75, 600))


SPAWNTOWER = pygame.USEREVENT
pygame.time.set_timer(SPAWNTOWER,1500)








game_on = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_on:
                bird_movement =0
                bird_movement -= 5
                flapp_sound.play()
            if event.key == pygame.K_SPACE and game_on == False:
                game_on = True
                tower_list.clear()
                bird_rect.center = (100,200)
                bird_movement = 0
                score = 0
        if event.type == SPAWNTOWER:
            tower_list.extend(create_tower())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    screen.blit(background_surface, (0, 0))
    if game_on:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird , bird_rect)
        collision_detector(tower_list )
        tower_list = move_tower(tower_list)
        draw_tower(tower_list)
        game_on  = collision_detector(tower_list)
        writing_score()
        score_check()
        displaying_score("initial_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score , high_score)
        displaying_score('game_over')
    floor_x_position -= 1.2
    draw_floor()
    if floor_x_position < -1000:
        floor_x_position = 0
        screen.blit(floor_surface, (floor_x_position,500))
    pygame.display.update()
    clock.tick(100)













