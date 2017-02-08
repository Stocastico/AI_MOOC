from collections import deque
from state import State

class Solver(object):
    """Solves a puzzle using one of the following methods:
       BFS --> Breadth First Search
       DFS --> Depth First Search
       AST --> A-star search
       IDA --> Ida-star search
    """

    method # method used to solve puzzle
    state # instance of State class
    goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8] # state representing the solution
    frontier # list of states to be explored
    explored # list of states already explored
    pathToGoal = [] # something like ['Up', 'Left', 'Left']
    costOfPath = 0
    nodesExpanded = 0
    fringeSize = 0
    maxFringeSize = 0
    searchDepth = 0
    maxSearchDepth = 0
    runningTime = 0.0
    maxRamUsage = 0.0

    def __init__(self, method, intialState):
        self.method = method
        self.state = State(initialState)

    def solve(self):
        """Main method for solving puzzle"""

        if self.method == 'bfs':
          retVal = self.bfs()
        elif self.method == 'dfs':
          retVal = self.dfs()
        elif self.method == 'ast':
          retVal = self.ast()
        elif self.method == 'ida':
          retVal = self.ida()
        else:
          raise ValueError('Possible methods are dfs, bfs, ast, ida')

        if not retVal:
          raise RuntimeError('Solver didn\'t reach final state')

    def bfs(self):
        self.frontier = deque([])
        self.frontier.append([self.state, ''])
        self.fringeSize += 1
        self.explored = set()

        while not self.frontier.empty():
            currState = self.frontier.popLeft()
            self.fringeSize -= 1
            self.explored.add(currState)

            if self.state.testEqual(self.goalState):
                return True

            for [neighbour, direction] in currState.neighbours():
                if neighbour not in self.frontier and neighbour not in self.explored:
                    self.frontier.append(neighbour)
                    self.fringeSize += 1

            if self.fringeSize > self.maxFringeSize:
                self.maxFringeSize = self.fringeSize






