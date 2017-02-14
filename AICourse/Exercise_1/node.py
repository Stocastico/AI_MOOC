from AbstractNode import AbstractNode
from board import Board

class Node(AbstractNode):
    """Implementation of node when solving n-puzzle"""

    def __init__(self, state, parent = None, action = None, path_cost = 0, goal = None):
        super(AbstractNode, self).__init__()
        self.board = Board(state)   # board configuration
        self.parent = parent        # Parent node
        self.action = action        # What brought us to this state
        self.path_cost = path_cost  # g in the lecture
        if goal == None:
            self.heuristics = 0
        else:
            self.heuristics = self.board.manhattanDist(goal)
        self.depth = 0              # depth of this node
        if parent:
            self.depth = parent.depth + 1

    def neighbours(self):
        """ extract all possible neighbours for this state"""
        possibleMoves = self.board.validMoves()
        nbrs = []
        cbr = self.board

        for move in possibleMoves:
            newConfig = cbr.swap(move)
            neigh = Node(newConfig, self, move, 1)
            nbrs.append(neigh)

        return nbrs

    def belongs(self, listOfNodes):
        for node in listOfNodes:
            if self.testEqual(node):
                return True
        return False

    def testEqual(self, goal):
        return self.board.isEqual(goal.board.values)

    def __str__(self):
        v = self.board.values
        string = '-------\n' + \
                 '|' + str(v[0]) + '|' + str(v[1]) + '|' + str(v[2]) + '|\n' + \
                 '-------\n' + \
                 '|' + str(v[3]) + '|' + str(v[4]) + '|' + str(v[5]) + '|\n' + \
                 '_______\n' + \
                 '|' + str(v[6]) + '|' + str(v[7]) + '|' + str(v[8]) + '|\n' + \
                 '-------'
        return string

    def __lt__(self, other):
        return (self.path_cost + self.heuristics) < (other.path_cost + other.heuristics)
