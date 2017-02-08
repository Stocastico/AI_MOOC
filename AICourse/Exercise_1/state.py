import AbstractState
from board import Board

class State(AbstractState):
    """Implementation of state when solving n-puzzle"""

    board
    parentBoard

    def __init__(self, initialState):
        super(AbstractOperation, self).__init__()
        self.board = Board(initialState)
        self.parentBoard = None

    def neighbours(self):
        """ extract all possible neighbours for this state"""
        possibleMoves = self.board.validMoves()
        nbrs = []

        for move in possibleMoves:
            nbr = Board(self.board.values)
            nbrs.add([nbr.swap(move), move])

        return nbrs

    def testEqual(self, goal):
        return isEqual(self.board, goal)



