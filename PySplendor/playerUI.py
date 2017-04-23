from player import Player
from game_splendor import GameSplendor
from const import *
from errors import *
import pygame


class PlayerUI(Player):

    game = []
    game_ui = []

    PICKING_TOKENS = 1
    PICKING_DESK_CARD = 2
    PICKING_PLAYER_CARD = 3

    def __init__(self, game, game_ui):
        self.game = game
        self.game_ui = game_ui

    def move(self):
        state = []
        tokens_selected = []
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.game.exit_game()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = self.game_ui.get_rect_from_coord(event.pos)
                print('state %s position %s' % (state, position))
                if not state and position is not None:
                    if position[0] == POSITION.TOKEN:
                        state = PlayerUI.PICKING_TOKENS
                    elif position[0] == POSITION.DESK:
                        state = PlayerUI.PICKING_DESK_CARD
                    elif position[0] == POSITION.PLAYER:
                        state = PlayerUI.PICKING_PLAYER_CARD
                    else:
                        raise NotImplementedError
                if state == PlayerUI.PICKING_TOKENS:
                    if position is None:
                        self.game_ui.discard_dialog()
                        tokens_selected = []
                        state = []
                    elif position == POSITION.DIALOG_OK:
                        self.game_ui.discard_dialog()
                        return [Player.MOVE_PICK_TOKENS, tokens_selected]
                    elif position[0] == POSITION.TOKEN:
                        tokens_selected.append(position[1])
                        successful = False
                        message = ''
                        try:
                            successful = self.game.is_allowed_tokens_selected(self, tokens_selected)
                        except TooManyTokensSelectedException:
                            message = 'You can not select more than 3 tokens'
                        except TwoIdenticalTokensSelectedException:
                            message = 'You can not select 2 identical tokens when selecting 3 tokens'
                        except TwoRareTokensSelectedException:
                            message = 'You can not select 2 identical tokens when it lefts less than 4'
                        except GoldenTokenSelectedException:
                            message = 'You can not pick a Gold token'
                        except TooManyTokensHeldException:
                            message = 'You can not hold more than 10 tokens'
                        if not successful:
                            tokens_selected.pop()
                        self.game_ui.show_token_selection_dialog(tokens_selected, message)
                    else:
                        self.game_ui.discard_dialog()
                        tokens_selected = []
                        state = []
                elif state == PlayerUI.PICKING_DESK_CARD:
                    if position is None:
                        self.game_ui.discard_dialog()
                        state = []
                    elif position == POSITION.DIALOG_OK:
                        self.game_ui.discard_dialog()
                        try:
                            self.calculate_card_price(self.game.desk_cards[position[1]][position[2]])
                        except NotEnoughTokensException:
                            return [Player.MOVE_BOOK_CARD, position[1:]]
                        return [Player.MOVE_BUY_CARD, position[1:]]
                    elif position[0] == POSITION.DESK:
                        message = 'For you it will cost'
                        price = []
                        try:
                            price = self.calculate_card_price(self.game.desk_cards[position[1]][position[2]])
                        except NotEnoughTokensException:
                            message = 'You don''t have enough tokens to pick this card. Book it?'
                        print('price %s' % price)
                        self.game_ui.show_card_selection_dialog(price, message)
                    else:
                        self.game_ui.discard_dialog()
                        state = []
                elif state == PlayerUI.PICKING_PLAYER_CARD:
                    # TODO : work with multiple players
                    pass
