
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
        self.groups = {
            "runs": [],
            "sets": [],
        }

    def set_hand(self, cards):
        self.hand = cards

    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)

    def hand_size(self):
        return len(self.hand)

    def move_to_group(self, card, group_name):
        # removes the card from player's hand or any other group it might be in:
        if card in self.hand:
            self.hand.remove(card) # if the card is already in the hand, remove it

        # remove from any group it's currently in
        for name in ("runs", "sets"):
            if card in self.groups[name]:
                self.groups[name].remove(card)

        self.groups[group_name].append(card) # appends card to target group

    def move_to_hand(self, card):
        for name in ("runs", "sets"):
            if card in self.groups[name]:
                self.groups[name].remove(card)
            if card not in self.hand:
                self.hand.append(card)