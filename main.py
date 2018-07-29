"""
Andrew Shen's << My Little Big World >> game
Created on [ 2018-7-12 9:00 AM ]

"""

import pygame as pyg
import math as m
from constants import *
import lib as lb
import gameData as gd
import ctypes  # for the sake of stretching on 1080-1920 screen
ctypes.windll.user32.SetProcessDPIAware()

#WORLD_NAME_FILE_INPUT = input("ENTER FILE NAME WITH FILE EXTENSION: ")
#myWorld = lb.WorldDt(WORLD_NAME_FILE_INPUT)
#data = myWorld.read()

# ( width or x, height or y)                                    _
# the point of origin is at the most top left corner pixel --> |

world_name = "Testing World"
world_size = (500, 250)
FPS = 100  # Frames / sec   this is the base unit of speed
title = "My Little Big World - {} ".format(world_name)

GAME_OPTIONS = {
    "AUTO-JUMP": True
}

pyg.init()
win = pyg.display.set_mode((0,0), pyg.FULLSCREEN)
clock = pyg.time.Clock()
pyg.display.set_caption(title)


char_name = ""
char_pos = [SCREEN_SIZE[1]//2-CHARACTER_BOX[1]*PIXEL_SZ//2, SCREEN_SIZE[0]//2-CHARACTER_BOX[0]*PIXEL_SZ//2]  # The unit is pixel
char_jump = False
char_jump_len = 0
tern_pos = [0, 0]  # The unit is pixel and THE POS OF TERRAIN. Starts @ very top-left corner
tern_ofs = [10, 10]  # Not techincally offset its more like the border of the viewbox
tern_dt = gd.terrain
ply_current_blk = "b"

onKey, collision, terrainBlock = [], [], []
MAIN_PLAYER = lb.Character(win, char_pos, tern_pos, CHARACTER_BOX, lb.hexTOrgb(gd.dt))
TERRAIN = lb.Terrain(win, TERRAIN_VIEWBOX, tern_dt, TERRAIN_BLOCK)

while MAIN_LOOP:
    win.fill((0, 0, 0))
    terrainCurrent = [tern_dt[i][tern_ofs[1]:TERRAIN_VIEWBOX[2]+tern_ofs[1]] for i in range(tern_ofs[0],TERRAIN_VIEWBOX[3]+tern_ofs[0])]
    for event in pyg.event.get():
        if event.type == pyg.QUIT: MAIN_LOOP = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE: MAIN_LOOP = False
            if event.key == eval(GK["jump"][1]) and SOUTH in collision: onKey.append(GK["jump"][0]); CHARACTER_JUMP = True
            if event.key == eval(GK["left"][1]): onKey.append(GK["left"][0])
            # if event.key == eval(GK["sneak"][1]) or event.key: CHARACTER_BOX = MAIN_PLAYER.sneak()
            if event.key == eval(GK["right"][1]): onKey.append(GK["right"][0])
        elif event.type == pyg.KEYUP:
            if event.key == eval(GK["left"][1]): onKey.remove(GK["left"][0])
            # if event.key == eval(GK["sneak"][1]): CHARACTER_BOX = MAIN_PLAYER.sneak()
            if event.key == eval(GK["right"][1]): onKey.remove(GK["right"][0])
            if event.key == eval(GK["jump"][1]):
                if onKey.count(GK["jump"][0]) > 0: onKey.remove(GK["jump"][0])
                CHARACTER_JUMP = False
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == eval(GK["place"][1]): onKey.append(GK["place"][0])
            if event.button == eval(GK["break"][1]): onKey.append(GK["break"][0])
        elif event.type == pyg.MOUSEBUTTONUP:
            if event.button == eval(GK["place"][1]): onKey.remove(GK["place"][0])
            if event.button == eval(GK["break"][1]): onKey.remove(GK["break"][0])

    TERRAIN.update(tern_pos, terrainCurrent)
    MAIN_PLAYER.update(char_pos, tern_pos)
    TERRAIN.display()
    MAIN_PLAYER.show()

    if GK["place"][0] in onKey or GK["break"][0] in onKey:
        EDIT = MAIN_PLAYER.edit(pyg.mouse.get_pos(), onKey, ply_current_blk, terrainCurrent)
        if EDIT[3]: tern_dt[EDIT[0]+tern_ofs[0]][EDIT[1]+tern_ofs[1]] = EDIT[2]
        # saving on main list bc the terrain block resets itself and not save it to main list, and saving block to main is time consuming
    tern_pos[1] -= FALL_SPEED
    COLLISION = MAIN_PLAYER.collision(terrainCurrent)
    if tern_ofs[0] < 0: COLLISION.append(WEST)
    if tern_ofs[1] < 1: COLLISION.append(NORTH); print("STP")
    if tern_ofs[0]+1 >= world_size[0]: COLLISION.append(EAST); print("SOUTH")
    if tern_ofs[1] >= world_size[1]: COLLISION.append(SOUTH)
    if SOUTH in COLLISION:
        tern_pos[1] += FALL_SPEED  # When it collides counter acts the fall speed
        if NORTH in COLLISION: tern_pos[1] += CHARACTER_SPEED**CHARACTER_SPEED  # Error checking, more like preventing the player going down
    if NORTH in COLLISION: CHARACTER_JUMP = False # counter-acts form going up
    if EAST in COLLISION and GK["right"][0] in onKey: tern_pos[0] += CHARACTER_SPEED   # counter-acts form going right
    if WEST in COLLISION and GK["left"][0] in onKey: tern_pos[0] -= CHARACTER_SPEED   # counter-acts form going left
    if tern_pos[0]/BLOCK_SZ >= 1.0:    tern_ofs[0] -= 1; tern_pos[0] = -CHARACTER_SPEED  # left side
    elif tern_pos[0]/BLOCK_SZ <= -1.0: tern_ofs[0] += 1; tern_pos[0] = -CHARACTER_SPEED  # right side
    elif tern_pos[1]/BLOCK_SZ >= 1.0:  tern_ofs[1] -= 1; tern_pos[1] = -CHARACTER_SPEED  # top side
    elif tern_pos[1]/BLOCK_SZ <= -1.0: tern_ofs[1] += 1; tern_pos[1] = -CHARACTER_SPEED  # bottom side
    if char_jump: tern_pos[1] += round(m.sin(m.radians(char_jump_len))*JUMP_HEIGHT); char_jump_len += JUMP_SPEED  # UP - Jump
    if GK["left"][0] in onKey: tern_pos[0] += CHARACTER_SPEED  # LEFT - Go lef
    # if GK["sneak"][0] in onKey: TERRAIN_POS[1] -= SPEED  # DOWN - Sneak
    if GK["right"][0] in onKey: tern_pos[0] -= CHARACTER_SPEED  # RIGHT - Go right
    if JUMP_MAX_LEN <= char_jump_len: CHARACTER_JUMP = False; CHARACTER_JUMP_LEN = 0;
    if (GK["jump"][0] in onKey and SOUTH in COLLISION) and GAME_OPTIONS["AUTO-JUMP"]: CHARACTER_JUMP = True  # To jump continously when pressed

    pyg.display.flip()
    clock.tick(FPS)

pyg.quit()
quit()