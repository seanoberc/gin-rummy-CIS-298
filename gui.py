import tkinter as tk
import pydealer

# generate a deck and deal hand:
deck = pydealer.Deck()
deck.shuffle()
hand = deck.deal(10)

# TKInter window:
root = tk.Tk()
root.title("Gin Rummy")
root.geometry("900x600")
root.configure(bg="darkgreen")

# title:
title = tk.Label(root, text="Gin Rummy", font=("Arial", 24, "bold"),
                 bg="darkgreen", fg="white")
title.pack(pady=10)

# hand frame:
hand_frame = tk.Frame(root, bg="darkgreen")
hand_frame.pack(pady=20)

# display the cards:
for card in hand:
