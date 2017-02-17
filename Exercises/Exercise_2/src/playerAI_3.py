from random import randint
from BaseAI_3 import BaseAI
from math import inf, log2
import time

class PlayerAI(BaseAI):

    def __init__(self):
        self.timeLimit = 0.095
        self.maxDepth = 2
        self.weightMonotonicity = 1.0
        self.weightEmpty = 1.0
        self.weightMax = 1.0
        self.weightSmooth = 1.0

    def getMove(self, grid):

        startTime = time.clock()
        moves = grid.getAvailableMoves()
        bestScore = -inf
        beta = inf
        bestMove = None
        self.maxDepth = 2
        
        while True:
            for move in moves:
                tmpGrid = grid.clone()
                tmpGrid.move(move)
                v = self.maximize(tmpGrid, bestScore, beta, 1, startTime)

                if v > bestScore:
                    bestScore = v
                    bestMove = move

            self.maxDepth += 2
            #print('MaxDepth: ' + str(self.maxDepth))
            if time.clock() - startTime > self.timeLimit:
                break

        return bestMove
        

    def maximize(self, grid, alpha, beta, depth, sTime):
        moves = grid.getAvailableMoves()
        
        if self.cutoffTest(depth, moves, sTime):
            return self.evalFunction(grid)

        v = -inf
        
        for move in moves:
            tmpGrid = grid.clone()
            tmpGrid.move(move)
            v = max(v, self.minimize(tmpGrid, alpha, beta, depth + 1, sTime))

            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v


    def minimize(self, grid, alpha, beta, depth, sTime):
        
        if self.cutoffTest(depth, [1], sTime):
            return self.evalFunction(grid)

        v = inf

        for i in grid.getAvailableCells():
            tmpGrid = grid.clone()
            tmpGrid.setCellValue(i, getNewTileValue())

            v = min(v, self.maximize(tmpGrid, alpha, beta, depth + 1, sTime))

            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def evalFunction(self, grid):
        a = self.weightEmpty * calcEmpty(grid)
        b = 0#self.weightMax * calcMaxValue(grid)
        c = self.weightMonotonicity * calcMonotonicity(grid)
        d = self.weightSmooth * calcSmoothness(grid)
        #print('Empty: ' + str(a) + ' Max: ' + str(b) + ' Mono: ' + str(c) + ' Smooth: ' + str(d) )
        #print('Monotonicity: ' + str(c))
        return a + b + c + d

    def cutoffTest(self, depth, moves, sTime):
        return time.clock() - sTime > self.timeLimit or \
               depth > self.maxDepth or \
               not moves

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
    return log2(maxVal)

def calcMonotonicity(grid):
    """ measures how monotonic the grid is. This means the values of the tiles
        are strictly increasing or decreasing in both the left/right
        and up/down directions """

    score = 0

    # up-down direction
    for x in range(4):
        for y in range(3):
            curr = log2(grid.map[x][y]) if grid.map[x][y] else 0
            next = log2(grid.map[x][y+1]) if grid.map[x][y+1] else 0
            score += curr - next

    # left-right direction
    for y in range(4):
        for x in range(3):
            curr = log2(grid.map[x][y]) if grid.map[x][y] else 0
            next = log2(grid.map[x+1][y]) if grid.map[x+1][y] else 0
            score += curr - next

    return score


def calcSmoothness(grid):
    """ measures how smooth the grid is (as if the values of the pieces
        were interpreted as elevations). Sums of the pairwise difference
        between neighboring tiles (in log space, so it represents the
        number of merges that need to happen before they can merge). 
        Note that the pieces can be distant """

    smoothness = 0
    tmpGrid = [[0] * (5) for i in range(5)]
    for i in range(4):
        tmpGrid[i][0:4] = grid.map[i][:]
    for x in range(4):
        for y in range(4):
            val = tmpGrid[x][y]
            if val > 0:
                equals = 0
                logVal = log2(val)
                for k in range(x+1,5):
                    if not (tmpGrid[k][y] == 0 or tmpGrid[k][y] == val):
                        break
                    if tmpGrid[k][y] == val:
                        equals += 1

                for k in range(y+1,5):
                    if not (tmpGrid[x][k] == 0 or tmpGrid[x][k] == val):
                        break
                    if tmpGrid[x][k] == val:
                        equals += 1
                
                smoothness += equals * logVal
        

    return smoothness