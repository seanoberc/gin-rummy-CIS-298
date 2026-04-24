import pygame

CARD_WIDTH = 80
CARD_HEIGHT = 110
HAND_SPACING = 90
HAND_MARGIN_X = 20
HAND_MARGIN_BOTTOM = 20

class HandView:
    def __init__(self, window_height, player):
        self.player = player
        self.hand_y = window_height - CARD_HEIGHT - HAND_MARGIN_BOTTOM

    # update x,y pos. of each card in the hand based on its index:
    def reposition(self):
        for i, card in enumerate(self.player.hand):
            card.rect.x = HAND_MARGIN_X + i * HAND_SPACING
            card.rect.y = self.hand_y

    # convert mouse-x pos. into a hand index:
    def index_at(self, mx):
        i = (mx - HAND_MARGIN_X) // HAND_SPACING
        return max(0, min(i, len(self.player.hand) - 1))

    # return top-most card at given moust pos. (or return `None`):
    def card_at(self, mx, my):
        for card in reversed(self.player.hand):
            if card.rect.collidepoint(mx, my):
                return card
        return None
