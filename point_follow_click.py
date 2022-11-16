import math
import pygame

BLACK =(0,0,0)
WHITE =(255,255,255)
RED = (255,0,0)
W,H =600,600
HW,HH = W/2,H/2

def move_point(destination = (0,0),pos = pygame.math.Vector2(0,0),time = 5):
    delta = destination - pos
    distance = round(math.hypot(delta[0],delta[1]))
    if not distance == 0:
        speed = distance/time
        direction = pygame.math.Vector2([math.cos(math.atan2(delta[1],delta[0])),math.sin(math.atan2(delta[1],delta[0]))]) 
        pos += direction * speed
    return pos
def main():       
    pygame.init()
    DS = pygame.display.set_mode((W,H))
    pygame.display.set_caption("distance and direction")

    pos = pygame.math.Vector2(HW,HH)
    destination = (HW,HH)
    time = 5
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            destination = pygame.mouse.get_pos()    
        pos = move_point(destination,pos)
        # delta = destination - pos
        # distance = round(math.hypot(delta[0],delta[1]))
        # speed = distance/time
        # direction = pygame.math.Vector2([math.cos(math.atan2(delta[1],delta[0])),math.sin(math.atan2(delta[1],delta[0]))]) 
        # pos += direction * speed
        pygame.draw.circle(DS,WHITE,pos,25)
        pygame.draw.circle(DS,RED,destination,5)
        pygame.display.update()
        pygame.time.Clock().tick(60)
        DS.fill(BLACK)
if __name__ == "__main__":
    main()