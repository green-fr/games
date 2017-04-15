from game import *

game = Game()
game.load_cards()
game.show_deck_and_desk()
game.show_tokens()

running = True
pygame.display.flip()
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        print(game.get_rect_from_coord(event.pos))
