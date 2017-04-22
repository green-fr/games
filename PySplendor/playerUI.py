from player import Player
import pygame


class PlayerUI(Player):

    game = []
    game_ui = []

    def __init__(self, game, game_ui):
        self.game = game
        self.game_ui = game_ui

    def move(self):
        running = True
        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.game.exit_game()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(self.game_ui.get_rect_from_coord(event.pos))
        return 0
