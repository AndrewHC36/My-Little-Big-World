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
FPS = 100  # Frames          / sec   this is the base unit of speed
TITLE = "My Little Big World - {} ".format(WORLD_NAME)

GAME_OPTIONS = {
    "AUTO-JUMP": False
}

pyg.init()
win = pyg.display.set_mode((0,0), pyg.FULLSCREEN)
clock = pyg.time.Clock()
pyg.display.set_caption(TITLE)


CHARACTER_NAME = ""
CHARACTER_POS = [SCREEN_SIZE[1]//2-CHARACTER_BOX[1]*PIXEL_SZ//2, SCREEN_SIZE[0]//2-CHARACTER_BOX[0]*PIXEL_SZ//2]  # The unit is pixel CHARACTER ALWAYS @ CENTER
CHARACTER_STATE = ""  # walkingLTa1, walkingRTa1, sneakLT, etc. etc.
CHARACTER_JUMP = False
CHARACTER_JUMP_LEN = 0

TERRAIN_POS = [0, 0]  # The unit is pixel and THE POS OF TERRAIN. Starts @ very top-left corner
TERRAIN_OFFSET = [10, 10]  # Not techincally offset its more like the border of the viewbox
TERRAIN_DATA = gd.terrain
PLAYER_CURRENT_BLOCK = "b"

ON_KEY, COLLISION, TERRAIN_BLOCK = [], [], []
MAIN_PLAYER = lb.Character(win, CHARACTER_POS, TERRAIN_POS, CHARACTER_BOX, lb.hexTOrgb(gd.dt), TERRAIN_OFFSET)
TERRAIN = lb.Terrain(win, TERRAIN_VIEWBOX, gd.terrain, TERRAIN_BLOCK)

while MAIN_LOOP:
    win.fill((0, 0, 0))
    TERRAIN_BLOCK = [TERRAIN_DATA[i][0+TERRAIN_OFFSET[1]:TERRAIN_VIEWBOX[2]+TERRAIN_OFFSET[1]] for i in range(0+TERRAIN_OFFSET[0],TERRAIN_VIEWBOX[3]+TERRAIN_OFFSET[0])]

    for event in pyg.event.get():
        if event.type == pyg.QUIT: MAIN_LOOP = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE: MAIN_LOOP = False
            if event.key == eval(GK["jump"][1]) and SOUTH in COLLISION: ON_KEY.append(GK["jump"][0]); CHARACTER_JUMP = True
            if event.key == eval(GK["left"][1]): ON_KEY.append(GK["left"][0])
            #if event.key == eval(GK["sneak"][1]) or event.key: CHARACTER_BOX = MAIN_PLAYER.sneak()
            if event.key == eval(GK["right"][1]): ON_KEY.append(GK["right"][0])
        elif event.type == pyg.KEYUP:
            if event.key == eval(GK["left"][1]): ON_KEY.remove(GK["left"][0])
            #if event.key == eval(GK["sneak"][1]): CHARACTER_BOX = MAIN_PLAYER.sneak()
            if event.key == eval(GK["right"][1]): ON_KEY.remove(GK["right"][0])
            if event.key == eval(GK["jump"][1]) and ON_KEY.count(GK["jump"][0]) > 0: ON_KEY.remove(GK["jump"][0])
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == eval(GK["place"][1]): ON_KEY.append(GK["place"][0])
            if event.button == eval(GK["break"][1]): ON_KEY.append(GK["break"][0])
        elif event.type == pyg.MOUSEBUTTONUP:
            if event.button == eval(GK["place"][1]): ON_KEY.remove(GK["place"][0])
            if event.button == eval(GK["break"][1]): ON_KEY.remove(GK["break"][0])

    TERRAIN.update(TERRAIN_POS, TERRAIN_BLOCK)
    MAIN_PLAYER.update(TERRAIN_POS, TERRAIN_OFFSET)
    TERRAIN.display()
    MAIN_PLAYER.show()
    if GK["place"][0] in ON_KEY or GK["break"][0] in ON_KEY:
        EDIT = MAIN_PLAYER.edit(pyg.mouse.get_pos(), ON_KEY, PLAYER_CURRENT_BLOCK)
        if EDIT[3]: TERRAIN_DATA[EDIT[0]+TERRAIN_OFFSET[0]][EDIT[1]+TERRAIN_OFFSET[1]] = EDIT[2]
        # saving on main list bc the terrain block resets  a self and not save it to main list, and saving block to main is time consuming

    TERRAIN_POS[1] -= FALL_SPEED
    COLLISION = MAIN_PLAYER.collision(TERRAIN_BLOCK)
    if SOUTH in COLLISION:
        TERRAIN_POS[1] += FALL_SPEED  # When it collides counter acts the fall speed
        if NORTH in COLLISION: TERRAIN_POS[1] += JUMP_SPEED+CHARACTER_SPEED+FALL_SPEED  # Error checking, more like preventing the player going down
    if NORTH in COLLISION: CHARACTER_JUMP = False;  TERRAIN_POS[1] -= JUMP_SPEED # counter-acts form going up
    if EAST in COLLISION and GK["right"][0] in ON_KEY: TERRAIN_POS[0] += CHARACTER_SPEED   # counter-acts form going right
    if WEST in COLLISION and GK["left"][0] in ON_KEY: TERRAIN_POS[0] -= CHARACTER_SPEED   # counter-acts form going left
    if TERRAIN_POS[0]/BLOCK_SZ >= 1.0:    TERRAIN_OFFSET[0] -= 1; TERRAIN_POS[0] = -CHARACTER_SPEED  # left side
    elif TERRAIN_POS[0]/BLOCK_SZ <= -1.0: TERRAIN_OFFSET[0] += 1; TERRAIN_POS[0] = -CHARACTER_SPEED  # right side
    elif TERRAIN_POS[1]/BLOCK_SZ >= 1.0:  TERRAIN_OFFSET[1] -= 1; TERRAIN_POS[1] = -CHARACTER_SPEED  # top side
    elif TERRAIN_POS[1]/BLOCK_SZ <= -1.0: TERRAIN_OFFSET[1] += 1; TERRAIN_POS[1] = -CHARACTER_SPEED  # bottom side
    if CHARACTER_JUMP: TERRAIN_POS[1] += round(m.sin(m.radians(CHARACTER_JUMP_LEN))*JUMP_HEIGHT); CHARACTER_JUMP_LEN += JUMP_SPEED  # UP - Jump
    if GK["left"][0] in ON_KEY: TERRAIN_POS[0] += CHARACTER_SPEED  # LEFT - Go lef
    # if GK["sneak"][0] in ON_KEY: TERRAIN_POS[1] -= SPEED  # DOWN - Sneak
    if GK["right"][0] in ON_KEY: TERRAIN_POS[0] -= CHARACTER_SPEED  # RIGHT - Go right
    if JUMP_MAX_LEN <= CHARACTER_JUMP_LEN: CHARACTER_JUMP = False; CHARACTER_JUMP_LEN = 0;
    if (GK["jump"][0] in ON_KEY and SOUTH in COLLISION) and GAME_OPTIONS["AUTO-JUMP"]: CHARACTER_JUMP = True  # To jump continously when pressed

    pyg.display.flip()
    clock.tick(FPS)

pyg.quit()
quit()
