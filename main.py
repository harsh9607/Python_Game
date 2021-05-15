import pygame
import random
import math
from pygame import mixer

# initialize
pygame.init()

#  width & height of screen
screen = pygame.display.set_mode((800, 600))

# Title &  Icon
# Image courtesy  Flaticon & freepik & smashikons & Adobe
pygame.display.set_caption("Kershlov")
icon = pygame.image.load('crush.png')
pygame.display.set_icon(icon)

# background image
background_img = pygame.image.load('Background2.jpg')
background_img = pygame.transform.scale(background_img, (800, 600))

# Backrgound sound
mixer.music.load('Tobu  Return To The Wild NCS Release.mp3')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('Mean_girl_edited.png')
# image was big so i made it a 64x64 bit image
playerImg = pygame.transform.scale(playerImg, (72, 72))

# X(370) & Y(480) coordinate of our hero
playerX = 370
playerY = 480
playerX_change = 0

# Score Keeping
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 128)


# Game over text function
def game_over_text(x, y):
    over_text = font.render(' GAME OVER ', True, (255, 255, 255))
    screen.blit(over_text, (x, y))


def showScore(x, y):
    score = font.render('Score : ' + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))
    controls = font.render('Controls : LEFT, RIGHT & SPACE', True, (255, 255, 255))
    screen.blit(controls, (0, 550))


# Enemy Section
enemy_alien = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemy_alien.append(pygame.image.load('heart.png'))
    enemy_alien[i] = pygame.transform.scale(enemy_alien[i], (32, 32))
    # X & Y coordinate of our enemy
    enemyX.append(random.randint(0, 732))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(random.randint(-5, 5))
    enemyX_change[i] = enemyX_change[i] / 8.0 + 0.25
    enemyY_change.append(25)

# X & Y coordinate of our Bullet
# ready state = bullet ready to be fired & Fire state = moving bullet
bullet_img = pygame.image.load('Girl_punch.jpg')
bullet_img = pygame.transform.scale(bullet_img, (48, 48))
bulletX = 0
bulletY = 480
bulletX_change = 0
bullety_change = 1
bullet_state = 'ready'


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(enemy_variable, x, y):
    screen.blit(enemy_variable, (x, y))
    # NEW ADDITION 2 under reviwe : rectangle
    # draw_rectangle(enemy_variable, x, y , (0,0,255))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 10, y + 5))
    # Addition here Under REVIEW : Rectangle
    # draw_rectangle(bullet_img,x,y)


'''
def draw_rectangle(my_object,X,Y,color=(255,0,0)):
    pygame.draw.rect(screen ,color , [X,Y,32,32 ])
'''


def is_collision(enemyX, enemyY, BulletX, BulletY):
    enemyX += 32
    enemyY += 16
    BulletX += 20
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY, 2)))

    if distance < 30:
        return True

    else:
        return False


'''
BASE FUNCTION 
def is_collision(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY, 2)))
    

    if distance < 20:
        return True

    else:
        return False
'''

# variable
running = True

# Game infinite Loop
while running:
    # RGB  screen
    screen.fill((0, 0, 0))
    # background image
    # screen.blit(background_img , (0,0))
    showScore(textX, textY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keycontrol -> Check if left or right
        # keydown = pressing a key & keyup is viceversa
        if event.type == pygame.KEYDOWN:
            print('A keystoke was pressed baba !')
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
                print('left key was pressed')
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
                print('Right key was pressed')
            if event.key == pygame.K_SPACE:
                print('space pressed')
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print('keystroke released')

    # playerX += 0.1
    playerX += playerX_change
    if playerX < 0 or playerX > 736:
        playerX -= playerX_change

    # Now after the IF Condition we change the player position
    player(playerX, playerY)

    # bullet movement
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bullety_change

    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 432
    # Collision
    for i in range(num_of_enemies):

        # GAME OVER !
        if enemyY[i] > 380:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(220, 300)
            # pygame.mixer.music.stop()
            my_man = pygame.image.load('Man_worried_edited.png')
            my_man = pygame.transform.scale(my_man, (64, 64))
            screen.blit(my_man, (300, 200))

            # game_over_sound = mixer.Sound('Game_over_mixKit.wav')
            # game_over_sound.play()
            break

        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = playerY
            bullet_state = 'ready'
            score_val += 5
            print(score_val)
            enemyX[i] = random.randint(0, 732)
            enemyY[i] = random.randint(50, 150)
            # Collision Sound
            collision_sound = mixer.Sound('Ouch Sound.mp3')
            collision_sound.play()

            # Now lets call the Enemy in main
        if enemyX[i] < 0 or enemyX[i] > 760:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        enemyX[i] += enemyX_change[i]
        enemy(enemy_alien[i], enemyX[i], enemyY[i])

    pygame.display.update()
