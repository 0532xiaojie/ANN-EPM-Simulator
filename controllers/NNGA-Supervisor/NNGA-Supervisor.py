"""NNGA-Supervisor controller."""

from GeneticAlgorithm import GA
from Genotype import Genotype

import numpy as np
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
from controller import *

weightNum = 150

def breakCondition():
    return False

def fitnessCalc():
    return 0

def resetPos():
    rpostion.setSFVec3f(start_pos)
    rrotation.setSFRotation(start_rot)

def fitnessFun(weights):
    emitter.send(weights)
    resetPos()
    startTime = sup.getTime()
    currentTime = 0.000
    while (currentTime < 30.000):
        if breakCondition():
            break
        currentTime = sup.getTime() - startTime
    return fitnessCalc()


def main():
    GA.Run()
    while sup.step(timestep) != -1:
        pass

GA = GA(Genotype(weightNum), fitnessFun)
sup = Supervisor()
timestep = sup.getBasicTimeStep()
emitter = sup.getEmitter("emitter")
robot = sup.getFromDef("Robot")
rpostion = robot.getField("translation")
start_pos = rpostion.getSFVec3f()
rrotation = robot.getField("rotation")
start_rot = rrotation.getSFRotation()

main()
