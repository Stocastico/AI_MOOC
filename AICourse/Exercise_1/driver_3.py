import sys
from solver import Solver

method = sys.argv[1]
initialState = sys.argv[2]

print(sys.argv)

mySolver = Solver(method, initialState)
mySolver.solve()
mySolver.writeResults()