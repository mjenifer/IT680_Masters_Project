# snake game in python

import pygame, sys, time, random
import os
from pynput.keyboard import Key, Controller
import tflearn
import tensorflow as tf
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tensorflow.keras.callbacks import TensorBoard
from statistics import median, mean
from collections import Counter
import numpy as np

goalSteps = 300
scoreRequirement = 150
initialGames = 100
keyboard = Controller()

# check for initialising error
checkError = pygame.init()
if checkError[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_error[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized")

mainScore = 0
# Play Surface
MAX_WIDTH = 720
MAX_HEIGHT = 460
playSurface = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
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
    Ssurf = sFont.render('Score : {0}'.format(mainScore), True, white)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 150)

    playSurface.blit(Ssurf, Srect)


def ResetGame():
    global changeTo
    global direction
    global foodPos
    global foodSpawn
    global snakeBody
    global snakePos
    global mainScore
    # Important Variables
    snakePos = [100, 200]
    snakeBody = [[100, 50], [90, 50], [80, 50]]  # ,[70,50],[60,50],[50,50],[40,50],[30,50],[20,50]

    foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True
    mainScore = 0
    direction = 'UP'
    changeTo = direction

def RandomInput():
    return random.randrange(0, 3)

def GetObservation():
    xIncrement = 10
    yIncrement = 10
    if direction == 'RIGHT':
        observation = np.array([
            # UP
            Look(0, -yIncrement),
            # Down
            Look(0, yIncrement),
            # Up Right
            Look(xIncrement, -yIncrement),
            # Down Right
            Look(xIncrement, yIncrement),
            # Right
            Look(xIncrement, 0)
        ])
    if direction == 'LEFT':
        observation = np.array([
        # UP
            Look(0, -yIncrement),
            # Down
            Look(0, yIncrement),
            # Up left
            Look(-xIncrement, -yIncrement),
            # Down Left
            Look(-xIncrement, yIncrement),
            # Left
            Look(-xIncrement, 0)
        ])
    if direction == 'UP':
        observation = np.array([
            # UP
            Look(0, -yIncrement),
            # Right
            Look(xIncrement, 0),
            # Up left
            Look(-xIncrement, -yIncrement),
            # Up Right
            Look(xIncrement, -yIncrement),
            # Left
            Look(-xIncrement, 0)
        ])
    if direction == 'DOWN':
        observation = np.array([
            # Down
            Look(0, yIncrement),
            # Right
            Look(xIncrement, 0),
            # Down left
            Look(xIncrement, -yIncrement),
            # Down Right
            Look(xIncrement, yIncrement),
            # Left
            Look(-xIncrement, 0)
        ])
    observation.shape = (15,)
    scale = np.sqrt((MAX_WIDTH ** 2) + (MAX_HEIGHT ** 2))
    observationScaled = 1-2 * observation / scale
    return observationScaled

def Look(xIncrement, yIncrement):
    x = snakePos[0]
    y = snakePos[1]
    foodFound = -1
    bodyFound = -1
    wallFound = -1
    maxDistance = np.sqrt(MAX_WIDTH ** 2 + MAX_HEIGHT ** 2)
    while ((x < MAX_WIDTH + 10) and (y < MAX_HEIGHT + 10)) and ((x > -1) and (y > -1)):
        if x == foodPos[0] and y == foodPos[1]:
            distance = np.sqrt((foodPos[0] - snakePos[0]) ** 2 + (foodPos[1] - snakePos[1]) ** 2)
            if foodFound == -1:
                foodFound = distance
        for bodySeg in snakeBody[1:]:
            if x == bodySeg[0] and y == bodySeg[1]:
                distance = np.sqrt((snakePos[0] - bodySeg[0]) ** 2 + (snakePos[1] - bodySeg[1]) ** 2)
                if bodyFound == -1:
                    bodyFound = distance
        if (x >= MAX_WIDTH) or (y >= MAX_HEIGHT) or (x <= 0) or (y <= 0):
            if direction == "RIGHT":
                distance = np.sqrt((snakePos[0] - MAX_WIDTH) ** 2)
            elif direction == "LEFT":
                distance = np.sqrt((snakePos[0]) ** 2)
            elif direction == "DOWN":
                distance = np.sqrt((snakePos[1] - MAX_WIDTH) ** 2)
            elif direction == "UP":
                distance = np.sqrt((snakePos[1]) ** 2)

            if wallFound == -1:
                #print("direction",direction, "wall Distance ", distance, "snakePos", snakePos, "MaxWidth", MAX_WIDTH, "maxHeight",MAX_HEIGHT)
                wallFound = distance

        x += xIncrement
        y += yIncrement
    if bodyFound == -1:
        #print("Max Body Distance ")
        bodyFound = maxDistance
    if foodFound == -1:
        #print("Max Food distance ")
        foodFound = maxDistance
    return [foodFound, bodyFound, wallFound]


def MainGame(action):
    global changeTo
    global direction
    global foodPos
    global foodSpawn
    global mainScore
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
    #x == 1
    if action == 1:
        changeTo = 'RIGHT'
    #x == 3
    if action == 3:
        changeTo = 'LEFT'
    #x == 0
    if action == 0:
        changeTo = 'UP'
    #x == 2
    if action == 2:
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
        observation = GetObservation()
    if direction == 'LEFT':
        snakePos[0] -= 10
        observation = GetObservation()
    if direction == 'UP':
        snakePos[1] -= 10
        observation = GetObservation()
    if direction == 'DOWN':
        snakePos[1] += 10
        observation = GetObservation()
    # snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        reward += 10
        foodSpawn = False
    else:
        mainScore += 1
        snakeBody.pop()

    if foodSpawn == False:
        foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    foodSpawn = True

    playSurface.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

    # Window Border
    if snakePos[0] > MAX_WIDTH or snakePos[0] < 0:
        lose = True
    if snakePos[1] > MAX_HEIGHT or snakePos[1] < 0:
        lose = True
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            lose = True
    showScore()
    pygame.display.flip()
    fpsController.tick(10)
    return observation, reward, lose, mainScore


def CreateDummyModel(trainingData):
    shapeSecondParameter = len(trainingData[0][0])
    x = np.array([i[0] for i in trainingData])
    X = x.reshape(-1, shapeSecondParameter, 1)
    y = [i[1] for i in trainingData]
    model = CreateNeuralNetworkModel(inputSize=len(X[0]), outputSize=len(y[0]))
    return model

def CreateNeuralNetworkModel(inputSize, outputSize):
    network = input_data(shape=[None, inputSize, 1], name='input')
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, outputSize, activation='softmax')
    network = regression(network, name='targets')
    model = tflearn.DNN(network, tensorboard_dir='tflearn_logs')
    print("Complete create neural network")
    return model

#Generate Training Data by using random inputs
def GenerateTrainingData(model):
    global scoreRequirement
    trainingData = []
    acceptedScores = []
    for _ in range(initialGames):
        print("Game # ", _, " out of ", str(initialGames))
        score = 0
        scores = []
        ResetGame()
        gameMemory = []
        previousObs = []
        for _ in range(goalSteps):

            if len(previousObs) == 0:
                action = RandomInput()
            else:
                if not model:
                    action = RandomInput()
                else:
                    prediction = model.predict(previousObs.reshape(-1, len(previousObs), 1))
                    action = np.argmax(prediction[0])
            observation, reward, done, info = MainGame(action)

            if len(previousObs) > 0:
                gameMemory.append([previousObs, action])
            previousObs = observation
            score += reward
            if done:
                break
        print("Score: ",score, "Score Req: ", scoreRequirement)
        if score >= scoreRequirement:
            acceptedScores.append(score)
            for data in gameMemory:
                actionSample = [0, 0, 0]
                actionSample[data[1]] = 1
                output = actionSample
                trainingData.append([data[0], output])
        scores.append(score)

    print('Average Accepted Score ', mean(acceptedScores))
    print('Score Requirement ', scoreRequirement)
    print('Median score for accepted scores:', median(acceptedScores))
    scoreRequirement = mean(acceptedScores)
    trainingDataSave = np.array([trainingData, scoreRequirement])
    np.save('TrainingData.npy', trainingDataSave)
    return trainingData

#
def TrainModel(trainingData, model=False):
    shapeSecondParameter = len(trainingData[0][0])
    x = np.array([i[0] for i in trainingData])
    X = x.reshape(-1, shapeSecondParameter, 1)
    y = [i[1] for i in trainingData]
    model.fit({'input': X}, {'targets': y}, n_epoch=10, batch_size=16, show_metric=True)
    model.save('SnakeModel.tflearn')
    return model

#Evaluate the generated model
def EvaluateModel(model):
    scores = []
    choices = []
    for _ in range(20):
        score = 0
        gameMemory = []
        previousObs = []
        ResetGame()
        for _ in range(goalSteps):

            if len(previousObs) == 0:
                action = RandomInput()
            else:
                prediction = model.predict(previousObs.reshape(-1, len(previousObs), 1))

                action = np.argmax(prediction[0])
            choices.append(action)
            newObservation, reward, done, info = MainGame(action)

            previousObs = newObservation
            gameMemory.append([newObservation, action])
            score += reward
            if done:
                break
        scores.append(score)
    print('Average Score:', sum(scores) / len(scores))

def main():

    # if os.path.isfile("TrainingData.npy"):
    #     print('File exists, loading previous data!')
    #     trainingData = list(np.load("TrainingData.npy"))
    #     model = CreateDummyModel(trainingData)
    #     model = TrainModel(trainingData, model)
    #     EvaluateModel(model)
    # else:

    #Generate Training Data using random inputs
    trainingData = GenerateTrainingData(None)
    #Build model using parameters within the training data
    model = CreateDummyModel(trainingData)
    #Train the model using the generated dummy model and the training data
    model = TrainModel(trainingData, model)
    #Put the model to the test
    EvaluateModel(model)


main()

#MainGame(None)
#trainingData = GenerateTrainingData(None)
