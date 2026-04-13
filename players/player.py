class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.hand = []
        self.score = 0
        self.is_human = is_human

    def set_hand(self, hand):
        self.hand = hand

    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)