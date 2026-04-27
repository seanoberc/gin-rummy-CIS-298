import os
import pygame
import unittest
from unittest.mock import patch
from models.card import Card, CARD_WIDTH, CARD_HEIGHT
from models.deck import Deck

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def fake_card_image(self):
    return pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)


# ChatGPT prompt: "generate an integration test for this Game class" (along with code for `game.py)
class TestDeck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    def test_deck_starts_with_52_unique_cards(self):
        with patch.object(Card, "_load_image", fake_card_image):
            deck = Deck()
            names = {(card.rank, card.suit) for card in deck.cards}

        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(names), 52)

    def test_draw_empty_deck_returns_none(self):
        with patch.object(Card, "_load_image", fake_card_image):
            deck = Deck()
            deck.cards = []
            self.assertIsNone(deck.draw())

    def test_discard_and_take_discard(self):
        with patch.object(Card, "_load_image", fake_card_image):
            deck = Deck()
            card = deck.draw()
            deck.discard(card)

        self.assertEqual(deck.top_discard(), card)
        self.assertEqual(deck.take_discard(), card)
        self.assertIsNone(deck.top_discard())

    def test_discard_none_raises_error(self):
        with patch.object(Card, "_load_image", fake_card_image):
            deck = Deck()
            with self.assertRaises(ValueError):
                deck.discard(None)


if __name__ == "__main__":
    unittest.main()
