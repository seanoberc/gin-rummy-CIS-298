import pygame

from models.card_sprite import load_card_images
from models.deck import Deck
from players.player import Player

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()


name = input("Enter your name: ")
player = Player(name, is_human=True)
deck = Deck()
hand = deck.deal(10)
hand.sort()
player.set_hand(hand)

images = load_card_images(hand)

#pygame - newbie guide to pygame, pygame sprites
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    y = 520
    spacing = 55
    n = len(hand)
    total_w = (n - 1) * spacing + 80
    start_x = (screen.get_width() - total_w) // 2

    screen.fill((20,120,60))
    for i, card in enumerate(hand):
        img = pygame.transform.smoothscale(images[str(card)], (80,120))
        screen.blit(img, (start_x + i * spacing, y))

    pygame.display.flip()
    clock.tick(60)

