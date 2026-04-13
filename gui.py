# import tkinter as tk
# # import pydealer
# from models.card import SUIT_SYMBOLS, RANK_SYMBOLS
# from game.game import Game
#
# def start_gui():
#     # generate a deck and deal hand:
#     # deck = pydealer.Deck()
#     # deck.shuffle()
#     # hand = deck.deal(10)
#
#     game = Game()
#     game.deal()
#
#     # TKInter window:
#     root = tk.Tk()
#     root.title("Gin Rummy")
#     root.geometry("900x600")
#     root.configure(bg="darkgreen")
#
#     # title:
#     title = tk.Label(root, text="Gin Rummy", font=("Arial", 24, "bold"),
#                      bg="darkgreen", fg="white")
#     title.pack(pady=10)
#
#     # card piles:
#     piles_frame = tk.Frame(root, bg="darkgreen")
#     piles_frame.pack(pady=20)
#
#     draw_label = tk.Label(piles_frame, text="🂠",
#                           font=("Arial", 28, "bold"), fg="white",
#                           bg="navy", width=4, height=3,
#                           relief="raised", borderwidth=2)
#     draw_label.pack(side="left", padx=20)
#
#     top_discard = game.get_top_discard()
#     discard_color = "red" if top_discard.suit in ["Hearts", "Diamonds"] else "black"
#     discard_label = tk.Label(piles_frame,
#                              text=f"{RANK_SYMBOLS[top_discard.value]}\n{SUIT_SYMBOLS[top_discard.suit]}",
#                              font=("Arial", 18, "bold"), fg=discard_color,
#                              bg="white", width=4, height=3,
#                              relief="raised", borderwidth=2)
#     discard_label.pack(side="left", padx=20)
#
#     # player hand:
#     hand_label = tk.Label(root, text="Your Hand", font=("Arial", 16),
#                           bg="darkgreen", fg="white")
#     hand_label.pack(pady=(20, 5))
#
#     # hand frame:
#     hand_frame = tk.Frame(root, bg="darkgreen")
#     hand_frame.pack(pady=20)
#
#     # display the cards:
#     for card in game.player_hand:
#         suit_sym = SUIT_SYMBOLS[card.suit]
#         rank_sym = RANK_SYMBOLS[card.value]
#         color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
#         card_label = tk.Label(
#             hand_frame,
#             text=f"{rank_sym}\n\n{suit_sym}",
#             font=("Arial", 10, "bold"),
#             fg=color,
#             bg="white",
#             width=8,
#             height=5,
#             relief="raised",
#             borderwidth=2
#         )
#         card_label.pack(side="left", padx=4)
#
#     root.mainloop()