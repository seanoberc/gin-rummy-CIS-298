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

    def draw(self):
        self.screen.fill(FELT_COLOR)

        # game title
        title = self.font_title.render("Gin Rummy", True, TITLE_COLOR)
        self.screen.blit(title, (
            self.window_width // 2 - title.get_width() // 2,
            self.window_height // 3 - title.get_height() // 2
        ))

        # player-name label
        label = self.font_label.render("Enter your name:", True, TEXT_COLOR)
        self.screen.blit(label, (
            self.window_width // 2 - label.get_width() // 2,
            self.input_rect.y - 36
        ))

        # text input box:
        input_color = INPUT_ACTIVE_COLOR if self.input_active else INPUT_COLOR
        pygame.draw.rect(self.screen, input_color, self.input_rect, border_radius=6)
        name_surface = self.font_input.render(self.player_name, True, (0, 0, 0))
        self.screen.blit(name_surface, (self.input_rect.x + 10, self.input_rect.y + 10))

        # cursor blinks when text input is active:
        if self.input_active:
            cursor_x = self.input_rect.x + 10 + name_surface.get_width() + 2
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(cursor_x, self.input_rect.y + 8, 2, 28))

        # start game button:
        mx, my = pygame.mouse.get_pos()
        start_color = BUTTON_HOVER_COLOR if self.start_rect.collidepoint(mx, my) else BUTTON_COLOR
        pygame.draw.rect(self.screen, start_color, self.start_rect, border_radius=6)
        start_label = self.font_button.render("Start Game", True, TEXT_COLOR)
        self.screen.blit(start_label, (
            self.start_rect.centerx - start_label.get_width() // 2,
            self.start_rect.centery - start_label.get_height() // 2
        ))

        # exit program button:
        exit_color = BUTTON_HOVER_COLOR if self.exit_rect.collidepoint(mx, my) else BUTTON_COLOR
        pygame.draw.rect(self.screen, exit_color, self.exit_rect, border_radius=6)
        exit_label = self.font_button.render("Exit", True, TEXT_COLOR)
        self.screen.blit(exit_label, (self.exit_rect.centerx - exit_label.get_width() // 2,
            self.exit_rect.centery - exit_label.get_height() // 2
        ))

        pygame.display.flip()