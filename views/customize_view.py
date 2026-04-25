import pygame
from models import card_style
from models.spritesheet import SpriteSheet
from views.button import Button

PANEL_WIDTH = 600
PANEL_HEIGHT = 400

OVERLAY_COLOR = (0, 0, 0, 180)
PANEL_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)
LABEL_COLOR = (180, 180, 180)
SELECTED_COLOR = (200, 200, 60)
BUTTON_COLOR = (20, 20, 20)
BUTTON_HOVER_COLOR = (50, 50, 50)

BACK_NAMES = ["red", "green", "blue", "peach"]

class CustomizeView:
    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.visible = False

        self.font_title = pygame.font.SysFont("Georgia", 2, bold=True)
        self.font_label = pygame.font.SysFont("Georgia", 20)
        # self.font_button = pygame.font.SysFont("Georgia", 22)

        # center panel on screen:
        self.panel_rect = pygame.Rect(
            window_width // 2 - PANEL_WIDTH // 2,
            window_height // 2 - PANEL_HEIGHT // 2,
            PANEL_WIDTH,
            PANEL_HEIGHT
        )

        # buttons to choose between 'default' and 'classic':
        self.default_button = Button(
            self.panel_rect.x + 60,
            self.panel_rect.y + 100, 180, 44,
            "Default"
        )
        self.classic_button = Button(
            self.panel_rect.x + 60,
            self.panel_rect.y + 100, 180, 44,
            "Classic"
        )
        self.default_button.enabled = True
        self.classic_button.enabled = True

        # buttons to choose 'classic' card back:
        self.back_buttons = {}
        for i, name in enumerate(BACK_NAMES):
            btn = Button(
                self.panel_rect.x + 40 + i * 130,
                self.panel_rect.y + 260, 100, 36,
                name.capitalize()
            )
            btn.enabled = True
            self.back_buttons[name] = btn

        # close window button:
        self.close_botton = Button(
            self.panel_rect.centerx - 60,
            self.panel_rect.bottom - 60,
            120, 40, "Done"
        )
        self.close_botton.enabled = True

        # load card back previews from spritesheet:
        self._back_previews = None

    def _load_back_previews(self):
        if self._back_previews is not None:
            return
        sheet = SpriteSheet()
        self._back_previews = {}
        for name in BACK_NAMES:
            image = sheet.get_card_back(name)
            scaled = pygame.transform.smoothscale(image, (50, 72))
            self._back_previews[name] = scaled

    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.default_button.is_clicked(mx, my):
                card_style.current_style = "default"
            elif self.classic_button.is_clicked(mx, my):
                card_style.current_style = "classic"

            if card_style.current_style == "classic":
                for name, btn in self.back_buttons.items():
                    if btn.is_clicked(mx, my):
                        card_style.current_back = name

            if self.close_botton.is_clicked(mx, my):
                self.visible = False

        return True

    def draw(self):
        if not self.visible:
            return