
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def set_hand(self, cards):
        self.hand = cards

    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)

    def hand_size(self):
        return len(self.hand)