import pygame, sys, random, time, csv, os
from pygame.locals import *
from tiles import *
from spritesheet import Spritesheet

levelList = "GuyIsHe.csv CrustTest.csv ButterflyParade.csv CircularOut.csv Hallward.csv Hillaze.csv RaindropFreeway.csv TerrorEye.csv HedgeFetch.csv RiverBoat.csv Pinkyard.csv Rivast.csv".split(
)
lNum = random.randint(0, len(levelList) - 1)
LEVEL_FILENAME = levelList[lNum]  #Random maps.

#LEVEL_FILENAME = "HedgeFetch.csv" #For Testing

BGCOLOR = (11, 11, 44)



#Clyde object class
class Clyde(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = clydeSprite[animDir][animIndex]
        self.image.set_colorkey((84, 84, 84))
        self.rect = pygame.Rect(playerX + 2, playerY + 2, 30, 30)
        self.collisionrect = pygame.Rect(self.rect.centerx, self.rect.centery,
                                         5, 5)
        self.collisionrect.center = (playerX + 16, playerY + 16)
        self.rect.center = (playerX + 2, playerY + 2)
        #self.rect.x, self.rect.y = map.start_x, map.start_y
        ########

    def getHits(self, tilesheet):
        global playerX, playerY, setDirX, setDirY, moveDirX, moveDirY
        playerCenterX, playerCenterY = playerX + 16, playerY + 16
        collisionRectPOS = (playerCenterX + setDirX * 1.7,
                            playerCenterY + setDirY * 1.7)
        clyde.collisionrect.center = collisionRectPOS
        for tile in tilesheet.tiles:
            if self.collisionrect.colliderect(tile):
                return
            else:
                change = True
        if change is True:
            moveDirY = setDirY
            moveDirX = setDirX

    def checkDir(self, tilesheet):
        global playerX, playerY, setDirX, setDirY, moveDirX, moveDirY
        playerCenterX, playerCenterY = playerX + 16, playerY + 16
        collisionRectPOS = (playerCenterX + moveDirX * 1.7,
                            playerCenterY + moveDirY * 1.7)
        clyde.collisionrect.center = collisionRectPOS
        for tile in tilesheet.tiles:
            if self.collisionrect.colliderect(tile):
                moveDirY = 0
                moveDirX = 0

        for pellet in tilesheet.pellets:
            if self.rect.colliderect(pellet):
                tilesheet.pellets.remove(pellet)
                eatit.play()


class PacMom(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pMomSprite[pmDir][pmIndex]
        self.image.set_colorkey((84, 84, 84))
        self.rect = pygame.Rect(pmX + 2, pmY + 2, 30, 30)
        self.collisionrect = pygame.Rect(self.rect.centerx + 4,
                                         self.rect.centery + 4, 8, 8)
        self.speed = 16

    def keepMoving(self, targetX, targetY, map):
        global pmDir, pmIndex, pm_Up
        goDirX = 0
        goDirY = 0
        self.collisionrect.center = self.rect.center
        flagR = True
        self.collisionrect.centerx += 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pmDir == 3:
                flagR = False
                break
        self.collisionrect.center = self.rect.center
        flagU = True
        self.collisionrect.centery -= 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pmDir == 0:
                flagU = False
                break
        self.collisionrect.center = self.rect.center
        flagL = True

        self.collisionrect.centerx -= 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pmDir == 2:
                flagL = False
                break
        self.collisionrect.center = self.rect.center
        flagD = True
        self.collisionrect.centery += 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pmDir == 1:
                flagD = False
                break

        self.collisionrect.center = self.rect.center
        if self.rect.x < targetX:
            if flagR == True:
                goDirX = self.speed
                goDirY = 0
                pmDir = 2
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.y > targetY:
                if flagU == True:
                    goDirX = 0
                    goDirY = -self.speed
                    pmDir = 1
                    pmIndex += 1
                    if pmIndex > len(pm_Up) - 1:
                        pmIndex = 0
                    self.image = pMomSprite[pmDir][pmIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagD == True:
                goDirX = 0
                goDirY = self.speed
                pmDir = 0
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY

        if self.rect.y > targetY:
            if flagU == True:
                goDirX = 0
                goDirY = -self.speed
                pmDir = 1
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.x > targetX:
                if flagL == True:
                    goDirX = -self.speed
                    goDirY = 0
                    pmDir = 3
                    pmIndex += 1
                    if pmIndex > len(pm_Up) - 1:
                        pmIndex = 0
                    self.image = pMomSprite[pmDir][pmIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagR == True:
                goDirX = self.speed
                goDirY = 0
                pmDir = 2
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY

        if self.rect.x > targetX:
            if flagL == True:
                goDirX = -self.speed
                goDirY = 0
                pmDir = 3
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.y < targetY:
                if flagD == True:
                    goDirX = 0
                    goDirY = self.speed
                    pmDir = 0
                    pmIndex += 1
                    if pmIndex > len(pm_Up) - 1:
                        pmIndex = 0
                    self.image = pMomSprite[pmDir][pmIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagU == True:
                goDirX = 0
                goDirY = -self.speed
                pmDir = 1
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
        if self.rect.y < targetY:
            if flagD == True:
                goDirX = 0
                goDirY = self.speed
                pmDir = 0
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.x < targetX:
                if flagR == True:
                    goDirX = self.speed
                    goDirY = 0
                    pmDir = 2
                    pmIndex += 1
                    if pmIndex > len(pm_Up) - 1:
                        pmIndex = 0
                    self.image = pMomSprite[pmDir][pmIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagL == True:
                goDirX = -self.speed
                goDirY = 0
                pmDir = 3
                pmIndex += 1
                if pmIndex > len(pm_Up) - 1:
                    pmIndex = 0
                self.image = pMomSprite[pmDir][pmIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
        if flagL == True:
            goDirX = -self.speed
            goDirY = 0
            pmDir = 3
            pmIndex += 1
            if pmIndex > len(pm_Up) - 1:
                pmIndex = 0
            self.image = pMomSprite[pmDir][pmIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY
        if flagD == True:
            goDirX = 0
            goDirY = self.speed
            pmDir = 0
            pmIndex += 1
            if pmIndex > len(pm_Up) - 1:
                pmIndex = 0
            self.image = pMomSprite[pmDir][pmIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY
        if flagR == True:
            goDirX = self.speed
            goDirY = 0
            pmDir = 2
            pmIndex += 1
            if pmIndex > len(pm_Up) - 1:
                pmIndex = 0
            self.image = pMomSprite[pmDir][pmIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY
        if flagU == True:
            goDirX = 0
            goDirY = -self.speed
            pmDir = 1
            pmIndex += 1
            if pmIndex > len(pm_Up) - 1:
                pmIndex = 0
            self.image = pMomSprite[pmDir][pmIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY


class PacChild(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pChildSprite[pcDir][pcIndex]
        self.image.set_colorkey((84, 84, 84))
        self.rect = pygame.Rect(pcX + 2, pcY + 2, 30, 30)
        self.collisionrect = pygame.Rect(self.rect.centerx + 4,
                                         self.rect.centery + 4, 8, 8)
        self.speed = 16

    def keepMoving(self, targetX, targetY, map):
        global pcDir, pcIndex, pc_Up
        goDirX = 0
        goDirY = 0
        self.collisionrect.center = self.rect.center
        flagR = True
        self.collisionrect.centerx += 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pcDir == 3:
                flagR = False
                break
        self.collisionrect.center = self.rect.center
        flagU = True
        self.collisionrect.centery -= 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pcDir == 0:
                flagU = False
                break
        self.collisionrect.center = self.rect.center
        flagL = True

        self.collisionrect.centerx -= 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pcDir == 2:
                flagL = False
                break
        self.collisionrect.center = self.rect.center
        flagD = True
        self.collisionrect.centery += 16
        for tile in map.tiles:
            if self.collisionrect.colliderect(tile) or pcDir == 1:
                flagD = False
                break

        self.collisionrect.center = self.rect.center
        if self.rect.x < targetX:
            if flagR == True:
                goDirX = self.speed
                goDirY = 0
                pcDir = 2
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.y > targetY:
                if flagU == True:
                    goDirX = 0
                    goDirY = -self.speed
                    pcDir = 1
                    pcIndex += 1
                    if pcIndex > len(pc_Up) - 1:
                        pcIndex = 0
                    self.image = pChildSprite[pcDir][pcIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagD == True:
                goDirX = 0
                goDirY = self.speed
                pcDir = 0
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY

        if self.rect.y > targetY:
            if flagU == True:
                goDirX = 0
                goDirY = -self.speed
                pcDir = 1
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.x > targetX:
                if flagL == True:
                    goDirX = -self.speed
                    goDirY = 0
                    pcDir = 3
                    pcIndex += 1
                    if pcIndex > len(pc_Up) - 1:
                        pcIndex = 0
                    self.image = pChildSprite[pcDir][pcIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagR == True:
                goDirX = self.speed
                goDirY = 0
                pcDir = 2
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY

        if self.rect.x > targetX:
            if flagL == True:
                goDirX = -self.speed
                goDirY = 0
                pcDir = 3
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.y < targetY:
                if flagD == True:
                    goDirX = 0
                    goDirY = self.speed
                    pcDir = 0
                    pcIndex += 1
                    if pcIndex > len(pc_Up) - 1:
                        pcIndex = 0
                    self.image = pChildSprite[pcDir][pcIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagU == True:
                goDirX = 0
                goDirY = -self.speed
                pcDir = 1
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
        if self.rect.y < targetY:
            if flagD == True:
                goDirX = 0
                goDirY = self.speed
                pcDir = 0
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
            elif self.rect.x < targetX:
                if flagR == True:
                    goDirX = self.speed
                    goDirY = 0
                    pcDir = 2
                    pcIndex += 1
                    if pcIndex > len(pc_Up) - 1:
                        pcIndex = 0
                    self.image = pChildSprite[pcDir][pcIndex]
                    self.image.set_colorkey((84, 84, 84))
                    return goDirX, goDirY
            elif flagL == True:
                goDirX = -self.speed
                goDirY = 0
                pcDir = 3
                pcIndex += 1
                if pcIndex > len(pc_Up) - 1:
                    pcIndex = 0
                self.image = pChildSprite[pcDir][pcIndex]
                self.image.set_colorkey((84, 84, 84))
                return goDirX, goDirY
        if flagL == True:
            goDirX = -self.speed
            goDirY = 0
            pcDir = 3
            pcIndex += 1
            if pcIndex > len(pc_Up) - 1:
                pcIndex = 0
            self.image = pChildSprite[pcDir][pcIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY
        if flagD == True:
            goDirX = 0
            goDirY = self.speed
            pcDir = 0
            pcIndex += 1
            if pcIndex > len(pc_Up) - 1:
                pcIndex = 0
            self.image = pChildSprite[pcDir][pcIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY
        if flagR == True:
            goDirX = self.speed
            goDirY = 0
            pcDir = 2
            pcIndex += 1
            if pcIndex > len(pc_Up) - 1:
                pcIndex = 0
            self.image = pChildSprite[pcDir][pcIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY
        if flagU == True:
            goDirX = 0
            goDirY = -self.speed
            pcDir = 1
            pcIndex += 1
            if pcIndex > len(pc_Up) - 1:
                pcIndex = 0
            self.image = pChildSprite[pcDir][pcIndex]
            self.image.set_colorkey((84, 84, 84))
            return goDirX, goDirY


GAME_TITLE = "Clyde"
pygame.init()
pygame.mixer.init()
DISPLAY_W, DISPLAY_H = 640, 640
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
DISPLAY_SURF = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption(GAME_TITLE)

DISPLAY_SURF.fill(BGCOLOR)
clock = pygame.time.Clock()

#current animation frame
animIndex = 0
#current direction (0 is down, 1 up, 2 right, 3 left)
animDir = 0

pmIndex = 0
pmDir = 0
pcIndex = 0
pcDir = 0
#pSpeed is how far Clyde moves each time he does
#clyde is a 32x32 sprite
pSpeed = 16

lvl_spritesheet = Spritesheet('pacmanATLAS.png')
clyde_spritesheet = Spritesheet('clydespritesheet.png')
pacmom_spritesheet = Spritesheet('pmspritesheet.png')
pacChild_spritesheet = Spritesheet('pcsprite.png')

clyde_Down = [
    clyde_spritesheet.parse_sprite('clydeDown0.png'),
    clyde_spritesheet.parse_sprite('clydeDown1.png'),
    clyde_spritesheet.parse_sprite('clydeDown2.png'),
    clyde_spritesheet.parse_sprite('clydeDown3.png')
]

clyde_Up = [
    clyde_spritesheet.parse_sprite('clydeUp0.png'),
    clyde_spritesheet.parse_sprite('clydeUp1.png'),
    clyde_spritesheet.parse_sprite('clydeUp2.png'),
    clyde_spritesheet.parse_sprite('clydeUp3.png')
]

clyde_Right = [
    clyde_spritesheet.parse_sprite('clydeRight0.png'),
    clyde_spritesheet.parse_sprite('clydeRight1.png'),
    clyde_spritesheet.parse_sprite('clydeRight2.png'),
    clyde_spritesheet.parse_sprite('clydeRight3.png')
]

clyde_Left = [
    clyde_spritesheet.parse_sprite('clydeLeft0.png'),
    clyde_spritesheet.parse_sprite('clydeLeft1.png'),
    clyde_spritesheet.parse_sprite('clydeLeft2.png'),
    clyde_spritesheet.parse_sprite('clydeLeft3.png')
]

pm_Down = [
    pacmom_spritesheet.parse_sprite('pmDown1.png'),
    pacmom_spritesheet.parse_sprite('pmDown2.png'),
    pacmom_spritesheet.parse_sprite('pmDown3.png'),
    pacmom_spritesheet.parse_sprite('pmDown4.png'),
    pacmom_spritesheet.parse_sprite('pmDown5.png'),
    pacmom_spritesheet.parse_sprite('pmDown6.png'),
    pacmom_spritesheet.parse_sprite('pmDown7.png'),
]

pm_Up = [
    pacmom_spritesheet.parse_sprite('pmUp1.png'),
    pacmom_spritesheet.parse_sprite('pmUp2.png'),
    pacmom_spritesheet.parse_sprite('pmUp3.png'),
    pacmom_spritesheet.parse_sprite('pmUp4.png'),
    pacmom_spritesheet.parse_sprite('pmUp5.png'),
    pacmom_spritesheet.parse_sprite('pmUp6.png'),
    pacmom_spritesheet.parse_sprite('pmUp7.png'),
]

pm_Right = [
    pacmom_spritesheet.parse_sprite('pmRight1.png'),
    pacmom_spritesheet.parse_sprite('pmRight2.png'),
    pacmom_spritesheet.parse_sprite('pmRight3.png'),
    pacmom_spritesheet.parse_sprite('pmRight4.png'),
    pacmom_spritesheet.parse_sprite('pmRight5.png'),
    pacmom_spritesheet.parse_sprite('pmRight6.png'),
    pacmom_spritesheet.parse_sprite('pmRight7.png'),
]

pm_Left = [
    pacmom_spritesheet.parse_sprite('pmLeft1.png'),
    pacmom_spritesheet.parse_sprite('pmLeft2.png'),
    pacmom_spritesheet.parse_sprite('pmLeft3.png'),
    pacmom_spritesheet.parse_sprite('pmLeft4.png'),
    pacmom_spritesheet.parse_sprite('pmLeft5.png'),
    pacmom_spritesheet.parse_sprite('pmLeft6.png'),
    pacmom_spritesheet.parse_sprite('pmLeft7.png'),
]

pc_Down = [
    pacChild_spritesheet.parse_sprite('pcDown1.png'),
    pacChild_spritesheet.parse_sprite('pcDown2.png'),
    pacChild_spritesheet.parse_sprite('pcDown3.png'),
    pacChild_spritesheet.parse_sprite('pcDown4.png')
]

pc_Up = [
    pacChild_spritesheet.parse_sprite('pcUp1.png'),
    pacChild_spritesheet.parse_sprite('pcUp2.png'),
    pacChild_spritesheet.parse_sprite('pcUp3.png'),
    pacChild_spritesheet.parse_sprite('pcUp4.png')
]

pc_Right = [
    pacChild_spritesheet.parse_sprite('pcRight1.png'),
    pacChild_spritesheet.parse_sprite('pcRight2.png'),
    pacChild_spritesheet.parse_sprite('pcRight3.png'),
    pacChild_spritesheet.parse_sprite('pcRight4.png')
]

pc_Left = [
    pacChild_spritesheet.parse_sprite('pcLeft1.png'),
    pacChild_spritesheet.parse_sprite('pcLeft2.png'),
    pacChild_spritesheet.parse_sprite('pcLeft3.png'),
    pacChild_spritesheet.parse_sprite('pcLeft4.png')
]

pMomSprite = [pm_Down, pm_Up, pm_Right, pm_Left]
clydeSprite = [clyde_Down, clyde_Up, clyde_Right, clyde_Left]
pChildSprite = [pc_Down, pc_Up, pc_Right, pc_Left]
map = TileMap(LEVEL_FILENAME, lvl_spritesheet)

maxPellets = len(map.pellets)
numPellets = maxPellets
#x and y are clyde's x and y position
playerX = map.start_x
playerY = map.start_y
clydePos = (playerX, playerY)

pmX = map.pmStartX
pmY = map.pmStartY
pcX = map.pcStartX
pcY = map.pcStartY
#both setDir variables are used to store the direction/speed Clyde should move when he does. moveDir is the used when movement is processed
moveDirX = 0
moveDirY = 0
setDirX = 0
setDirY = 0

eatit = pygame.mixer.Sound('eating_pellet2.wav')
deadass = pygame.mixer.Sound('death_sound.wav')

clyde = Clyde()
pMom = PacMom()
pChild = PacChild()
#flipper is used as a control number to get Clyde to only move every set number of frames. change flipperMAX (>=1) and clyde will update more often or less often
flipper = 0
flipperMAX = 3
PC_SCATTER_FRAMES = 300
PC_CHASE_FRAMES = 300
PM_SCATTER_FRAMES = 150
PM_CHASE_FRAMES = 450
pcScatter = False
pmScatter = False
pmCounter = PM_CHASE_FRAMES
pcCounter = PC_CHASE_FRAMES
pcPX = 544
pcPY = 96
pmPX = 96
pmPY = 544
font = pygame.font.Font('kongtext.ttf', 18)
smallFont = pygame.font.Font('kongtext.ttf', 6)
songList = "Clide2.wav Clide3.wav Clide4.wav Clide5.wav".split()

pygame.mixer.music.load("Clide0.wav")
pygame.mixer.music.play()
rngSongNum = random.randint(0,len(songList)-1)
gameOver = False
winText = font.render("Congratulations!", False, (255, 255, 255))
gameOverText = font.render('Would You like to play again?', False, (255,255,255))
pressSpace = font.render('Press Space!', False, (255, 255, 255))
textRect = gameOverText.get_rect()
pressSpaceRect = pressSpace.get_rect()
winTextRect = winText.get_rect()
textRect.center = (DISPLAY_W // 2 , DISPLAY_H // 2)
winTextRect.center = (textRect.x, textRect.y-(textRect.height/2))
pressSpaceRect.center = (textRect.centerx, textRect.centery+(textRect.height))
winner = True

while True:
    while pygame.mixer.music.get_busy():
        canvas.fill(BGCOLOR)
        map.draw_map(canvas)
        DISPLAY_SURF.blit(canvas, (0, 0))
        pygame.display.update()
        clock.tick(30)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(songList[rngSongNum])
    pygame.mixer.music.play(-1)
    while numPellets != 0:
        if pmScatter == False:
            pmCounter -= 1
            if pmCounter == 0:
                pmScatter = True
                pmCounter = PM_SCATTER_FRAMES
        if pcScatter == False:
            pcCounter -= 1
            if pcCounter == 0:
                pcScatter = True
                pcCounter = PC_SCATTER_FRAMES
        if pmScatter == True:
            pmCounter -= 1
            if pmCounter == 0:
                pmScatter = False
                pmCounter = PM_CHASE_FRAMES
        if pcScatter == True:
            pcCounter -= 1
            if pcCounter == 0:
                pcScatter = False
                pcCounter = PC_CHASE_FRAMES
        numPellets = len(map.pellets)
        events = pygame.event.get()
        playerCenterX, playerCenterY = playerX + 16, playerY + 16
        playerCenter = (playerCenterX, playerCenterY)
        for event in events:

            #keys holds all keys pressed since last process
            keys = pygame.key.get_pressed()

            #player movement decision making(not including collision)
            if keys[K_UP]:
                setDirY = -pSpeed
                setDirX = 0
                clyde.getHits(map)

            elif keys[K_DOWN]:
                setDirY = pSpeed
                setDirX = 0
                clyde.getHits(map)

            elif keys[K_LEFT]:
                setDirX = -pSpeed
                setDirY = 0
                clyde.getHits(map)

            elif keys[K_RIGHT]:
                setDirX = pSpeed
                setDirY = 0
                clyde.getHits(map)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #player Movement process
        if flipper == 0:
            clyde.checkDir(map)
            playerX += moveDirX
            playerY += moveDirY
            flipper += 1
            if animIndex >= (len(clydeSprite[animDir]) - 1):
                animIndex = 0
            if (moveDirX, moveDirY) == (0, pSpeed):
                animDir = 0
                animIndex += 1
            elif (moveDirX, moveDirY) == (0, -pSpeed):
                animDir = 1
                animIndex += 1
            elif (moveDirX, moveDirY) == (pSpeed, 0):
                animDir = 2
                animIndex += 1
            elif (moveDirX, moveDirY) == (-pSpeed, 0):
                animDir = 3
                animIndex += 1
            if playerX < 0:
                playerX = 640
            elif playerX > 640:
                playerX = 0
            if playerY < 0:
                playerY = 640
            elif playerY > 640:
                playerY = 0
            clyde.rect.center = (playerX + 16, playerY + 16)
            clyde.image = clydeSprite[animDir][animIndex]

            if pmScatter == False:
                pmGoX, pmGoY = pMom.keepMoving(playerX, playerY, map)
            else:
                pmGoX, pmGoY = pMom.keepMoving(pmPX, pmPY, map)
            pmX += pmGoX
            pmY += pmGoY
            if pcScatter == False:
                pcGoX, pcGoY = pChild.keepMoving(playerX, playerY, map)
            else:
                pcGoX, pcGoY = pChild.keepMoving(pcPX, pcPY, map)
            pcX += pcGoX
            pcY += pcGoY
        else:
            flipper += 1
            if flipper >= flipperMAX:
                flipper = 0

        if numPellets == 0:
            gameOver = True
        pChild.rect.topleft = (pcX, pcY)
        pMom.rect.topleft = (pmX, pmY)
        pChild.collisionrect.center = pChild.rect.center
        pMom.collisionrect.center = pMom.rect.center
        if clyde.rect.colliderect(pMom.rect) or clyde.rect.colliderect(pChild.rect):
            winner = False
            deadass.play()
            gameOver = True
            break
        canvas.fill(BGCOLOR)
        map.draw_map(canvas)
        canvas.blit(pChild.image, (pcX, pcY))
        canvas.blit(pMom.image, (pmX, pmY))
        canvas.blit(clyde.image, (playerX, playerY))
        DISPLAY_SURF.blit(canvas, (0, 0))
        pygame.display.update()
        clock.tick(30)

    while gameOver == True:
        events = pygame.event.get()
        for event in events:
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                gameOver = False
                reset = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        canvas.fill(BGCOLOR)
        map.draw_map(canvas)
        canvas.blit(gameOverText,textRect)
        canvas.blit(pressSpace, pressSpaceRect)
        if winner == True:
            canvas.blit(winText, winTextRect)
        DISPLAY_SURF.blit(canvas, (0, 0))
        pygame.display.update()
        clock.tick(30)
        pass

    while reset == True:
        lNum = random.randint(0, len(levelList) - 1)
        LEVEL_FILENAME = levelList[lNum]
        map = TileMap(LEVEL_FILENAME, lvl_spritesheet)
        maxPellets = len(map.pellets)
        numPellets = maxPellets
        pmX = map.pmStartX
        pmY = map.pmStartY
        pcX = map.pcStartX
        pcY = map.pcStartY
        playerX = map.start_x
        playerY = map.start_y
        rngSongNum = random.randint(0, len(songList) - 1)
        pygame.mixer.music.unload()
        pygame.mixer.music.load("Clide0.wav")
        canvas.fill(BGCOLOR)
        map.draw_map(canvas)
        canvas.blit(pChild.image, (pcX, pcY))
        canvas.blit(pMom.image, (pmX, pmY))
        canvas.blit(clyde.image, (playerX, playerY))
        DISPLAY_SURF.blit(canvas, (0, 0))
        pygame.display.update()
        pygame.mixer.music.play()
        reset = False
        clock.tick(30)

