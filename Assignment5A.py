# Class: CSE 1321L
# Section: BJD
# Term: Fall 2024
# Instructor: Tejaswini Karanam
# Name: Zachary Taylor
# Program: Assignment5A.py

#I started this assignment too late and was not able to finish it completely, I apologize.

import pygame, sys, random, json
from pygame.locals import *

#setup pygame window
pygame.init()
clock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Lab 8C Zachary Taylor')
moveSpeed = 5

#make the surface and the rect
surf = pygame.Surface((800, 800))
surf.fill((0, 0, 0))
smallRect = pygame.Rect(380, 380, 40, 40)
pygame.draw.rect(surf, (0, 255, 255), smallRect)
screen.blit(surf, (0, 0))

#make random asteroid function
def makeAsteroid():
    side = random.randint(1, 4)
    sX = random.randint(20, 60)
    sY = sX
    match side:
        case side if side==1: #spawns on the top
            x, y, dX, dY = (random.randint(0, width)), (0), (0), (random.randint(3, 10))
        case side if side==2: #spawns on the right
            x, y, dX, dY = (width - sX), (random.randint(0, height)), (random.randint(-5, -1)), (0)
        case side if side==3: #spawns on the bottom
            x, y, dX, dY = (random.randint(0, width)), (height - sY), (0), (random.randint(-10, -3))
        case side if side==4: #spawns on the left
            x, y, dX, dY = (0), (random.randint(0, height)), (random.randint(1, 5)), (0)
    x, y = ( (width-sX) if x>(width-sX) else x ), ( (height-sY) if y>(height-sY) else y )
    #print(f"side:{side}, sX:{sX}, sY:{sY}, x:{x}, y:{y}, dX:{dX}, dY:{dY}\n")
    return sX, sY, x, y, dX, dY

def reset(score):
    ticker = 0
    ticker2 = 0
    asteroids = {}
    spawnRate = 300
    timer = 0
    collide = False
    counter = 0
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 75)
    gameOverText = font.render(f"Game over! Your score was: {score}", True, pygame.Color('Red'))
    screen.blit(gameOverText, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)
#set all variables used in the loop
ticker = 0
ticker2 = 0
asteroids = {}
asteroidID = 0
spawnRate = 300
run = True
timer = 0
collide = False
counter = 0
while run:
    asteroidRemoval = []
    surf.fill((0, 0, 0))
    playerX, playerY = smallRect.left, smallRect.top
    #keys, movement, and events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit(0) #quit if escape key is pressed
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
    movement = {
        pygame.K_w: (0, -moveSpeed),
        pygame.K_a: (-moveSpeed, 0),
        pygame.K_s: (0, moveSpeed),
        pygame.K_d: (moveSpeed, 0),
    }
    for key, (dirX, dirY) in movement.items():
        if keys[key]:
            new_rect = smallRect.move(dirX, dirY)
            if 0 <= new_rect.x <= width-smallRect.width and 0 <= new_rect.y <= height-smallRect.height:
                smallRect = new_rect
    if ticker == 0: #make an asteroid every so often and change the spawn rate by -0.25 seconds every 5 spawns until it reaches 1 second
        sX, sY, x, y, dX, dY = makeAsteroid()
        asteroidTemp = pygame.Rect(x, y, sX, sY)
        asteroids[asteroidID] = (asteroidTemp, dX, dY)
        asteroidID += 1
        counter += 1 if counter<5 else 0
        if counter == 5:
            spawnRate -= 15 if spawnRate > 60 else 0
            counter = 0
    if ticker2 == 60:
        timer += 1
    for asteroid_id, asteroid in asteroids.items(): #make the rect for the asteroid and add it to "asteroids" dict
        rect, dX, dY = asteroid
        rect = rect.move(dX, dY)
        if pygame.Rect.colliderect(rect, smallRect):
            collide = True
        if not collide:
            asteroids[asteroid_id] = (rect, dX, dY)
            pygame.draw.rect(surf, (169, 169, 169), rect)
            screen.blit(surf, (0, 0))
    for asteroid_id, asteroid in asteroids.items(): #check if any asteroid is out of bounds, and if so, delete it
        rect, dX, dY = asteroid
        if (rect.x + rect.width < 0 or rect.x > width or 
            rect.y + rect.height < 0 or rect.y > height):
            asteroidRemoval.append(asteroid_id)   
    for ID in asteroidRemoval: #delete any asteroids colliding with player after done iterating
        del asteroids[ID]
    #redraw surface
    if not collide:
        pygame.draw.rect(surf, (0, 255, 255), smallRect)
        screen.blit(surf, (0, 0))
    if collide:
        reset(timer)
    pygame.display.flip()
    clock.tick(60)
    ticker +=1 if ticker<spawnRate else -spawnRate
    ticker2 +=1 if ticker2<=60 else -60