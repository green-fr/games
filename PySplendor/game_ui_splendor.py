import pygame
from game_ui import *
from const import *


class GameUISplendor(GameUI):

    game = []
    screen = []
    deck_rectangle = []
    deck_surfaces = []
    desk_rectangle = []
    desk_surfaces = []
    for i in range(DESK.Y_SIZE):
        desk_rectangle.append([])
        desk_surfaces.append([])
    token_rectangle = []

    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN.WIDTH, SCREEN.HEIGHT])
        self.screen.fill(SCREEN.BG_COLOR)

    def show(self):
        self.show_deck_and_desk()
        self.show_tokens()
        pygame.display.flip()

    def show_deck_and_desk(self):
        y = DESK.Y0
        for i in range(DESK.Y_SIZE):
            x = DESK.X0
            deck_rectangle = pygame.Rect((x, y), (CARD.WIDTH, CARD.HEIGHT))
            self.deck_rectangle.append(deck_rectangle)
            pygame.draw.rect(self.screen, COLORS.DECK, deck_rectangle)
            for j in range(DESK.X_SIZE):
                x += CARD.WIDTH + DESK.X_STEP
                desk_rectangle = pygame.Rect((x, y), (CARD.WIDTH, CARD.HEIGHT))
                self.desk_rectangle[i].append(desk_rectangle)
                pygame.draw.rect(self.screen, COLORS.CARD, desk_rectangle)
            y += CARD.HEIGHT + DESK.Y_STEP

    def show_tokens(self):
        myfont = pygame.font.SysFont('monospace', 15)
        y = TOKENS.Y0
        x = TOKENS.X0
        for i in range(TOKENS.NUMBER):
            token_rectangle = pygame.draw.circle(self.screen, COLORS.ORDER[i], (x, y), TOKENS.RADIUS)
            self.token_rectangle.append(token_rectangle)
            label = myfont.render(str(self.game.deck_tokens[i]), 1, (255, 255, 0))
            self.screen.blit(label, token_rectangle)
            x += TOKENS.X_STEP

    def exit_game(self):
        pygame.quit()

    @staticmethod
    def get_coord_from_index(position, index):
        if position == POSITION.STACK:
            return [DESK.X0,
                    index * (CARD.HEIGHT + DESK.Y_STEP) + DESK.Y0]
        if position == POSITION.DESK:
            return [index[1] * (CARD.WIDTH + DESK.X_STEP) + DESK.X0,
                    index[0] * (CARD.HEIGHT + DESK.Y_STEP) + DESK.Y0]
        else:
            return 0

    def get_rect_from_coord(self, coord):
        for row in range(len(self.desk_rectangle)):
            for column in range(len(self.desk_rectangle[row])):
                rect = self.desk_rectangle[row][column]
                if rect.collidepoint(coord):
                    return POSITION.DESK, row, column
        for column in range(len(self.token_rectangle)):
            rect = self.token_rectangle[column]
            if rect.collidepoint(coord):
                return POSITION.TOKEN, column

    def show_winner(self):
        return 0

