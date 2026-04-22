from views.gui import start_gui

def print_menu():
    print("\t\tGIN RUMMY\t\t")
    print("\t1. New Game")
    print("\t2. Rules")
    print("\t3. Quit")

def main():
    while True:
        print_menu()
        choice = input("> ").strip()
        if choice == "1":
            start_gui()
        elif choice == "2":
            print("Print the rules here...")
        elif choice == "3":
            print("Quitting game...")
            break

        for ci, card in enumerate(stack):
            r = pygame.Rect(x + ci * STACK_X_SPACING, y, CARD_WIDTH, CARD_HEIGHT)
            rects.append((si, ci, card, r))

        x = x + w + STACK_GAP

    return rects



name = input("Enter your name: ")
player = Player(name, is_human=True)
deck = Deck()
hand = deck.deal(10)
hand.sort()
player.set_hand(hand)

deck.discard_card(deck.draw_card())

images = load_card_images(player.hand)

for k in list(images.keys()):
    images[k] = pygame.transform.smoothscale(images[k], (CARD_WIDTH, CARD_HEIGHT))

drag_i = None
drag_card = None
drag_source = None
drag_offset = (0,0)

#pygame - newbie guide to pygame, pygame sprites
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drag_card = None
            drag_source = None
            drag_i = None
            mx, my = event.pos
            drop_pos = (mx, my)
            for si, ci, card, r in bin_card_rects(player.groups["runs"], RUNS_BIN):
                if r.collidepoint(mx, my):
                    drag_source = ("runs", si, ci)
                    drag_card = card
                    drag_offset = (mx - r.x, my - r.y)
                    break

            if drag_card is None:
                for si, ci, card, r in bin_card_rects(player.groups["sets"], SETS_BIN):
                    if r.collidepoint(mx, my):
                        drag_source = ("sets", si, ci)
                        drag_card = card
                        drag_offset = (mx - r.x, my - r.y)
                        break
            if drag_card is not None:
                continue

            if DECK_RECT.collidepoint(mx, my) and len(player.hand) == 10:
                card = deck.draw_card()
                player.add_card(card)

                if str(card) not in images:
                    images[str(card)] = pygame.transform.smoothscale(pygame.image.load(card_file(card)).convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
                continue
            if len(player.hand) == 11:
                idx = hand_index_at(mx, my, player)
                if idx is not None:
                    card = player.hand.pop(idx)
                    deck.discard_card(card)
                    continue
            if len(player.hand) == 10:
                if DISCARD_RECT.collidepoint(mx, my) and deck.top_discard() is not None:
                    card = deck.take_discard()
                    player.add_card(card)
                    continue


            n = len(player.hand)
            for i in range(n - 1, -1, -1):
                r = deadwood_slot_rect(i, n)
                if r.collidepoint(mx, my):
                    drag_i = i
                    drag_offset = (mx -r.x, my - r.y)
                    break

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mx, my = event.pos

            if drag_card is not None and drag_source is not None:
                if DEADWOOD_BIN.collidepoint(mx, my):
                    group, si, ci = drag_source
                    player.groups[group][si].pop(ci)
                    if len(player.groups[group][si]) == 0:
                        player.groups[group].pop(si)
                    player.hand.append(drag_card)
                drag_source = None
                drag_card = None
                continue

            if drag_i is None:
                continue

            drop_pos = (mx, my)

            from_i = drag_i
            dragged_card = player.hand[from_i]
            drag_i = None


            if str(dragged_card) not in images:
                images[str(dragged_card)] = pygame.transform.smoothscale(pygame.image.load(card_file(dragged_card)).convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))

            if RUNS_BIN.collidepoint(drop_pos):
                player.move_to_group(dragged_card, "runs")
                continue
            elif SETS_BIN.collidepoint(drop_pos):
                player.move_to_group(dragged_card, "sets")
                continue


            to_i = deadwood_drop_index(mx, len(player.hand))
            player.move_card(from_i, to_i)




    screen.fill((20, 120, 60))
    screen.blit(deck_img, DECK_RECT)

    top = deck.top_discard()
    if top is not None:
        if str(top) not in images:
            images[str(top)] = pygame.transform.smoothscale(pygame.image.load(card_file(top)).convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        screen.blit(images[str(top)], DISCARD_RECT)

    pygame.draw.rect(screen, (30, 30, 30), RUNS_BIN, 2)
    pygame.draw.rect(screen, (30, 30, 30), SETS_BIN, 2)
    pygame.draw.rect(screen, (30, 30, 30), DEADWOOD_BIN,2)

    draw_stacks_in_bin(screen, player.groups["runs"], RUNS_BIN, images)
    draw_stacks_in_bin(screen, player.groups["sets"], SETS_BIN, images)

    runs_label = label_font.render("RUNS", True, (240, 240, 240))
    sets_label = label_font.render("SETS", True, (240, 240, 240))
    deadwood_label = label_font.render("DEADWOOD", True, (240, 240, 240))

    screen.blit(runs_label, (RUNS_BIN.x + 10, RUNS_BIN.y + 8))
    screen.blit(sets_label, (SETS_BIN.x + 10, SETS_BIN.y + 8))
    screen.blit(deadwood_label, (DEADWOOD_BIN.x + 10, DEADWOOD_BIN.y + 8))

    if drag_card is not None:
        mx, my = pygame.mouse.get_pos()
        screen.blit(images[str(drag_card)], (mx - drag_offset[0], my - drag_offset[1]))

    if drag_i is not None:
        mx, my = pygame.mouse.get_pos()
        if RUNS_BIN.collidepoint(mx,my):
            pygame.draw.rect(screen, (200,200,60), RUNS_BIN, 3)
        elif SETS_BIN.collidepoint(mx,my):
            pygame.draw.rect(screen, (200,200,60), SETS_BIN, 3)
        elif DEADWOOD_BIN.collidepoint(mx,my):
            pygame.draw.rect(screen, (200,200,60), DEADWOOD_BIN, 3)



    n = len(player.hand)
    mx, my = pygame.mouse.get_pos()
    order = list(range(n))

    if drag_i is not None:
        hi = deadwood_drop_index(mx, n)
        idx = order.pop(drag_i)
        order.insert(hi, idx)
        dragged_card = player.hand[drag_i]
    else:
        dragged_card = None

    for slot_i, card_i in enumerate(order):
        card = player.hand[card_i]
        r = deadwood_slot_rect(slot_i,n)
        if dragged_card is not None and card is dragged_card:
            continue
        screen.blit(images[str(card)], r)

    if dragged_card is not None:
        screen.blit(images[str(dragged_card)], (mx - drag_offset[0], my - drag_offset[1]))

    pygame.display.flip()
    clock.tick(60)

