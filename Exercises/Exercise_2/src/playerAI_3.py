from random import randint
from BaseAI_3 import BaseAI
import time

score_map = {0:0,
             2:1,
             4:2,
             8:3,
             16:4,
             32:5,
             64:6,
             128:7,
             256:8,
             512:9,
             1024:10,
             2048:100,
             4096:1000,
             8192:10000,
             16384:100000}
possMoves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
biggerGrid = [[0] * (5) for i in range(5)]

class PlayerAI(BaseAI):

    def __init__(self):
        #self.timeLimit = 0.095
        self.timeLimit = 0.5
        self.infinity = float('Inf')
        self.maxDepth = 2
        self.weightMonotonicity = 5
        self.weightEmpty = 3
        self.weightMax = 5
        self.weightSmooth = 10
        self.startTime = 0.0
        self.gridWeights = [[ 6,  5,  4,  1],
                            [ 5,  4,  1,  0],
                            [ 4,  1,  0, -1],
                            [ 1,  0, -1, -2]]

    def getMove(self, grid):

        self.startTime = time.clock()
        moves = grid.getAvailableMoves()
        bestScore = -self.infinity
        alpha = -self.infinity
        beta = self.infinity
        bestMove = None
        self.maxDepth = 2
        chosenMoves = []
        
        while True:
            _, v, move = self.maximize(grid, alpha, beta, 1)

            if v > bestScore:
                bestScore = v
                bestMove = move
                    
            #print('Move chosen at depth : ' + str(self.maxDepth) + ' = ' + possMoves[bestMove] + ' - Utility = ' + str(bestScore))
            self.maxDepth += 2
            chosenMoves.append((bestMove, bestScore))
            bestScore = -self.infinity
            #print('MaxDepth: ' + str(self.maxDepth))
            if time.clock() - self.startTime > self.timeLimit:
                break

        if chosenMoves[-1][1] > chosenMoves[-2][1]:
            return chosenMoves[-1][0]
        else:
            return chosenMoves[-2][0]
        

    def maximize(self, grid, alpha, beta, depth):
        if self.cutoffTest(depth):
            return (None, self.evalFunction(grid), None)

        maxVal = -self.infinity
        maxChild = None
        maxMove = None

        for mv in grid.getAvailableMoves():
            child = grid.clone()
            child.move(mv)
            _, val, _ = self.minimize(child, alpha, beta, depth + 1)
            if val > maxVal:
                maxVal = val
                maxChild = child
                maxMove = mv
            #print('In maximize, value: ' + str(val) + ' current beta: ' + str(beta))
            if maxVal >= beta:
                return (maxChild, maxVal, maxMove)
            if maxVal > alpha:
               alpha = maxVal
        return (maxChild, maxVal, maxMove)


    def minimize(self, grid, alpha, beta, depth):
        
        if self.cutoffTest(depth):
            return (None, self.evalFunction(grid), None)

        minVal = self.infinity
        minChild = None

        for i in grid.getAvailableCells():
            child = grid.clone()
            child.setCellValue(i, getNewTileValue())

            _, val, _ = self.maximize(child, alpha, beta, depth + 1)
            if val < minVal:
                minChild = child
                minVal = val
            #print('In minimize, value: ' + str(val) + ' current alpha: ' + str(alpha))
            if val <= alpha:
                return (minChild, minVal, None)
            if minVal < beta:
                beta = minVal
        return (minChild, minVal, None)

    def evalFunction(self, grid):
        #a = self.weightEmpty * calcEmpty(grid)
        return self.calcWeightValue(grid)
        #c = self.weightMonotonicity * calcMonotonicity(grid)
        #d = self.weightSmooth * calcSmoothness(grid)
        #print('Gradient: ' + str(b) + ' Mono: ' + str(c) + ' Smooth: ' + str(d) )
        #print('Monotonicity: ' + str(c))
        #return a + b + c + d


    def cutoffTest(self, depth):
        return time.clock() - self.startTime > self.timeLimit or \
               depth > self.maxDepth

    def calcWeightValue(self, grid):
        val = 0
        for x in range(grid.size):
            for y in range(grid.size):
                val += grid.map[x][y] * self.gridWeights[x][y]
        return val

# List of utility functions
def getNewTileValue():
    if randint(0,99) < 90:
        return 2
    else:
        return 4;


def calcEmpty(grid):
    emptyCells = 0

    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] == 0:
                emptyCells += 1
    return emptyCells


def calcMaxValue(grid):
    maxVal = 0

    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] > maxVal:
                maxVal = grid.map[x][y]
    return score_map[maxVal]

def calcMonotonicity(grid):
    score = 0

    for x in range(4):
        for y in range(3):
            b = [score_map[grid.map[x][y]], score_map[grid.map[x][y+1]]]
            score += min(0, b[0] - b[1])

    for y in range(4):
        for x in range(3):
            b = [score_map[grid.map[x][y]], score_map[grid.map[x+1][y]]]
            score += min(0, b[0] - b[1])

    return score

def calcSmoothness(grid):
    """ measures how smooth the grid is (as if the values of the pieces
        were interpreted as elevations). Sums of the pairwise difference
        between neighboring tiles (in log space, so it represents the
        number of merges that need to happen before they can merge). 
        Note that the pieces can be distant """

    smoothness = 0
    #tmpGrid = [[0] * (5) for i in range(5)]
    for i in range(4):
        biggerGrid[i][0:4] = grid.map[i][:]
    for x in range(4):
        for y in range(4):
            val = biggerGrid[x][y]
            if val > 0:
                if biggerGrid[x+1][y] == val:
                    smoothness += 1
                if biggerGrid[x][y+1] == val:
                    smoothness += 1
                
    return smoothness