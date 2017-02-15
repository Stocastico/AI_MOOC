from random import randint
from BaseAI_3 import BaseAI
from math import inf
import time

timeLimit = 0.1

class PlayerAI(BaseAI):

    def __init__(self):
        children = [] # list of available grid states
        iter = 0

    def getMove(self, grid):

        moves = grid.getAvailableMoves()
        self.iter = 0

        #return moves[randint(0, len(moves) - 1)] if moves else None
        
        if moves:
            return self.maximize(grid, moves, -inf, inf)
        else:
            return None

    def maximize(self, state, moves, alpha, beta):
        """ Find the child state with the highest utility value """
        if self.terminalTest(state):
            return (None, self.eval(state))

        # increase iteration... temp hack before adding time constraint
            self.iter += 1

        (maxChild, maxUtility) = (None, -inf)

        for currMove in moves:
            tempState = state.clone()
            tempState.move(currMove)
            newMoves = tempState.getAvailableMoves()

            (_, utility) = self.minimize(tempState, newMoves, alpha, beta)

            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)

            if maxUtility >= beta:
                break

            if maxUtility > alpha:
                alpha = maxUtility

        return (maxChild, maxUtility)

    def minimize(self, state, moves, alpha, beta):
        """ Find the child state with the highest utility value """
        if self.terminalTest(state):
            return (null, self.eval(state))

        (minChild, minUtility) = (None, inf)

        for currMove in moves:
            tempState = state.clone()
            tempState.move(currMove)
            newMoves = tempState.getAvailableMoves()

            (_, utility) = self.maximize(tempState, newMoves, alpha, beta)

            if utility < minUtility:
                (minChild, minUtility) = (child, utility)

            if minUtility <= alpha:
                break

            if minUtility < beta:
                beta = minUtility

        return (minChild, minUtility)

    def terminalTest(self, state):
        return self.iter >= 3

    def eval(self, state):
        """ Compute value for non-terminal node """
        return self.numEmptyCells(state)

    def numEmptyCells(self, grid):
        emptyCells = 0

        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] == 0:
                    emptyCells += 1

        return emptyCells