import pygame

CARD_WIDTH = 80
CARD_HEIGHT = 110

SUIT_TO_FILE = {
    "Clubs":    "Clovers",
    "Diamonds": "Tiles",
    "Hearts":   "Hearts",
    "Spades":   "Pikes",
}

RANK_TO_FILE = {
    "Ace": "A",
    "2": "2", "3": "3", "4": "4", "5": "5",
    "6": "6", "7": "7", "8": "8", "9": "9", "10": "10",
    "Jack": "Jack", "Queen": "Queen", "King": "King",
}

# Card class extends Pygame's Sprite class
class Card(pygame.sprite.Sprite):
    def __init__(self, rank, suit):
        super().__init__()  # constructor for the parent class (which is now `Sprite`)
        self.rank = rank
        self.suit = suit

        path = self._image_path()
        image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.smoothscale(image, (CARD_WIDTH, CARD_HEIGHT)) # Pygame uses `Surface` for the canvas
        self.rect = self.image.get_rect()       # Pygame's 'rect` stores the card position on the screen

    def _image_path(self):
        suit_name = SUIT_TO_FILE[self.suit]
        rank_name = RANK_TO_FILE[self.rank]
        return f"assets/images/sprites/{suit_name}_{rank_name}_black.png"

        # Draw the rank and suit onto the card image
        # self._draw_card()

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    @property
    def point_val(self):
        if self.rank in ("Jack", "Queen", "King"):
            return 10
        elif self.rank == "Ace":
            return 1
        else:
            return int(self.rank)


