import pydealer

class Hand:
    def __init__(self):
        self.cards = pydealer.Stack()

    def add(self, cards):
        self.cards.add(cards)

    def remove(self, card):
        return self.cards.get(str(card))
        self.cards.get(card.value + " of " + card.suit)

    def size(self):
        return self.cards.size