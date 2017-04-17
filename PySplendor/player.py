from abc import ABC, abstractmethod
from const import *


class Player(ABC):

    cards = []
    tokens = [0] * TOKENS.NUMBER
    visitors = []

    @abstractmethod
    def move(self, game):
        pass
