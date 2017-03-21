import sys

def initialize(input):
    """ Initilaize and create sudoku """
    NUM_ROWS = 9
    rows = 'abcdefghi'
    cols = '123456789'
    digits = cols
    return createSudoku(input, rows, cols, digits)

def createSudoku(input, rows, cols, digits):
    """ Take the input string and create a dictionary representing
    the sudoku table from that. Furthermore, create a grid that will
    be used during processing, containing all possible values for each
    square in the grid """
    pos = 0
    keys = cross(rows, cols)
    sudoku = {}
    for c in list(input):
        key = keys[pos]
        val = input[pos]
        if '0' == val:
            sudoku[key] = digits
        else:
            sudoku[key] = val
        pos += 1
    return sudoku

def solve(sudoku):
    """ Solves a sudoku puzzle """
    # apply AC-3 algorithm
    (_, sudoku) = AC3(sudoku)

    # backtracking search
    sudoku = backtrackingSearch(sudoku)

    return sudoku


def sameRow(sudoku, key):
    """Extracts all the keys sharing the same row as key"""
    row = key[0] # row is first char
    cols = '123456789'
    keys = cross(row, cols)
    rowNeighbours = set(keys)
    rowNeighbours.remove(key)
    return rowNeighbours

def sameCol(sudoku, key):
    """Extracts all the key sharing the same column as key"""
    col = key[1] # col is second char
    rows = 'abcdefghi'
    keys = cross(rows, col)
    colNeighbours = set(keys)
    colNeighbours.remove(key)
    return colNeighbours

def sameSquare(sudoku, key):
    """Extracts all the keys sharing the same area as key"""
    row = key[0] # row is first char
    col = key[1] # col is second char
    if row in 'abc':
        rows = 'abc'
    elif row in 'def':
        rows = 'def'
    else:
        rows = 'ghi'
    if col in '123':
        cols = '123'
    elif col in '456':
        cols = '456'
    else:
        cols = '789'
    keys = cross(rows, cols)
    squareNeighbours = set(keys)
    squareNeighbours.remove(key)
    return squareNeighbours

def getConstraints(sudoku, key):
    """ Get all the constraints for a specific key """
    rowConstraints = sameRow(sudoku, key)
    colConstraints = sameCol(sudoku, key)
    squConstraints = sameSquare(sudoku, key)
    constraints = rowConstraints | colConstraints | squConstraints
    return constraints

def backtrackingSearch(sudoku):
    """ Implement backtracking algorithm """
    return backtrack(sudoku)

def backtrack(sudoku):
    """ Recursive backtrack search """
    while True:
        unassigned = getUnassignedSquares(sudoku)
        if not unassigned:
            return sudoku

        for key in unassigned:

            if len(sudoku[key]) == 0:
                print('???')
            for d in sudoku[key]:
                tmp = sudoku.copy()
                tmp[key] = d
                [valid, result] = AC3(tmp)
                #printSudoku(result, 9, 'abcdefghi', '123456789')
                if valid:
                    result = backtrack(result)
                if isComplete(result):
                    return result
                sudoku[key] = sudoku[key].replace(d, '')
            return sudoku


def getUnassignedSquares(sudoku):
    """ create a list of unassigned squares, sorted by number of options"""

    unassigned = list();
    for k, v in sudoku.items():
        if len(v) > 1:
            unassigned.append((k, len(v)))

    if unassigned:
        unassigned.sort(key=lambda tup: tup[1])
        tmp, _ = zip(*unassigned)
    else:
        tmp = list()
    return tmp

def AC3(sudoku):
    """ Implements AC-3 algorithm for sudoku.
    The algorithm makes the CSP arc-consistent """
    # first, create queue
    queue = set()
    for key, val in sudoku.items():
        if len(val) > 1: # don't check values already assigned
            constraints = getConstraints(sudoku, key)
            for c in constraints:
                queue.add((key, c))
    # then iterate over each element in the queue
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(sudoku, Xi, Xj):
            if len(sudoku[Xi]) == 0: # INCONSISTENCY FOUND!
                return (False, sudoku)
            # update queue
            constraints = getConstraints(sudoku, Xi)
            constraints.remove(Xj)
            for Xk in constraints:
                queue.add((Xk, Xi))
    return (True, sudoku)

def revise(sudoku, Xi, Xj):
    revised = False
    digits1 = sudoku[Xi]
    digits2 = sudoku[Xj]
    for d in digits1:
        if d in digits2 and len(digits2) == 1:
            sudoku[Xi] = sudoku[Xi].replace(d, "")
            revised = True
    return revised

def printSudoku(sudoku, numRows, rows, cols):
    """ Print a sudoku as a grid """
    for m in range(numRows):
        for n in range(numRows):
            if n % 3 == 0:
                print('|', end = '')
            row = rows[m]
            col = cols[n]
            key = row+col
            if len(sudoku[key]) > 1:
                print('.', end = '')
            else:
                print(sudoku[key], end = '')
        print('|')
        if m % 3 == 2:
            print(' _ _ _ _ _ _ ')
    print('\n\n')

def outputResult(sudoku):
    res = ''
    rows = 'abcdefghi'
    cols = '123456789'
    keys = cross(rows, cols)
    for k in keys:
        v = sudoku[k]
        if len(v) > 1:
            res = res + '0'
        else:
             res = res + v
    return res

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def isComplete(sudoku):
    for v in sudoku.values():
        if len(v) > 1 or len(v) == 0:
            return False
    return True

if __name__ == '__main__':
    # get input
    inputString = sys.argv[1]

    # initialize
    sudoku = initialize(inputString)

     # show sudoku
    #printSudoku(sudoku, 9, 'abcdefghi', '123456789')

    # solve
    sudoku = solve(sudoku)

    # show sudoku
    #printSudoku(sudoku, 9, 'abcdefghi', '123456789')

    # output results
    print(outputResult(sudoku))

