import os

# globally tracks selected card style
#       (putting this here to avoid any circular loading)
# current options: "default" or "classic"

current_style = "default"
current_back = "blue"

ASSETS_DIR = os.path.join("assets", "images")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites", "black")
CLASSIC_DIR = os.path.join(ASSETS_DIR, "sprites", "classic")
CARD_BACK_PATH = os.path.join(ASSETS_DIR, "sprites", "Blue_card_back.png")
