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

    # Iterate through ranks, checks if its 3 or 4 cards
    for rank in set(ranks):
        if ranks.count(rank) not in (3, 4):
            return False

    # return len(set(ranks)) == 1 ##old, only allows for 1 set in the bin to be valid, if there's >1 set then its invalid
    return True


# a valid run is 3 or more cards of same suit in consecutive rank order
# Ace is always low; can pair with a 2 but not with a King
def is_valid_run(cards):
    #old implementation: doesn't allow for multiple runs to be marked as valid in the bin
    #example, club 1,2,3,4 is a valid run but club 1,2,3 and heart 1,2,3 in the bin together is not valid
    # suits = [card.suit for card in cards]
    # indices = sorted([rank_index(card) for card in cards])

    # if len(cards) < 3:
    #     return False
    # if len(set(suits)) != 1:
    #     return False
    # for i in range(1, len(indices)):
    #     if indices[i] != indices[i - 1] + 1:
    #         return False
    # return True

    #new implementation: allows for multiple different runs in the same bin to be marked as valid
    if cards and isinstance(cards[0], (list, tuple)):
        flat_cards = []
        for group in cards:
            flat_cards.extend(group)
        cards = flat_cards

    if not cards or len(cards) < 3:
        return False
    
    def get_val(card):
        return RANK_ORDER.index(str(card.rank).upper())

    #sorts by suits then rank
    sorted_cards = sorted(cards, key=lambda c: (c.suit, get_val(c)))

    #iterate and validate length
    current_run_length = 1

    for i in range(1, len(sorted_cards)):
        previous_card = sorted_cards[i - 1]
        current_card = sorted_cards[i]
        
        #check if the current card continues the exact sequence
        is_same_suit = current_card.suit == previous_card.suit
        is_consecutive = get_val(current_card) == get_val(previous_card) + 1

        if is_same_suit and is_consecutive:
            current_run_length += 1
        else:
            if current_run_length < 3:
                return False
            
            # Reset the counter for the start of the next potential run
            current_run_length = 1

    # Check the very last run in the list after the loop finishes
    if current_run_length < 3:
        return False

    return True

# checks whether a group of cards as either a run or a set, otherwise return False:
def is_valid_meld(cards, meld_type):
    if meld_type == "runs":
        return is_valid_run(cards)
    elif meld_type == "sets":
        return is_valid_set(cards)
    return False
