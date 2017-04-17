from game import *
from playerUI import *

game = Game()
game.load_card_surfaces()
game.show_deck_and_desk()
game.show_tokens()
pygame.display.flip()
game.add_player(PlayerUI())
game.play()
