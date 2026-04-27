import unittest
from types import SimpleNamespace
from models.meld import is_valid_run, is_valid_set, is_valid_meld


def card(rank, suit):
    return SimpleNamespace(rank=rank, suit=suit)


# ChatGPT prompt: "generate a unit test for this Meld class" (along with code for `meld.py)
class TestMelds(unittest.TestCase):
    def test_valid_run(self):
        cards = [card("3", "Hearts"), card("4", "Hearts"), card("5", "Hearts")]
        self.assertTrue(is_valid_run(cards))
        self.assertTrue(is_valid_meld(cards, "runs"))

    def test_invalid_run_with_wrong_suit(self):
        cards = [card("3", "Hearts"), card("4", "Clubs"), card("5", "Hearts")]
        self.assertFalse(is_valid_run(cards))

    def test_valid_set(self):
        cards = [card("7", "Spades"), card("7", "Hearts"), card("7", "Diamonds")]
        self.assertTrue(is_valid_set(cards))
        self.assertTrue(is_valid_meld(cards, "sets"))

    def test_invalid_set_with_wrong_rank(self):
        cards = [card("7", "Spades"), card("8", "Hearts"), card("7", "Diamonds")]
        self.assertFalse(is_valid_set(cards))


if __name__ == "__main__":
    unittest.main()
