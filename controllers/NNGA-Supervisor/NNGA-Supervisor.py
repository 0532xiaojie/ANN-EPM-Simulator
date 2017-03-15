from GeneticAlgorithm import GA
from Genotype import Genotype

import numpy as np
from controller import *
import json
import math

weightNum = 50

def breakCondition():
    current_pos = rpostion.getSFVec3f()
    return current_pos[1] < 1

def fitnessCalc():
    fitness = 0
    current_pos = rpostion.getSFVec3f()
    if (current_pos[2] > 0.1 or current_pos[2] < -0.1):
        fitness -= 1
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
    i = (int)(math.floor(current_pos[0] / 0.05) + 16)
    j = 0
    if current_pos[2] > 0:
        j = 1
    numMap[i][j] += 1
    return numMap

def fitnessFun(weights):
    numMap = []
    prevMap = []
    for i in range(33):
        numMap.append([0,0])
        prevMap.append([0,0])
    fitness = 0

    weightsJSON = json.dumps(weights.tolist())
    emitter.send(weightsJSON)

    resetPos()

    startTime = sup.getTime()
    currentTime = 0.000
    while sup.step(timestep) != -1:
        if currentTime > 30.000:
            break
        if breakCondition():
            return 0
        currentTime = sup.getTime() - startTime
        checkMap(numMap)
        fitness += fitnessCalc()

    minMap = np.inf
    count  = 0
    for i in range(33):
        for j in range(2):
            val = numMap[i][j]
            if val < minMap:
                minMap = val
            if val > 0:
                count += 1
            #fitness += numMap[i][j]
    fitness += (count * 15)
    fitness += (minMap * 1000)

    print "Fitness: ",
    print fitness
    return fitness


def main():
    #ts = sup.getFromDef("touch_sensor")
    #ts.enable(timestep)
    GA.Run()
    while sup.step(timestep) != -1:
        pass

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
