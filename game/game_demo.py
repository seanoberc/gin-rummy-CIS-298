from game.game import Game


class DemoGame(Game):
    # ChatGPT prompt: "generate two Python dictionaries for a game of Gin Rummy that represent two hands.
    #   "one should be for the human player and one for the computer player.
    #   "follow this convention: `HAND = [ ("Rank", "Suit"), ("Rank", "Suit"), ]`,
    #   "generate at least three ready-made runs and sets according to Gin Rummy rules.
    #   "initial hand size should be 10 cards."

    HUMAN_HAND = [
        # Ready-made run: 3-4-5 of Hearts
        ("3", "Hearts"),
        ("4", "Hearts"),
        ("5", "Hearts"),

        # Ready-made set: three 7s
        ("7", "Spades"),
        ("7", "Hearts"),
        ("7", "Diamonds"),

        # Ready-made run: 9-10-Jack of Clubs
        ("9", "Clubs"),
        ("10", "Clubs"),
        ("Jack", "Clubs"),

        # Low deadwood, useful for demonstrating knock after grouping melds
        ("Ace", "Spades"),
    ]

    CPU_HAND = [
        ("2", "Clubs"),
        ("2", "Diamonds"),
        ("King", "Spades"),
        ("Queen", "Hearts"),
        ("8", "Diamonds"),
        ("6", "Clubs"),
        ("4", "Spades"),
        ("9", "Diamonds"),
        ("Jack", "Hearts"),
        ("Ace", "Clubs"),
    ]

    STARTING_DISCARD = ("6", "Hearts")

    def __init__(self, player_name="Demo Player", auto_group=False):
        super().__init__(player_name)
        self.demo_mode = True
        self._replace_random_deal(auto_group=auto_group)

    def _replace_random_deal(self, auto_group=False):
        self.deck.cards.extend(self.player.hand)
        self.deck.cards.extend(self.cpu.hand)
        self.deck.cards.extend(self.deck.discard_pile)
        self.deck.discard_pile = []

        human_cards = self._take_cards(self.HUMAN_HAND)
        cpu_cards = self._take_cards(self.CPU_HAND)
        discard_card = self._take_card(*self.STARTING_DISCARD)  # cool: `*` Python operator cuts tuple into separate args

    def _take_cards(self, specs):
        return [self._take_card(rank, suit) for rank, suit in specs]

    def _take_card(self, rank, suit):
        for card in self.deck.cards:
            if card.rank == rank and card.suit == suit:
                self.deck.cards.remove(card)
                return card
        raise ValueError(f"ERROR: Demo card not found in deck: {rank} of {suit}.")

    def _auto_group_human_melds(self):
        cards_by_name = {
            (card.rank, card.suit): card for card in self.player.hand
        }

        run_one = [cards_by_name[spec] for spec in self.HUMAN_HAND[0:3]]
        set_one = [cards_by_name[spec] for spec in self.HUMAN_HAND[3:6]]
        run_two = [cards_by_name[spec] for spec in self.HUMAN_HAND[6:9]]

        for card in run_one + set_one + run_two:
            self.player.hand.remove(card)

        self.player.groups["runs"] = [run_one, run_two]
        self.player.groups["sets"] = [set_one]
