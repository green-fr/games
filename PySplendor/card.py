from const import *


class Card:
    deck = []
    color = []
    points = []
    price = []

    def __init__(self, card_definition):
        self.price = [0]
        for price in card_definition[0:5]:
            self.price.append(price)
        self.color = card_definition[5]
        self.points = card_definition[6]
        self.deck = card_definition[7] - 1
