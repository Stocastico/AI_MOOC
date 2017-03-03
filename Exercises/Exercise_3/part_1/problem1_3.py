import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
import time

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
        X = np.concatenate((X, ones), axis = 1)
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
        h = 0.02
        x_min, x_max = X[1:self.numFeatures, 0].min() - 1, X[1:self.numFeatures, 0].max() + 1
        y_min, y_max = X[1:self.numFeatures, 1].min() - 1, X[1:self.numFeatures, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        # Plot the training points
        self.ax.scatter(X[:, 0], X[:, 1], c = y, cmap = plt.cm.Paired)
        # Plot the separation line
        n = np.linalg.norm(self.w)
        ww = self.w / n
        ww1 = [ww[1], -ww[0]]
        ww2 = [-ww[1], ww[0]]
        plt.plot([ww1[0], ww2[0]], [ww1[1], ww2[1]], 'k')
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