from abc import ABC, abstractmethod

class UserInput(ABC): 
    @abstractmethod
    def getData(self):
        pass
