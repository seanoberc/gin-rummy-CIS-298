import pydealer
from models.card import SUIT_SYMBOLS, RANK_SYMBOLS

class Hand:
    def __init__(self):
        self.cards = pydealer.Stack()

        def add(self, cards):
            self.cards.add(cards)

        def remove(self, card):
            self.cards.get(card.value + " of " + card.suit)

        def size(self):
            return self.cards.size