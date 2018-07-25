# !=====! IMMUTABLE CONSTANTS !=====!

# ( width or x, height or y)
SCREEN_SIZE = (1960, 1080)
PIXEL_SZ = 5  # the most base unit of the game.
BLOCK_SZ = 10*PIXEL_SZ  # the size of the block in game pixel :: square
MAIN_LOOP = True
GAME_BOX = ((0, 0), SCREEN_SIZE)
CHARACTER_BOX = (9, 15)  # follows the proportion of 3:5
TERRAIN_FULLBOX = (500, 250)
TERRAIN_VIEWBOX = (-1, -1, 24, 41)
CHARACTER_SPEED = 5  # unit - pixels per fps

# collision
COLLISION_SZ = 2  # DEFUALT IS 2; BUT do to the fall speed I must do make the sz 2 else it would go through blocks
TP_P = -5  # Top padding
BT_P = 5  # Bottom padding
RT_P = 5  # Right padding
LT_P = -5  # Left padding

# placing and breaking
EDIT_MAX_CIRCLE = 5  # Radius; block
EDIT_PP_SIZE = 5

# jumping mechanism
FALL_SPEED = 5  # DEFUALT: 5
JUMP_SPEED = 5  # DEFUALT: 5
JUMP_HEIGHT = 16  # 16
JUMP_MAX_LEN = 181  # 180 + 1

# variable name
# direction
EAST  = 1  # Right
SOUTH = 2  # Bottom
WEST  = 3  # Left
NORTH = 4  # Top
import pygame as pyg
RIGHT_CLK = 1
LEFT_CLK = 3
# block
BLK = {
    "air": "a",
    "stone": "b"
}

COLLISION_OFS = (BLOCK_SZ, BLOCK_SZ)

# OPTIONS:
KEY_VALUE = {

}

# shorten from GAME_KEYS
GK = {
    "right": ["d", "pyg.K_d"],
    "left": ["a", "pyg.K_a"],
    "jump": ["w", "pyg.K_w"],
    "sneak": ["s", "pyg.K_s"],
    "place": [3, "3"],
    "break": [1, "1"],
}