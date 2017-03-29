from GeneticAlgorithm import GA
from Genotype import Genotype

import numpy as np
from controller import *
import json
import math

weightNum = 50

def breakCondition():
    current_pos = rpostion.getSFVec3f()
    return (current_pos[0] < -0.05 or current_pos[0] > 0.05) and (current_pos[2] < -0.15 or current_pos[2] > 0.15)

def fitnessCalc():
    fitness = 0
    current_pos = rpostion.getSFVec3f()
    if (current_pos[2] > 0.0363 or current_pos[2] < -0.0363):
        fitness -= 4
        if (current_pos[2] > 0.1 or current_pos[2] < -0.1):
            fitness -= 5
    elif (current_pos[0] > 0.763 or current_pos[2] < -0.763):
        fitness -= 4

    return fitness

def resetPos():
    rpostion.setSFVec3f(start_pos)
    rrotation.setSFRotation(start_rot)
    rpostion.setSFVec3f(start_pos)
    rrotation.setSFRotation(start_rot)

def checkMap(numMap):
    """
    -0.75 < x < 0.75
    0.5 incements
    -0.2 < z < 0.2
    0.2 incements
    """
    current_pos = rpostion.getSFVec3f()
    if (current_pos[2] > 0.1 or current_pos[2] < -0.1):
        return numMap
    if current_pos[1] < 1:
        return numMap
    i = 0
    i = (int)(math.floor(current_pos[0] / 0.05) + 15)
    j = 0
    if current_pos[2] > 0:
        j = 1
    if i < 0 or i > 31 or j < 0 or j > 1:
        return numMap
    numMap[i][j] += 1
    return numMap

def minMap(numMap):
    minVal = np.inf
    for i in range(31):
        for j in range(2):
            val = numMap[i][j]
            if val < minVal:
                minVal = val
    return minVal

def fitnessFun(weights):
    numMap = []
    for i in range(31):
        numMap.append([0,0])
    fitness = 0

    weightsJSON = json.dumps(weights.tolist())
    emitter.send(weightsJSON)

    resetPos()

    startTime = sup.getTime()
    currentTime = 0.000
    while sup.step(timestep) != -1:
        currentTime = sup.getTime() - startTime
        if currentTime > 300.000:
            break
        if breakCondition():
            fitness += -10000
            print "Fitness: ",
            print fitness
            return fitness
        if minMap(numMap) > 0:
            #fitness = 10000 + (3000 - currentTime)
            fitness += 20000 + (30000 - currentTime)
            print "Fitness: ",
            print fitness,
            print "    Completed Maze in ",
            print currentTime,
            print " seconds"
            return fitness
        numMap = checkMap(numMap)
        fitness += fitnessCalc()

    count  = 0
    for i in range(31):
        for j in range(2):
            val = numMap[i][j]
            if val > 0:
                count += 1
    #fitness += (count * 15)
    fitness += (count * 1000)

    print "Fitness: ",
    print fitness
    return fitness


def main():
    f = open('weights', 'w')

    weights =  GA.Run()
    resetPos()
    weightsJSON = json.dumps(weights.tolist())
    f.write(weightsJSON)
    emitter.send(weightsJSON)
    print "Best Weights: ",
    print weights
    #while sup.step(timestep) != -1:
        #pass

GA = GA(Genotype(weightNum), fitnessFun)
sup = Supervisor()
timestep = int(sup.getBasicTimeStep())
emitter = sup.getEmitter("emitter")

robot = sup.getFromDef("Robot")

rpostion = robot.getField("translation")
start_pos = rpostion.getSFVec3f()
rrotation = robot.getField("rotation")
start_rot = rrotation.getSFRotation()

main()
