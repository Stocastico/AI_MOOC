import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def doSVM(X_train, X_test, y_train, y_test, outputFile):
    # Linear
    print('------ Linear SVM -------')
    tuned_parameters_linear = {'kernel': ['linear'],
                               'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
    clf1 = GridSearchCV(SVC(), tuned_parameters_linear, cv = 5)   
    clf1.fit(X_train, y_train)
    print(clf1.best_params_)
    bestScore = clf1.best_score_
    testScore = clf1.score(X_test, y_test)
    writeData(outputFile, 'svm_linear', bestScore, testScore)
    # Polynomial
    print('------ Polynomial SVM -------')
    tuned_parameters_poly = {'kernel': ['poly'],
                             'C': [0.1, 1, 3], 
                             'degree': [4, 5, 6],
                             'gamma': [0.1, 1]}
    clf2 = GridSearchCV(SVC(), tuned_parameters_poly, cv = 5, n_jobs = 8)   
    clf2.fit(X_train, y_train)
    print(clf2.best_params_)
    bestScore = clf2.best_score_
    testScore = clf2.score(X_test, y_test)
    writeData(outputFile, 'svm_polynomial', bestScore, testScore)
    # RBF
    print('------ RBF SVM -------')
    tuned_parameters_rbf = {'kernel': ['rbf'],
                            'C': [0.1, 0.5, 1, 5, 10, 50, 100], 
                            'gamma': [0.1, 0.5, 1, 3, 6, 10]}
    clf3 = GridSearchCV(SVC(), tuned_parameters_rbf, cv = 5)   
    clf3.fit(X_train, y_train)
    print(clf3.best_params_)
    bestScore = clf3.best_score_
    testScore = clf3.score(X_test, y_test)
    writeData(outputFile, 'svm_rbf', bestScore, testScore)

def doLogisticRegression(X_train, X_test, y_train, y_test, outputFile):
    print('------ Logistic Regression -------')
    tuned_parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
    clf = GridSearchCV(LogisticRegression(), tuned_parameters, cv = 5)   
    clf.fit(X_train, y_train)
    print(clf.best_params_)
    bestScore = clf.best_score_
    testScore = clf.score(X_test, y_test)
    writeData(outputFile, 'logistic', bestScore, testScore)

def doKNN(X_train, X_test, y_train, y_test, outputFile):
    print('------ KNN ------')
    tuned_parameters = {'n_neighbors': range(1, 51), 
                        'leaf_size': range(5, 61, 5)}
    clf = GridSearchCV(KNeighborsClassifier(), tuned_parameters, cv = 5)   
    clf.fit(X_train, y_train)
    print(clf.best_params_)
    bestScore = clf.best_score_
    testScore = clf.score(X_test, y_test)
    writeData(outputFile, 'knn', bestScore, testScore)

def doDecisionTree(X_train, X_test, y_train, y_test, outputFile):
    print('------ Decision tree ------')
    tuned_parameters = {'max_depth': range(1, 51), 
                        'min_samples_split ': range(1, 11)}
    clf = GridSearchCV(DecisionTreeClassifier(), tuned_parameters, cv = 5)   
    clf.fit(X_train, y_train)
    print(clf.best_params_)
    bestScore = clf.best_score_
    testScore = clf.score(X_test, y_test)
    writeData(outputFile, 'decision_tree', bestScore, testScore)

def doRandomForest(X_train, X_test, y_train, y_test, outputFile):
    print('------ Random forest ------')
    tuned_parameters = {'max_depth': range(1, 51), 
                        'min_samples_split ': range(1, 11)}
    clf = GridSearchCV(RandomForestClassifier(), tuned_parameters, cv = 5)   
    clf.fit(X_train, y_train)
    print(clf.best_params_)
    bestScore = clf.best_score_
    testScore = clf.score(X_test, y_test)
    writeData(outputFile, 'random_forest', bestScore, testScore)

def writeData(outName, method, trainScore, testScore):
    with open(outName, 'a') as outFile:
        outFile.write('{},{},{}\n'.format(method, trainScore, testScore))

if __name__ == '__main__':
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    # Read data
    input = np.loadtxt(open(inputFile, 'r'), delimiter=',', skiprows = 1)
    y = input[:, -1]
    X = input[:, 0:-1]
    # Split into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y, train_size = 0.6)

    # SVM
    doSVM(X_train, X_test, y_train, y_test, outputFile)

    # Logistic regression
    doLogisticRegression(X_train, X_test, y_train, y_test, outputFile)

    # KNN
    doKNN(X_train, X_test, y_train, y_test, outputFile)

    # Decision Trees
    doDecisionTree(X_train, X_test, y_train, y_test, outputFile)

    # Random forests
    doRandomForest(X_train, X_test, y_train, y_test, outputFile)