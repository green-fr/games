from player import Player
from game_splendor import GameSplendor
from const import *
from errors import *
import pygame


class PlayerUI(Player):

    STATE_BASE = 0
    STATE_CHOOSE_TOKEN = 1
    STATE_CHOOSE_TOKEN_CANCEL = 2
    STATE_CHOOSE_TOKEN_ERROR = 3
    STATE_CHOOSE_TOKEN_OUTPUT = 4
    STATE_CHOOSE_CARD = 11
    STATE_CHOOSE_CARD_CANCEL = 12
    STATE_CHOOSE_CARD_ERROR = 13
    STATE_BUY_CARD_POSSIBLE = 14
    STATE_BOOK_CARD_POSSIBLE = 15
    STATE_OUTPUT = 99

    MESSAGE_OTHER = 0
    MESSAGE_TOKEN = 1
    MESSAGE_DESK = 2
    MESSAGE_OK = 3
    MESSAGE_AUTO = 4

    game = []
    game_ui = []
    state_ui = STATE_BASE
    tokens_selected = [0] * 6

    states = {
                 STATE_BASE: {
                     MESSAGE_TOKEN: STATE_CHOOSE_TOKEN,
                     MESSAGE_OTHER: STATE_BASE,
                     MESSAGE_DESK: STATE_CHOOSE_CARD},
                 STATE_CHOOSE_TOKEN: {
                     MESSAGE_OK: STATE_CHOOSE_TOKEN_OUTPUT,
                     MESSAGE_TOKEN: STATE_CHOOSE_TOKEN,
                     MESSAGE_AUTO: STATE_CHOOSE_TOKEN_ERROR,
                     MESSAGE_OTHER: STATE_CHOOSE_TOKEN_CANCEL},
                 STATE_CHOOSE_TOKEN_ERROR: {MESSAGE_OTHER: STATE_BASE},
                 STATE_CHOOSE_TOKEN_CANCEL: {MESSAGE_AUTO: STATE_BASE},
                 STATE_CHOOSE_CARD: {
                     MESSAGE_AUTO: STATE_BUY_CARD_POSSIBLE,
                     MESSAGE_AUTO: STATE_BOOK_CARD_POSSIBLE,
                     MESSAGE_AUTO: STATE_CHOOSE_CARD_ERROR},
                 STATE_BUY_CARD_POSSIBLE: {
                     MESSAGE_OK: STATE_OUTPUT,
                     MESSAGE_OTHER: STATE_CHOOSE_CARD_CANCEL},
                 STATE_BOOK_CARD_POSSIBLE: {
                     MESSAGE_OK: STATE_OUTPUT,
                     MESSAGE_OTHER: STATE_CHOOSE_CARD_CANCEL},
                 STATE_CHOOSE_CARD_ERROR: {MESSAGE_AUTO: STATE_CHOOSE_CARD_CANCEL},
                 STATE_CHOOSE_CARD_CANCEL: {MESSAGE_AUTO: STATE_BASE}}

    PICKING_TOKENS = 1
    PICKING_DESK_CARD = 2
    PICKING_PLAYER_CARD = 3

    def __init__(self, game, game_ui):
        self.game = game
        self.game_ui = game_ui

    def do_exit(self):
        self.game.exit_game()
        return None

    def decrypt_message(self, position):
        if position is None:
            message = PlayerUI.MESSAGE_OTHER
        elif position == POSITION.DIALOG_OK:
            message = PlayerUI.MESSAGE_OK
        elif position[0] == POSITION.TOKEN:
            message = PlayerUI.MESSAGE_TOKEN
        elif position[0] == POSITION.DESK:
            message = PlayerUI.MESSAGE_DESK
        elif position[0] == POSITION.PLAYER:
            raise NotImplementedError
        else:
            message = PlayerUI.MESSAGE_OTHER
        return message

    def resolve_state(self, message):
        states_tree = self.states[self.state_ui]
        if message in states_tree.keys():
            return states_tree[message]
        else:
            return states_tree[PlayerUI.MESSAGE_OTHER]

    def move(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return self.do_exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = self.game_ui.get_rect_from_coord(event.pos)
                message = self.decrypt_message(position)
                new_state = self.resolve_state(message)
                print('%s -> %s' % (self.state_ui, new_state))
                if new_state == PlayerUI.STATE_CHOOSE_TOKEN:
                    self.choose_token(position)
                elif new_state == PlayerUI.STATE_CHOOSE_TOKEN_CANCEL:
                    self.choose_token_cancel()
                elif new_state == PlayerUI.STATE_CHOOSE_TOKEN_OUTPUT:
                    return self.choose_token_output()
                self.state_ui = new_state

    def choose_token(self, position):
        self.tokens_selected[position[1]] += 1
        error = self.game.is_token_selected_error(self, self.tokens_selected)
        if error == GameSplendor.TOO_MANY_TOKENS_SELECTED:
            message = 'You can not select more than 3 tokens'
        elif error == GameSplendor.TWO_IDENTICAL_TOKENS_SELECTED:
            message = 'You can not select 2 identical tokens when selecting 3 tokens'
        elif error == GameSplendor.TWO_RARE_TOKENS_SELECTED:
            message = 'You can not select 2 identical tokens when it lefts less than 4'
        elif error == GameSplendor.GOLDEN_TOKEN_SELECTED:
            message = 'You can not pick a Gold token'
        elif error == GameSplendor.TOO_MANY_TOKENS_HELD:
            message = 'You can not hold more than 10 tokens'
        else:
            message = ''
        if error:
            self.tokens_selected[position[1]] -= 1
        self.game_ui.show_token_selection_dialog(self.tokens_selected, message)

    def choose_token_cancel(self):
        self.game_ui.discard_dialog()
        self.tokens_selected = [0] * 6
        self.state_ui = PlayerUI.STATE_BASE

    def choose_token_output(self):
        self.game_ui.discard_dialog()
        tokens_selected = self.tokens_selected
        self.tokens_selected = [0] * 6
        self.state_ui = PlayerUI.STATE_BASE
        return [Player.MOVE_PICK_TOKENS, tokens_selected]

    def move_old(self):
        state = []
        tokens_selected = []
        card_selected = []
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.game.exit_game()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = self.game_ui.get_rect_from_coord(event.pos)
                # print('state %s position %s' % (state, position))
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
                        if successful:
                            return [Player.MOVE_PICK_TOKENS, tokens_selected]
                    elif position[0] == POSITION.TOKEN:
                        tokens_selected.append(position[1])
                        successful = False
                        message = ''
                        try:
                            successful = self.game.is_token_selected_error(self, tokens_selected)
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
                        card_selected = []
                        state = []
                    elif position == POSITION.DIALOG_OK:
                        self.game_ui.discard_dialog()
                        try:
                            self.calculate_card_price(self.game.desk_cards[card_selected[0]][card_selected[1]])
                        except NotEnoughTokensException:
                            return [Player.MOVE_BOOK_CARD, card_selected]
                        return [Player.MOVE_BUY_CARD, card_selected]
                    elif position[0] == POSITION.DESK:
                        message = 'For you it will cost'
                        price = []
                        card_selected = position[1:]
                        try:
                            price = self.calculate_card_price(self.game.desk_cards[position[1]][position[2]])
                        except NotEnoughTokensException:
                            message = 'You don''t have enough tokens to pick this card. Book it?'
                        #print('price %s' % price)
                        self.game_ui.show_card_selection_dialog(price, message)
                    else:
                        self.game_ui.discard_dialog()
                        state = []
                elif state == PlayerUI.PICKING_PLAYER_CARD:
                    # TODO : work with multiple players
                    pass
