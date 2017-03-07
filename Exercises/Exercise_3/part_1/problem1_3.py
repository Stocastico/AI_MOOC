import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
import time
from drawLine import newline

class Perceptron:
    """ Class implementing the Perceptron Learning Algorithm """

    def __init__(self, file):
        input = np.loadtxt(open(inputFile, 'r'), delimiter=',')
        inputData = input[:, 0:-1]
        self.numSamples, self.numFeatures = np.shape(inputData)
        ones = np.ones((self.numSamples, 1))
        self.X = np.concatenate((ones, inputData), axis = 1)
        self.y = input[:,-1]
        self.maxIter = 100# self.numSamples
        self.w = np.zeros(self.numFeatures + 1)
        self.fig, self.ax = plt.subplots()
        plt.ion()
        plt.show()

    def pla(self):
        """ Train the perceptron """
        self.weightAsString = np.array_str(self.w) + '\n'
        # check initial accuracy
        classif = np.sign(self.X.dot(self.w))
        error = self.calcError()

        numIt = 0
        while error > 0 and numIt < self.maxIter:
            for k in range(np.shape(self.X)[0]):
                f_x = self.f(self.X[k, :])
                if self.y[k] * self.f(self.X[k, :]) <= 0:
                    self.w += self.y[k] * self.X[k, :]
                    self.weightAsString += ('{} {} {}\n'.format(self.w[1], self.w[2], self.w[0]))
                    #print('Point # {}, w = {}'.format(k, self.w))
                    self.plot()
            error = self.calcError()
            numIt += 1

        ##perform actual training
        #numIt = 0
        #while numIt < self.maxIter and error > 0:
        #    numIt += 1
        #    posPt = np.random.randint(self.numSamples)
        #    while classif[posPt] == self.y[posPt]:
        #        posPt = np.random.randint(self.numSamples)
        #    # update weights
        #    self.w += self.y[posPt] * self.X[posPt, :]
        #    classif = np.sign(self.X.dot(self.w))
        #    error = self.calcError()
        #    self.weightAsString += np.array_str(self.w) + '\n'
        #    #self.plot()

        if numIt == self.maxIter:
            print('Convergence not reached!!!')

    def f(self, x):
        return np.sign(self.w.dot(x)) 

    def calcError(self):
        numPts = len(self.y)
        nError = 0
        for k in range(numPts):
            val = self.f(self.X[k,:])
            if val != self.y[k]:
                nError += 1
        return nError / numPts


    def classify(self, x):
        """ Classify a new sample """
        return np.sign(np.dot(self.w, x))

    def writeOutput(self, outName):
        with open(outName, 'w') as outFile:
            outFile.write(self.weightAsString)

    def plot(self):
        """ Plot the current status of the Perceptron """
        plt.cla()
        h = 0.02
        #x_min, x_max = X[1:self.numFeatures, 1].min() - 1, X[1:self.numFeatures, 1].max() + 1
        #y_min, y_max = X[1:self.numFeatures, 2].min() - 1, X[1:self.numFeatures, 2].max() + 1
        #xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        # Plot the training points
        self.ax.scatter(self.X[:, 1], self.X[:, 2], c = self.y, cmap = plt.cm.Paired)
        # Plot the separation line
        x0 = 0
        y0 = -self.w[0] / self.w[2]
        x1 = 1
        y1 = -(self.w[1] + self.w[0]) / self.w[2]
        p1 = (x0, y0)
        p2 = (x1, y1)
        newline(p1, p2)
        plt.draw()
        plt.pause(0.5)

if __name__ == '__main__':
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    perc = Perceptron(inputFile)
    perc.pla()
    perc.writeOutput(outputFile)