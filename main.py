"""
Andrew Shen's << My Little Big World >> game
Created on [ 2018-7-12 9:00 AM ]

"""

import pygame as pyg
from constants import *
import lib as lb
import gameData as gd
import ctypes  # for the sake of stretching on high PPI screen
ctypes.windll.user32.SetProcessDPIAware()

#WORLD_NAME_FILE_INPUT = input("ENTER FILE NAME WITH FILE EXTENSION: ")
#myWorld = lb.WorldDt(WORLD_NAME_FILE_INPUT)
#data = myWorld.read()

# ( width or x, height or y)                                    _
# the point of origin is at the most top left corner pixel --> |

WORLD_RTIME = (True, 2018, 5, 15, 7, 30, 1)  #
WORLD_GTIME = 0  # 0 - 240000 unit - tps
WORLD_NAME = "Testing World"
WORLD_DATA = ""
WORLD_SIZE = (500, 250)
LPS = 20  # Lighting Update / sec
TPS = 10  # Ticks           / sec
FPS = 100  # Frames          / sec   this is the base unit of speed
SPEED = 5  # unit - pixels per fps
GRAVITY = 5  # unit - pixels per fps
TITLE = "My Little Big World - {} ".format(WORLD_NAME)

pyg.init()
win = pyg.display.set_mode((0,0), pyg.FULLSCREEN)
clock = pyg.time.Clock()
pyg.display.set_caption(TITLE)

ON_KEY = []
CHARACTER_NAME = ""
CHARACTER_POS = [SCREEN_SIZE[1]//2-CHARACTER_BOX[1]*PIXEL_SZ//2, SCREEN_SIZE[0]//2-CHARACTER_BOX[0]*PIXEL_SZ//2]  # The unit is pixel CHARACTER ALWAYS @ CENTER
TERRAIN_POS = [0, 0]  # The unit is pixel and THE POS OF TERRAIN. Starts @ very top-left corner
TERRAIN_OFFSET = [10, 10]  # Not techincally offset its more like the border of the viewbox
TERRAIN_DATA = gd.terrain
TERRAIN_BLOCK = []
CHARACTER_STATE = ""  # walkingLTa1, walkingRTa1, sneakLT, etc. etc.
RATE = [LPS, TPS, FPS]
player = lb.Character(win, CHARACTER_POS, CHARACTER_BOX, lb.hexTOrgb(gd.dt))
terrain = lb.Terrain(win, TERRAIN_VIEWBOX, gd.terrain, TERRAIN_BLOCK)
while MAIN_LOOP:
    win.fill((0, 0, 0))
    TERRAIN_BLOCK = [TERRAIN_DATA[i][0+TERRAIN_OFFSET[1]:TERRAIN_VIEWBOX[2]+TERRAIN_OFFSET[1]] for i in range(0+TERRAIN_OFFSET[0],TERRAIN_VIEWBOX[3]+TERRAIN_OFFSET[0])]
    if "w" in ON_KEY: TERRAIN_POS[1] += SPEED  # UP - Jump
    if "a" in ON_KEY: TERRAIN_POS[0] += SPEED  # LEFT - Go left
    if "s" in ON_KEY: TERRAIN_POS[1] -= SPEED  # DOWN - Sneak            <--         MAKESHIFT <--
    if "d" in ON_KEY: TERRAIN_POS[0] -= SPEED  # RIGHT - Go right
    if "_" in ON_KEY: TERRAIN_POS[1] += SPEED
    if "^" in ON_KEY: pass  # to 's'
    for event in pyg.event.get():
        if event.type == pyg.QUIT: MAIN_LOOP = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE: MAIN_LOOP = False
            if event.key == pyg.K_w: ON_KEY.append("w")
            if event.key == pyg.K_a: ON_KEY.append("a")
            if event.key == pyg.K_s: ON_KEY.append("s")
            if event.key == pyg.K_d: ON_KEY.append("d")
            if event.key == pyg.K_SPACE:    ON_KEY.append("_")
            if event.key == pyg.KMOD_SHIFT: ON_KEY.append("^")
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_w: ON_KEY.remove("w")
            if event.key == pyg.K_a: ON_KEY.remove("a")
            if event.key == pyg.K_s: ON_KEY.remove("s")
            if event.key == pyg.K_d: ON_KEY.remove("d")
            if event.key == pyg.K_SPACE:    ON_KEY.remove("_")
            if event.key == pyg.KMOD_SHIFT: ON_KEY.remove("^")

    terrain.update(TERRAIN_POS, TERRAIN_BLOCK)
    try:
        terrain.display()  # this checks if the player is out of bound of terrain size
    except IndexError:
        TERRAIN_OFFSET = [5, 5]

    player.update(CHARACTER_POS)
    player.show()

    COL = player.collision(TERRAIN_BLOCK)
    if EAST in COL:
        if "d" in ON_KEY: TERRAIN_POS[0] += SPEED  # counter-acts form going down
    if SOUTH in COL:
        if "s" in ON_KEY: TERRAIN_POS[1] += SPEED  # counter-acts form going down
    if WEST in COL:
        if "a" in ON_KEY: TERRAIN_POS[0] -= SPEED  # counter-acts form going down
    if NORTH in COL:
        if "w" in ON_KEY: TERRAIN_POS[1] -= SPEED  # counter-acts form going down

    if TERRAIN_POS[0]/BLOCK_SZ >= 1.0:  # left side
        TERRAIN_OFFSET[0] -= 1
        TERRAIN_POS[0] = 0
    elif (TERRAIN_POS[0])/BLOCK_SZ <= -1.0:  # right side
        TERRAIN_OFFSET[0] += 1
        TERRAIN_POS[0] = 0
    elif (TERRAIN_POS[1])/BLOCK_SZ >= 1.0:  # top side
        TERRAIN_OFFSET[1] -= 1
        TERRAIN_POS[1] = 0
    elif (TERRAIN_POS[1])/BLOCK_SZ <= -1.0:  # bottom side
        TERRAIN_OFFSET[1] += 1
        TERRAIN_POS[1] = 0

    pyg.display.flip()
    clock.tick(FPS)

pyg.quit()
quit()

"""
Character State:
>BASIC<
walkingLTa1   -  Mandatory - Walking Animation face left frame #1  
walkingRTa1   -  Mandatory - Walking Animation face right frame #1    
walkingLTa2   -  Mandatory - Walking Animation face left frame #2  
walkingRTa2   -  Mandatory - Walking Animation face right frame #2  
walkingLTa3   -  Voluntary - Walking Animation face left frame #3  
walkingRTa3   -  Voluntary - Walking Animation face right frame #3  
sneakLTa1     -  Mandatory - Sneaking Animation face left frame #1
snakeRTa1     -  Mandatory - Sneaking Animation face right frame #1
sneakLTa2     -  Mandatory - Sneaking Animation face left frame #2
snakeRTa2     -  Mandatory - Sneaking Animation face right frame #2
sneakLTa3     -  Voluntary - Sneaking Animation face left frame #3
snakeRTa3     -  Voluntary - Sneaking Animation face right frame #3
jumpingLT     -  Mandatory - Jumping facing left
jumpingRT     -  Mandatory - Jumping facing right
jumpingLTo1   -  Voluntary - Jumping facing left using secondary animation
jumpingRTo2   -  Voluntary - Jumping facing right using secondary animation
fallingLT     -  Mandatory - Falling facing left
fallingRT     -  Mandatory - Falling facing right
fallingLTo1   -  Voluntary - Falling facing left using secondary animation
fallingRTo1   -  Voluntary - Falling facing right using secondary animation
>CRAFTING<

"""