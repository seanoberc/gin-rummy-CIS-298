from models.deck import Deck
from models.player import Player

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Human")
        self.phase = "draw"

        # deal 10 cards to player:
        self.player.set_hand(self.deck.deal(10))

        # flip one card to start discard pile
        self.deck.discard(self.deck.draw())

    def draw_from_stock(self):
        if self.phase != "draw":
            return None
        card = self.deck.draw()
        self.player.add_card(card)
        self.phase = "discard"
        return card

    def draw_from_discard(self):
        if self.phase != "draw" or self.deck.top_discard() is None:
            return None
        card = self.deck.take_discard()
        self.player.add_card(card)
        self.phase = "discard"
        return card

    def discard_card(self, card):
        if self.phase != "discard":
            return False
        self.deck.discard(card)
        self.player.remove_card(card)
        self.phase = "draw"
        return True