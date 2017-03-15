from NeuralNetwork import NeuralNetwork
from GeneticAlgorithm import GA
from Genotype import Genotype

from controller import *
import numpy as np

sensorNum = 8

def calcFitness(sensors):
	print "calculating fitness"
	for sensor in sensors:
		if sensor > 1:
			return 0
	return 1


def fitness(weights):

	sensors = []
	sensorValue = []
	fitness=0

	print "Fitness"

	timestep = int(dw.getBasicTimeStep())

	for i in range(sensorNum):
		sensors.append(dw.getDistanceSensor('ps'+str(i)))
		sensors[i].enable(timestep)
		sensorValue.append(0)

	dw.enableEncoders(timestep)

	NN.setWeights(weights)

	#reset the epuck

	startTime = dw.getTime()
	while (dw.step(timestep)!=-1):
		for i in range(sensorNum):
			sensorValue[i] = sensors[i].getValue()

		currentTime = dw.getTime() - startTime
		print currentTime

		if(currentTime > 30.000):
			#Timeout
			fitness += calcFitness(sensorValue)
			break;

		speed = NN.run(np.array(sensorValue))
		dw.setSpeed(speed[0]*1000, speed[1]*1000)

	print "Finished That Round"
	return fitness

def main():
	GA.Run()

NN = NeuralNetwork()
GA = GA(Genotype(NN.weightNum), fitness)
#robot = Robot()
dw = DifferentialWheels()
print "Running"

main()
