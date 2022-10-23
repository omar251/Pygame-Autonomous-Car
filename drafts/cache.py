import math
from turtle import distance
import pygame
BLACK =(0,0,0,255)
WHITE =(255,255,255,255)
RED = (255,0,0,255)
BLUE = (0,0,255,255)
GREEN = (0,255,0,255)
W,H =600,600
HW,HH =W/2,H/2
AREA = W * H
class Car:
    def __init__(self,screen,map):
        self.map = map
        self.screen  = screen
        self.destination =[]
        self.source =[]
        self.radars = []
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
        self.brakes = False
        self.radar_length = 100
    def rot_center(self,image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    def draw_Car(self): 
        # pygame.draw.rect(self.screen,(255,0,0),self.rect)
        self.screen.blit(self.rotate_surface, self.rect)   
        # pygame.draw.line(self.screen,(255,0,0),self.rect.center, self.destination, 1)
        pygame.draw.circle(self.screen,BLUE,self.destination,9,0)
        pygame.draw.circle(self.screen,GREEN,self.rect.center,5,0)
        # pygame.draw.circle(self.screen,BLUE,self.radar,2,0) 
        # pygame.draw.line(self.screen,(0,255,0),self.rect.center, self.radar, 1)
        self.draw_radar()
    def check_radar(self,degree = 0):
        self.radar_length = 0
        radian =math.radians(self.rotation_speed - self.current_angle + degree)
        dx,dy = int(math.cos(radian) * self.radar_length),int(math.sin(radian) * self.radar_length)
        self.radar = x,y = self.rect.center[0] + dx, self.rect.center[1] + dy
        while not self.map.get_at((x, y)) == (255, 255, 255, 255) and self.radar_length < 100:
            self.radar_length += 1
            radian =math.radians(self.rotation_speed - self.current_angle + degree)
            dx,dy = int(math.cos(radian) * self.radar_length),int(math.sin(radian) * self.radar_length)
            self.radar = x,y = self.rect.center[0] + dx, self.rect.center[1] + dy            
        radar_distance = int(math.hypot(x - self.rect.center[0],y - self.rect.center[1]))  
        self.radars.append([(x,y),radar_distance])
    def update_radars(self):
        self.radars.clear()
        for degree in range(-90, 120, 45):
            self.check_radar(degree)
    def draw_radar(self):
        self.update_radars()
        color = GREEN
        for r in self.radars:
            pos = r[0]
            if r[1] < 50:color = RED
            else : color = GREEN
            pygame.draw.line(self.screen, color, self.rect.center, pos, 1)
            pygame.draw.circle(self.screen, color, pos, 5)  
    
        
    def get_destination(self):
        self.update_radars()
        radar_distances = [i[1] for i in self.radars]
        if radar_distances[2] == max(radar_distances):
            destination = self.radars[2][0]
        else:
            destination = self.radars[radar_distances.index(max(radar_distances))][0]  
        return destination
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
        if not self.distance == 0 :
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
                self.calculated_speed = max(int(speeds.pop(int((len(speeds))/2))),self.speed)              
    def move_car_to_point(self):
        if not self.distance == 0 and self.angle_of_rotation == 0 :  
            self.calculate_speed()     
            self.distance -= self.calculated_speed
            self.x += self.dx * self.calculated_speed
            self.y += self.dy * self.calculated_speed
            self.rect.center = self.source = (self.x,self.y)
    def brake_car(self):
        self.destination = self.rect.center
        self.distance = self.angle_of_rotation = 0
        self.brakes = True
    def movecar(self):
        self.calculate_directions()
        self.rotate_car()
        self.move_car_to_point()
    def move_to_point(self,point = None ):
        if point == None:
            # self.destination = self.rect.center
            self.brake_car()
        else:
            if not self.brakes or True:
                self.destination = point 
                self.movecar()
                self.brake_car()
                # self.brakes = True
            else: 
                # self.destination = self.rect.center
                self.brakes = False

        self.draw_Car()

        
def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W,H))
pygame.display.set_caption("distance and direction")
map = pygame.image.load('ring3.png')
FPS = 120
car = Car(DS,map)
points =[]
point = HW,HH
click = True
while True :
    events()
    DS.blit(map, (0, 0))
    m =pygame.mouse.get_pressed()
    
    if m[2]:
        point = car.rect.center
        car.brake_car()
    if m[0] :#and car.brakes:
        point = pygame.mouse.get_pos()
        # car.brakes = False
    car.move_to_point(point)
    print(car.brakes,car.distance,car.angle_of_rotation,point)
    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)