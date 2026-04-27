import pygame

SUIT_TO_FILE = {
    'Clubs': 'Clovers',
    'Diamonds': 'Tiles',
    'Hearts': 'Hearts',
    'Spades': 'Pikes'
}

RANK_TO_FILE = {
    'Ace': 'A',
    'Jack': 'Jack',
    'Queen': 'Queen',
    'King': 'King',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
}

def card_file(pydealer_card, folder = 'black', ext= 'png'):
    rank, suit = str(pydealer_card).split(" of ")
    suit_name = SUIT_TO_FILE[suit]
    rank_name = RANK_TO_FILE[rank]
    return f"{folder}/{suit_name}_{rank_name}_black.{ext}"

def load_card_images(cards):
    cache = {}
    for card in cards:
        key = str(card)
        if key not in cache:
            cache[key] = pygame.image.load(card_file(card)).convert_alpha()
    return cache



