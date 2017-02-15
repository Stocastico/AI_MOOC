import math

def getValuesFromString(str):
    strList = str.split(',')
    return list(map(int, strList))

class Board(object):
    """Representation of a N x N board"""

    def __init__(self, vals):
        if isinstance(vals, str):
            listStrVal = vals.split(',')
            self.values = [int(i) for i in listStrVal]
        else:
            self.values = vals
        self.N = round(math.sqrt(len(self.values)))

    def valuesAsString(self):
        out = ''
        for val in self.values:
            out = out + str(val) + ','
        return out[:-1]

    def manhattanDist(self, goal = None):
        totDist = 0
        if goal == None:
            goal = list(range(self.N*self.N))
        for pos, val in enumerate(self.values):
            posGoal = goal.index(val)
            colGoal = posGoal % self.N
            rowGoal = posGoal // self.N

            colSelf = pos % self.N
            rowSelf = pos // self.N
            totDist += abs(colGoal - colSelf) + abs(rowGoal - rowSelf)
        return totDist

    def validMoves(self):
        """Check possible movements of empty square"""
        position = self.values.index(0); # 0 represents the empty square
        # first the four corners
        if 0 == position:
            return ['Down', 'Right']
        elif (self.N - 1) == position:
            return ['Down', 'Left']
        elif (self.N ** 2 - self.N) == position:
            return ['Up', 'Right']
        elif (self.N ** 2 - 1) == position:
            return ['Up', 'Left']
        # then the borders
        elif position < self.N - 1:
            return ['Down', 'Left', 'Right']
        elif position > (self.N ** 2 - self.N):
            return ['Up', 'Left', 'Right']
        elif 0 == position % self.N:
            return ['Up', 'Down', 'Right']
        elif self.N-1 == position % self.N:
             return ['Up', 'Down', 'Left']
        # inside points
        else:
            return ['Up', 'Down', 'Left', 'Right']

    def swap(self, direction):
      """Switch position of empty suare with tile indicated by direction """
      positionEmpty = self.values.index(0);
      newState = list(self.values)
      if 'Up' == direction:
          positionToSwap = positionEmpty - 3
          newState[positionEmpty] = self.values[positionToSwap]
          newState[positionToSwap] = 0
      elif 'Down' == direction:
          positionToSwap = positionEmpty + 3
          newState[positionEmpty] = self.values[positionToSwap]
          newState[positionToSwap] = 0
      elif 'Left' == direction:
          positionToSwap = positionEmpty - 1
          newState[positionEmpty] = self.values[positionToSwap]
          newState[positionToSwap] = 0
      elif 'Right' == direction:
          positionToSwap = positionEmpty + 1
          newState[positionEmpty] = self.values[positionToSwap]
          newState[positionToSwap] = 0
      else:
          raise ValueError('direction should be one of Up, Down, Left, Right')

      return newState

    def isEqual(self, test):
        return self.values == test
