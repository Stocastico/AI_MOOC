import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
import time
from drawLine import newline

class PLA:
    """ Class implementing the Perceptron Learning Algorithm """

    def __init__(self, maxIter = 1000):
        self.max_iter = maxIter
        self.w = []
        self.numFeatures = 0
        self.numSamples = 0
        self.fig, self.ax = plt.subplots()
        plt.ion()
        plt.show()

    def train(self, X, y):
        """ Train the perceptron """
        # perform some initialization
        self.numSamples, self.numFeatures = np.shape(X)
        self.w = np.random.random(self.numFeatures + 1)
        self.weightAsString = np.array_str(self.w) + '\n'
        maxIter = self.numSamples
        # add a column of ones at the end of X
        ones = np.ones((self.numSamples, 1))
        X = np.concatenate((ones, X), axis = 1)
        # check initial accuracy
        classif = np.sign(np.dot(X, self.w))
        correct = np.equal(classif, y)

        #perform actual training
        numIt = 0
        while numIt < maxIter and not np.all(correct):
            numIt += 1
            posPt = np.random.randint(self.numSamples)
            while classif[posPt] == y[posPt]:
                posPt = np.random.randint(self.numSamples)
            # update weights
            tmp = y[posPt] * X[posPt, :]
            self.w = self.w + tmp
            classif = np.sign(np.dot(X, self.w))
            correct = np.equal(classif, y)
            self.weightAsString += np.array_str(self.w) + '\n'
            self.plot(X, y)

        if numIt == maxIter:
            print('Convergence not reached!!!')

    def classify(self, x):
        """ Classify a new sample """
        return np.sign(np.dot(self.w, x))

    def writeOutput(self, outName):
        with open(outName, 'w') as outFile:
            outFile.write(self.weightAsString)

    def plot(self, X, y):
        """ Plot the current status of the Perceptron """
        plt.cla()
        h = 0.02
        x_min, x_max = X[1:self.numFeatures, 1].min() - 1, X[1:self.numFeatures, 1].max() + 1
        y_min, y_max = X[1:self.numFeatures, 2].min() - 1, X[1:self.numFeatures, 2].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        # Plot the training points
        self.ax.scatter(X[:, 1], X[:, 2], c = y, cmap = plt.cm.Paired)
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
    input = np.loadtxt(open(inputFile, 'r'), delimiter=',')
    inputData = input[:, 0:-1]
    inputLabels = input[:,-1]
    pla = PLA()
    pla.train(inputData, inputLabels)
    pla.writeOutput(outputFile)