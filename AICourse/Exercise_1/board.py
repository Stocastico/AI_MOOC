class Board(object):
    """Representation of a 3x3 board"""

    values = []

    def __init__(self, vals):
      self.values = vals

    def validMoves(self):
      """Check possible movements of empty square"""
      position = self.values.index(0);

      if 0 == position:
        return ['D', 'R']
      elif 1 == position:
        return ['D', 'L', 'R']
      elif 2 == position:
        return ['D', 'L']
      elif 3 == position:
        return ['U', 'D', 'R']
      elif 4 == position:
        return ['U', 'D', 'L', 'R']
      elif 5 == position:
        return ['U', 'D', 'L']
      elif 6 == position:
        return ['U', 'R']
      elif 7 == position:
        return ['U', 'L', 'R']
      elif 8 == position:
        return ['U', 'L']
      else:
        raise ValueError('position should be a number between 0 and 8')

    def swap(self, direction):
      """Switch position of empty suare with tile indicated by direction """
      positionEmpty = self.values.index(0);

      if 'U' == direction:
        positionToSwap = positionEmpty - 3
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      elif 'D' == direction:
        positionToSwap = positionEmpty + 3
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      elif 'L' == direction:
        positionToSwap = positionEmpty - 1
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      elif 'R' == direction:
        positionToSwap = positionEmpty + 1
        self.values[positionEmpty] = self.values[positionToSwap]
        self.values[positionToSwap] = 0
      else:
        raise ValueError('direction should be one of U, D, L, R')
        




  