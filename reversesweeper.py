import pygame, random, math, sys
from pygame.locals import *
from pygame.time import Clock

pygame.init()

BOARD_SIZE = 13

screen = pygame.display.set_mode((BOARD_SIZE * 50,  BOARD_SIZE * 50 + 100))
myimage = pygame.image.load("assets/board.png")
imagerect = Rect(0, 0, BOARD_SIZE * 50, BOARD_SIZE * 50 + 100)

FPS = 60
clock = pygame.time.Clock()

images = []
for imNum in range(9):
    images.append(pygame.image.load("assets/" + str(imNum) + ".png"))

for imStr in ["mines","notmines","uk","flag"]:
    images.append(pygame.image.load("assets/" + imStr + ".png"))

lines = []
revealedList = []

def clean():
    lines.clear()
    revealedList.clear()
    for times in range(BOARD_SIZE):
        emptyTab = []
        for timesx in range(BOARD_SIZE):
            emptyTab.append(0)
        revealedList.append(emptyTab)
    for x in range(BOARD_SIZE):
        xarray = []
        for y in range(BOARD_SIZE):
            xarray.append(random.choice([10, 10, 10, 10, 9]))
        lines.append(xarray)
    finalClean()

def finalClean():
    for l in range(BOARD_SIZE):
        for z in range(BOARD_SIZE):
            minesNear = 0
            if lines[l][z] == 10:
                for r in range(max(0, l - 1), min(BOARD_SIZE - 1, l + 1) + 1):
                    for c in range(max(0, z - 1), min(BOARD_SIZE - 1, z + 1) + 1):
                        if lines[r][c] == 9: minesNear += 1
                lines[l][z] = 8 - minesNear

clean()

def gameEnd():
    endAtRenderStop = True
    for revX in range(BOARD_SIZE):
        for revY in range(BOARD_SIZE):
            revealedList[revX][revY] = 1
    render()

endAtRenderStop = False
gameOn = True
def render():
    screen.fill([255, 255, 255])
    screen.blit(myimage, imagerect)
    linestart = 100
    for line in lines:
        numsquare = 0;
        for square in line:
            loadImg = images[11]
            xpos = math.floor(numsquare / 50)
            ypos = math.floor((linestart - 100) / 50)
            if revealedList[xpos][ypos] == 1:
                loadImg = images[square]
            if revealedList[xpos][ypos] == 0.5:
                loadImg = images[12]
            screen.blit(loadImg, Rect(numsquare, linestart, 50, 50))
            numsquare = numsquare + 50
        linestart = linestart + 50
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            posx = pos[0]
            posy = pos[1]
            if posy > 100:
                posy = posy - 100
                posx = min(max(math.floor(posx / 50), 0), BOARD_SIZE - 1)
                posy = min(max(math.floor(posy / 50), 0), BOARD_SIZE - 1)
                revealedList[posx][posy] = 1;
                if lines[posy][posx] == 9:
                    gameEnd()
            else:
                clean()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            pos = pygame.mouse.get_pos()
            posx = pos[0]
            posy = pos[1]
            if posy > 100:
                posy = posy - 100
                posx = min(max(math.floor(posx / 50), 0), BOARD_SIZE - 1)
                posy = min(max(math.floor(posy / 50), 0), BOARD_SIZE - 1)
                if (revealedList[posx][posy] == 0):
                    revealedList[posx][posy] = 0.5
                elif (revealedList[posx][posy] == 0.5):
                    revealedList[posx][posy] = 0
            else:
                clean()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
            clean()
    pygame.display.flip()
    if endAtRenderStop:
        gameOn = False

while gameOn:
    render()
    clock.tick(FPS)
