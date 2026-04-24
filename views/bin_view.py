import pygame

CARD_WIDTH = 80
CARD_HEIGHT = 110
BIN_MARGIN = 20
BIN_WIDTH = 400
BIN_HEIGHT = 200
BIN_BORDER_COLOR = (30, 30, 30)
BIN_LABEL_COLOR = (240, 240, 240)
CARD_SPACING = 30


class BinView:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont(None, 32)

        # runs-bin placed at top left:
        self.runs_rect = pygame.Rect(BIN_MARGIN, BIN_MARGIN, BIN_WIDTH, BIN_HEIGHT)

        # sets-bin placed below runs-bin:
        self.sets_rect = pygame.Rect(BIN_MARGIN, BIN_MARGIN + BIN_HEIGHT + BIN_MARGIN, BIN_WIDTH, BIN_HEIGHT)

    # draw runs-bin:
    def draw(self):
        pygame.draw.rect(self.screen, BIN_BORDER_COLOR, self.runs_rect, 2)
        runs_label = self.font.render("RUNS", True, BIN_LABEL_COLOR)
        self.screen.blit(runs_label, (self.runs_rect.x + 10, self.runs_rect.y + 8))

        # draw sets-bin:
        pygame.draw.rect(self.screen, BIN_BORDER_COLOR, self.sets_rect, 2)
        sets_label = self.font.render("SETS", True, BIN_LABEL_COLOR)
        self.screen.blit(sets_label, (self.sets_rect.x + 10, self.sets_rect.y + 8))

        # draw cards inside each bin:
        self._draw_cards_in_bin(self.player.groups["runs"], self.runs_rect)
        self._draw_cards_in_bin(self.player.groups["sets"], self.sets_rect)