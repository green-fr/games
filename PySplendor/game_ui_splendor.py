import pygame
from game_ui import *
from const import *


class GameUISplendor(GameUI):

    game = []
    screen_surface = []
    background_surface = []
    deck_rect = []
    desk_rect = []
    for i in range(DESK.Y_SIZE):
        desk_rect.append([])
    token_rect = []
    dialog_rect = []
    dialog_ok_rect = []
    label_font = []

    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen_surface = pygame.display.set_mode([SCREEN.WIDTH, SCREEN.HEIGHT])
        self.screen_surface.fill(SCREEN.BG_COLOR)
        self.label_font = pygame.font.SysFont('monospace', 15, True)

    def initial_setup(self):
        self.show_deck_and_desk()
        self.show_tokens()

    def show_players(self):
        # TODO : implement multiple players
        player_rect = pygame.Rect((180, 570), (700, 100))
        pygame.draw.rect(self.screen_surface, UI_COLORS.DIALOG, player_rect)
        y = 610
        x = 300
        for i in range(TOKENS.NUMBER):
            player_token_rectangle = pygame.draw.circle(self.screen_surface, GAME_COLORS.ORDER[i], (x, y), TOKENS.RADIUS)
            label = self.create_label(str(self.game.players[0].tokens[i]))
            # TODO : magic numbers for font size and other elements
            label_rect = pygame.Rect((player_token_rectangle.centerx - 5, player_token_rectangle.centery - 8), (10, 10))
            self.screen_surface.blit(label, label_rect)
            x += 100
        y = 640
        x = 370
        for i in range(1, TOKENS.NUMBER):
            player_bonus_rectangle = pygame.Rect((x, y), (60, 20))
            pygame.draw.rect(self.screen_surface, GAME_COLORS.ORDER[i], player_bonus_rectangle)
            label = self.create_label(str(self.game.players[0].bonuses[i]))
            label_rect = pygame.Rect((player_bonus_rectangle.centerx - 5, player_bonus_rectangle.centery - 8), (10, 10))
            self.screen_surface.blit(label, label_rect)
            x += 100
        label = self.create_label('Score :' + str(self.game.players[0].points))
        label_rect = pygame.Rect((185, player_bonus_rectangle.centery - 50), (10, 10))
        self.screen_surface.blit(label, label_rect)
        pygame.display.flip()

    def show_deck_and_desk(self):
        y = DESK.Y0
        for i in range(DESK.Y_SIZE):
            x = DESK.X0
            deck_rectangle = pygame.Rect((x, y), (CARD.WIDTH, CARD.HEIGHT))
            self.deck_rect.append(deck_rectangle)
            pygame.draw.rect(self.screen_surface, UI_COLORS.DECK, deck_rectangle)
            for j in range(DESK.X_SIZE):
                x += CARD.WIDTH + DESK.X_STEP
                desk_rectangle = pygame.Rect((x, y), (CARD.WIDTH, CARD.HEIGHT))
                self.desk_rect[i].append(desk_rectangle)
                self.show_card(self.game.desk_cards[i][j], desk_rectangle)
            y += CARD.HEIGHT + DESK.Y_STEP
        pygame.display.flip()

    def show_card(self, card, card_rectangle):
        pygame.draw.rect(self.screen_surface, UI_COLORS.CARD, card_rectangle)
        # TODO : magic numbers for font size and other elements
        header_rect = pygame.Rect((card_rectangle.x + 10, card_rectangle.y + 10), (card_rectangle.w - 20, 20))
        pygame.draw.rect(self.screen_surface, GAME_COLORS.ORDER[card.color], header_rect)
        label = self.create_label(str(card.points))
        label_rect = pygame.Rect((header_rect.centerx - 5, header_rect.centery - 8), (10, 10))
        self.screen_surface.blit(label, label_rect)
        for i in range(1, len(card.price)):
            price_rect = pygame.draw.circle(self.screen_surface, GAME_COLORS.ORDER[i], (card_rectangle.x + 18 * i - 6, card_rectangle.y + card_rectangle.h - 12), 8)
            label = self.create_label(str(card.price[i]))
            label_rect = pygame.Rect((price_rect.x + 4, price_rect.y), (10, 10))
            self.screen_surface.blit(label, label_rect)

    def show_tokens(self):
        y = TOKENS.Y0
        x = TOKENS.X0
        for i in range(TOKENS.NUMBER):
            token_rectangle = pygame.draw.circle(self.screen_surface, GAME_COLORS.ORDER[i], (x, y), TOKENS.RADIUS)
            self.token_rect.append(token_rectangle)
            label = self.create_label(str(self.game.deck_tokens[i]))
            # TODO : magic numbers for font size and other elements
            label_rect = pygame.Rect((token_rectangle.centerx - 5, token_rectangle.centery - 8), (10, 10))
            self.screen_surface.blit(label, label_rect)
            x += TOKENS.X_STEP
        pygame.display.flip()

    def show_token_selection_dialog(self, tokens_selected, message):
        # TODO : may be move this method to PlayerUI (if dialog's position is different for different players)
        self.dialog_rect = pygame.Rect((180, 300), (700, 200))
        self.dialog_ok_rect = pygame.Rect((self.dialog_rect.centerx - 10, self.dialog_rect.y + self.dialog_rect.h - 30), (20, 20))
        if not self.background_surface:
            self.background_surface = self.screen_surface.subsurface(self.dialog_rect).copy()
        pygame.draw.rect(self.screen_surface, UI_COLORS.DIALOG, self.dialog_rect)
        pygame.draw.rect(self.screen_surface, UI_COLORS.WHITE, self.dialog_ok_rect, 1)
        label = self.create_label('ok')
        self.screen_surface.blit(label, self.dialog_ok_rect)
        x = self.dialog_rect.x + 100
        y = self.dialog_rect.y + 50
        for i in range(len(tokens_selected)):
            pygame.draw.circle(self.screen_surface, GAME_COLORS.ORDER[tokens_selected[i]], (x, y), TOKENS.RADIUS)
            x += TOKENS.X_STEP
        label = self.create_label(message)
        label_rect = pygame.Rect((self.dialog_rect.x + 100, self.dialog_rect.y + 150), (10, 10))
        self.screen_surface.blit(label, label_rect)
        pygame.display.flip()

    def discard_dialog(self):
        self.screen_surface.subsurface(self.dialog_rect).blit(self.background_surface, (0, 0))
        self.background_surface = []
        pygame.display.flip()

    def show_card_selection_dialog(self, price, message):
        self.dialog_rect = pygame.Rect((180, 300), (700, 200))
        self.dialog_ok_rect = pygame.Rect((self.dialog_rect.centerx - 10, self.dialog_rect.y + self.dialog_rect.h - 30), (20, 20))
        if not self.background_surface:
            self.background_surface = self.screen_surface.subsurface(self.dialog_rect).copy()
        pygame.draw.rect(self.screen_surface, UI_COLORS.DIALOG, self.dialog_rect)
        pygame.draw.rect(self.screen_surface, UI_COLORS.WHITE, self.dialog_ok_rect, 1)
        label = self.create_label('ok')
        self.screen_surface.blit(label, self.dialog_ok_rect)
        x = self.dialog_rect.x + 100
        y = self.dialog_rect.y + 50
        if price is not None:
            for i in range(len(price)):
                token_rectangle = pygame.draw.circle(self.screen_surface, GAME_COLORS.ORDER[i], (x, y), TOKENS.RADIUS)
                label = self.create_label(str(price[i]))
                # TODO : magic numbers for font size and other elements
                label_rect = pygame.Rect((token_rectangle.centerx - 5, token_rectangle.centery - 8), (10, 10))
                self.screen_surface.blit(label, label_rect)
                x += TOKENS.X_STEP
        label = self.create_label(message)
        label_rect = pygame.Rect((self.dialog_rect.x + 100, self.dialog_rect.y + 150), (10, 10))
        self.screen_surface.blit(label, label_rect)
        pygame.display.flip()

    def exit_game(self):
        pygame.quit()

    def get_rect_from_coord(self, coord):
        # Attention : dialog is always on the top of other choices, it must my checked before them
        if self.dialog_ok_rect and self.dialog_ok_rect.collidepoint(coord):
            return POSITION.DIALOG_OK
        for row in range(len(self.desk_rect)):
            for column in range(len(self.desk_rect[row])):
                rect = self.desk_rect[row][column]
                if rect.collidepoint(coord):
                    return POSITION.DESK, row, column
        for column in range(len(self.token_rect)):
            rect = self.token_rect[column]
            if rect.collidepoint(coord):
                return POSITION.TOKEN, column

    def create_label(self, text):
        # TODO : put font settings into the properties
        return self.label_font.render(text, True, UI_COLORS.TEXT)

    def show_winner(self):
        return 0

