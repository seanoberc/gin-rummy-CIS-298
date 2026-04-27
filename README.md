# Gin Rummy (CIS 298 Project)

## Overview

This project is a digital implementation of the card game **Gin Rummy**.  
It includes a graphical interface, turn-based gameplay, scoring, and both human and AI players.

---

## Features

- Interactive GUI with drag-and-drop card mechanics
- Modular view system (hand, bins, pile, menu, score)
- AI (CPU) player support
- Full gameplay loop (draw → meld → discard → score)
- Knock and Gin logic implemented
- Customizable card visuals
- Round-over display and scoring system

---

# Commit History / Contributions

## Sean Oberc

### Commits from Apr 24–25, 2026

- Refactored `main.py` and pulled functionality out into other files.
- Undid a Git stash.
- Fixed a bug that caused the game to crash during the discard phase.
- Moved logic from `app.py` to `game.py`.
- Created view files for the hand, bin, and pile.
- Moved functions from `app.py` to `hand_view.py`.
- Removed old functions in `app.py` that were replaced by `hand_view.py`.
- Added `pile_view.py`.
- Added `bin_view.py`.
- Added a `draw()` function to `bin_view.py`.
- Fixed `move_to_group()` in `player.py`, which was causing crashes.
- Added highlighting to bins.
- Fixed dragging cards out of bins and returning them to the player’s hand.
- Added `button.py` class to `/views`.
- Added `draw()` and `is_clicked()` functions to the button class.
- Added `menu_view.py` to handle the game’s startup menu.
- Added start and exit buttons to `menu_view.py`.
- Added a start menu with a text field for the player name.
- Added `score_view.py`.
- Modified `app.py` to use the new `score_view.py`.
- Wired up the main menu so the user’s name input displays correctly.
- Added `meld.py` to the models directory.
- Added additional card sprites and sprite-related functionality.
- Debugged and fixed alternate card faces.
- Added `handle_event()` function to `customize_view.py`.
- Added buttons to `customize_view.py`.
- Debugged the customize view.
- Fixed button spacing on the main menu.
- Cleaned up code formatting in PyCharm.

---

## David / `daviddor-umich`

### Commits from Apr 26, 2026

- Fixed meld checks and implemented score logic.
- Merged the `david` branch into the main project branch.
- Completed gin and knock handling.
- Merged the `david` branch into the main project branch.
- Added reshuffling for the draw function in `deck.py`.
- Merged the `david` branch into the main project branch.
- Completed the main gameplay loop.

---

## Max / `kstmax955`

### Commits from Apr 26–27, 2026

- Implemented AI player logic in `ai_player.py`.
- Added `is_human` parameter to the `Player` constructor.
- Added CPU player and updated turn management.
- Implemented round-over display and buttons.
- Refactored game logic for handling knock and gin.
- Refactored card drawing in bins to handle dragging.
- Refactored game round handling and removed unused code.
- Improved card management in the `Player` class.
- Refactored meld validation functions for clarity.

---

## Notes

This contribution record is based on the visible GitHub commit history. Some commits may overlap in functionality due to
branching, merging, or collaborative work.