class Player:
    def __init__(self, name, is_human = True):
        self.name = name
        self.hand = []
        self.score = 0
        self.is_human = is_human
        self.groups = {
            "runs": [],
            "sets": [],
        }

    def set_hand(self, cards):
        self.hand = list(cards)
        self.groups = {
            "runs": [],
            "sets": []
        }

    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)

    def hand_size(self):
        return len(self.hand)

    def move_to_group(self, card, group_name):
        if card in self.hand:
            self.hand.remove(card)

        if group_name not in ("runs", "sets"):
            raise ValueError("group_name must be 'runs' or 'sets'")

        for g in ("runs", "sets"):
            for group in self.groups[g]:
                if card in group:
                    group.remove(card)

        for g in ("runs", "sets"):
            self.groups[g] = [grp for grp in self.groups[g] if grp]

        self.groups[group_name].append([card])

    def move_to_hand(self, card):
        for g in ("runs", "sets"):
            for group in self.groups[g]:
                if card in group:
                    group.remove(card)
        for g in ("runs", "sets"):
            self.groups[g] = [grp for grp in self.groups[g] if grp]

        if card not in self.hand:
            self.hand.append(card)

    def deadwood_val(self):
        return sum(card.point_val for card in self.hand)
    

