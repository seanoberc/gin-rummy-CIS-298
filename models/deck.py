import pydealer

class Deck:
    def __init__(self):
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.discard = pydealer.Stack()

    def deal(self, n):
        return self.deck.deal(n)

    def draw_card(self):
        return self.deck.deal(1)[0]

    def top_discard(self):
        if len(self.discard) > 0:
            return self.discard[-1]
        else:
            return None

    def take_discard(self):
        return self.discard.pop()

    def discard_card(self, card):
        self.discard.add(card)



