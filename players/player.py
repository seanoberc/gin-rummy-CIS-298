class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.hand = []
        self.score = 0
        self.is_human = is_human
        self.groups = {
            'runs': [],
            'sets': [],
        }
    def reset_groups(self):
        self.groups = {
            'runs': [],
            'sets': [],
        }

    def set_hand(self, hand):
        self.hand = list(hand)
        self.reset_groups()

    def move_to_group(self, card, group_name):
        if group_name not in ("runs", "sets"):
            raise ValueError("group_name must be 'runs' or 'sets'")

        if card in self.hand:
            self.hand.remove(card)

        for g in ("runs", "sets"):
            for stack in self.groups[g]:
                if card in stack:
                    stack.remove(card)

        self.groups[group_name].append([card])


    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)

    def move_card(self, from_i, to_i):
        card = self.hand.pop(from_i)
        self.hand.insert(to_i, card)

    def discard_at(self, i):
        return self.hand.pop(i)


