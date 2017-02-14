import sys

sys.path.insert(1, 'D:\Code\VisualStudio\Python\AICourse\AICourse\Exercise_1') 

from solver import Solver

method = sys.argv[1]
initialState = sys.argv[2]

print(sys.argv)

mySolver = Solver(method, initialState)
mySolver.solve()
mySolver.writeResults()