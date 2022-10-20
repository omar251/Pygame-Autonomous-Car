import math
from pickle import TRUE
from turtle import distance
from numpy import source
import pygame
BLACK =(0,0,0,255)
WHITE =(255,255,255,255)
W,H =600,600
HW,HH =W/2,H/2
AREA = W * H
class Car:
    def __init__(self,screen):
        self.screen  = screen
        self.destination =[]
        self.source =[]
        self.radar = HW,HH
        self.angle_count = 0
        self.dx,self.dy = 0,0
        self.distance = 0
        self.speed = self.calculated_speed = 1
        self.surface = pygame.image.load("car.png")
        self.rotate_surface = self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.rect = self.rotate_surface.get_rect()  
        self.rect.center = self.source = self.destination = self.x,self.y = HW,HH 
        self.angle_of_rotation = self.current_angle = self.new_angle = self.rot_angle = 0 
        self.rotation_speed = 1    
        self.car_moving = False
    def rot_center(self,image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    def draw_Car(self): 
        self.screen.blit(self.rotate_surface, self.rect)
        # pygame.draw.line(self.screen,(255,0,0),self.rect.center, self.destination, 1)
        pygame.draw.circle(self.screen,(255,0,0),self.destination,9,0)
        pygame.draw.circle(self.screen,(0,255,0),self.rect.center,5,0)
        pygame.draw.circle(self.screen,(0,0,255),self.destination,2,0) 
    def check_radar(self,len = 100):
        x = int(self.rect.center[0] + math.cos(math.radians(((self.rot_angle ) - 360))) * len)
        y = int(self.rect.center[1] + math.sin(math.radians(((self.rot_angle ) - 360))) * len)
        # dist = int(math.sqrt(math.pow(x - self.rect.center[0], 2) + math.pow(y - self.rect.center[1], 2)))
        self.radar = x, y
    def calculate_directions(self): 
        if self.distance == 0 and self.angle_of_rotation == 0 :
            self.distance = int(math.hypot(self.destination[0] - self.source[0],self.destination[1] - self.source[1])/self.speed)  
            
            radians =math.atan2(self.destination[1] - self.source[1],self.destination[0] - self.source[0])
            self.dx = math.cos(radians)*self.speed
            self.dy = math.sin(radians)*self.speed
            
            # self.new_angle = self.rot_angle = int(math.degrees(math.atan2(-(self.destination[1] - self.rect.center[1]), self.destination[0] - self.rect.center[0])))
            self.new_angle = self.rot_angle = int(math.degrees(math.atan2(-(self.destination[1] - self.source[1]), self.destination[0] - self.source[0])))
            self.angle_of_rotation = x =(self.new_angle - self.current_angle) % 360
            if abs(self.angle_of_rotation) > 180:
                self.angle_of_rotation = int(self.angle_of_rotation - (360 * (self.angle_of_rotation/abs(self.angle_of_rotation))))
    def rotate_car(self):
        if not self.distance == 0:
            self.calculate_rotation_speed()
            self.current_angle += self.rotation_speed
            self.angle_of_rotation -= self.rotation_speed
            self.rotate_surface = self.rot_center(self.surface,self.current_angle)         
    def calculate_rotation_speed(self):
        speeds = []
        if self.angle_of_rotation == 0:
            self.rotation_speed = 0
        else:
            for i in range(1,abs(self.angle_of_rotation)+1,1):
                if abs(self.angle_of_rotation)%i == 0:
                    speeds.append(self.angle_of_rotation/i)
            if(len(speeds)>0):
                self.rotation_speed = int(speeds.pop(int((len(speeds))/2))) 
    def calculate_speed(self):
        speeds = []
        if self.distance == 0:
            self.calculated_speed = 0
        else:
            for i in range(1,abs(self.distance)+1,1):
                if abs(self.distance)%i == 0:
                    speeds.append(self.distance/i)
            if(len(speeds)>0):
                self.calculated_speed = int(speeds.pop(int((len(speeds))/2)))               
    def move_car_to_point(self):
        if not self.distance == 0 and self.angle_of_rotation == 0 :  
            self.calculate_speed()     
            self.distance -= self.calculated_speed
            self.x += self.dx * self.calculated_speed
            self.y += self.dy * self.calculated_speed
            self.rect.center = self.source = (self.x,self.y)
    def move_to_point(self,point):
        self.destination = point 
        self.calculate_directions()
        self.rotate_car()
        self.move_car_to_point()
    def rotate_and_move_car(self,point):
        self.move_to_point(point)
        self.draw_Car()
def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W,H))
pygame.display.set_caption("distance and direction")
FPS = 120
car = Car(DS)
points =[]
point = HW,HH
click = True
while True :
    events()
    m =pygame.mouse.get_pressed()
    if m[0]:
        point = pygame.mouse.get_pos()
    car.rotate_and_move_car(point)
    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)