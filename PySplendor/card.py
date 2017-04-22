from const import *


class Card:
    deck = []
    color = []
    points = []
    price = [0] * TOKENS.NUMBER

    def __init__(self, card_definition):
        self.price = card_definition[0:5]
        self.color = card_definition[5]
        self.points = card_definition[6]
        self.deck = card_definition[7] - 1
