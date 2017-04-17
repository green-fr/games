from player import Player
import pygame


class PlayerUI(Player):
    def move(self, game):
        running = True
        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                game.exit_game()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(game.get_rect_from_coord(event.pos))
        return 0
