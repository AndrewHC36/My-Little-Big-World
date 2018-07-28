import pygame as pyg
from constants import *
pyg.init()


def rnd(n, base):
    return int(base*round(float(n)/base))


class WorldDt:
    def __init__(self, fname):
        self.fname = fname

    def read(self):
        fdata = open(self.fname, "r")
        fdata = [i.strip("\n") for i in fdata]
        time = fdata[0]
        sizeHL = fdata[1].split("x")
        title = fdata[2]
        tick = fdata[3]
        worldDT = fdata[5:len(fdata)]
        inGame_time = fdata[4]
        return time, sizeHL, title, worldDT, tick, inGame_time


class Character:
    def __init__(self, win, ploc, tloc, sz, dt, ofs):
        self.y = ploc[0]
        self.x = ploc[1]
        self.tx = tloc[0]
        self.ty = tloc[1]
        self.win = win
        self.dt = dt
        self.sz = sz
        self.ofs = ofs

    def update(self, tloc, ofs):
        self.tx = tloc[0]
        self.ty = tloc[1]
        self.ofs = ofs

    def show(self):
        for i in range(self.sz[0]):
            for j in range(self.sz[1]):
                pyg.draw.rect(self.win, self.dt[i][j], (self.x+i*PIXEL_SZ, self.y+j*PIXEL_SZ, PIXEL_SZ, PIXEL_SZ))

    def collision(self, blockt):
        COL = []  # pos of 4 points of character box; rounded to nearest block pos
        x, y, X, Y = self.x, self.y, self.x+CHARACTER_BOX[0]*PIXEL_SZ, self.y+CHARACTER_BOX[1]*PIXEL_SZ
        a, b, A, B = x//BLOCK_SZ*BLOCK_SZ, y//BLOCK_SZ*BLOCK_SZ, X//BLOCK_SZ*BLOCK_SZ, Y//BLOCK_SZ*BLOCK_SZ
        for i in range(-BLOCK_SZ*COLLISION_SZ, BLOCK_SZ*COLLISION_SZ+1, BLOCK_SZ):
            for j in range(-BLOCK_SZ*COLLISION_SZ, BLOCK_SZ*COLLISION_SZ+1, BLOCK_SZ):
                if blockt[x//BLOCK_SZ+i//BLOCK_SZ-COLLISION_OFS[0]][y//BLOCK_SZ+j//BLOCK_SZ-COLLISION_OFS[1]+1] != BLK["air"]:  # BOTTOM
                    if (y < j+B+self.ty < Y+BT_P) and (i+a+self.tx < x < i+A+self.tx or i+a+self.tx < X < i+A+self.tx): COL.append(SOUTH)
                if blockt[x//BLOCK_SZ+i//BLOCK_SZ-COLLISION_OFS[0]][y//BLOCK_SZ+j//BLOCK_SZ-COLLISION_OFS[1]-1] != BLK["air"]:  # TOP
                    if (Y > j+b+self.ty > y+TP_P) and (i+a+self.tx < x < i+A+self.tx or i+a+self.tx < X < i+A+self.tx): COL.append(NORTH)
                if blockt[x//BLOCK_SZ+i//BLOCK_SZ-COLLISION_OFS[0]-1][y//BLOCK_SZ+j//BLOCK_SZ-COLLISION_OFS[1]] != BLK["air"]:  # LEFT
                    if (X > i+a+self.tx > x+LT_P) and (j+b+self.ty < y < j+B+self.ty or j+b+self.ty < Y < j+B+self.ty): COL.append(WEST)
                if blockt[x//BLOCK_SZ+i//BLOCK_SZ-COLLISION_OFS[0]+1][y//BLOCK_SZ+j//BLOCK_SZ-COLLISION_OFS[1]] != BLK["air"]:  # RIGHT
                    if (x < i+A+self.tx < X+RT_P) and (j+b+self.ty < y < j+B+self.ty or j+b+self.ty < Y < j+B+self.ty): COL.append(EAST)

        return COL  # at most two collision, sometime three.

    def edit(self, loc, key, chosenBlock):
        x, y = self.x+CHARACTER_BOX[0]*PIXEL_SZ//2, self.y+CHARACTER_BOX[1]*PIXEL_SZ//2
        BXI, BYI = (loc[0]-self.tx)//BLOCK_SZ-TERRAIN_VIEWBOX[0], (loc[1]-self.ty)//BLOCK_SZ-TERRAIN_VIEWBOX[1]  # Block's [x/y] index of the block terrain
        if abs(loc[0]-x)+abs(loc[1]-y) > EDIT_MAX_CIRCLE*BLOCK_SZ: return 0, 0, 0, False
        elif GK["break"][0] in key: BLOCK = BLK["air"]  # Left  Click - Break - Break into an air
        elif GK["place"][0] in key: BLOCK = chosenBlock  # Right Click - Place - Place onto there chosen block
        return BXI, BYI, BLOCK, True

    def sneak(self):
        return (CHARACTER_BOX[1], CHARACTER_BOX[0])

class Terrain:
    def __init__(self, win, viewBX, terrainDT, currentBLK):
        self.win = win
        self.VSx = viewBX[0]
        self.VSy = viewBX[1]
        self.VEx = viewBX[2]
        self.VEy = viewBX[3]
        self.dt = terrainDT
        self.blk = currentBLK

    def update(self, pLOC, curBLK):
        self.plyLOC = pLOC
        self.blk = curBLK

    def display(self):
        hCode = {"a":"clr", "b": (100, 200, 100), "c": (100, 100, 100)}
        for i in range(self.VEy):
            for j in range(self.VEx):
                if hCode[self.blk[i][j]] == "clr": pass
                else: pyg.draw.rect(self.win, hCode[self.blk[i][j]], (i*BLOCK_SZ+self.plyLOC[0]+self.VSx*BLOCK_SZ, j*BLOCK_SZ+self.plyLOC[1]+self.VSx*BLOCK_SZ, BLOCK_SZ, BLOCK_SZ))


def hexTOrgb(data, sz=(12, 18)):
    return [[tuple([int(data[(i*sz[0]+j)*6:(i*sz[0]+j+1)*6][k*2:k*2+2], 16) for k in range(3)]) for j in range(sz[1])] for i in range(sz[0])]

