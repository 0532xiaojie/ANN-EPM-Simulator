from controller import *
"""
from controller import DistanceSensor
from controller import Receiver
from controller import Robot
from controller import DifferentialWheels
from controller import Accelerometer
from controller import Camera
"""

SensorNum = 8

sensors[SensorNum]
sensorValue[SensorNum]
speed[2]

NN = NeuralNetwork()
GA = GA(Genotype(SensorNum), fitness)

def fitness(weights):
	robot = Robot()

	timestep = int(robot.getBasicTimeStep())

	for i in range(SensorNum):
		sensors[i] = robot.getDistanceSensor('ps'+str(i))
		sensors[i].enable(timestep)

	DifferentialWheels.enableEncoders(timestep)

	NN.setWeights(weights)

	while (robot.step(timestep) != -1):
		for i in range(SensorNum):
			sensorValue[i] = sensors[i].getValue()

		speed = NN.run(sensorValue)

		DifferentialWheels.setSpeed(speed[0], speed[1])

def main():
	GA.run()
