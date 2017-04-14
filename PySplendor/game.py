import pygame
from const import *


class Game:
    screen = []
    cardsImages = []

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN.WIDTH, SCREEN.HEIGHT])

    def load_cards(self):
        self.cardsImages.append(pygame.image.load('images/carteVerso.png'))
        self.cardsImages.append(pygame.image.load('images/carteRecto.png'))

    def show_desk(self):
        self.screen.fill((0, 250, 0))  # produces a green-color background

    def show_cards(self):
        for i in range(0, DESK.Y_SIZE):
            self.screen.blit(self.cardsImages[0], Game.get_coord_from_index(POSITION.DESK, [i, 0]))
            for j in range(1, DESK.X_SIZE + 1):
                self.screen.blit(self.cardsImages[1], Game.get_coord_from_index(POSITION.DESK, [i, j]))

    @staticmethod
    def get_coord_from_index(position, index):
        if position == POSITION.DESK:
            return [index[1] * (CARD.WIDTH + DESK.X_STEP) + DESK.X0,
                    index[0] * (CARD.HEIGHT + DESK.Y_STEP) + DESK.Y0]
        else:
            return 0

    @staticmethod
    def get_index_from_coord(coord):
        if coord[0] < DESK.X0:
            x_index = -1
        else:
            x_index = (coord[0] - DESK.X0) // (CARD.WIDTH + DESK.X_STEP)
            if x_index > DESK.X_SIZE:
                x_index = -1
            if coord[0] - DESK.X0 - x_index * (CARD.WIDTH + DESK.X_STEP) > CARD.WIDTH:
                x_index = -1
        if coord[1] < DESK.Y0:
            y_index = -1
        else:
            y_index = (coord[1] - DESK.Y0) // (CARD.HEIGHT + DESK.Y_STEP) + 1
            if y_index > DESK.Y_SIZE:
                y_index = -1
            if coord[1] - DESK.Y0 - (y_index - 1) * (CARD.HEIGHT + DESK.Y_STEP) > CARD.HEIGHT:
                y_index = -1
        if x_index == -1 or y_index == -1:
            x_index = -1
            y_index = -1
        return [x_index, y_index]
