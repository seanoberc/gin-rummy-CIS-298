"""
`Meld` class handles the validation logic for valid melds
"""

RANK_ORDER = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


def is_valid_set_group(cards):
    return len(cards) in (3, 4) and len({c.rank for c in cards}) == 1

def is_valid_run_group(cards):
    if len(cards) < 3:
        return False
    if len({c.suit for c in cards}) != 1:
        return False
    idx = sorted(RANK_ORDER.index(c.rank) for c in cards)
    return all(idx[i] == idx[i-1] + 1 for i in range(1, len(idx)))



# in Gin Rummy, a valid set is a made of 3 or 4 cards of the same rank
def is_valid_set(groups):
    if not groups:
        return False
    if isinstance(groups[0], (list, tuple)):
        return all(is_valid_set_group(g) for g in groups)
    return is_valid_set_group(groups)


# a valid run is 3 or more cards of same suit in consecutive rank order
# Ace is always low; can pair with a 2 but not with a King
def is_valid_run(groups):
    if not groups:
        return False
    if isinstance(groups[0], (list, tuple)):
        return all(is_valid_run_group(g) for g in groups)
    return is_valid_run_group(groups)



# checks whether a group of cards as either a run or a set, otherwise return False:
def is_valid_meld(cards, meld_type):
    if meld_type == "runs":
        return is_valid_run(cards)
    elif meld_type == "sets":
        return is_valid_set(cards)
    return False