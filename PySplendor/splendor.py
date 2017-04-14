import pygame
import game

game = game.Game()
game.loadCards()
game.showDesk()
game.showCards()

running = True
pygame.display.flip()
while running == True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        print(event.button)
        print(event.pos)
        print(game.getIndexFromCoords(event.pos))
        