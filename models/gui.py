import tkinter as tk
import pydealer
from models.card import SUIT_SYMBOLS, RANK_SYMBOLS
from game.game import Game

CARD_WIDTH = 60
CARD_HEIGHT = 90


class GinRummyGUI:
    def __init__(self):
        self.game = Game()
        self.game.deal()

        self.root = tk.Tk()
        self.root.title("Gin Rummy")
        self.root.geometry("900x600")

        # use the `canvas` feature from TKInter instead of just labels:
        self.canvas = tk.Canvas(self.root, width=900, height=600, bg="darkgreen")
        self.canvas.pack()

        # state "drag-and-drop"
        self.drag_data = {
            "item": None, "x": 0, "y": 0,
            "cards": []
        }

        # draw table:
        self.draw_title()
        self.draw_piles()
        self.draw_hand()

        # bind drag actions to click events:
        self.canvas.tag_bind("card", "<ButtonPress-1>", self.on_card_press)
        self.canvas.tag_bind("card", "<B1-Motion>", self.on_card_drag)
        self.canvas.tag_bind("card", "<ButtonRelease-1>", self.on_card_release)

        self.root.mainloop()

        # draw title:

    def draw_title(self):
        self.canvas.create_text(450, 30, text="Gin Rummy",
                                font=("Arial", 24, "bold"), fill="white")

    # draw piles
    def draw_piles(self):
        # face-down draw pile:
        self.draw_pile_x, self.draw_pile_y = 350, 150

        self.canvas.create_rectangle(
            self.draw_pile_x, self.draw_pile_y,
            self.draw_pile_x + CARD_WIDTH, self.draw_pile_y + CARD_HEIGHT,
            fill="navy", outline="white", width=2, tags="draw_pile"
        )

        self.canvas.create_text(
            self.draw_pile_x + CARD_WIDTH // 2,
            self.draw_pile_y + CARD_HEIGHT // 2,
            text="🂠", font=("Arial", 24), fill="white", tags="draw_pile"
        )

        self.canvas.create_text(
            self.draw_pile_x + CARD_WIDTH // 2,
            self.draw_pile_y + CARD_HEIGHT + 15,
            text="Draw", font=("Arial", 12), fill="white"
        )

        # face-up discard pile:
        self.discard_x, self.dicard_y = 490, 150
        self.draw_discard_top()
        self.canvas.create_text(
            self.discard_x + CARD_WIDTH // 2,
            self.discard_y + CARD_HEIGHT + 15,
            text="Discard", font=("Arial", 12), fill="white"
        )

    def draw_discard_top(self):
        self.canvas.delete("discard_card")
        top = self.game.get_top_discard()
        self.draw_card_at(self.discard_x, self.discard_y, top, "discard_card")

    def draw_hand(self):
        self.canvas.delete("card")      # deletes existing card graphics from the canvas before redrawing
        self.canvas.delete("card_text")

        # set positions by pixel:
        start_x = 120
        y = 400

        # enumerate gives index and value for list iteration:
        #   for loop determines card spacing on table
        for i, card in enumerate(self.game.player_hand):
            x = start_x + i * (CARD_WIDTH + 8)
            self.draw_card_at(x, y, card, "card")

    def draw_card_at(self, x, y, card, tag):
        color = "red" if card.suit in ["Hearts", "Diamonds"] else "black"
        rank_sym = RANK_SYMBOLS[card.value]
        suit_sym = SUIT_SYMBOLS[card.suit]

        rect = self.canvas.create_rectangle(
            x, y, x + CARD_WIDTH, y + CARD_HEIGHT,
            fill="white", outline="gray", width=2, tags=tag
        )
        text = self.canvas.create_text(
            x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2,
            text=f"{rank_sym}\n{suit_sym}",
            font=("Arial", 16, "bold"), fill=color, tags=tag
        )

        # store card data on both the rect and text
        self.canvas.itemconfig(rect, tags=(tag, f"carddata_{card.value}_of_{card.suit}"))
        self.canvas.itemconfig(text, tags=(tag, f"carddata_{card.value}_of_{card.suit}"))

    def on_card_press(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)

        # find the carddata tag
        card_tag = [t for t in tags if t.startswith("carddata_")]
        if not card_tag:
            return

        # find all canvas items with this card's tag
        self.drag_data["cards"] = self.canvas.find_withtag(card_tag[0])
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_card_drag(self, event):
        if not self.drag_data["cards"]:
            return
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        for item in self.drag_data["cards"]:
            self.canvas.move(item, dx, dy)
            self.canvas.tag_raise(item)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_card_release(self, event):
        if not self.drag_data["cards"]:
            return

        # check if dropped on discard pile
        if (self.discard_x <= event.x <= self.discard_x + CARD_WIDTH and
                self.discard_y <= event.y <= self.discard_y + CARD_HEIGHT):

            # find which card was dragged
            tags = self.canvas.gettags(self.drag_data["cards"][0])
            card_tag = [t for t in tags if t.startswith("carddata_")][0]
            card_str = card_tag.replace("carddata_", "").replace("_", " ")

            # find and discard the card
            for card in self.game.player_hand:
                if f"{card.value} of {card.suit}" == card_str:
                    self.game.player_hand.get(card.value + " of " + card.suit)
                    self.game.discard_pile.add(pydealer.Stack(cards=[card]))
                    break

            self.draw_discard_top()

        # redraw hand (snaps back if not discarded)
        self.draw_hand()
        self.drag_data = {"item": None, "x": 0, "y": 0, "cards": []}

def start_gui():
    GinRummyGUI()