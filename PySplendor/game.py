import pygame
import const
from collections import namedtuple

class Game:

    screen = []
    cardsImages = []

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([const.SCREEN.WIDTH, const.SCREEN.HEIGHT])
        
    def loadCards(self):
        self.cardsImages.append(pygame.image.load('images/carteVerso.png'))
        self.cardsImages.append(pygame.image.load('images/carteRecto.png'))

    def showDesk(self):
        self.screen.fill((0, 250, 0)) #produces a green-color background
		
    def showCards(self):
        for i in range(0, const.DESK.Y_SIZE):
            self.screen.blit(self.cardsImages[0], self.getCoordsFromIndex(const.CARD_POSITION.DESK, [i, 0]))
            for j in range(1, const.DESK.X_SIZE + 1):
                self.screen.blit(self.cardsImages[1], self.getCoordsFromIndex(const.CARD_POSITION.DESK, [i, j]))

    def getCoordsFromIndex(self, position, index):
        if position == const.CARD_POSITION.DESK:
            return [index[1] * (const.CARD.WIDTH + const.DESK.X_STEP) + const.DESK.X0,
                    index[0] * (const.CARD.HEIGHT + const.DESK.Y_STEP) + const.DESK.Y0]
        else:
            return 0

    def getIndexFromCoords(self, coords):
        if coords[0] < const.DESK.X0:
            xIndex = -1
        else:
            xIndex = (coords[0] - const.DESK.X0) // (const.CARD.WIDTH + const.DESK.X_STEP)
            if xIndex > const.DESK.X_SIZE:
                xIndex = -1
            if coords[0] - const.DESK.X0 - xIndex * (const.CARD.WIDTH + const.DESK.X_STEP) > const.CARD.WIDTH:
                xIndex = -1
        if coords[1] < const.DESK.Y0:
            yIndex = -1
        else:
            yIndex = (coords[1] - const.DESK.Y0) // (const.CARD.HEIGHT + const.DESK.Y_STEP)
            if yIndex > const.DESK.Y_SIZE:
                yIndex = -1
            if coords[1] - const.DESK.Y0 - yIndex * (const.CARD.HEIGHT + const.DESK.Y_STEP) > const.CARD.HEIGHT:
                yIndex = -1
        if xIndex == -1 or yIndex == -1:
            xIndex = -1
            yIndex = -1
        return [xIndex, yIndex]
