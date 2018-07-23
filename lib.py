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
        if SHOW_PLAYER_COLLISION:
            pyg.draw.line(self.win, (0, 255, 0), (x, y), (x, Y), 4)  # LEFT
            pyg.draw.line(self.win, (0, 255, 0), (X, y), (X, Y), 4)  # RIGHT
            pyg.draw.line(self.win, (0, 255, 0), (x, y), (X, y), 4)  # TOP
            pyg.draw.line(self.win, (0, 255, 0), (x, Y), (X, Y), 4)  # BOTTOM
            for i in range(-BLOCK_SZ*COLLISION_SZ,BLOCK_SZ*COLLISION_SZ+1,BLOCK_SZ):
                for j in range(-BLOCK_SZ*COLLISION_SZ,BLOCK_SZ*COLLISION_SZ+1,BLOCK_SZ):
                    pyg.draw.rect(self.win, (255, 0, 255), (a+self.tx+i, B+self.ty+j, BLOCK_SZ, BLOCK_SZ), 1)  # The purple square
                    if blockTerrain[(a+i)//BLOCK_SZ-1][(B+j)//BLOCK_SZ-1] != B_AIR:  # BOTTOM
                        pyg.draw.line(self.win, (255, 255, 0), (a+self.tx+i, B+self.ty+j), (A+self.tx+i, B+self.ty+j), 4)
                    if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-2] != B_AIR:  # TOP
                        pyg.draw.line(self.win, (255, 255, 0), (a+self.tx+i, b+self.ty+j), (A+self.tx+i, b+self.ty+j), 4)
                    if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-1] != B_AIR:  # LEFT
                        pyg.draw.line(self.win, (255, 255, 0), (a+self.tx+i, b+self.ty+j), (a+self.tx+i, B+self.ty+j), 4)
                    if blockTerrain[(A+i)//BLOCK_SZ-2][(B+j)//BLOCK_SZ-2] != B_AIR:  # RIGHT
                        pyg.draw.line(self.win, (255, 255, 0), (A+self.tx+i, b+self.ty+j), (A+self.tx+i, B+self.ty+j), 4)

        for i in range(-BLOCK_SZ*COLLISION_SZ,BLOCK_SZ*COLLISION_SZ+1,BLOCK_SZ):
            for j in range(-BLOCK_SZ*COLLISION_SZ,BLOCK_SZ*COLLISION_SZ+1,BLOCK_SZ):
                if blockTerrain[(a+i)//BLOCK_SZ-1][(B+j)//BLOCK_SZ-1] != B_AIR:  # BOTTOM
                    if B+self.ty+j+BOT_PAD < Y and (x < x+self.tx+i < X or x < X+self.tx+i-1 < X): col.append(SOUTH)
                if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-2] != B_AIR:  # TOP
                    if b+self.ty+j+TOP_PAD > y and (x < x+self.tx+i < X or x < X+self.tx+i-1 < X): col.append(NORTH)
                if blockTerrain[(a+i)//BLOCK_SZ-1][(b+j)//BLOCK_SZ-1] != B_AIR:  # LEFT side collision is when the player goes RIGHT
                    if x < x+self.tx+i+LFT_PAD < X and (y < y+self.ty+j < Y or y < Y+self.ty+j-1 < Y): col.append(EAST)
                if blockTerrain[(A+i)//BLOCK_SZ-2][(B+j)//BLOCK_SZ-2] != B_AIR:  # RIGHT; and vice versa
                    if x < A+self.tx+i+RGT_PAD < X and (y < Y+self.ty+j < Y or y < y+self.ty+j-1 < Y): col.append(WEST)
        return col # at most 2 side collision. since character-bx is smaller than block; maybe 3 due to the paddings

    def raycast(self, RAYCAST_PP, button, chosenBlock):
        X, Y = self.x+CHARACTER_BOX[0]//2*PIXEL_SZ, self.y+CHARACTER_BOX[1]//2*PIXEL_SZ
        BXI, BYI = (RAYCAST_PP[0]+self.ty)//BLOCK_SZ-1, (RAYCAST_PP[1]+self.tx)//BLOCK_SZ-1  # Block's [x/y] index of the block terrain
        BXL, BYL = BXI*BLOCK_SZ, BYI*BLOCK_SZ  # Block [x/y] location
        BLOCK = ""
        if SHOW_RAYCAST:
            pyg.draw.circle(self.win, (255, 0, 0), (X, Y), RAYCAST_MAX_CIRCLE*BLOCK_SZ, 2)
            pyg.draw.line(self.win, (0, 0, 255), (X, Y), (X, Y+RAYCAST_MAX_CIRCLE*BLOCK_SZ), 2)
            pyg.draw.rect(self.win, (255, 200, 100), (BXL, BYL, BLOCK_SZ, BLOCK_SZ))
            pyg.draw.rect(self.win, (255, 125, 0), (BXL, BYL, BLOCK_SZ, BLOCK_SZ), 4)
        if button == LEFT_CLK: BLOCK = "a"  # Left  Click - Break - Break into an air
        if button == RIGHT_CLK: BLOCK = chosenBlock # Right Click - Place - Place onto there chosen block
        print(BXL, BYL, BXI, BYI)
        return BXI, BYI, BLOCK # Coordinates of BLOCK TERRAIN/Break or Place - POS, BLOCK_ID

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
                else: pyg.draw.rect(self.win, hCode[self.blk[i][j]], (i*BLOCK_SZ+self.plyLOC[0]-self.VSx*BLOCK_SZ, j*BLOCK_SZ+self.plyLOC[1]-self.VSx*BLOCK_SZ, BLOCK_SZ, BLOCK_SZ))


def hexTOrgb(data, sz=(12, 18)):
    return [[tuple([int(data[(i*sz[0]+j)*6:(i*sz[0]+j+1)*6][k*2:k*2+2], 16) for k in range(3)]) for j in range(sz[1])] for i in range(sz[0])]

