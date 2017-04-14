from game import *

game = Game()
game.load_cards()
game.show_desk()
game.show_cards()

running = True
pygame.display.flip()
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        print(event.button)
        print(event.pos)
        print(Game.get_index_from_coord(event.pos))
