from genericpath import sameopenfile
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

    def get_deadwood_val(deadwood_stack):
        total = 0
        #loop through dead stack then returns total points
        for card in deadwood_stack:
            total += card.get_value()
        return total
        
    def handle_knock(self, opponent):
        my_deadwood = self.player.get_deadwood_val(self.hand)
        opponent_deadwood = opponent.player.get_deadwood_val(opponent.hand) 

        if my_deadwood < opponent_deadwood:  # KNOCK WIN player wins round and gains deadwood difference
            points = opponent_deadwood - my_deadwood
            self.player.score += points
            return (self.name + " KNOCK WIN", points)

        else:  # UNDERCUT LOSS opponent wins with 10-point bonus
            points = 10 + (my_deadwood - opponent_deadwood)
            return (opponent.name + " UNDERCUT WIN", points)

    def handle_gin(self, opponent):
        # player declares Gin (scores 20 + opponent's deadwood)
        opponent_deadwood = opponent.player.get_deadwood_val(opponent.hand) 
        points = 20 + opponent_deadwood
        self.player.score += points
        return (self.name + " GIN WIN", points)
