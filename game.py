import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode((1000,550))
pygame.display.set_caption('Jump Joy')
clock= pygame.time.Clock()
font= pygame.font.Font('Pixeltype.ttf',70)

sky     = pygame.image.load('image/Sky2.png').convert_alpha()
ground  = pygame.image.load('image/ground.png').convert_alpha()

#obstacle
ob1= pygame.image.load('image/tcc.png').convert_alpha()
ob2= pygame.image.load('image/tcc11.png').convert_alpha()
ob3= pygame.image.load('image/tcc22.png').convert_alpha()
ob5= pygame.image.load('image/Fly1.png').convert_alpha()
ob6= pygame.image.load('image/Fly2.png').convert_alpha()
ob7= pygame.image.load('image/tc4.png').convert_alpha()

fly_obs=[ob5,ob6]

fly_indx=0
ob4 = fly_obs[fly_indx]

obstacle_rect_list=[]

p_stand= pygame.image.load('image/player_stand.png').convert_alpha()
p_walk1= pygame.image.load('image/player_walk_1.png').convert_alpha()
p_walk2= pygame.image.load('image/player_walk_2.png').convert_alpha()
p_walk= [p_walk1,p_walk2]
p_index=0
p_jump = pygame.image.load('image/jump.png').convert_alpha()
player_walk= p_walk[p_index]

p_rect= player_walk.get_rect(midbottom= (100,480))
p_scale= pygame.transform.rotozoom(p_stand,0,2)
p_scale_rect= p_scale.get_rect(center=(500,270))

game_name= font.render('JUMP JOY',False,(218,220,218))
game_name_rect = game_name.get_rect(center=(513,130))


gravity=0
game_active = False
c_time=0
game_score=0
t=0

jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.5)

bg_sound = pygame.mixer.Sound('audio/Juhani Junkala [Retro Game Music Pack] Level 3.wav')
bg_sound.set_volume(0.5)
bg_sound.play(loops= -1)

coll_sound = pygame.mixer.Sound('audio/coll.wav')
coll_sound.set_volume(0.5)

eat_sound = pygame.mixer.Sound('audio/eat.wav')

def obstacle_movement(obs_list):
    save=-1
    for obs in obs_list:
        obs.x-=(6+t)
        if save == -1:
            save= obs.x
        else:
            df= obs.x - save
            if df < 300:
                obs.x=(300 + save)
            save= obs.x

        if obs.y % 10 == 0:
            screen.blit(ob1,obs)
        elif obs.y % 10 == 1:
            screen.blit(ob2, obs)
        elif obs.y % 10 == 2:
            screen.blit(ob3, obs)
        elif obs.y % 10 == 3:
            screen.blit(ob4, obs)
        else:
            screen.blit(ob7, obs)

    obs_list = [obs for obs in obs_list if obs.x >  -100]
    if not obs_list:
        obs_list=[]

    return obs_list
def update():
    global gravity
    global p_rect
    global obstacle_rect_list

    obstacle_rect_list= obstacle_movement(obstacle_rect_list)

#player
    gravity+=1
    p_rect.y+=gravity

    if p_rect.bottom > 480:
        p_rect.bottom = 480
    return
def insert():
    screen.blit(sky,(0,0))
    screen.blit(ground,(0,480))
    player_animation()
    screen.blit(player_walk,p_rect)

    update()

    return

def disp_score():
    global c_time

    ac_time=int(c_time)
    score = font.render(f'Score: {ac_time}', False, (64,64,64))
    score_rect = score.get_rect(topleft=(70, 50))
    screen.blit(score, score_rect)
    c_time+=0.03

    return ac_time

def collision(player,obstacle):
    global c_time
    if obstacle:
        for obs in obstacle:
            if player.colliderect(obs):
                if obs.y %10 == 9:
                    c_time+=(10)
                    obs.x=-50
                    eat_sound.play()
                    return True

                return False
    return True

def player_animation():
    global player_walk,p_index

    if p_rect.bottom < 480 :
        player_walk = p_jump
    else:
        p_index+=0.1
        if int(p_index) ==2:
            p_index=0
        player_walk= p_walk[int(p_index)]

#Timer
obs_timer = pygame.USEREVENT + 1
time=2500
pygame.time.set_timer(obs_timer,time)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if p_rect.collidepoint(event.pos)  and p_rect.bottom == 480 :
        #         gravity=-24
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and p_rect.bottom == 480 and game_active == True:
                gravity=-22
                jump_sound.play()
            if event.key == pygame.K_SPACE:
                game_active = True
        if event.type == obs_timer and game_active == True:
            rd= int(randint(0,4))
            if rd == 0:
                obstacle_rect_list.append(ob1.get_rect(topleft=(randint(1100,1200), 420)))
            elif rd == 1:
                obstacle_rect_list.append(ob2.get_rect(topleft=(randint(1100, 1200), 421)))
            elif rd == 2:
                obstacle_rect_list.append(ob3.get_rect(topleft=(randint(1100, 1200), 422)))
            elif rd == 3:
                obstacle_rect_list.append(ob4.get_rect(topleft=(randint(1100, 1200), 313)))
            else:
                obstacle_rect_list.append(ob7.get_rect(topleft=(randint(1100, 1200), 429)))


    if game_active == True:

        if time>1000:
            time-=10

        insert()
        fly_indx+=0.1
        if int(fly_indx)== 2:
            fly_indx=0
        ob4 = fly_obs[int(fly_indx)]


        game_score= disp_score()

        if game_score % 20 == 0:
            t+=0.005
        game_active = collision(p_rect,obstacle_rect_list)
        if game_active == False:
            coll_sound.play()

    else:
        screen.fill((94,129,162))
        screen.blit(p_scale,p_scale_rect)
        screen.blit(game_name,game_name_rect)

        score_msg = font.render(f'Your score:  {game_score}', False, 'White')
        score_msg_rect = score_msg.get_rect(center=(530, 400))

        game_msg = font.render('Press space to run', False, 'White')
        game_msg_rect = game_msg.get_rect(center=(500, 400))
        game_msg_rect2= game_msg.get_rect(center=(530, 450))

        obstacle_rect_list.clear()
        p_rect.bottom = 480
        gravity=0

        if game_score== 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)
            screen.blit(game_msg, game_msg_rect2)
        c_time=0


    pygame.display.update()
    clock.tick(20)
