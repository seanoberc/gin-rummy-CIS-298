import sys
import pygame
from models.card import Card
from models.deck import Deck
from models.player import Player
from game.game import Game

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FELT_COLOR = "#0B5D3B"

CARD_WIDTH = 80
CARD_HEIGHT = 110
HAND_Y = WINDOW_HEIGHT - CARD_HEIGHT - 20  # 20px margin from bottom
HAND_SPACING = 90  # horizontal gap between each card

# constants to define center of table for stock and discard piles
CENTER_Y = WINDOW_HEIGHT // 2 - CARD_HEIGHT // 2
STOCK_X = WINDOW_WIDTH // 2 - CARD_WIDTH - 20
DISCARD_X = WINDOW_WIDTH // 2 + 20


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # drag state:
        self.dragging_card = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Pygame `Group` to hold all internal sprites used:
        self.all_sprites = pygame.sprite.Group()

        # Game class now controls all state:
        self.game = Game()

        # set up deck and player:
        # self.deck = Deck()
        # hand = deck.deal(10)  # test deck
        # self.player = Player("Human")
        # self.player.set_hand(self.deck.deal(10))

        # flip one card to begin discard pile:
        # self.deck.discard(self.deck.draw())

        # draw and discard phases:
        # self.phase = "draw"

        # load `Blue_card_back.png` image for the stockpile:
        stock_image = pygame.image.load("assets/images/Blue_card_back.png").convert_alpha()
        self.stock_image = pygame.transform.smoothscale(stock_image, (CARD_WIDTH, CARD_HEIGHT))

        # position the player hand:
        for i, card in enumerate(self.game.player.hand):
            card.rect.x = 20 + i * HAND_SPACING
            card.rect.y = HAND_Y
            self.all_sprites.add(card)

        # make a test card:
        # card = Card("Ace", "Spades")
        # card.rect.x = 100
        # card.rect.y = 100
        # self.all_sprites.add(card)      # add test card to Sprite Group
        # print(len(self.all_sprites))  # should print 1

    # helper function to govern event handling:
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # `event.button == 1` is left click (2 is middle; 3 is right button):
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos  # stores mouse cursor coords as tuple (mouse-x and mouse-y)

                # draw phase; allows only drawing cards:
                if self.game.phase == "draw":
                    stock_rect = pygame.Rect(STOCK_X, CENTER_Y, CARD_WIDTH, CARD_HEIGHT)
                    if stock_rect.collidepoint(mx, my):
                        card = self.game.draw_from_stock()
                        if card:
                            # card.rect.x = 20 + (len(self.game.player.hand) - 1) * HAND_SPACING
                            # card.rect.y = HAND_Y
                            self.all_sprites.add(card)
                            self._reposition_hand()
                            return

                    discard_rect = pygame.Rect(DISCARD_X, CENTER_Y, CARD_WIDTH, CARD_HEIGHT)
                    if discard_rect.collidepoint(mx, my):
                        card = self.game.draw_from_discard()
                        if card:
                            # card.rect.x = 20 + (len(self.game.player.hand) - 1) * HAND_SPACING
                            # card.rect.y = HAND_Y
                            self.all_sprites.add(card)
                            self._reposition_hand()
                            # self.phase = "discard"
                            return

                # discard phase; allows only dragging cards:
                # elif self.phase == "discard":
                for card in reversed(self.game.player.hand):
                    if card.rect.collidepoint(mx, my):
                        self.dragging_card = card
                        self.drag_offset_x = mx - card.rect.x
                        self.drag_offset_y = my - card.rect.y
                        break

                # `for card in reverserd()` loops through the hand in reverse order;
                # because the last card dealt sits on top, the top-most card gets checked first.
                # `rect` is a Pygame method that returns `True` if the given coords fall within that rectangle.
                # checks if the mouse click landed inside the card
                # for card in reversed(self.player.hand):
                #     if card.rect.collidepoint(mx, my):
                #         self.dragging_card = card
                #         self.drag_offset_x = mx - card.rect.x   # calculates how far from the center of the card's left edge the click occured
                #         self.drag_offset_y = my - card.rect.y
                #         break   # break (stop looking) when the top-most card is clicked

                # stock_rect = pygame.Rect(STOCK_X, CENTER_Y, CARD_WIDTH, CARD_HEIGHT)
                # if stock_rect.collidepoint(mx, my):
                #     card = self.deck.draw()
                #     self.player.add_card(card)
                #     card.rect.x = 20 + (len(self.player.hand) - 1) * HAND_SPACING
                #     card.rect.y = HAND_Y
                #     self.all_sprites.add(card)

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_card:
                    mx, my = event.pos
                    self.dragging_card.rect.x = mx - self.drag_offset_x
                    self.dragging_card.rect.y = my - self.drag_offset_y

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                if self.dragging_card:
                    # check if card is dropped on discard pile:
                    discard_rect = pygame.Rect(DISCARD_X, CENTER_Y, CARD_WIDTH, CARD_HEIGHT)

                    if discard_rect.colliderect(self.dragging_card.rect):
                        # print(f"phase: {self.game.phase}")
                        success = self.game.discard_card(self.dragging_card)
                        # print(f"discard success: {success}")
                        if success:
                            self.dragging_card.rect.x = DISCARD_X
                            self.dragging_card.rect.y = CENTER_Y
                            self.all_sprites.remove(self.dragging_card)
                            self._reposition_hand()

                    else:
                        old_index = self.game.player.hand.index(self.dragging_card)
                        new_index = self._hand_index_at(mx)
                        # i = self.player.hand.index(self.dragging_card)
                        # self.dragging_card.rect.x = 20 + i * HAND_SPACING
                        # self.dragging_card.rect.y = HAND_Y
                        self.game.player.hand.pop(old_index)
                        self.game.player.hand.insert(new_index, self.dragging_card)
                        self._reposition_hand()

                    self.dragging_card = None

    # `_hand_index_at()` converts a mouse position into a "hand" index:
    def _hand_index_at(self, mx):
        i = (mx - 20) // HAND_SPACING  # divide x-pos. by spacing to get slot index
        return max(0, min(i, len(self.game.player.hand) - 1))  # prevents position from going below 0 or going above last card

    def _reposition_hand(self):
        for i, card in enumerate(self.game.player.hand):
            card.rect.x = 20 + i * HAND_SPACING
            card.rect.y = HAND_Y

    # helper function to draw table:
    def _draw_table(self):
        self.screen.fill(FELT_COLOR)

    # helper function to draw stockpile:
    def _draw_piles(self):
        self.screen.blit(self.stock_image, (STOCK_X, CENTER_Y))

        # draw top of discard pile (face-up):
        top = self.game.deck.top_discard()
        if top is not None:
            self.screen.blit(top.image, (DISCARD_X, CENTER_Y))

    def run(self):
        while self.running:
            self._handle_events()
            self._draw_table()
            self.all_sprites.draw(self.screen)
            self._draw_piles()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
