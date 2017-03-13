from NeuralNetwork import NeuralNetwork
from GeneticAlgorithm import GA
from Genotype import Genotype

from controller import *
import numpy as np

sensorNum = 8


def fitness(weights):

	sensors = []
	sensorValue = []

	print "Fitness"

	timestep = int(dw.getBasicTimeStep())

	for i in range(sensorNum):
		sensors.append(dw.getDistanceSensor('ps'+str(i)))
		sensors[i].enable(timestep)
		sensorValue.append(0)

	dw.enableEncoders(timestep)

	NN.setWeights(weights)
	
	#Use manual timing?
	#Start timer

	#While (true) loop
	while (dw.step(timestep) < 100):
		#Check Timer
			#Break?
		print dw.step(timestep)
		for i in range(sensorNum):
			sensorValue[i] = sensors[i].getValue()

		speed = NN.run(np.array(sensorValue))

		dw.setSpeed(speed[0], speed[1])

	return 0

def main():
	GA.Run()

NN = NeuralNetwork()
GA = GA(Genotype(NN.weightNum), fitness)
#robot = Robot()
dw = DifferentialWheels()
print "Running"

main()
