import sys
import pygame
import math 
from pygame import mixer
from pygame.locals import *
import random

pygame.init()
screen = pygame.display.set_mode((800,600))

background=pygame.image.load('images/background2.png')


#music and sound
mixer.music.load("music/space.mp3")
mixer.music.play(-1)


#caption,icon
pygame.display.set_caption("Space Inavder")
icon=pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

#score
score_value=0
font=pygame.font.Font('Lato-Black.ttf',32)

textX=10
textY=10



#player
playerImage=pygame.image.load('images/spaceship_.png')
playerX=370
playerY=480
playerX_change=0

def player(x,y):
    screen.blit(playerImage,(x,y))


#enemy
enemyImage = [
   
]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
total_enemies=10

for i in range(total_enemies):
    enemyImage.append(pygame.image.load('images/enemy0.png'))
    enemyImage.append(pygame.image.load('images/enemy3.png'))
    enemyImage.append(pygame.image.load('images/enemy4.png'))
    enemyImage.append(pygame.image.load('images/enemy5.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(10,350))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x,y,i): #index of list of images
    screen.blit(enemyImage[i],(x,y))
def show_score(x,y):
    score = font.render("Score : "+str(score_value),True,(255,255,255))
    # print("Current Score:", score_value)
    screen.blit(score,(x,y))
#bullet and fire
bulletImage=pygame.image.load('images/bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"


def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImage,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False
    
def game_over():
    game_over_font = pygame.font.Font('ChrustyRock-ORLA.ttf', 64)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (200, 250))
    pygame.display.update()  # Update the display before delay
    pygame.time.delay(5000)  # Pause for 5 seconds
    

def player_enemy_collision(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt(math.pow(playerX - enemyX, 2) + (math.pow(playerY - enemyY, 2)))
    if distance < 23:
        return True
    else:
        return False
    

def set_background():
    global background
    screen.fill((0,0,0))#empty rectangle
    screen.blit(background,(0,0)) # background image

#bullet movement
def bullet_movement():
    global bulletX,bulletY,bullet_state
    if bulletY<=0:
        bulletY=420
        bullet_state="ready"

    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change


#keyboard input

def keyboard_input():
    global running, playerX_change, bulletX, playerX, bulletY
        #keystroke
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound =mixer.Sound("music/laser.wav")
                    bulletSound.play()

                    bulletX=playerX #current x coordinate of spaceship
                    fire_bullet(bulletX,bulletY)
                
        if event.type==pygame.KEYUP:

            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

def enemy_movement():
        #enemy movement
    global enemyX,enemyX_change,enemyY,enemyY_change
    for i in range(total_enemies):
        # move enemy position
        enemyX[i]+=enemyX_change[i]

        # turn around movement if edge is crossed
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
 
        #Enemy Image show
        enemy(enemyX[i], enemyY[i], i)
def show_text(x, y, text):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))
def bullet_collision():
    global total_enemies,enemyX,enemyY,bulletX,bulletY,bullet_state,score_value
    for i in range(total_enemies):
        #collision
            collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
            if collision:
                explosionSound=mixer.Sound("music/explosion.wav")
                explosionSound.play()
                bulletY=480
                bullet_state="ready"
                score_value+=1
                print("Score Updated:", score_value)
                enemyX[i]=random.randint(0,736)  
                enemyY[i]=random.randint(50,150)     
    
                

#game loop
game_over_flag = False
running=True
while running:
    set_background()

    keyboard_input()

    enemy_movement()

    


    bullet_collision()  

    bullet_movement()
    

    if not game_over_flag:
        # Check player-enemy collision only if game over is not flagged
        for i in range(total_enemies):
            collision = player_enemy_collision(playerX, playerY, enemyX[i], enemyY[i])
            if collision:
                game_over()
                game_over_flag = True  # Set the game over flag
            # running = False

        player(playerX, playerY)
    
    # player(playerX,playerY)
    
    
 

    title1 = font.render("SAVE THE SPACE",True,(255, 174, 66))
   
    screen.blit(title1,(300,20))
    show_score(textX,textY)
  
    pygame.display.update()
    FPS = pygame.time.Clock()
    FPS.tick(60)
