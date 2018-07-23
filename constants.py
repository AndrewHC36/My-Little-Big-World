# !=====! IMMUTABLE CONSTANTS !=====!

# ( width or x, height or y)
SCREEN_SIZE = (1960, 1080)
PIXEL_SZ = 5  # the most base unit of the game.
BLOCK_SZ = 10*PIXEL_SZ  # the size of the block in game pixel :: square
MAIN_LOOP = True
GAME_BOX = ((0, 0), SCREEN_SIZE)
CHARACTER_BOX = (9, 15)  # follows the proportion of 3:5
TERRAIN_FULLBOX = (500, 250)
TERRAIN_VIEWBOX = (-1, -1, 25, 40)
VIEWBOX_SMOOTHER = 5  # pixels

# collision
COLLISION_SZ = 2  # DEFUALT IS 2; BUT do to the fall speed I must do make the sz 2 else it would go through blocks
TOP_PAD = 4
BOT_PAD = -4
RGT_PAD = 5
LFT_PAD = -11

# placing and breaking
RAYCAST_LINE_DEG = 50  # Degree; number
RAYCAST_MAX_CIRCLE = 8  # Radius; block
RAYCAST_PP_SIZE = 5

# jumping mechanism
FALL_SPEED = 5
JUMP_SPEED = 5
JUMP_HEIGHT = 15
JUMP_MAX_LEN = 181

# variable name
# direction
EAST  = 1  # Right
SOUTH = 2  # Bottom
WEST  = 3  # Left
NORTH = 4  # Top

RIGHT_CLK = 1
LEFT_CLK = 3
# block
B_AIR = "a"
B_STONE = "b"

COLLISION_OFS = (BLOCK_SZ, BLOCK_SZ)

# **DEBUGGING**
SHOW_PLAYER_COLLISION = False
PLAYER_FREE_MOVE = False
SHOW_RAYCAST = True
