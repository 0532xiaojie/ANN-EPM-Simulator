from NeuralNetwork import NeuralNetwork

from controller import *
import numpy as np

sensorNum = 8

def main():
	NN = NeuralNetwork()
	dw = DifferentialWheels()

	sensors = []
	sensorValue = []
	fitness=0

	timestep = int(dw.getBasicTimeStep())
	dw.enableEncoders(timestep)

	for i in range(sensorNum):
		sensors.append(dw.getDistanceSensor('ps'+str(i)))
		sensors[i].enable(timestep)
		sensorValue.append(0)

	receiver = dw.getReceiver("receiver")
	receiver.enable(timestep)

	dw.setSpeed(0.0,0.0)

	while (dw.step(timestep)!=-1):
		if receiver.getQueueLength() != 0:
			NN.setWeights(receiver.getData())

		for i in range(sensorNum):
			sensorValue[i] = sensors[i].getValue()

		speed = NN.run(np.array(sensorValue))
		dw.setSpeed(speed[0]*1000, speed[1]*1000)




main()
