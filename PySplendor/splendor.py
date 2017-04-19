from game_splendor1 import *
from game_ui_splendor import *
from playerUI import *

game = GameSplendor()
game_ui = GameUISplendor()
game.attach_ui(game_ui)

game.load_card_surfaces()
game.show_deck_and_desk()
game.show_tokens()
pygame.display.flip()
game.add_player(PlayerUI())
game.play()
