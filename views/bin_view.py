import pygame
from models.meld import is_valid_run, is_valid_set

CARD_WIDTH = 80
CARD_HEIGHT = 110
BIN_MARGIN = 20
BIN_WIDTH = 400
BIN_HEIGHT = 260
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
        self._draw_cards_in_bin(self.player.groups["runs"], self.runs_rect, "runs", dragging_card)
        self._draw_cards_in_bin(self.player.groups["sets"], self.sets_rect, "sets", dragging_card)

    def _draw_cards_in_bin(self, groups, bin_rect, meld_type, dragging_card=None):
        if not groups:
            return

        valid = is_valid_run(groups) if meld_type == "runs" else is_valid_set(groups)
        indicator_color = (80, 200, 80) if valid else (200, 80, 80)
        pygame.draw.circle(self.screen, indicator_color, (bin_rect.right - 20, bin_rect.y + 20), 8)

        pad_x = 10
        pad_top = 40
        pad_y = 10

        x = bin_rect.x + pad_x
        y = bin_rect.y + pad_top
        row_h = CARD_HEIGHT + pad_y

        for group in groups:

            group_w = CARD_WIDTH + max(0, len(group) - 1) * CARD_SPACING


            if x + group_w > bin_rect.right - pad_x:
                x = bin_rect.x + pad_x
                y += row_h

            if y + CARD_HEIGHT > bin_rect.bottom - pad_y:
                break

            for ci, card in enumerate(group):
                if card is dragging_card:
                    continue
                card.rect.x = x + ci * CARD_SPACING
                card.rect.y = y
                self.screen.blit(card.image, card.rect)

            x += group_w + 20

    def card_at(self, mx, my):
        """Return the card and its group name if the mouse is over a bin card."""
        for group_name in ("runs", "sets"):
            for group in reversed(self.player.groups[group_name]):
                for card in reversed(group):
                    if card.rect.collidepoint(mx, my):
                        return card, group_name
        return None, None

    def is_runs_drop(self, rect):
        return self.runs_rect.colliderect(rect)

    def is_sets_drop(self, rect):
        return self.sets_rect.colliderect(rect)
