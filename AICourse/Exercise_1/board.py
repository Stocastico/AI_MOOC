class Board(object):
    """Representation of a 3x3 board"""

    values = []

    def __init__(self, vals):
      self.values = getValuesFromString(self, vals)

    def getValuesFromString(self, str):
      strList = str.split(',')
      self.values = list(map(int, strList))

    def valuesAsString(self):
      out = ''
      for val in self.values:
        out = out + str(val) + ','
      return out[:-1]

    def validMoves(self):
      """Check possible movements of empty square"""
      position = self.values.index(0);
      if 0 == position:
        return ['Down', 'Right']
      elif 1 == position:
        return ['Down', 'Left', 'Right']
      elif 2 == position:
        return ['Down', 'Left']
      elif 3 == position:
        return ['Up', 'Down', 'Right']
      elif 4 == position:
        return ['Up', 'Down', 'Left', 'Right']
      elif 5 == position:
        return ['Up', 'Down', 'Left']
      elif 6 == position:
        return ['Up', 'Right']
      elif 7 == position:
        return ['Up', 'Left', 'Right']
      elif 8 == position:
        return ['Up', 'Left']
      else:
        raise ValueError('position should be a number between 0 and 8')

    def swap(self, direction):
      """Switch position of empty suare with tile indicated by direction """
      positionEmpty = self.values.index(0);
      if 'Up' == direction:
        positionToSwap = positionEmpty - 3
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      elif 'Down' == direction:
        positionToSwap = positionEmpty + 3
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      elif 'Left' == direction:
        positionToSwap = positionEmpty - 1
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      elif 'Right' == direction:
        positionToSwap = positionEmpty + 1
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      else:
        raise ValueError('direction should be one of Up, Down, Left, Right')

    def isEqual(self, test):
      return self.values == test
