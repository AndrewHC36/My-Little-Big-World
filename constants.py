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
COLLISION_SZ = 2  # DEFUALT IS 2; BUT do to the fall speed I must do make the sz 2 else it would go through blocks

FALL_SPEED = 3
GRAVITY = 5

# variable name
# direction
EAST  = 1  # Right
SOUTH = 2  # Bottom
WEST  = 3  # Left
NORTH = 4  # Top
# block
B_AIR = "a"
B_STONE = "b"

COLLISION_OFS = (BLOCK_SZ, BLOCK_SZ)

# **DEBUGGING**
SHOW_PLAYER_COLLISION = False
