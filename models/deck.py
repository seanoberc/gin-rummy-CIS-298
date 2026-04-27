import random
from models.card import Card

SUITS = ["Spades", "Hearts", "Diamonds", "Clubs"]
RANKS = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


class Deck:
    def __init__(self):
        # constructs a 52-card deck as a list of Card objects:
        self.cards = []
        self.discard_pile = []

        # loop through each rank; for each rank loop through each suit
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append(Card(rank, suit))  # create a card for each combination

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    # def draw(self):  # pops a card from the end of the list           
    #     return self.cards.pop()

    def draw(self):  # pops a card from the end of the list          
        if len(self.cards) == 0:
            if len(self.discard_pile) > 1:
                self.cards = self.discard_pile[:-1]
                
                self.discard_pile = [self.discard_pile[-1]]
                

                self.shuffle()
                print("The discard pile was reshuffled into the deck!")
                
                
        return self.cards.pop()

    def deal(self, n):
        return [self.draw() for _ in range(n)]

    def discard(self, card):
        self.discard_pile.append(card)

    def top_discard(self):
        if self.discard_pile:
            return self.discard_pile[-1]
        return None

    def take_discard(self):
        if self.discard_pile:
            return self.discard_pile.pop()
        return None

    def cards_remaining(self):
        return len(self.cards)
