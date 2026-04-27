from models.deck import Deck
from models.player import Player
from models.ai_player import cpu_take_turn
from models.meld import is_valid_run_group, is_valid_set_group


class Game:
    def __init__(self, player_name="Human"):
        self.deck = Deck()
        self.player = Player(player_name, is_human=True)
        self.cpu = Player("CPU", is_human=False)
        self.turn = "human"
        self.phase = "draw"

        # deal 10 cards to player:
        self.player.set_hand(self.deck.deal(10))
        self.cpu.set_hand(self.deck.deal(10))

        # flip one card to start discard pile
        self.deck.discard(self.deck.draw())

    def draw_from_stock(self):
        if self.turn != "human" or self.phase != "draw":
            return None
        card = self.deck.draw()
        if card is None:
            return None
        self.player.add_card(card)
        self.phase = "discard"
        return card

    def draw_from_discard(self):
        if self.turn != "human" or self.phase != "draw":
            return None
        card = self.deck.take_discard()
        if card is None:
            return None
        self.player.add_card(card)
        self.phase = "discard"
        return card

    def discard_card(self, card):
        if self.turn != "human" or self.phase != "discard":
            return False
        self.deck.discard(card)
        self.player.remove_card(card)
        self.phase = "draw"
        self.turn = "cpu"
        cpu_take_turn(self.deck, self.cpu)
        self.turn = "human"
        self.phase = "draw"
        return True

    def handle_knock(self, opponent):
        if self.turn != "human" or self.phase != "discard":
            return ("not_allowed", 0)

        my_deadwood = self.effective_deadwood_val(self.player)
        opponent_deadwood = self.effective_deadwood_val(opponent)

        if my_deadwood > 10:
            return ("cannot_knock", 0)

        if my_deadwood < opponent_deadwood:  # KNOCK WIN player wins round and gains deadwood difference
            points = opponent_deadwood - my_deadwood
            self.player.score += points
            return (self.player.name + " KNOCK WIN", points)

        else:  # UNDERCUT LOSS opponent wins with 10-point bonus
            points = 10 + (my_deadwood - opponent_deadwood)
            opponent.score += points
            return (opponent.name + " UNDERCUT WIN", points)

    @staticmethod
    def effective_deadwood_val(player):
        total = sum(c.point_val for c in player.hand)

        for g in player.groups["runs"]:
            if not is_valid_run_group(g):
                total += sum(c.point_val for c in g)

        for g in player.groups["sets"]:
            if not is_valid_set_group(g):
                total += sum(c.point_val for c in g)

        return total

    def handle_gin(self, opponent):
        # player declares Gin (scores 20 + opponent's deadwood)
        if self.turn != "human" or self.phase != "discard":
            return ("not_allowed", 0)

        if self.effective_deadwood_val(self.player) != 0:
            return ("not_gin", 0)

        opponent_deadwood = self.effective_deadwood_val(opponent)
        points = 20 + opponent_deadwood
        self.player.score += points
        return (self.player.name + " GIN WIN", points)



