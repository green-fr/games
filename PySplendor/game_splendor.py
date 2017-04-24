from card import *
from const import *
from errors import *
from game import *
import numpy
import random
from player import Player


class GameSplendor(Game):
    game_ui = []
    players = []
    active = True
    deck_cards = []
    for i in range(DESK.Y_SIZE):
        deck_cards.append([])
    desk_cards = []
    for i in range(DESK.Y_SIZE):
        desk_cards.append([])
    deck_tokens = []

    def __init__(self):
        self.load_card_definitions()

    def load_card_definitions(self):
        cards_data = numpy.genfromtxt('resources/Cards.csv', delimiter=';')
        cards_data = cards_data[1:, :] # Skip first (headers) line
        for card_definition in cards_data:
            card = Card(card_definition.astype(int)) # Converting to int, as card definition is read as numpy.float
            self.deck_cards[card.deck].append(card)
        
    def attach_ui(self, game_ui):
        self.game_ui = game_ui

    def add_players(self, players):
        self.players.extend(players)
        self.game_ui.show_players()

    def initial_setup(self):
        # TODO : adjust initial setup depending on the number of players
        self.deck_tokens = [5, 7, 7, 7, 7, 7]
        for i in range(len(self.deck_cards)):
            deck = self.deck_cards[i]
            random.shuffle(deck)
            for j in range(DESK.X_SIZE):
                card = deck.pop()
                self.desk_cards[i].append(card)
        self.game_ui.initial_setup()

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
        while not self.check_end():
            for player in self.players:
                if not self.check_end():
                    move = player.move()
                    print(move)
                    if move is not None:
                        if move[0] == Player.MOVE_PICK_TOKENS:
                            if self.is_allowed_tokens_selected(player, move[1]):
                                self.take_tokens(move[1])
                                self.game_ui.show_tokens()
                                player.put_tokens(move[1])
                                self.game_ui.show_players()
                        elif move[0] == Player.MOVE_BUY_CARD:
                            card = self.desk_cards[move[1][0]][move[1][1]]
                            price = player.calculate_card_price(card)
                            player.take_tokens(price)
                            self.put_tokens(price)
                            self.replace_desk_card(move[1])
                            player.add_card(card)
                            self.game_ui.show_players()
                            self.game_ui.show_tokens()
                            self.game_ui.show_deck_and_desk()
                        elif move[0] == Player.MOVE_BOOK_CARD:
                            pass
                        else:
                            print(move)
                            raise NotImplementedError
        print('And the winner is the player #%s' % self.get_winner())
        self.game_ui.show_winner()

    def is_allowed_tokens_selected(self, player, tokens_selected):
        if len(tokens_selected) > 3:
            raise TooManyTokensSelectedException()
        if len(numpy.unique(tokens_selected)) != len(tokens_selected):
            if len(tokens_selected) >= 3:
                raise TwoIdenticalTokensSelectedException()
            if self.deck_tokens[tokens_selected[0]] < 4:
                raise TwoRareTokensSelectedException()
        if 0 in tokens_selected:
            raise GoldenTokenSelectedException()
        if sum(player.tokens) + len(tokens_selected) > 10:
            raise TooManyTokensHeldException()
        return True

    def take_tokens(self, tokens):
        for i in range(len(tokens)):
            self.deck_tokens[i] -= tokens[i]

    def put_tokens(self, tokens):
        for i in range(len(tokens)):
            self.deck_tokens[i] += tokens[i]

    def replace_desk_card(self, position):
        deck = position[0]
        new_card = self.deck_cards[deck].pop()
        self.desk_cards[deck][position[1]] = new_card
