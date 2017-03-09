#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import GeneticAlgorithm as ga

class Neural_Network(object):
    def __init__(self):
        self.inputLayerSize = 13
        self.outputLayerSize = 2
        self.hiddenLayerSize = 15

        self.W1 = np.random.randn(self.inputLayerSize,self.hiddenLayerSize)
        self.W2 = np.random.randn(self.hiddenLayerSize,self.outputLayerSize)

    def run(self, x):
        z2 = np.dot(x, self.W1)
        a2 = self.tanH(z2)
        z3 = np.dot(a2, self.W2)
        y = self.tanH(z3)
        return y

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def tanH(self, z):
        return (2/(1 + np.exp(-2 * z))) - 1

    def costFunction(self, x, y):
        yPrime = self.run(x)
        cost = 0.5*sum((y-yPrime)**2)
        return cost

    def setWeights(self, weights):
        index = 0

        d1 = len(self.W1)
        d2 = len(self.W1[0])
        arrayList = []
        for i in range(d1):
            arrayList.append(np.array(weights[index:index+d2]))
        self.W1 = np.array(arrayList[0])
        for i in range(1,len(arrayList)):
            if i == 1:
                self.W1 = np.append([self.W1], [arrayList[i]], axis = 0)
            else:
                self.W1 = np.append(self.W1, [arrayList[i]], axis = 0)

        d1 = len(self.W2)
        d2 = len(self.W2[0])
        arrayList = []
        for i in range(d1):
            arrayList.append(np.array(weights[index:index+d2]))
        self.W2 = np.array(arrayList[0])
        for i in range(1,len(arrayList)):
            if i == 1:
                self.W2 = np.append([self.W2], [arrayList[i]], axis = 0)
            else:
                self.W2 = np.append(self.W2, [arrayList[i]], axis = 0)

    def weightAmount(self):
        amount = 0
        amount = amount + (len(self.W1) * len(self.W1[0]))
        amount = amount + (len(self.W2) * len(self.W2[0]))
        return amount
