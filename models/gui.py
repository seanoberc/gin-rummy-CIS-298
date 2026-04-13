import tkinter as tk
from models.card import SUIT_SYMBOLS, RANK_SYMBOLS
from game.game import Game

CARD_WIDTH = 60
CARD_HEIGHT = 90


class GinRummyGUI:
    def __init__(self):
        self.game = Game()
        self.game.deal()

        self.root.tk.Tk()
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
