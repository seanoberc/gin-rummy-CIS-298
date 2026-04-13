import pydealer

# class Deck():
#
#     def __init__(self):
#

deck = pydealer.Deck()
deck.shuffle()
hand = deck.deal(10)

# for card in hand:
#     print(card)