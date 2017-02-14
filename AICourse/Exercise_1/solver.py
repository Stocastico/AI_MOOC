from collections import deque
from node import Node
from board import Board
from time import process_time

class Solver(object):
    """Solves a puzzle using one of the following methods:
       BFS --> Breadth First Search
       DFS --> Depth First Search
       AST --> A-star search
       IDA --> Ida-star search
    """

    def __init__(self, method, initialState):
        self.method = method  # method used to solve puzzle
        self.state = Node(initialState) # instance of State class
        self.tree = self.state # tree starting from initial configuration
        if self.method == 'bfs':
            self.frontier = deque([self.state], None)
        else:
            self.frontier = [self.state] # list of states to be explored
        self.explored = set() # list of states already explored
        self.goal = Node(list(range(len(initialState.split(',')))))
        self.pathToGoal = [] # something like ['Up', 'Left', 'Left']
        self.costOfPath = 0
        self.nodesExpanded = 0
        self.fringeSize = 1
        self.maxFringeSize = 0
        self.searchDepth = 0
        self.maxSearchDepth = 0
        self.runningTime = 0.0
        self.maxRamUsage = 0.0
        self.start = process_time()

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
        
        self.runningTime = process_time() - self.start
        self.maxRamUsage = 0; #resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    def bfs(self):

        while len(self.frontier) > 0:
            self.state = self.frontier.popleft()
            print("Current State: " + str(self.state.board.values))
            self.fringeSize -= 1
            self.explored.add(str(self.state.board.values))

            if self.state.testEqual(self.goal):
                self.searchDepth = self.state.depth
                self.costOfPath = self.state.depth
                self.pathToGoal = self.getPathToGoal()
                return True

            for neighbour in self.state.neighbours():
                #if not neighbour.belongs(self.frontier) and not neighbour.belongs(self.explored):
                if str(neighbour.board.values) not in self.explored:
                    self.frontier.append(neighbour)
                    self.explored.add(str(neighbour.board.values))
                    self.fringeSize += 1
                    if neighbour.depth > self.maxSearchDepth:
                        self.maxSearchDepth = neighbour.depth

            self.nodesExpanded += 1

            if self.fringeSize > self.maxFringeSize:
                self.maxFringeSize = self.fringeSize

    def dfs(self):
        while len(self.frontier) > 0:
            self.state = self.frontier.pop()
            #print("Current State:\n" + str(self.state))
            self.fringeSize -= 1
            self.explored.add(str(self.state.board.values))

            if self.state.testEqual(self.goal):
                self.searchDepth = self.state.depth
                self.costOfPath = self.state.depth
                self.pathToGoal = self.getPathToGoal()
                return True

            neighbours = reversed(self.state.neighbours())

            for neighbour in neighbours:
                #if not neighbour.belongs(self.frontier) and not neighbour.belongs(self.explored):
                if str(neighbour.board.values) not in self.explored:
                    self.frontier.append(neighbour)
                    self.explored.add(str(neighbour.board.values))
                    self.fringeSize += 1
                    if neighbour.depth > self.maxSearchDepth:
                        self.maxSearchDepth = neighbour.depth

            self.nodesExpanded += 1

            if self.fringeSize > self.maxFringeSize:
                self.maxFringeSize = self.fringeSize

    def ast(self):
        pass

    def ida(self):
        pass

    def writeResults(self):
        f = open('output.txt', 'w')
        s = "path_to_goal: " + str(self.pathToGoal) + "\n"
        s += "cost_of_path: " + str(self.costOfPath) + "\n"
        s += "nodes_expanded: " + str(self.nodesExpanded) + "\n"
        s += "fringe_size: " + str(self.fringeSize) + "\n"
        s += "max_fringe_size: " + str(self.maxFringeSize) + "\n"
        s += "search_depth: " + str(self.searchDepth) + "\n"
        s += "max_search_depth: " + str(self.maxSearchDepth) + "\n"
        s += "running_time: " + str(self.runningTime) + "\n"
        s += "max_ram_usage: " + str(self.maxRamUsage)
        f.write(s)
        f.close()

    def getPathToGoal(self):
        cState = self.state
        path = []
        while cState.action is not None:
            path.append(cState.action)
            cState = cState.parent
        return path[::-1]















