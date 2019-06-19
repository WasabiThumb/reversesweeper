import pygame, random, math, sys
from pygame.locals import *
from pygame.time import Clock

pygame.init()

BOARD_SIZE = 13
SQUARE_SIZE = 50 # You shouldn't change this, unless the textures change size.

# Put all user customization options in this section (this includes evaluateMineNumber() so we can change how they are determined)
screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE,  BOARD_SIZE * SQUARE_SIZE + 100))
myimage = pygame.image.load("assets/board.png")
imagerect = Rect(0, 0, BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE + 100)

FPS = 60
clock = pygame.time.Clock()

images = []
for imNum in range(9):
    images.append(pygame.image.load("assets/" + str(imNum) + ".png"))

for imStr in ["mines","notmines","uk","flag"]:
    images.append(pygame.image.load("assets/" + imStr + ".png"))

def evaluateMineNumber(nMines, nNeighbors):
    # nMines is number of mines in neighborhood
    # nNeighbors is number of squares in neighborhood
    # nNeighbors-nMines = empty square #
    # nMines = mine #

    return nNeighbors-nMines

    # return nMines
    # regular minesweeper ^

# End customization section

lines = []
revealedList = []
hasCascaded = []
global firstMove
firstMove = True

def clean():
    global firstMove
    lines.clear()
    revealedList.clear()
    hasCascaded.clear()
    firstMove = True
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
                maxMines = 8
                onEdge = (l == 0) or (l == BOARD_SIZE - 1)
                onTopEdge = (z == 0) or (z == BOARD_SIZE - 1)
                if onEdge and onTopEdge:
                    maxMines = 3
                elif onEdge or onTopEdge:
                    maxMines = 5
                lines[l][z] = evaluateMineNumber(minesNear, maxMines)

clean()

def winDetect():
    hasWon = True
    for r in range(0, BOARD_SIZE):
        for c in range(0, BOARD_SIZE):
            if revealedList[r][c] < 1:
                if lines[c][r] != 9:
                    hasWon = False
    if hasWon:
        gameEnd()

def startCascade(l,z):
    for r in range(max(0, l - 1), min(BOARD_SIZE - 1, l + 1) + 1):
        for c in range(max(0, z - 1), min(BOARD_SIZE - 1, z + 1) + 1):
            revealedList[r][c] = 1
            if [r,c] not in hasCascaded:
                hasCascaded.append([r,c]) # dev note! almost did .push, too much JS for me
                if lines[c][r] == 8:
                    startCascade(r,c)
    winDetect()

def gameEnd():
    endAtRenderStop = True
    for revX in range(BOARD_SIZE):
        for revY in range(BOARD_SIZE):
            if revealedList[revX][revY] == 0.5:
                if lines[revY][revX] != 9:
                    lines[revY][revX] = 10
            revealedList[revX][revY] = 1
    render()

endAtRenderStop = False
gameOn = True
def render():
    global firstMove
    screen.fill([255, 255, 255])
    screen.blit(myimage, imagerect)
    linestart = 100
    for line in lines:
        numsquare = 0;
        for square in line:
            loadImg = images[11]
            xpos = math.floor(numsquare / SQUARE_SIZE)
            ypos = math.floor((linestart - 100) / SQUARE_SIZE)
            if revealedList[xpos][ypos] == 1:
                loadImg = images[square]
            if revealedList[xpos][ypos] == 0.5:
                loadImg = images[12]
            screen.blit(loadImg, Rect(numsquare, linestart, SQUARE_SIZE, SQUARE_SIZE))
            numsquare = numsquare + SQUARE_SIZE
        linestart = linestart + SQUARE_SIZE
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
                posx = min(max(math.floor(posx / SQUARE_SIZE), 0), BOARD_SIZE - 1)
                posy = min(max(math.floor(posy / SQUARE_SIZE), 0), BOARD_SIZE - 1)
                if not revealedList[posx][posy] == 0.5:
                    if revealedList[posx][posy] == 1:
                        shouldChord = True
                        for r in range(max(0, posx - 1), min(BOARD_SIZE - 1, posx + 1) + 1):
                            for c in range(max(0, posy - 1), min(BOARD_SIZE - 1, posy + 1) + 1):
                                if lines[c][r] == 9:
                                    if revealedList[r][c] != 0.5:
                                        shouldChord = False
                        if shouldChord:
                            for r in range(max(0, posx - 1), min(BOARD_SIZE - 1, posx + 1) + 1):
                                for c in range(max(0, posy - 1), min(BOARD_SIZE - 1, posy + 1) + 1):
                                    if lines[c][r] != 9:
                                        revealedList[r][c] = 1;
                    revealedList[posx][posy] = 1;
                    if lines[posy][posx] == 9:
                        if firstMove:
                            while lines[posy][posx] == 9:
                                clean()
                            revealedList[posx][posy] = 1;
                        else:
                            gameEnd()
                    else:
                        # win detection should be here, and after startCascade loop for best performance
                        winDetect()
                    if lines[posy][posx] == 8:
                        startCascade(posx,posy)
                firstMove = False
            else:
                clean()
        #MMB "Cheat" function for testing
        #elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
        #    for revX in range(BOARD_SIZE):
        #        for revY in range(BOARD_SIZE):
        #            if lines[revY][revX] != 9:
        #                revealedList[revX][revY] = 1
        #    winDetect()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            pos = pygame.mouse.get_pos()
            posx = pos[0]
            posy = pos[1]
            if posy > 100:
                posy = posy - 100
                posx = min(max(math.floor(posx / SQUARE_SIZE), 0), BOARD_SIZE - 1)
                posy = min(max(math.floor(posy / SQUARE_SIZE), 0), BOARD_SIZE - 1)
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
