# point values for Gin Rummy:
#   Ace = 1; number cards = face value; face cards = 10

VALUES = {
    "Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "Jack": 10, "Queen": 10, "King": 10
}

# rank order for detecting runs (Ace is lowest):
RANK_ORDER = {
    "Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "Jack": 11, "Queen": 12, "King": 13
}

def get_value(card):
    return VALUES[card.value]

def get_rank_order(card):
    return RANK_ORDER[card.value]