import sys
import pygame
from game.game import Game
from views.hand_view import HandView

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FELT_COLOR = "#0B5D3B"

CARD_WIDTH = 80
CARD_HEIGHT = 110

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
        self.hand_view = HandView(WINDOW_HEIGHT, self.game.player)

        stock_image = pygame.image.load("assets/images/Blue_card_back.png").convert_alpha()
        self.stock_image = pygame.transform.smoothscale(stock_image, (CARD_WIDTH, CARD_HEIGHT))

        # position the player hand:
        for card in self.game.player.hand:
            self.all_sprites.add(card)
        self.hand_view.reposition()

    # helper function to govern event handling:
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if self.game.phase == "draw":
                    stock_rect = pygame.Rect(STOCK_X, CENTER_Y, CARD_WIDTH, CARD_HEIGHT)
                    if stock_rect.collidepoint(mx, my):
                        card = self.game.draw_from_stock()
                        if card:
                            self.all_sprites.add(card)
                            self.hand_view.reposition()
                            return

                    discard_rect = pygame.Rect(DISCARD_X, CENTER_Y, CARD_WIDTH, CARD_HEIGHT)
                    if discard_rect.collidepoint(mx, my):
                        card = self.game.draw_from_discard()
                        if card:
                            self.all_sprites.add(card)
                            self.hand_view.reposition()
                            return

                card = self.hand_view.card_at(mx, my)
                if card:
                    self.dragging_card = card
                    self.drag_offset_x = mx - card.rect.x
                    self.drag_offset_y = my - card.rect.y

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_card:
                    mx, my = event.pos
                    self.dragging_card.rect.x = mx - self.drag_offset_x
                    self.dragging_card.rect.y = my - self.drag_offset_y

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                if self.dragging_card:
                    discard_rect = pygame.Rect(DISCARD_X, CENTER_Y, CARD_WIDTH, CARD_HEIGHT)

                    if discard_rect.colliderect(self.dragging_card.rect):
                        success = self.game.discard_card(self.dragging_card)
                        if success:
                            self.dragging_card.rect.x = DISCARD_X
                            self.dragging_card.rect.y = CENTER_Y
                            self.all_sprites.remove(self.dragging_card)
                            self.hand_view.reposition()
                    else:
                        old_index = self.game.player.hand.index(self.dragging_card)
                        new_index = self.hand_view.index_at(mx)
                        self.game.player.hand.pop(old_index)
                        self.game.player.hand.insert(new_index, self.dragging_card)
                        self.hand_view.reposition()

                    self.dragging_card = None

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
