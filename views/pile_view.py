import pygame
from pygame.examples.setmodescale import screen

from models.deck import Deck

CARD_WIDTH = 80
CARD_HEIGHT = 110

class PileView:
    def __init__(self, screen, deck, window_width, window_height):
        self.screen = screen
        self.deck = deck

        # calculate center of card table:
        self.center_y = window_height // 2 - CARD_HEIGHT // 2
        self.stock_x = window_width // 2 - CARD_HEIGHT - 20
        self.discard_x = window_width // 2 + 20

        # load card-back image for stockpile:
        stock_image = pygame.image.load("assets/images/Blue_card_back.png").convert_alpha()
        self.stock_image = pygame.transform.smoothscale(stock_image, (CARD_WIDTH, CARD_HEIGHT))

    def draw(self):
        # draw the stockpile:
        self.screen.blit(self.stock_image, (self.stock_x, self.center_y))

        # draw top of discard pile:
        top = self.deck.top_discard()
        if top is not None:
            self.screen.blit(top.image, (self.discard_x, self.center_y))

    def stock_rect(self):
        return pygame.Rect(self.stock_x, self.center_y, CARD_WIDTH, CARD_HEIGHT)

    def discard_rect(self):
        return pygame.Rect(self.discard_x, self.center_y, CARD_WIDTH, CARD_HEIGHT)