import pygame

PANEL_COLOR = (20, 20, 20)
TEXT_COLOR = (240, 240, 240)
LABEL_COLOR = (180, 180, 180)
DEADWOOD_COLOR = (200, 80, 80)
MARGIN = 20
PANEL_WIDTH = 200
PANEL_HEIGHT = 120


class ScoreView:
    def __init__(self, screen, player, window_width):
        self.screen = screen
        self.player = player

        self.font_name = pygame.font.SysFont("Georgia", 20, bold=True)
        self.font_label = pygame.font.SysFont("Georgia", 16)
        self.font_value = pygame.font.SysFont("Georgia", 20)

        self.panel_rect = pygame.Rect(
            window_width - PANEL_WIDTH - MARGIN,
            MARGIN,
            PANEL_WIDTH,
            PANEL_HEIGHT,
        )

    def draw(self):
        # draw panel background:
        pygame.draw.rect(self.screen, PANEL_COLOR, self.panel_rect, border_radius=8)

        # player name:
        name = self.font_name.render(self.player.name, True, TEXT_COLOR)
        self.screen.blit(name, (self.panel_rect.x + 12, self.panel_rect.y + 12))

        # score:
        score_label = self.font_label.render("Score", True, LABEL_COLOR)
        score_value = self.font_value.render(str(self.player.score), True, TEXT_COLOR)
        self.screen.blit(score_label, (self.panel_rect.x + 12, self.panel_rect.y + 44))
        self.screen.blit(score_value, (self.panel_rect.right - score_value.get_width() - 12, self.panel_rect.y + 44))

        # deadwood:
        deadwood = self.player.deadwood_val()
        deadwood_label = self.font_label.render("Deadwood", True, LABEL_COLOR)
        deadwood_value = self.font_label.render(str(deadwood), True, DEADWOOD_COLOR)
        self.screen.blit(deadwood_label, (self.panel_rect.x + 12, self.panel_rect.y + 76))
        self.screen.blit(deadwood_value,
                         (self.panel_rect.right - deadwood_value.get_width() - 12, self.panel_rect.y + 76))
