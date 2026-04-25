import pygame
from models.meld import is_valid_run, is_valid_set

CARD_WIDTH = 80
CARD_HEIGHT = 110
BIN_MARGIN = 20
BIN_WIDTH = 400
BIN_HEIGHT = 200
BIN_BORDER_COLOR = (30, 30, 30)
BIN_LABEL_COLOR = (240, 240, 240)
CARD_SPACING = 30
HIGHLIGHT_COLOR = (200, 200, 60)

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
    def draw(self, dragging_card=None):
        pygame.draw.rect(self.screen, BIN_BORDER_COLOR, self.runs_rect, 2)
        runs_label = self.font.render("RUNS", True, BIN_LABEL_COLOR)
        self.screen.blit(runs_label, (self.runs_rect.x + 10, self.runs_rect.y + 8))

        # draw sets-bin:
        pygame.draw.rect(self.screen, BIN_BORDER_COLOR, self.sets_rect, 2)
        sets_label = self.font.render("SETS", True, BIN_LABEL_COLOR)
        self.screen.blit(sets_label, (self.sets_rect.x + 10, self.sets_rect.y + 8))

        # highlight bins when a card is dragged over them
        if dragging_card:
            if self.is_runs_drop(dragging_card.rect):
                pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, self.runs_rect, 3)
            elif self.is_sets_drop(dragging_card.rect):
                pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, self.sets_rect, 3)

        # draw cards inside each bin:
        self._draw_cards_in_bin(self.player.groups["runs"], self.runs_rect, "runs")
        self._draw_cards_in_bin(self.player.groups["sets"], self.sets_rect, "sets")

    def _draw_cards_in_bin(self, cards, bin_rect, meld_type):
        if not cards:
            return

        # check is current group is a valid meld:
        if meld_type == "runs":
            valid = is_valid_run(cards)
        else:
            valid = is_valid_set(cards)

        # validity indicator:
        if valid:
            indicator_color = (80, 200, 80)     # green
        else:
            indicator_color = (200, 80, 80)     # red
        pygame.draw.circle(self.screen, indicator_color, (bin_rect.right - 20, bin_rect.y + 20), 8)

        # lay cards out left to right with slight overlap
        for i, card in enumerate(cards):
            card.rect.x = bin_rect.x + 10 + i * CARD_SPACING
            card.rect.y = bin_rect.y + (bin_rect.height - CARD_HEIGHT) // 2
            self.screen.blit(card.image, card.rect)

    def card_at(self, mx, my):
        """Return the card and its group name if the mouse is over a bin card."""
        for group_name in ("runs", "sets"):
            for card in reversed(self.player.groups[group_name]):
                if card.rect.collidepoint(mx, my):
                    return card, group_name
        return None, None

    def is_runs_drop(self, rect):
        return self.runs_rect.colliderect(rect)

    def is_sets_drop(self, rect):
        return self.sets_rect.colliderect(rect)