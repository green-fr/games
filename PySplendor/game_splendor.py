from card import *
from const import *
from game import *
from numpy import genfromtxt
import random


class GameSplendor(Game):
    game_ui = []
    players = []
    active = True
    deck_cards = []
    for i in range(DESK.Y_SIZE):
        deck_cards.append([])
    deck_tokens = []

    def __init__(self):
        self.load_card_definitions()

    def load_card_definitions(self):
        cards_data = genfromtxt('resources/Cards.csv', delimiter=';')
        cards_data = cards_data[1:, :] # Skip first (headers) line
        for card_definition in cards_data:
            card = Card(card_definition.astype(int)) # Converting to int, as card definition is read as numpy.float
            self.deck_cards[card.deck].append(card)
        
    def attach_ui(self, game_ui):
        self.game_ui = game_ui

    def add_player(self, player):
        self.players.append(player)

    def initial_setup(self):
        # TODO : adjust initial setup depending on the number of players
        self.deck_tokens = [5, 7, 7, 7, 7, 7]
        for deck in self.deck_cards:
            random.shuffle(deck)
            for i in range(DESK.X_SIZE):
                card = deck.pop()
                print(card.price)

    def check_end(self):
        if self.active:
            return False
        else:
            return True

    def get_winner(self):
        return 1

    def exit_game(self):
        self.game_ui.exit_game()
        self.active = False

    def play(self):
        if self.game_ui:
            self.game_ui.show()
        while not self.check_end():
            for player in self.players:
                if not self.check_end():
                    player.move()
        print(self.get_winner())
        self.game_ui.show_winner()