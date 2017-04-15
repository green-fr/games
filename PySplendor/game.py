import pygame
from const import *


class Game:
    screen = []
    card_surfaces = []
    deck_rectangle = []
    desk_rectangle = []
    for i in range(DESK.Y_SIZE):
        desk_rectangle.append([])
    token_rectangle = []

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN.WIDTH, SCREEN.HEIGHT])
        self.screen.fill(SCREEN.BG_COLOR)

    def load_cards(self):
        self.card_surfaces.append(pygame.image.load('images/carteVerso.png'))
        self.card_surfaces.append(pygame.image.load('images/carteRecto.png'))

    def show_deck_and_desk(self):
        y = DESK.Y0
        for i in range(DESK.Y_SIZE):
            x = DESK.X0
            self.deck_rectangle.append(pygame.Rect((x, y), (CARD.WIDTH, CARD.HEIGHT)))
            self.screen.blit(self.card_surfaces[0], self.deck_rectangle[i])
            for j in range(DESK.X_SIZE):
                x += CARD.WIDTH + DESK.X_STEP
                self.desk_rectangle[i].append(pygame.Rect((x, y), (CARD.WIDTH, CARD.HEIGHT)))
                self.screen.blit(self.card_surfaces[1], self.desk_rectangle[i][j])
            y += CARD.HEIGHT + DESK.Y_STEP

    def show_tokens(self):
        y = TOKENS.Y0
        x = TOKENS.X0
        for i in range(TOKENS.NUMBER):
            self.token_rectangle.append(pygame.draw.circle(self.screen, COLORS.ORDER[i], (x, y), TOKENS.RADIUS))
            x += TOKENS.X_STEP

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
                    return row, column
