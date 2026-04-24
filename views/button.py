import pygame

BUTTON_COLOR = (20, 20, 20)
BUTTON_HOVER_COLOR = (50, 50, 50)
BUTTON_DISABLED_COLOR = (60, 60, 60)
TEXT_COLOR = (240, 240, 240)
TEXT_DISABLED_COLOR = (120, 120, 120)

class Button:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.enabled = False  # disabled by default until game logic enables them
        self.font = pygame.font.SysFont(None, 28)

    