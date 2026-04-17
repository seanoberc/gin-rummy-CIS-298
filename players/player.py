# `abc` is a Python lib for defining abstract classes:
from abc import ABC, abstractmethod
# from models.hand import Hand

# abstract base class for a Gin Rummy player:
class Player(ABC):

    def __init__(self, name):
        self.name = name
        # self.hand = Hand()
        self.score = 0
