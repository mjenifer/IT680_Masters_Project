# snake game in python

import pygame, sys, time, random
import os
from pynput.keyboard import Key, Controller
import tflearn
import tensorflow as tf
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter
import numpy as np

learning_rate = 1e-3
goalSteps = 300
scoreRequirement = 50
initialGames = 1000
n_iterations = 1000

n_inputs = 4
n_hidden = 4
n_outputs = 4

keyboard = Controller()

# check for initialising error
check_error = pygame.init()
if check_error[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_error[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized")

score = 0
x = 0
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
# Play Surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake Game ----:>')
# time.sleep(5)

# Colors
red = pygame.Color(255, 0, 0)  # gameOver
green = pygame.Color(0, 255, 0)  # Snake
black = pygame.Color(0, 0, 0)  # Score
white = pygame.Color(255, 255, 255)  # background
brown = pygame.Color(162, 42, 42)  # food
gray = pygame.Color(112, 128, 144)  # food

# FPS Controller
fpsController = pygame.time.Clock()

# Important Variables
snakePos = [100, 100]
snakeBody = [[100, 50], [90, 50], [80, 50]]  # ,[70,50],[60,50],[50,50],[40,50],[30,50],[20,50]

foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
foodSpawn = True

direction = 'UP'
changeTo = direction
score = 0


def reset_variables():
    global changeTo
    global direction
    global foodPos
    global foodSpawn
    global snakeBody
    global snakePos

    # Important Variables
    snakePos = [100, 200]
    snakeBody = [[100, 50], [90, 50], [80, 50]]  # ,[70,50],[60,50],[50,50],[40,50],[30,50],[20,50]

    foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True

    direction = 'UP'
    changeTo = direction


# Game Over Function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 15)
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
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 150)

    playSurface.blit(Ssurf, Srect)


def reset_game():
    print("Game Reset")
    reset_variables()


def random_input():
    return random.randrange(1, 5)

    # if x == 1:
    #     keyboard.press('w')
    #     keyboard.release('w')
    # elif x == 2:
    #     keyboard.press('d')
    #     keyboard.release('d')
    # elif x == 3:
    #     keyboard.press('s')
    #     keyboard.release('s')
    # else:
    #     keyboard.press('a')
    #     keyboard.release('a')


def random_games():
    goalSteps = 300
    print('in random games')
    for _ in range(2):
        reset_game()
        for _ in range(goalSteps):
            action = random_input()
            observation, score, reward, done = main_game(action)
            look(snakePos[0], snakePos[1])
            if done:
                print('Observation: ', observation, 'Score: ', score, ' reward: ', reward, ' done: ', done)
                break

    return


def getObservation(snakePost):
    xIncrement = 10
    yIncrement = 10
    if direction == 'RIGHT':
        observation = np.array([
            # UP
            look(snakePos[0], snakePos[1], 0, -yIncrement),
            # Down
            look(snakePos[0], snakePos[1], 0, yIncrement),
            # Up Right
            look(snakePos[0], snakePos[1], xIncrement, -yIncrement),
            # Down Right
            look(snakePos[0], snakePos[1], xIncrement, yIncrement),
            # Right
            look(snakePos[0], snakePos[1], xIncrement, 0)
        ])


        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1]), (snakePos[0] + offSet,snakePos[1]-viewDistance))
        # #Down
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0] + offSet,snakePos[1]+viewDistance + offSet))
        # #UP Right
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0]+viewDistance + offSet,snakePos[1]-viewDistance - offSet))
        # #Down Right
        # pygame.draw.line(playSurface, green, (snakePos[0],snakePos[1]), (snakePos[0]+viewDistance,snakePos[1]+viewDistance))
        # #Right
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0]+viewDistance,snakePos[1] + offSet))
    if direction == 'LEFT':
        observation = np.array([
        # UP
            look(snakePos[0], snakePos[1], 0, -yIncrement),
            # Down
            look(snakePos[0], snakePos[1], 0, yIncrement),
            # Up left
            look(snakePos[0], snakePos[1], -xIncrement, -yIncrement),
            # Down Left
            look(snakePos[0], snakePos[1], -xIncrement, yIncrement),
            # Left
            look(snakePos[0], snakePos[1], -xIncrement, 0)
        ])


        # #UP
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1]), (snakePos[0] + offSet,snakePos[1]-viewDistance))
        # #Left
        # pygame.draw.line(playSurface, green, (snakePos[0],snakePos[1] + offSet), (snakePos[0]-viewDistance,snakePos[1] + offSet))
        # #Down Left
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0]-viewDistance + offSet,snakePos[1]+viewDistance + offSet))
        # #Up Left
        # pygame.draw.line(playSurface, green, (snakePos[0],snakePos[1]), (snakePos[0]-viewDistance,snakePos[1]-viewDistance))
        # #Down
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0] + offSet,snakePos[1]+viewDistance + offSet))
    if direction == 'UP':
        observation = np.array([
            # UP
            look(snakePos[0], snakePos[1], 0, -yIncrement),
            # Right
            look(snakePos[0], snakePos[1], xIncrement, 0),
            # Up left
            look(snakePos[0], snakePos[1], -xIncrement, -yIncrement),
            # Up Right
            look(snakePos[0], snakePos[1], xIncrement, -yIncrement),
            # Left
            look(snakePos[0], snakePos[1], -xIncrement, 0)
        ])
        #  #UP
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1]), (snakePos[0] + offSet,snakePos[1]-viewDistance))
        # #Left
        # pygame.draw.line(playSurface, green, (snakePos[0], snakePos[1] + offSet), (snakePos[0]-viewDistance,snakePos[1] + offSet))
        # #UP Right
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0]+viewDistance +offSet,snakePos[1]- viewDistance - offSet))
        # #Up Left
        # pygame.draw.line(playSurface, green, (snakePos[0],snakePos[1]), (snakePos[0]-viewDistance,snakePos[1]-viewDistance))
        # #Right
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0]+viewDistance +offSet,snakePos[1] + offSet))
    if direction == 'DOWN':
        observation = np.array([
            # Down
            look(snakePos[0], snakePos[1], 0, yIncrement),
            # Right
            look(snakePos[0], snakePos[1], xIncrement, 0),
            # Down left
            look(snakePos[0], snakePos[1], xIncrement, -yIncrement),
            # Down Right
            look(snakePos[0], snakePos[1], xIncrement, yIncrement),
            # Left
            look(snakePos[0], snakePos[1], -xIncrement, 0)
        ])
        # #Down
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1]), (snakePos[0] + offSet,snakePos[1]+viewDistance))
        # #Left
        # pygame.draw.line(playSurface, green, (snakePos[0],snakePos[1] + offSet), (snakePos[0]-viewDistance,snakePos[1] + offSet))
        # #Down Right
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet * 2,snakePos[1]+ offSet * 2), (snakePos[0]+viewDistance+ offSet * 2,snakePos[1]+viewDistance+ offSet * 2))
        # #Down Left
        # pygame.draw.line(playSurface, green, (snakePos[0],snakePos[1] + offSet * 2), (snakePos[0]-viewDistance,snakePos[1]+viewDistance + offSet * 2))
        # #Right
        # pygame.draw.line(playSurface, green, (snakePos[0] + offSet,snakePos[1] + offSet), (snakePos[0]+viewDistance +offSet,snakePos[1] + offSet))
    observation.shape = (15,)
    return observation

def look(snakePosX, snakePosY, xIncrement, yIncrement):
    x = snakePosX
    y = snakePosY
    isFoodFound = 0
    isBodyFound = 0
    isWallFound = 0
    if (x > 720) or (y > 460) or (x < 0) or (y < 0):
        isWallFound = 1
    else:
        x += xIncrement
        y += yIncrement
        if snakePosX == foodPos[0] and snakePosY == foodPos[1]:
            isFoodFound = 1
        for bodySeg in snakeBody[1:]:
            if snakePosX == bodySeg[0] and snakePosY == bodySeg[1]:
                isBodyFound = 1

        else:
            look(x, y, xIncrement, yIncrement)
    return [isFoodFound, isBodyFound, isWallFound]


def main_game(action):
    global changeTo
    global direction
    global foodPos
    global foodSpawn
    global score
    lose = False
    reward = 1
    observation = []
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_RIGHT or event.key == ord('d'):
    #                 changeTo = 'RIGHT'
    #             if event.key == pygame.K_LEFT or event.key == ord('a'):
    #                 changeTo = 'LEFT'
    #             if event.key == pygame.K_UP or event.key == ord('w'):
    #                 changeTo = 'UP'
    #             if event.key == pygame.K_DOWN or event.key == ord('s'):
    #                 changeTo = 'DOWN'

    #Main Logic Of Game
    #x == 2
    if action == 2:
        changeTo = 'RIGHT'
    #x == 4
    if action == 4:
        changeTo = 'LEFT'
    #x == 1
    if action == 1:
        changeTo = 'UP'
    #x == 3
    if action == 3:
        changeTo = 'DOWN'

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
        reward += 10
        foodSpawn = False
    else:
        score += 1
        snakeBody.pop()

    if foodSpawn == False:
        foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True

    playSurface.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))
    observation = getObservation(snakePos)
    # Window Border
    if snakePos[0] > 710 or snakePos[0] < 0:
        lose = True
    if snakePos[1] > 450 or snakePos[1] < 0:
        lose = True
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            lose = True
    showScore()
    pygame.display.flip()
    fpsController.tick(10)
    return observation, reward, lose, score


def create_dummy_model(training_data):
    shape_second_parameter = len(training_data[0][0])
    x = np.array([i[0] for i in training_data])
    X = x.reshape(-1, shape_second_parameter, 1)
    y = [i[1] for i in training_data]
    model = create_neural_network_model(input_size=len(X[0]), output_size=len(y[0]))
    return model


def generateTrainingData(model):
    global scoreRequirement
    trainingData = []
    scores = []
    acceptedScores = []

    for _ in range(initialGames):
        print("Game # ", _, " out of ", str(initialGames))
        score = 0
        scores =[]

        reset_game()
        for _ in range(goalSteps):
            gameMemory = []
            previousObs = []
            if len(previousObs) == 0:
                action = random_input()
            else:
                if not model:
                    action = random_input()
                else:
                    prediction = model.predict(previousObs.reshape(-1, len(previousObs), 1))
                    action = np.argmax(prediction[0])

            observation, reward, done, info = main_game(action)
            if len(previousObs) > 0:
                gameMemory.append([previousObs, action])
            previousObs = observation
            score += reward
            if done:
                break
        print("Score: ",score, "Score Req: ", scoreRequirement)
        if score >= scoreRequirement:
            acceptedScores.append(score)
            print('Accepted Scores', acceptedScores)
            for data in gameMemory:
                print('Game Memory ', gameMemory)
                actionSample = [0, 0, 0]
                actionSample[data[1]] = 1
                output = actionSample
                trainingData.append([data[0], output])
                print('training data ', trainingData)
            scores.append(score)

    print('Average Accepted Score ', mean(acceptedScores))
    print('Score Requirement ', scoreRequirement)
    print('Median score for accepted scores:', median(acceptedScores))

    scoreRequirement = mean(acceptedScores)
    traingDataSave = np.array([trainingData, scoreRequirement])
    np.save('TrainingData.npy', traingDataSave)
    return trainingData



# drawEyes(snakePos)

# random_games()
trainingData = generateTrainingData(None)
# print('TraingData ', trainingData)
# print(create_dummy_model(trainingData))


# trainingData = generateTrainingData(None)


# Try creating observation method to check if snake is in vicinity of food, wall or self
