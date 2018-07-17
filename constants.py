# ( width or x, height or y)
SCREEN_SIZE = (1960, 1080)
PIXEL_SZ = 5  # the most base unit of the game.
BLOCK_SZ = 10*PIXEL_SZ  # the size of the block in game pixel :: square
MAIN_LOOP = True
GAME_BOX = ((0, 0), SCREEN_SIZE)
CHARACTER_BOX = (9, 12)  # follows the proportion of 3:4
TERRAIN_FULLBOX = (500, 250)
TERRAIN_VIEWBOX = (-1, -1, 25, 40)
VIEWBOX_SMOOTHER = 5  # pixels
EAST  = 1  # Right
SOUTH = 2  # Bottom
WEST  = 3  # Left
NORTH = 4  # Top
