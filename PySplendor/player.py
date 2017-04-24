from abc import ABC, abstractmethod
from const import *
from errors import *
import operator


class Player(ABC):

    cards = []
    bonuses = [0] * TOKENS.NUMBER
    tokens = [5] * TOKENS.NUMBER
    visitors = []
    points = 0

    MOVE_PICK_TOKENS = 1
    MOVE_BUY_CARD = 2
    MOVE_BOOK_CARD = 3
    MOVE_BUY_RESERVED_CARD = 4

    @abstractmethod
    def move(self):
        pass

    def calculate_card_price(self, card):
        price_list = []
        for i in range(len(card.price)):
            price = max(0, card.price[i] - self.bonuses[i])
            rest = self.tokens[i] - price
            if rest < 0:
                raise NotEnoughTokensException()
            price_list.append(price)
        return price_list

    def take_tokens(self, tokens):
        for i in range(len(tokens)):
            self.tokens[i] -= tokens[i]

    def put_tokens(self, tokens):
        for i in range(len(tokens)):
            self.tokens[i] += tokens[i]

    def add_card(self, card):
        self.cards.append(card)
        self.bonuses[card.color] += 1
        self.points += card.points