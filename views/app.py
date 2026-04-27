import sys
import pygame
from game.game import Game
from views.hand_view import HandView
from views.pile_view import PileView
from views.bin_view import BinView
from views.button import Button
from views.menu_view import MenuView
from views.score_view import ScoreView
from views.customize_view import CustomizeView

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FELT_COLOR = "#0B5D3B"

CARD_WIDTH = 80
CARD_HEIGHT = 110


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = "menu"
        self.round_over_msg = ""
        self.round_over_points = 0
        self.play_again_button = Button(WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT // 2 + 40, 120, 45, "Play again")
        self.quit_button = Button(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 + 40, 120, 45, "Quit")

        # pre-game menu view:
        self.menu_view = MenuView(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT)

        # game-related attributes that initialize when game starts:
        self.game = None
        self.customize_view = CustomizeView(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.hand_view = None
        self.pile_view = None
        self.bin_view = None
        self.score_view = None
        self.knock_button = None
        self.gin_button = None
        self.all_sprites = None
        self.dragging_card = None
        self.drag_source = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def _start_game(self, player_name):
        self.game = Game(player_name)
        self.all_sprites = pygame.sprite.Group()
        self.hand_view = HandView(WINDOW_HEIGHT, self.game.player)
        self.pile_view = PileView(self.screen, self.game.deck, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.bin_view = BinView(self.screen, self.game.player)
        self.score_view = ScoreView(self.screen, self.game.player, WINDOW_WIDTH)

        self.knock_button = Button(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 80, 90, 40, "Knock")
        self.gin_button = Button(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 80, 90, 40, "Gin!")

        for card in self.game.player.hand:
            self.all_sprites.add(card)
        self.hand_view.reposition()
        self.scene = "game"

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # MOUSEBUTTON_DOWN
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if self.game.phase == "draw":
                    stock_rect = self.pile_view.stock_rect()
                    if stock_rect.collidepoint(mx, my):
                        card = self.game.draw_from_stock()
                        if card:
                            self.all_sprites.add(card)
                            self.hand_view.reposition()
                            return

                    discard_rect = self.pile_view.discard_rect()
                    if discard_rect.collidepoint(mx, my):
                        card = self.game.draw_from_discard()
                        if card:
                            self.all_sprites.add(card)
                            self.hand_view.reposition()
                            return

                card = self.hand_view.card_at(mx, my)
                if card:
                    self.dragging_card = card
                    self.drag_source = "hand"
                    self.drag_offset_x = mx - card.rect.x
                    self.drag_offset_y = my - card.rect.y
                else:
                    card, group_name = self.bin_view.card_at(mx, my)
                    if card:
                        self.dragging_card = card
                        self.drag_source = "bin"
                        self.drag_offset_x = mx - card.rect.x
                        self.drag_offset_y = my - card.rect.y
                        self.all_sprites.add(card)

                if self.knock_button.is_clicked(mx, my):
                    result, points = self.game.handle_knock(self.game.cpu)
                    self.round_over_msg = result
                    self.round_over_points = points
                    self.scene = "round_over"
                    self.dragging_card = None
                    self.drag_source = None
                    return

                if self.gin_button.is_clicked(mx, my):
                    result, points = self.game.handle_gin(self.game.cpu)
                    self.round_over_msg = result
                    self.round_over_points = points
                    self.scene = "round_over"
                    self.dragging_card = None
                    self.drag_source = None
                    return

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_card:
                    mx, my = event.pos
                    self.dragging_card.rect.x = mx - self.drag_offset_x
                    self.dragging_card.rect.y = my - self.drag_offset_y

            # MOUSEBUTTON_UP
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                if self.dragging_card:
                    discard_rect = self.pile_view.discard_rect()

                    if self.bin_view.is_runs_drop(self.dragging_card.rect):
                        self.game.player.move_to_group(self.dragging_card, "runs")
                        self.all_sprites.remove(self.dragging_card)
                        self.hand_view.reposition()

                    elif self.bin_view.is_sets_drop(self.dragging_card.rect):
                        self.game.player.move_to_group(self.dragging_card, "sets")
                        self.all_sprites.remove(self.dragging_card)
                        self.hand_view.reposition()

                    elif discard_rect.colliderect(self.dragging_card.rect):
                        success = self.game.discard_card(self.dragging_card)
                        if success:
                            self.dragging_card.rect.x = discard_rect.x
                            self.dragging_card.rect.y = discard_rect.y
                            self.all_sprites.remove(self.dragging_card)
                            self.hand_view.reposition()

                    else:
                        if self.drag_source == "bin":
                            self.game.player.move_to_hand(self.dragging_card)
                            # self.all_sprites.add(self.dragging_card)

                        if self.dragging_card in self.game.player.hand:
                            old_index = self.game.player.hand.index(self.dragging_card)
                            new_index = self.hand_view.index_at(mx)
                            self.game.player.hand.pop(old_index)
                            self.game.player.hand.insert(new_index, self.dragging_card)
                            self.hand_view.reposition()

                    self.dragging_card = None
                    self.drag_source = None

    def _draw_table(self):
        self.screen.fill(FELT_COLOR)

    def _draw_round_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(0, 0, 520, 260)
        panel.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        pygame.draw.rect(self.screen, (30, 30, 30), panel, border_radius=12)
        pygame.draw.rect(self.screen, (220, 220, 220), panel, 2, border_radius=12)

        font = pygame.font.SysFont(None, 48)
        small = pygame.font.SysFont(None, 32)
        title = font.render("Round Over", True, (240, 240, 240))
        msg = small.render(f"{self.round_over_msg} (+{self.round_over_points})", True, (240, 240, 240))

        self.screen.blit(title, (panel.x + 30, panel.y + 30))
        self.screen.blit(msg, (panel.x + 30, panel.y + 95))

        self.play_again_button.draw(self.screen)
        self.quit_button.draw(self.screen)



    def _update_buttons(self):
        if self.game.phase == "discard":
            deadwood = self.game.player.deadwood_val()
            self.knock_button.enabled = deadwood <= 10
            self.gin_button.enabled = deadwood == 0
        else:
            self.knock_button.enabled = False
            self.gin_button.enabled = False

    def run(self):
        while self.running:
            if self.scene == "menu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if not self.customize_view.handle_event(event):
                        result = self.menu_view.handle_event(event)
                        if result == "start":
                            self._start_game(self.menu_view.player_name.strip())
                        elif result == "exit":
                            self.running = False
                        elif result == "customize":
                            self.customize_view.visible = True
                self.menu_view.draw()
                self.customize_view.draw()
                pygame.display.flip()

            elif self.scene == "game":
                self._handle_events()
                self._update_buttons()
                self._draw_table()
                self.all_sprites.draw(self.screen)
                self.pile_view.draw()
                self.bin_view.draw(self.dragging_card)
                self.score_view.draw()
                self.knock_button.draw(self.screen)
                self.gin_button.draw(self.screen)
                pygame.display.flip()

            elif self.scene == "round_over":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = event.pos
                        if self.play_again_button.is_clicked(mx, my):
                            self._start_game(self.game.player.name)
                        elif self.quit_button.is_clicked(mx, my):
                            self.running = False


                self._draw_table()
                self.all_sprites.draw(self.screen)
                self.pile_view.draw()
                self.bin_view.draw(None)
                self.score_view.draw()

                self._draw_round_over()
                pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()