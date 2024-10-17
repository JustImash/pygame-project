import pygame, random, math

#-------------------------------------------------------------------------------------------
#function for support of working
def blitcenter(surf, pos):
    screen.blit(surf, [pos[0] - surf.get_size()[0] / 2, pos[1] - surf.get_size()[1] / 2])

def distance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def cos(x):
    return math.cos(math.radians(x))

def sin(x):
    return math.sin(math.radians(x))
#-------------------------------------------------------------------------------------------
# Pygame configuration
pygame.init()
mixer = pygame.mixer
mixer.init()

#-------------------------------------------------------------------------------------------
#Creation of window for the game

window = pygame.display.set_mode([600, 500])
pygame.display.set_caption('Game')
#-------------------------------------------------------------------------------------------
#Uploading of sprites
heart = pygame.image.load('Images/Heart.png')
game_over_sprite = pygame.image.load('Images/Game_over.png')
sprnames = ['Images/bone_hor.png', 'Images/bone_ver.png']
spr = [pygame.image.load(i) for i in sprnames]
#-------------------------------------------------------------------------------------------
# Uploading of Sounds and Music

boom = mixer.Sound('Sounds/boom.wav')

def start_music():
    mixer.music.load('Music/Background_music.ogg')
    mixer.music.play(-1)

start_music()
#-------------------------------------------------------------------------------------------
# Starting parametrs of Player
player_x = 300
player_y = 300
player_speed = 4

pygame.key.set_repeat(1, 1)
#-------------------------------------------------------------------------------------------
# Parametrs of Attacks
atime = 600  
attack = 0
bullets = []  
#-------------------------------------------------------------------------------------------
# Parametrs of Game
tick = 0
hp = 100
maxhp = 100
alt = 0
#-------------------------------------------------------------------------------------------

clock = pygame.time.Clock()
#-------------------------------------------------------------------------------------------
#Gameover function - end of the game
def gameover():
    
    mixer.music.stop()
    mixer.music.load('Music/Death_music.ogg')
    mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  

        window.fill([0, 0, 0])  
        window.blit(game_over_sprite, (87, 50))  
        pygame.display.flip()  

        clock.tick(60)
#-------------------------------------------------------------------------------------------
#Function for resseting game after 'Game Over'
def reset_game():
    global player_x, player_y, hp, maxhp, bullets, atime, attack, tick
    player_x = 300
    player_y = 300
    hp = 100
    maxhp = 100
    bullets = []
    atime = 600
    attack = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    tick = 0
    start_music()  
#-------------------------------------------------------------------------------------------
# Основной игровой цикл
reset_game()

#-------------------------------------------------------------------------------------------
#Limits for game zone, playable space
zone_left = 200
zone_right = 400
zone_top = 200
zone_bottom = 400
#-------------------------------------------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
#-------------------------------------------------------------------------------------------
#Control of player
    keys = pygame.key.get_pressed()
    moving = 1
    if keys[pygame.K_UP] and player_y - 8 > zone_top:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y + 8 < zone_bottom:
        player_y += player_speed
    if keys[pygame.K_LEFT] and player_x - 8 > zone_left:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + 8 < zone_right:
        player_x += player_speed
#-------------------------------------------------------------------------------------------
#Attack logic - 10 different patterns of attacks that change every 10 seconds
    atime -= 1
    if atime <= 0:
        attack = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  
        atime = 600  
        bullets = []

# Vertical attacks
    if attack == 0:  
        if tick % 24 == 0:
            if alt == 0:
                bullets.append([0, zone_left, random.randint(zone_top, zone_bottom), 0, 6])
                alt = 1
            else:
                bullets.append([0, zone_left, random.randint(zone_top, zone_bottom), 0, 6])
                alt = 0
#Double Diagonal Attacks
    elif attack == 1:  
        if tick % 40 == 0:
            bullets.append([0, zone_left, random.randint(zone_top, zone_bottom), 10, 8])
            bullets.append([0, zone_right, random.randint(zone_top, zone_bottom), 170, 8])
#Horizontal Attacks
    elif attack == 2:  
        if tick % 30 == 0:
            bullets.append([0, zone_left, random.randint(zone_top, zone_bottom), 0, 8])
            bullets.append([0, zone_right, random.randint(zone_top, zone_bottom), 180, 8])
#Attacks up
    elif attack == 3:  
        if tick % 50 == 0:
            bullets.append([0, random.randint(zone_left, zone_right), zone_bottom, -90, 6])
#Attacks from corners
    elif attack == 4:  
        if tick % 35 == 0:
            bullets.append([0, zone_left, random.randint(zone_top, zone_bottom), 45, 7])
            bullets.append([0, zone_right, random.randint(zone_top, zone_bottom), -135, 7])
#Attack-Rain
    elif attack == 5: 
        if tick % 10 == 0:
            bullets.append([0, random.randint(zone_left, zone_right), zone_top, 90, 8])
#Spiral attack
    elif attack == 6:  
        if tick % 15 == 0:
            bullets.append([0, (zone_left + zone_right) // 2, (zone_top + zone_bottom) // 2, tick % 360, 5])
#Range Attack
    elif attack == 7:  
        if tick % 25 == 0:
            bullets.append([0, (zone_left + zone_right) // 2, (zone_top + zone_bottom) // 2, random.randint(0, 360), 7])
#Attack follow      
    elif attack == 8: 
        if tick % 20 == 0:
            angle = math.degrees(math.atan2(player_y - (zone_top + zone_bottom) // 2, player_x - (zone_left + zone_right) // 2))
            bullets.append([0, (zone_left + zone_right) // 2, (zone_top + zone_bottom) // 2, angle, 6])
#Random
    elif attack == 9:  
        if tick % 60 == 0:
            boom.play()
            bullets.append([0, random.randint(zone_left, zone_right), random.randint(zone_top, zone_bottom), random.randint(0, 360), 8])

#-------------------------------------------------------------------------------------------
#Screen Update
    screen = pygame.Surface([600, 500])
    screen.fill([0, 0, 0])
    pygame.draw.rect(screen, [255, 255, 255], [zone_left, zone_top, 200, 200])
    pygame.draw.rect(screen, [0, 0, 0], [zone_left + 4, zone_top + 4, 192, 192])

#-------------------------------------------------------------------------------------------
    screen.blit(heart, [player_x - 8, player_y - 8])
    

    blitcenter(pygame.image.load('Villain/legs_villain.png'), [300, 137])
    blitcenter(pygame.image.load('Villain/body_villain.png'), [300, 90])
    blitcenter(pygame.image.load('Villain/face_villain.png'), [300, 50])
#-------------------------------------------------------------------------------------------
#Bullet hit and decreasing hp
    
    for b in bullets:
        bullet = pygame.transform.rotate(spr[b[0]], b[3])
        screen.blit(bullet, [b[1], b[2]])
        b[1] += cos(b[3]) * b[4]
        b[2] += sin(b[3]) * b[4]

        if distance(b[1], b[2], player_x, player_y) < 10:
            hp -= 10  
#-------------------------------------------------------------------------------------------
#Health Bar
    pygame.draw.rect(screen, [255, 0, 0], [8, 8, maxhp, 16])
    pygame.draw.rect(screen, [255, 255, 0], [8, 8, hp, 16])
    font = pygame.font.Font('Fonts/Font1.ttf', 25)
    screen.blit(font.render(f'HP {hp}/{maxhp}', True, [255, 255, 255]), [12, 24])

    window.blit(screen, [0, 0])
    pygame.display.flip()

    tick += 1
#-------------------------------------------------------------------------------------------

    clock.tick(60)
#-------------------------------------------------------------------------------------------
#Game Over
    if hp <= 0:
        gameover()
        reset_game()
#-------------------------------------------------------------------------------------------