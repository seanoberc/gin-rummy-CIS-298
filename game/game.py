from models.deck import Deck
from models.player import Player


class Game:
    def __init__(self, player_name="Human"):
        self.deck = Deck()
        self.player = Player(player_name)
        self.phase = "draw"

        # deal 10 cards to player:
        self.player.set_hand(self.deck.deal(10))

        # flip one card to start discard pile
        self.deck.discard(self.deck.draw())

    def draw_from_stock(self):
        if self.phase != "draw":
            return None
        card = self.deck.draw()
        self.player.add_card(card)
        self.phase = "discard"
        return card

    def draw_from_discard(self):
        if self.phase != "draw" or self.deck.top_discard() is None:
            return None
        card = self.deck.take_discard()
        self.player.add_card(card)
        self.phase = "discard"
        return card

    def discard_card(self, card):
        if self.phase != "discard":
            return False
        self.deck.discard(card)
        self.player.remove_card(card)
        self.phase = "draw"
        return True

    def handle_knock(self):
        player_deadwood = self.player.deadwood_val()
        opponent_deadwood = 0  # TODO: placholder

        if player_deadwood < opponent_deadwood:  # player wins round
            points = opponent_deadwood - player_deadwood
            self.player.score += points
            return ("player_wins", points)
        else:  # opponent wins with 10-point bonus
            points = 10 + (player_deadwood - opponent_deadwood)
            return ("opponent_wins", points)

    def handle_gin(self):  # player declares Gin (scores 20 + opponent's deadwood)
        opponent_deadwood = 0
        points = 20 + opponent_deadwood
        self.player.score += points
        return ("gin", points)
