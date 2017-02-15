from random import randint
from BaseAI_3 import BaseAI
import time

timeLimit = 0.1

class PlayerAI(BaseAI):

    def getMove(self, grid):

        moves = grid.getAvailableMoves()
        return moves[randint(0, len(moves) - 1)] if moves else None

    def maximize(self, grid):
        pass

    def minimize(self, grid):
        pass