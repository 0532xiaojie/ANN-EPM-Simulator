from NeuralNetwork import NeuralNetwork
from GeneticAlgorithm import GA
from Genotype import Genotype

from controller import *
import numpy as np

sensorNum = 8

def calcFitness():
	print "calculating fitness"
	return 0


def fitness(weights):

	sensors = []
	sensorValue = []
	fitness=0
	
	#need to find a way to make sure robot is in correct pos

	print "Fitness"

	timestep = int(dw.getBasicTimeStep())

	for i in range(sensorNum):
		sensors.append(dw.getDistanceSensor('ps'+str(i)))
		sensors[i].enable(timestep)
		sensorValue.append(0)

	dw.enableEncoders(timestep)

	NN.setWeights(weights)

	#While (true) loop
	while (dw.step(timestep)!=-1):
		for i in range(sensorNum):
			sensorValue[i] = sensors[i].getValue()
			
		
		speed = NN.run(np.array(sensorValue))
		
		
		#Check Timer
		print dw.getTime()
		if(dw.getTime() > 300.000):
    			#calculate fitness
    			fitness = calcFitness()
    			break;
    		
    		#Check if any collisions have occured
    		
    		#Check if on the open arm
				

		dw.setSpeed(speed[0]*500, speed[1]*500)
		
		

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
