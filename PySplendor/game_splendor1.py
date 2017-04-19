from const import *
from game import *


class GameSplendor(Game):
    game_ui = []
    players = []
    active = True

    def attach_ui(self, game_ui):
        self.game_ui = game_ui

    def load_card_definitions(self):
        raise NotImplementedError

    def add_player(self, player):
        self.players.append(player)

    def check_end(self):
        if self.active:
            return False
        else:
            return True

    def exit_game(self):
        self.game_ui.exit_game()
        self.active = False

    def play(self):
        while not self.check_end():
            for player in self.players:
                if not self.check_end():
                    player.move(self)
        self.show_winner()