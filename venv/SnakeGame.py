# snake game in python

import pygame, sys, time, random
import os
from pynput.keyboard import Key, Controller

keyboard = Controller()

# check for initialising error
check_error = pygame.init()
if check_error[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_error[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized")


x = 0
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
# Play Surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake Game ----:>')
#time.sleep(5)

# Colors
red = pygame.Color(255, 0, 0)#gameOver
green = pygame.Color(0, 255, 0)#Snake
black = pygame.Color(0, 0,0)#Score
white = pygame.Color(255, 255,255)#background
brown = pygame.Color(162, 42, 42)#food
gray = pygame.Color(112, 128, 144)#food

# FPS Controller
fpsController = pygame.time.Clock()

# Important Variables
snakePos = [100,200]
snakeBody = [[100,50],[90,50],[80,50]] #,[70,50],[60,50],[50,50],[40,50],[30,50],[20,50]

foodPos = [random.randrange(1,72)*10, random.randrange(1,46)*10]
foodSpawn = True

direction = 'UP'
changeTo = direction
score = 0


def reset_variables():

    global changeTo
    global direction
    global foodPos
    global foodSpawn
    global score
    global snakeBody
    global snakePos

    # Important Variables
    snakePos = [100, 200]
    snakeBody = [[100, 50], [90, 50], [80, 50]]  # ,[70,50],[60,50],[50,50],[40,50],[30,50],[20,50]

    foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True

    direction = 'UP'
    changeTo = direction
    score = 0

#Game Over Function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360,15)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# score function
def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 24)
    Ssurf = sFont.render('Score : {0}'.format(score), True, white)
    Srect = Ssurf.get_rect()
    if choice ==1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 150)

    playSurface.blit(Ssurf, Srect)

def reset_game():
    print("Game Reset")
    reset_variables()

def ranom_input():
    x = random.randrange(1, 4)
    if x == 1:
        keyboard.press('w')
        keyboard.release('w')
    elif x == 2:
        keyboard.press('d')
        keyboard.release('d')
    elif x == 3:
        keyboard.press('s')
        keyboard.release('s')
    else:
        keyboard.press('a')
        keyboard.release('a')

def main_game():
    global changeTo
    global direction
    global foodPos
    global foodSpawn
    global score


    #Main Logic Of Game
    while True:
        #ranom_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reset_game()
            elif event.type == pygame.KEYDOWN:
                #x == 2
                if event.key == keyboard.press('d') or event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('D Pressed')
                    changeTo = 'RIGHT'
                #x == 4
                if event.key == keyboard.press('a') or event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('A Pressed')
                    changeTo = 'LEFT'
                #x == 1
                if event.key == keyboard.press('w') or event.key == pygame.K_UP or event.key == ord('w'):
                    print('W Pressed')
                    changeTo = 'UP'
                #x == 3
                if event.key == keyboard.press('s') or event.key == pygame.K_DOWN or event.key == ord('s'):
                    print('S Pressed')
                    changeTo = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Validation of direction
        if changeTo == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'
        if changeTo == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if changeTo == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if changeTo == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'

        if direction == 'RIGHT':
            snakePos[0] += 10
        if direction == 'LEFT':
            snakePos[0] -= 10
        if direction == 'UP':
            snakePos[1] -= 10
        if direction == 'DOWN':
            snakePos[1] += 10

        # snake body mechanism
        snakeBody.insert(0, list(snakePos))
        if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
            score += 10
            foodSpawn = False
        else:
            snakeBody.pop()

        if foodSpawn == False:
            foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        foodSpawn = True

        playSurface.fill(black)
        for pos in snakeBody:
            pygame.draw.rect(playSurface,green,pygame.Rect(pos[0], pos[1],10,10))

        pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

        #Window Border
        if snakePos[0] > 710 or snakePos[0] < 0:
            reset_game()
        if snakePos[1] > 450 or snakePos[1] < 0:
            reset_game()

        for block in snakeBody[1:]:
            if snakePos[0] == block[0] and snakePos[1] == block[1]:
                reset_game()

        showScore()
        pygame.display.flip()
        fpsController.tick(10)

main_game()
