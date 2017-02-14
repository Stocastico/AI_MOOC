from abc import ABC, abstractmethod

class AbstractNode(ABC):
    """generic class representing a state when searching"""

    def __init__(self):
      super(AbstractNode, self).__init__()

    @abstractmethod
    def testEqual(self, goalState):
      """check if state correspond to our goal"""
      pass

    @abstractmethod
    def neighbours(self):
      """extract all neighbours of the state"""
      pass


