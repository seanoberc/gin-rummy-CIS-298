import os
import pygame
import unittest
from unittest.mock import patch
from models.card import Card, CARD_WIDTH, CARD_HEIGHT

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

def fake_card_image(self):
    return pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)


# ChatGPT prompt: "generate a unit test for this Card class" (along with code for `card.py)
class TestCard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    def test_card_points(self):
        with patch.object(Card, "_load_image", fake_card_image):
            self.assertEqual(Card("Ace", "Spades").point_val, 1)
            self.assertEqual(Card("9", "Clubs").point_val, 9)
            self.assertEqual(Card("King", "Hearts").point_val, 10)

    def test_card_repr(self):
        with patch.object(Card, "_load_image", fake_card_image):
            card = Card("5", "Diamonds")
            self.assertEqual(repr(card), "5 of Diamonds")

    def test_bad_rank_raises_error(self):
        with patch.object(Card, "_load_image", Card._image_path):
            with self.assertRaises(ValueError):
                Card("BadRank", "Spades")


if __name__ == "__main__":
    unittest.main()