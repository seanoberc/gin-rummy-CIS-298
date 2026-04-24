import pygame

FELT_COLOR = "#0B5D3B"
TITLE_COLOR = (240, 220, 100)
TEXT_COLOR = (240, 240, 240)
INPUT_COLOR = (255, 255, 255)
INPUT_ACTIVE_COLOR = (200, 230, 200)
BOX_COLOR = (20, 20, 20)
BUTTON_COLOR = (20, 20, 20)
BUTTON_HOVER_COLOR = (50, 50, 50)

class MenuView:
    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height

        self.font_title = pygame.font.SysFont("Georgia", 64)
        self.font_label = pygame.font.SysFont("Georgia", 24)
        self.font_button = pygame.font.SysFont("Georgia", 28)
        self.font_input = pygame.font.SysFont("Georgia", 24)

        # player name input state:
        self.player_name = ""
        self.input_active = False

        # input box rect:
        self.input_rect = pygame.Rect(
            window_width // 2 - 150,
            window_height // 2,
            300, 44
        )

        # start button rect:
        self.start_rect = pygame.Rect(
            window_width // 2 - 100,
            window_height // 2 + 80,
            200, 50
        )

        # exit button rect:
        self.exit_rect = pygame.Rect(
            window_width // 2 - 100,
            window_height // 2 + 150,
            200, 50
        )

    # handles user input events:
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # toggle input box active state:
            self.input_active = self.input_rect.collidepoint(mx, my)

            # start button:
            if self.start_rect.collidepoint(mx, my) and self.player_name.strip():
                return "start"

            # exit button:
            if self.exit_rect.collidepoint(mx, my):
                return "exit"

        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN:
                if self.player_name.strip():
                    return "start"
            # else limit name to 20 characters in length:
            else:
                if len(self.player_name) < 20:
                    self.player_name += event.unicode

        return None