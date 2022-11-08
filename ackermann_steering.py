import math
import pygame

BLACK =(0,0,0)
WHITE =(255,255,255)
RED = (255,0,0)
BLUE = (0,0,255,255)
GREEN = (0,255,0)
W,H =600,600
HW,HH =(W/2),(H/2)
class Car:
    def __init__(self,screen) -> None:  
        self.map = map
        self.screen  = screen
        self.surface = pygame.image.load("car.png")
        self.rotate_surface = self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.source = pygame.math.Vector2(HW,HH)
        self.offset = pygame.math.Vector2(30,0) 
        self.rotated_offset = self.offset.rotate(0)      
        self.rect = self.rotate_surface.get_rect(center = self.source + self.rotated_offset)  
        self.angle_of_rotation = self.current_angle  = 0      
        self.raduis= 0 
        self.rear_wheels = self.front_wheels = pygame.math.Vector2(0,0)
        self.speed = 1
        self.steering_speed = 1

    def rotate(self):
        self.rotated_offset = self.offset.rotate(self.current_angle)
        self.rotate_surface = pygame.transform.rotozoom(self.surface, -self.current_angle, 1)  
        self.rect = self.rotate_surface.get_rect(center=self.source+self.rotated_offset) 

    def move(self):
        keys = pygame.key.get_pressed()
        if not self.angle_of_rotation >= 30 and keys[pygame.K_RIGHT]:self.angle_of_rotation += self.steering_speed
        if not self.angle_of_rotation <= -30 and keys[pygame.K_LEFT]:self.angle_of_rotation -= self.steering_speed 
        self.raduis = 30/math.sin(math.radians(self.angle_of_rotation)) if not self.angle_of_rotation == 0 else 0
        self.rear_wheels  = pygame.math.Vector2(0,self.raduis).rotate(self.current_angle)
        self.front_wheels = pygame.math.Vector2(0,self.raduis).rotate(self.current_angle + self.angle_of_rotation)
        print(self.angle_of_rotation)
        if keys[pygame.K_UP]:
            self.source += self.speed*(math.cos(math.radians(self.current_angle))),self.speed * (math.sin(math.radians(self.current_angle)))
            self.rect = self.rotate_surface.get_rect(center=self.source+self.rotated_offset) 
            self.rotate()
            self.update_angle()
        
    def update_angle(self):
        self.current_angle += math.copysign(0 if (self.angle_of_rotation == 0) else self.speed*(60/self.raduis),self.angle_of_rotation)
        self.current_angle = self.current_angle % 360
        self.angle_of_rotation -= math.copysign(0 if (self.angle_of_rotation == 0) else self.steering_speed,self.angle_of_rotation)
    def draw(self): 
        pygame.draw.rect(self.screen,RED,self.rect,1)
        self.screen.blit(self.rotate_surface, self.rect)   
        pygame.draw.circle(self.screen,GREEN,self.source,5,0)
        pygame.draw.circle(self.screen,RED,self.rect.center,5,0)
        x = 100*math.cos(math.radians((self.current_angle)))+ (self.rect.centerx)
        y = 100*math.sin(math.radians((self.current_angle)))+ (self.rect.centery) 
        pygame.draw.line(self.screen,GREEN,self.rect.center, (x,y) , 3)
        x = 100*math.cos(math.radians((self.angle_of_rotation+self.current_angle)))+ (self.rect.centerx)
        y = 100*math.sin(math.radians((self.angle_of_rotation+self.current_angle)))+ (self.rect.centery) 
        pygame.draw.line(self.screen,BLUE,self.rect.center, (x,y) , 3)
        pygame.draw.line(self.screen,GREEN,self.source, self.source + self.rear_wheels , 3)
        pygame.draw.circle(self.screen,GREEN,self.source + self.rear_wheels,abs(self.raduis),1)
        pygame.draw.line(self.screen,GREEN,self.rect.center, self.rect.center + self.front_wheels , 3)
  

pygame.init()
DS = pygame.display.set_mode((W,H))
pygame.display.set_caption("distance and direction")

car = Car(DS)
time = 10
point = [W/2,H/2]
while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    car.move()
    car.draw()
    pygame.display.update()
    pygame.time.Clock().tick(60)
    DS.fill(BLACK)