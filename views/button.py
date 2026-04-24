import pygame

BUTTON_COLOR = (20, 20, 20)
BUTTON_HOVER_COLOR = (50, 50, 50)
BUTTON_DISABLED_COLOR = (60, 60, 60)
TEXT_COLOR = (240, 240, 240)
TEXT_DISABLED_COLOR = (120, 120, 120)

class Button:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.enabled = False  # disabled by default until game logic enables them
        self.font = pygame.font.SysFont(None, 28)

    def draw(self, screen):
        # pick colors based on state
        if not self.enabled:
            color = BUTTON_DISABLED_COLOR
            text_color = TEXT_DISABLED_COLOR
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            color = BUTTON_HOVER_COLOR
            text_color = TEXT_COLOR
        else:
            color = BUTTON_COLOR
            text_color = TEXT_COLOR

        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        label_surface = self.font.render(self.label, True, text_color)
        label_x = self.rect.centerx - label_surface.get_width() // 2
        label_y = self.rect.centery - label_surface.get_height() // 2
        screen.blit(label_surface, (label_x, label_y))

    def is_clicked(self, mx, my):
        return self.enabled and self.rect.collidepoint(mx, my)