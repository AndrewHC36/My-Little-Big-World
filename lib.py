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
    def __init__(self, win, loc, sz, dt):
        self.y = loc[1]
        self.x = loc[0]
        self.win = win
        self.dt = dt
        self.sz = sz

    def update(self, loc):
        self.y = loc[0]
        self.x = loc[1]

    def show(self):
        for i in range(self.sz[0]):
            for j in range(self.sz[1]):
                pyg.draw.rect(self.win, self.dt[i][j], (self.x+i*PIXEL_SZ, self.y+j*PIXEL_SZ, PIXEL_SZ, PIXEL_SZ))

    def collision(self, blockTerrain):
        col = []
        print(blockTerrain[rnd(self.x//BLOCK_SZ, BLOCK_SZ)][rnd(self.y//BLOCK_SZ, BLOCK_SZ)], "=", rnd(self.x//BLOCK_SZ, BLOCK_SZ), rnd(self.y//BLOCK_SZ, BLOCK_SZ))

        return col # at most 2 side collision. since character-bx is smaller than block


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
        hCode = {"a":"clr", "b": (100, 100, 100), "c": (255, 100, 100)}
        for i in range(self.VEy):
            for j in range(self.VEx):
                if hCode[self.blk[i][j]] == "clr": pass
                else: pyg.draw.rect(self.win, hCode[self.blk[i][j]], (i*BLOCK_SZ+self.plyLOC[0]-self.VSx*BLOCK_SZ, j*BLOCK_SZ+self.plyLOC[1]-self.VSx*BLOCK_SZ, BLOCK_SZ, BLOCK_SZ))


def hexTOrgb(data, sz=(12, 18)):
    return [[tuple([int(data[(i*sz[0]+j)*6:(i*sz[0]+j+1)*6][k*2:k*2+2], 16) for k in range(3)]) for j in range(sz[1])] for i in range(sz[0])]


"""
PRE
s = special
b = block
e = entity
p = particle
l = liquid
SUF
f = foreground
w = background (wall)
t = together (f and w)

|| FILE-ID || BLOCK-ID || - - BLOCK-NAME - - || - - - - - - BLOCK-DF_TEXTURE - - - - - - ||        
||=========||==========||====================||==========================================||
|| a       || s000t    || Air                || FFFFFF 
|| b       || b000f    || Stone              || FFFFFF 
"""