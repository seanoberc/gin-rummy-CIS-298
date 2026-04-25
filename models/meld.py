"""
`Meld` class handles the validation logic for valid melds
"""

RANK_ORDER = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

# returns the index of a card's rank according to the RANK_ORDER array:
def rank_index(card):
    return RANK_ORDER.index(card.rank)

# in Gin Rummy, a valid set is a made of 3 or 4 cards of the same rank
def is_valid_set(cards):
    if len(cards) < 3:
        return False
    ranks = [card.rank for card in cards]
    return len(set(ranks)) == 1

# a valid run is 3 or more cards of same suit in consecutive rank order
# Ace is always low; can pair with a 2 but not with a King
def is_valid_run(cards):
    suits = [card.suit for card in cards]
    indices = sorted([rank_index(card) for card in cards])

    if len(cards) < 3:
        return False
    if len(set(suits)) != 1:
        return False
    for i in range(1, len(indices)):
        if indices[i] != indices[i -1] + 1:
            return False
    return True

# checks whether a group of cards as either a run or a set, otherwise return False:
def is_valid_meld(cards, meld_type):
    if meld_type == "runs":
        return is_valid_run(cards)
    elif meld_type == "sets":
        return is_valid_set(cards)
    return False