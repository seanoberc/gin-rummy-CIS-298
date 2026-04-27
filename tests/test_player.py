import unittest
from types import SimpleNamespace
from models.player import Player


# ChatGPT prompt: "generate a unit test for this Player class" (along with code for `player.py)
def card(rank, suit, points):
    return SimpleNamespace(rank=rank, suit=suit, point_val=points)


class TestPlayer(unittest.TestCase):
    def test_set_hand_and_deadwood(self):
        player = Player("Tester")
        player.set_hand([card("Ace", "Spades", 1), card("King", "Clubs", 10)])
        self.assertEqual(player.hand_size(), 2)
        self.assertEqual(player.deadwood_val(), 11)

    def test_move_card_to_group_and_back(self):
        player = Player("Tester")
        ace = card("Ace", "Spades", 1)
        player.set_hand([ace])

        player.move_to_group(ace, "runs")
        self.assertEqual(player.hand_size(), 0)
        self.assertIn([ace], player.groups["runs"])

        player.move_to_hand(ace)
        self.assertIn(ace, player.hand)
        self.assertEqual(player.groups["runs"], [])

    def test_bad_group_name_raises_error(self):
        player = Player("Tester")
        ace = card("Ace", "Spades", 1)
        with self.assertRaises(ValueError):
            player.move_to_group(ace, "bad group")


if __name__ == "__main__":
    unittest.main()
