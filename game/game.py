from genericpath import sameopenfile
from models.deck import Deck
from models.player import Player
from models.ai_player import cpu_take_turn


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
        if self.phase != "draw" or self.turn != "draw":
            return None
        card = self.deck.take_discard()
        if card is None:
            return None
        self.player.add_card(card)
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

    def get_deadwood_val(deadwood_stack):
        total = 0
        #loop through dead stack then returns total points
        for card in deadwood_stack:
            total += card.get_value()
        return total
        
    # def handle_knock(me, opponent):
    #     my_deadwood = me.deadwood_val()
    #     opponent_deadwood = opponent.deadwood_val()

    #     if my_deadwood < opponent_deadwood:  # KNOCK WIN player wins round and gains deadwood difference
    #         points = opponent_deadwood - my_deadwood
    #         me.player.score += points
    #         return (me.player.name + " KNOCK WIN", points)

    #     else:  # UNDERCUT LOSS opponent wins with 10-point bonus
    #         points = 10 + (my_deadwood - opponent_deadwood)
    #         return (opponent.player.name + " UNDERCUT WIN", points)

    # def handle_gin(me, opponent):
    #     # player declares Gin (scores 20 + opponent's deadwood)
    #     opponent_deadwood = opponent.deadwood_val()
    #     points = 20 + opponent_deadwood
    #     me.player.score += points
    #     return (me.player.name + " GIN WIN", points)

    def handle_knock(self, opponent):
        my_deadwood = self.player.deadwood_val()
        opponent_deadwood = opponent.deadwood_val() 

        if my_deadwood < opponent_deadwood: # KNOCK WIN player wins round and gains deadwood difference
            points = opponent_deadwood - my_deadwood
            self.player.score += points
            return (self.player.name + " KNOCK WIN", points)

        else:  # UNDERCUT LOSS opponent wins with 10-point bonus
            points = 10 + (my_deadwood - opponent_deadwood)
            return (opponent.name + " UNDERCUT WIN", points)

    def handle_gin(self, opponent):
        # player declares Gin (scores 20 + opponent's deadwood)
        opponent_deadwood = opponent.deadwood_val() 
        points = 20 + opponent_deadwood
        self.player.score += points
        return (self.player.name + " GIN WIN", points)
