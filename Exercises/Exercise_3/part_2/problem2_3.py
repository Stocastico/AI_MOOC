from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

class LinearRegression:
    """ Class implementing Linear Regression """
    pass

    def __init__(self, learning_rate = 0.01):
        # Open file
        input = np.loadtxt(open(inputFile, 'r'), delimiter=',')
        # Set features
        inputData = input[:, 0:-1]
        self.numSamples, self.numFeatures = np.shape(inputData)
        ones = np.ones((self.numSamples, 1))
        self.X = np.concatenate((ones, inputData), axis = 1)
        # Set labels
        self.y = input[:,-1]
        #set weights
        self.w = np.zeros(self.numFeatures + 1)
        # Set learning rate
        self.alpha = learning_rate
        # Set number of iterations
        self.maxIter = 100
        # Define figure
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

    def normalize(self):
        means = np.mean(self.X[:, 1:], axis = 1)
        stddevs = np.std(self.X[:, 1:], axis = 1)
        X[:, 1:] = (X[:, 1:] - means[:, np.newaxis] ) / stddevs

    def train(self):
        self.iter = 0
        while self.iter < self.maxIter:
            self.iter += 1
            # Shuffle the samples and labels
            order = np.random.permutation(self.numSamples)
            Xp = self.X[order, :]
            yp = self.y[order]
            # Update weights
            for k in range(self.numSamples):
                self.w -= self.alpha * self.gradientError(Xp[k, :], yp[k])

            # Compute error
            error = self.calcCost()
            print('Error = {}'.format(error))
            # Show plot
            self.plot()

    def writeOutput(self):
        with open(outName, 'w') as outFile:
            outFile.write('{},{},{},{},{}\n'.format(self.alpha, self.iter, self.w[1], self.w[2], self.w[0]))

    def calcCost(self):
        c = 0
        for k in range(self.numSamples):
            c += (self.f(X[k,:]) - self.y[k]) ** 2
        return c / (2*self.numSamples)

    def plot(self):
        self.ax.scatter(self.X[:, 1], self.X[:, 2], self.y, c='r', marker='o')

        self.ax.set_xlabel('Age (norm.)')
        self.ax.set_ylabel('Weight (norm.)')
        self.ax.set_zlabel('Height')

    def f(self, x):
        return x.dot(self.w)


if __name__ == '__main__':
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    lr = LinearRegression(inputFile)
    lr.normalize()
    lr.train()
    lr.writeOutput(outputFile)