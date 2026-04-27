import pygame

"""
`subsurface()`
    create a new surface that references its parent
    subsurface(Rect) -> Surface

Returns a new Surface that shares its pixels with its new parent. The new Surface is considered a child of the original.
    Modifications to either Surface pixels will effect each other.
    Surface information like clipping area and color keys are unique to each Surface.

The new Surface will inherit the palette, color key, and alpha settings from its parent.

It is possible to have any number of subsurfaces and subsubsurfaces on the parent.
It is also possible to subsurface the display Surface if the display mode is not hardware accelerated.

See get_offset() and get_parent() to learn more about the state of a subsurface.

A subsurface will have the same class as the parent surface.
"""

CARD_WIDTH = 57
CARD_HEIGHT = 89

# order of suits in `card_faces.png` card sheet:
SUIT_ROW = {
    "Clubs": 0,
    "Diamonds": 1,
    "Spades": 2,
    "Hearts": 3,
}

# ChatGPT prompt: "generate a dictionary to map string keys
#   for each rank in a 52-card deck to int vals"
# the order of ranks in the faces sheet (left to right)
RANK_COL = {
    "Ace": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "10": 9,
    "Jack": 10,
    "Queen": 11,
    "King": 12,
}

BACK_NAMES = ["red", "green", "blue", "peach"]


class SpriteSheet:
    def __init__(self):
        self.faces = pygame.image.load("assets/images/sprites/classic/card_faces.png").convert_alpha()
        self.backs = pygame.image.load("assets/images/sprites/classic/card_backs.png").convert_alpha()

    # slice a single card face from the "faces" sprite sheet:
    def get_card_face(self, rank, suit):
        col = RANK_COL[rank]
        row = SUIT_ROW[suit]
        x = col * CARD_WIDTH
        y = row * CARD_HEIGHT
        return self.faces.subsurface(pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT))

    # slice a single card back from the "backs" sprite sheet:
    def get_card_back(self, style="blue"):
        col = BACK_NAMES.index(style)
        x = col * CARD_WIDTH
        return self.backs.subsurface(pygame.Rect(x, 0, CARD_WIDTH, CARD_HEIGHT))
