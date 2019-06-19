import pygame, random, math, sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((600, 800))
myimage = pygame.image.load("assets/board.png")
imagerect = Rect(0,0,600,800)

images = [];
for imNum in range(9):
    images.append(pygame.image.load("assets/" + str(imNum) + ".png"))

for imStr in ["mines","notmines","uk"]:
    images.append(pygame.image.load("assets/" + imStr + ".png"))

lines = []
def clean():
    for x in range(13):
        xarray = []
        for y in range(13):
            xarray.append(random.choice([10,10,10,10,9]))
        lines.append(xarray)
    finalClean()

def finalClean():
    for l in range(13):
        for z in range(13):
            if lines[l][z] == 10:
                neighbora = None
                neighborb = None
                neighborc = None
                if len(lines) > (l-1): neighbora = lines[l-1]
                totalneighbors = []
                if neighbora:
                    squara = None
                    squarb = None
                    squarc = None
                    if len(neighbora) > (z-1): squara = neighbora[z-1]
                    if len(neighbora) > (z): squarb = neighbora[z]
                    if len(neighbora) > (z+1): squarc = neighbora[z+1]
                    neighbora = []
                    if squara: neighbora.append(squara)
                    if squarb: neighbora.append(squarb)
                    if squarc: neighbora.append(squarc)
                    for neighbor in neighbora:
                        totalneighbors.append(neighbor)
                if len(lines) > (l): neighborb = lines[l]
                if neighborb:
                    squara = None
                    squarc = None
                    if len(neighborb) > (z-1): squara = neighborb[z-1]
                    if len(neighborb) > (z+1): squarc = neighborb[z+1]
                    neighborb = []
                    if squara: neighborb.append(squara)
                    if squarc: neighborb.append(squarc)
                    for neighbor in neighborb:
                        totalneighbors.append(neighbor)
                if len(lines) > (l+1): neighborc = lines[l+1]
                if neighborc:
                    squara = None
                    squarb = None
                    squarc = None
                    if len(neighborc) > (z-1): squara = neighborc[z-1]
                    if len(neighborc) > (z): squarb = neighborc[z]
                    if len(neighborc) > (z+1): squarc = neighborc[z+1]
                    neighborc = []
                    if squara: neighborc.append(squara)
                    if squarb: neighborc.append(squarb)
                    if squarc: neighborc.append(squarc)
                    for neighbor in neighborc:
                        totalneighbors.append(neighbor)
                minesNear = 0;
                for n in totalneighbors:
                    if n == 9:
                        minesNear = minesNear + 1
                lines[l][z] = 8-minesNear

revealedList = []
for times in range(13):
    emptyTab = []
    for timesx in range(13):
        emptyTab.append(0)
    revealedList.append(emptyTab)

clean()

def gameEnd():
    endAtRenderStop = True
    for revX in range(13):
        for revY in range(13):
            revealedList[revX][revY] = 1
    render()

endAtRenderStop = False
gameOn = True
def render():
    screen.fill([0,0,0])
    screen.blit(myimage, imagerect)
    linestart = 100
    for line in lines:
        numsquare = 0;
        for square in line:
            loadImg = images[11]
            xpos = math.floor(numsquare/50)
            ypos = math.floor((linestart-100)/50)
            if revealedList[xpos][ypos] == 1:
                loadImg = images[square]
            screen.blit(loadImg, Rect(numsquare, linestart, 50, 50))
            numsquare = numsquare + 50
        linestart = linestart + 50
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            posx = pos[0]
            posy = pos[1]
            if posy > 100:
                posy = posy - 100
                posx = min(max(math.floor(posx/50), 0), 12)
                posy = min(max(math.floor(posy/50), 0), 12)
                revealedList[posx][posy] = 1;
                if lines[posy][posx] == 9:
                    gameEnd()
    pygame.display.flip()
    if endAtRenderStop:
        gameOn = False

while gameOn:
    render()
