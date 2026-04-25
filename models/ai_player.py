RANKS = {"Ace":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10,
         "Jack":11, "Queen":12, "King":13}

DEADWOOD = {"Ace":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
            "10":10, "Jack":10, "Queen":10, "King":10}

def card_rank(card):
    return RANKS[card.rank]

def card_points(card):
    return DEADWOOD[card.rank]

def helps_hands(card, hand):
    if any(c.rank == card.rank for c in hand):
        return True
    r = card_rank(card)
    return any((c.suit == card.suit and abs(card_rank(c) - r) == 1) for c in hand)

def discard_score(card, hand):
    r = card_rank(card)
    has_some_rank = any( c is not card and c.rank == card.rank for c in hand)
    has_neighbor = any((c is not card) and (c.suit == card.suit) and (abs(card_rank(c) - r) == 1) for c in hand)
    score = card_points(card)
    if has_some_rank:
        score = score - 4
    if has_neighbor:
        score = score - 3
    return score

def cpu_take_turn(deck, cpu_player):
    top = deck.top_discard()
    if top is not None and helps_hands(top, cpu_player.hand):
        cpu_player.add_card(deck.take_discard())
    else:
        cpu_player.add_card(deck.draw())

    worst = max(cpu_player.hand, key=lambda c: discard_score(c, cpu_player.hand))
    cpu_player.remove_card(worst)
    deck.discard(worst)