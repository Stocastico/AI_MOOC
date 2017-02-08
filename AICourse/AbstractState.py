from abc import ABC, abstractmethod

class AbstractState(ABC):
    """generic class representing a state when searching"""

    def __init__(self):
      super(AbstractOperation, self).__init__()

    @abstractmethod
    def goalTest(self, goalState):
      """check if state correspond to our goal"""
      pass

    @abstractmethod
    def neighbours(self):
      """extract all neighbours of the state"""
      pass


