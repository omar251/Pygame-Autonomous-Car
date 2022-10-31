import math
import pygame

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
W,H =600,600
HW,HH =W/2,H/2
AREA = W * H

pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W,H))
pygame.display.set_caption("distance and direction")
FPS = 120
BLACK =(0,0,0,255)
WHITE =(255,255,255,255)

x,y = HW,HH
pmx,pmy = x,y
dx,dy = 0,0
distance = 0
speed = 8
while True :
    events()
    m =pygame.mouse.get_pressed()
    if m[0] and not distance:
        mx,my = pygame.mouse.get_pos()
        
        radians =math.atan2(my - pmy,mx - pmx)
        distance = int(math.hypot(mx - pmx,my - pmy)/speed)
        
        dx, dy= math.cos(radians)*speed,math.sin(radians)*speed
        pmx,pmy = mx,my
    if distance:
        distance -=1
        x += dx
        y += dy
    pygame.draw.circle(DS,WHITE,(int(x),int(y)),25,0)
    if distance:
        pygame.draw.circle(DS,(255,0,0),(pmx,pmy),5,0)
    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)