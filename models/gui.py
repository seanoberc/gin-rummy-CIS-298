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

        