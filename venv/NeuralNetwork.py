import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter
import numpy as np
import SnakeGame as snake

learningRate = 1e-3
goalSteps = 200
scoreRequirement = 50
initialGames = 5000


def generateTrainingData(model):
    global scoreRequirement
    traingData = []
    scores = []
    acceptedScores = []

    for _ in range(initialGames):
        print("Game # ", _, " out of ", str(initial_games))
        score = 0
        gameMemory =[]
        prevousObs = []
        for _ in range(goalSteps):

        if score >= scoreRequirement:
            acceptedScores.append(score)
        print('Average Accepted Score ', mean(acceptedScores))
        print('Score Requirement ', scoreRequirement)
        print('Median score for accepted scores:', median(acceptedScores))
        print(Counter(acceptedScores))

        scores.append(score)
        scoreRequirement = mean(acceptedScores)
        traingDataSave = np.array([traingData, scoreRequirement])
        np.save('TrainingData.npy', traingDataSave)
    return traingData

    traingData = generateTrainingData(None)



