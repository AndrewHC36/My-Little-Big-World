"""
Andrew Shen's << My Little Big World >> game
Created on [ 2018-7-12 9:00 AM ]

"""

import pygame as pyg
import math as m
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
CHARACTER_STATE = ""  # walkingLTa1, walkingRTa1, sneakLT, etc. etc.
CHARACTER_JUMP = False
CHARACTER_JUMP_LEN = 0
COLLISION = []
TERRAIN_POS = [0, 0]  # The unit is pixel and THE POS OF TERRAIN. Starts @ very top-left corner
TERRAIN_OFFSET = [10, 10]  # Not techincally offset its more like the border of the viewbox
TERRAIN_DATA = gd.terrain
TERRAIN_BLOCK = []
PLAYER_CURRENT_BLOCK = "b"
MAIN_PLAYER = lb.Character(win, CHARACTER_POS, TERRAIN_POS, CHARACTER_BOX, lb.hexTOrgb(gd.dt), TERRAIN_OFFSET)
TERRAIN = lb.Terrain(win, TERRAIN_VIEWBOX, gd.terrain, TERRAIN_BLOCK)

while MAIN_LOOP:
    win.fill((0, 0, 0))
    TERRAIN_BLOCK = [TERRAIN_DATA[i][0+TERRAIN_OFFSET[1]:TERRAIN_VIEWBOX[2]+TERRAIN_OFFSET[1]] for i in range(0+TERRAIN_OFFSET[0],TERRAIN_VIEWBOX[3]+TERRAIN_OFFSET[0])]

    for event in pyg.event.get():
        if event.type == pyg.QUIT: MAIN_LOOP = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE: MAIN_LOOP = False
            if PLAYER_FREE_MOVE:
                if event.key == pyg.K_w or event.key == pyg.K_UP: ON_KEY.append("w")
                if event.key == pyg.K_a or event.key == pyg.K_LEFT: ON_KEY.append("a")
                if event.key == pyg.K_s or event.key == pyg.K_DOWN: ON_KEY.append("s")
                if event.key == pyg.K_d or event.key == pyg.K_RIGHT: ON_KEY.append("d")
            else:
                if (event.key == pyg.K_UP or event.key == pyg.K_w) and SOUTH in COLLISION: CHARACTER_JUMP = True
                if event.key == pyg.K_a or event.key == pyg.K_LEFT: ON_KEY.append("a")
                if event.key == pyg.K_s or event.key == pyg.K_DOWN: CHARACTER_BOX = MAIN_PLAYER.sneak()
                if event.key == pyg.K_d or event.key == pyg.K_RIGHT: ON_KEY.append("d")
                if (event.key == pyg.K_UP or event.key == pyg.K_SPACE) and SOUTH in COLLISION: CHARACTER_JUMP = True
        elif event.type == pyg.KEYUP:
            if PLAYER_FREE_MOVE:
                if event.key == pyg.K_w or event.key == pyg.K_UP: ON_KEY.remove("w")
                if event.key == pyg.K_a or event.key == pyg.K_LEFT: ON_KEY.remove("a")
                if event.key == pyg.K_s or event.key == pyg.K_DOWN: ON_KEY.remove("s")
                if event.key == pyg.K_d or event.key == pyg.K_RIGHT: ON_KEY.remove("d")
            else:
                if event.key == pyg.K_a: ON_KEY.remove("a")
                if event.key == pyg.K_s: CHARACTER_BOX = MAIN_PLAYER.sneak()
                if event.key == pyg.K_d: ON_KEY.remove("d")
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == RIGHT_CLK: ON_KEY.append("1")
            if event.button == LEFT_CLK: ON_KEY.append("3")
        elif event.type == pyg.MOUSEBUTTONUP:
            if event.button == RIGHT_CLK: ON_KEY.remove("1")
            if event.button == LEFT_CLK: ON_KEY.remove("3")

    TERRAIN.update(TERRAIN_POS, TERRAIN_BLOCK)
    MAIN_PLAYER.update(TERRAIN_POS, TERRAIN_OFFSET)
    TERRAIN.display()
    MAIN_PLAYER.show()
    if "1" in ON_KEY or "3" in ON_KEY:
        if "1" in ON_KEY: RAYCAST = MAIN_PLAYER.raycast(pyg.mouse.get_pos(), LEFT_CLK, PLAYER_CURRENT_BLOCK)
        if "3" in ON_KEY: RAYCAST = MAIN_PLAYER.raycast(pyg.mouse.get_pos(), RIGHT_CLK, PLAYER_CURRENT_BLOCK)
        TERRAIN_DATA[RAYCAST[0]+TERRAIN_OFFSET[0]][RAYCAST[1]+TERRAIN_OFFSET[1]] = RAYCAST[2]
        # saving on main list bc the terrain block resets  a self and not save it to main list, and saving block to main is time consuming

    if not PLAYER_FREE_MOVE:
        TERRAIN_POS[1] -= FALL_SPEED
        COLLISION = MAIN_PLAYER.collision(TERRAIN_BLOCK)
        if SOUTH in COLLISION:
            if "s" in ON_KEY: TERRAIN_POS[1] += SPEED  # counter-acts from going down
            TERRAIN_POS[1] += FALL_SPEED  # When it collides counter acts the fall speed
            if NORTH in COLLISION: TERRAIN_POS[1] += JUMP_SPEED+SPEED  # Error checking, more like preventing the player going down
        if NORTH in COLLISION: TERRAIN_POS[1] -= JUMP_SPEED+SPEED  # counter-acts form going up
        if EAST in COLLISION and "d" in ON_KEY: TERRAIN_POS[0] += SPEED   # counter-acts form going right
        if WEST in COLLISION and "a" in ON_KEY: TERRAIN_POS[0] -= SPEED   # counter-acts form going left
    if TERRAIN_POS[0]/BLOCK_SZ >= 1.0:    TERRAIN_OFFSET[0] -= 1; TERRAIN_POS[0] = -SPEED  # left side
    elif TERRAIN_POS[0]/BLOCK_SZ <= -1.0: TERRAIN_OFFSET[0] += 1; TERRAIN_POS[0] = -SPEED  # right side
    elif TERRAIN_POS[1]/BLOCK_SZ >= 1.0:  TERRAIN_OFFSET[1] -= 1; TERRAIN_POS[1] = -SPEED  # top side
    elif TERRAIN_POS[1]/BLOCK_SZ <= -1.0: TERRAIN_OFFSET[1] += 1; TERRAIN_POS[1] = -SPEED  # bottom side

    if PLAYER_FREE_MOVE:
        if "w" in ON_KEY: TERRAIN_POS[1] += SPEED
        if "a" in ON_KEY: TERRAIN_POS[0] += SPEED
        if "s" in ON_KEY: TERRAIN_POS[1] -= SPEED
        if "d" in ON_KEY: TERRAIN_POS[0] -= SPEED
    else:
        if CHARACTER_JUMP: TERRAIN_POS[1] += round(m.sin(m.radians(CHARACTER_JUMP_LEN))*JUMP_HEIGHT); CHARACTER_JUMP_LEN += JUMP_SPEED  # UP - Jump
        if "a" in ON_KEY: TERRAIN_POS[0] += SPEED  # LEFT - Go lef
        # if "s" in ON_KEY: TERRAIN_POS[1] -= SPEED  # DOWN - Sneak
        if "d" in ON_KEY: TERRAIN_POS[0] -= SPEED  # RIGHT - Go right
        if JUMP_MAX_LEN <= CHARACTER_JUMP_LEN: CHARACTER_JUMP = False; CHARACTER_JUMP_LEN = 0;

    pyg.display.flip()
    clock.tick(FPS)

pyg.quit()
quit()
