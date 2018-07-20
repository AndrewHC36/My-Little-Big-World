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

    def collision(self, blockTerrain):
        col = []
        x, y, X, Y = self.x, self.y, CHARACTER_BOX[0]*PIXEL_SZ+self.x, CHARACTER_BOX[1]*PIXEL_SZ+self.y
        a, b, A, B = (x//BLOCK_SZ)*BLOCK_SZ, (y//BLOCK_SZ)*BLOCK_SZ, (X//BLOCK_SZ)*BLOCK_SZ, (Y//BLOCK_SZ)*BLOCK_SZ
        C = BLOCK_SZ
        if SHOW_PLAYER_COLLISION:
            pyg.draw.line(self.win, (0, 255, 0), (x, y), (x, Y), 4)  # LEFT
            pyg.draw.line(self.win, (0, 255, 0), (X, y), (X, Y), 4)  # RIGHT
            pyg.draw.line(self.win, (0, 255, 0), (x, y), (X, y), 4)  # TOP
            pyg.draw.line(self.win, (0, 255, 0), (x, Y), (X, Y), 4)  # BOTTOM
            [pyg.draw.rect(self.win, (255, 0, 255), (a+self.tx+i, B+self.ty+j, BLOCK_SZ, BLOCK_SZ), 1) for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C) for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C)]
            for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # BOTTOM
                for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                    if blockTerrain[(a+i)//BLOCK_SZ-1][(B+j)//BLOCK_SZ-1] != B_AIR:
                        pyg.draw.line(self.win, (0, 255, 255), (a+self.tx+i, B+self.ty+j), (A+self.tx+i, B+self.ty+j), 4)
            for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # TOP
                for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                    if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-2] != B_AIR:
                        pyg.draw.line(self.win, (255, 255, 0), (a+self.tx+i, b+self.ty+j), (A+self.tx+i, b+self.ty+j), 4)
            for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # LEFT
                for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                    if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-1] != B_AIR:
                        pyg.draw.line(self.win, (255, 255, 0), (a+self.tx+i, b+self.ty+j), (a+self.tx+i, B+self.ty+j), 4)
            for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # RIGHT
                for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                    if blockTerrain[(A+i)//BLOCK_SZ-2][(B+j)//BLOCK_SZ-2] != B_AIR:
                        pyg.draw.line(self.win, (0, 255, 255), (A+self.tx+i, b+self.ty+j), (A+self.tx+i, B+self.ty+j), 4)

        for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # BOTTOM
            for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                if blockTerrain[(a+i)//BLOCK_SZ-1][(B+j)//BLOCK_SZ-1] != B_AIR:
                    if B+self.ty+j < Y and (x < x+self.tx+i < X or x < X+self.tx+i-1 < X): col.append(SOUTH)
        for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # TOP
            for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-2] != B_AIR:
                    if b+self.ty+j > y and (x < x+self.tx+i < X or x < X+self.tx+i-1 < X): col.append(NORTH)
        for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # LEFT side collision is when the player goes RIGHT
            for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-1] != B_AIR:
                    if x < x+self.tx+i-11 < X and (y < y+self.ty+j < Y or y < Y+self.ty+j-1 < Y): col.append(EAST)
        for i in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):  # RIGHT; and vice versa
            for j in range(-C*COLLISION_SZ,C*COLLISION_SZ+1,C):
                if blockTerrain[(A+i)//BLOCK_SZ-2][(B+j)//BLOCK_SZ-2] != B_AIR:
                    if x < A+self.tx+i+5 < X and (y < Y+self.ty+j < Y or y < y+self.ty+j-1 < Y): col.append(WEST)
        return col # at most 2 side collision. since character-bx is smaller than block

    def jump(self, ): pass


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
                else: pyg.draw.rect(self.win, hCode[self.blk[i][j]], (i*BLOCK_SZ+self.plyLOC[0]-self.VSx*BLOCK_SZ, j*BLOCK_SZ+self.plyLOC[1]-self.VSx*BLOCK_SZ, BLOCK_SZ, BLOCK_SZ))


def hexTOrgb(data, sz=(12, 18)):
    return [[tuple([int(data[(i*sz[0]+j)*6:(i*sz[0]+j+1)*6][k*2:k*2+2], 16) for k in range(3)]) for j in range(sz[1])] for i in range(sz[0])]

