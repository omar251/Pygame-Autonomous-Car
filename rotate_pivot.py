import pygame, math, sys
from pygame.locals import *
 
Blue = (0,0,255)
Black = (0, 0, 0) 
Green = (0,255,0)
White = (255,255,255)
  
pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Sailing!')
  
FPS = 30
fpsClock = pygame.time.Clock()
  
Sail = pygame.Surface([100,50])
Sail.set_colorkey(Black)
Sail.fill(White)
  
degrees = 0

x = 300
y = 300

def blitRotate(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h         = image.get_size()
    sin_a, cos_a = math.sin(math.radians(angle)), math.cos(math.radians(angle)) 
    min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_x - pivot_move[0], pos[1] - originPos[1] - min_y + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(Black)
    blitRotate(DISPLAYSURF, Sail, (x, y), (0, 5), degrees)   
    pygame.display.flip()
    fpsClock.tick(FPS)
    degrees += 20
