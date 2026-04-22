import pydealer

class Game:
    def __init__(self):
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.discard_pile = pydealer.Stack()
        self.player_hand = None
        self.ai_hand = None

    # TODO: func deal()
    def deal(self):
        self.player_hand = self.deck.deal(10)
        self.ai_hand = self.deck.deal(10)

        # flip one card to begin the discard pile:
        self.discard_pile.add(self.deck.deal(1))

    # TODO: func draw()
    def get_top_discard(self):
        return self.discard_pile[-1]

    # TODO: func discard()
    def draw_from_deck(self):
        return self.deck.deal(1)

    def discard(self, card):
        self.discard_pile.add(card)
