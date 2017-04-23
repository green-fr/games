from game_splendor import GameSplendor
from game_ui_splendor import GameUISplendor
from playerUI import PlayerUI
import pygame

game = GameSplendor()
game_ui = GameUISplendor(game)
game.attach_ui(game_ui)
game.add_players([PlayerUI(game, game_ui)])
game.initial_setup()
game.play()
