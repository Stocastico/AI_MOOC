import sys
from driver_3 import initialize, solve, outputResult

if __name__ == '__main__':
    # get input
    inputFile = sys.argv[1]
    #get output
    outputFile = sys.argv[2]

    numTest = 0
    numCorrect = 0
    numWrong = 0

    with open(inputFile) as problems, open(outputFile) as solutions:
        for prob, sol in zip(problems, solutions):
            if prob[-1] == '\n':
                prob = prob[:-1]
            if sol[-1] == '\n':
                sol = sol[:-1]
            assert(len(prob) == 81)
            assert(len(sol) == 81)
            numTest += 1
            print('Test #' + str(numTest))
            sudokuStart = initialize(prob)
            sudokuFinish = solve(sudokuStart)
            test = outputResult(sudokuFinish)
            if test == sol:
                numCorrect += 1
            else:
                numWrong += 1

    print('Solved ' + str(numCorrect) + ' sudokus out of ' + str(numTest))

