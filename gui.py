import tkinter as tk
import pydealer

def start_gui():
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
        color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
        card_label = tk.Label(
            hand_frame,
            text=f"{card.value}\nof\n{card.suit}",
            font=("Arial", 10, "bold"),
            fg=color,
            bg="white",
            width=8,
            height=5,
            relief="raised",
            borderwidth=2
        )
        card_label.pack(side="left", padx=4)

    root.mainloop()