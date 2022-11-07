import math
import pygame
BLACK =(0,0,0,255)
WHITE =(255,255,255,255)
RED = (255,0,0,255)
BLUE = (0,0,255,255)
GREEN = (0,255,0,255)
W,H =600,600
car_shift = 100,100
HW,HH =(W/2),(H/2)
AREA = W * H
class Car:
    def __init__(self,screen,map):
        self.map = map
        self.map_H,self.map_W = map.get_height(),map.get_width()
        self.screen  = screen
        self.destination =[]
        self.source =[]
        self.rotated_offset = self.offset = pygame.math.Vector2(40,0)
        self.front_radars =[]
        self.back_radars = []
        self.radars =[]
        self.radar = HW,HH
        self.directions = pygame.math.Vector2(0,0)
        self.distance = 0
        self.speed = self.calculated_speed = 1
        self.surface = pygame.image.load("car.png")
        self.rotate_surface = self.surface = pygame.transform.scale(self.surface, (150, 150))
        self.source = self.destination = pygame.math.Vector2(HW,HH)
        self.rect = self.rotate_surface.get_rect(center = self.source + self.rotated_offset)  
        self.angle_of_rotation = self.current_angle = self.new_angle = 0   
        self.brakes = False
        self.obstacle = False
        self.calculate_rotation = True
        self.calculate_direction_and_distance = True
        self.reached = True
        self.radar_length = self.max_radar = 100
        self.time = 15
    
    def Right(self,speed = 3):   
        self.rotate(speed)
   
    def Left(self,speed = 3):
        self.rotate(-speed)
       
    def Forword(self,speed = 5):     
        self.directions *=0 
        self.directions += math.cos(math.radians(self.current_angle)),math.sin(math.radians(self.current_angle))
        self.source += self.directions * speed
        self.rect = self.rotate_surface.get_rect(center = self.source + self.rotated_offset)
        
    def Backword(self,speed = 5):
        self.directions *=0 
        self.directions += math.cos(math.radians(self.current_angle)),math.sin(math.radians(self.current_angle))
        self.source -= self.directions * speed
        self.rect = self.rotate_surface.get_rect(center = self.source + self.rotated_offset)

    def move(self):
        keys = pygame.key.get_pressed()
        border = False
        
        if self.source[0] < 20 or self.source[0] > W - 20 or self.source[1] > H - 20 or self.source[1] < 20: border = True
        
        if self.source[0] < 20: self.source[0] = 20
        elif self.source[0] > W - 20: self.source[0] = W - 20
        
        if self.source[1] < 20: self.source[1]= 20
        elif self.source[1] > H - 20: self.source[1] = H - 20
        
        if not border:
            if keys[pygame.K_UP]:
                self.Forword()
                if keys[pygame.K_RIGHT]:
                    self.Right()
                if keys[pygame.K_LEFT]:
                    self.Left()
    
            if keys[pygame.K_DOWN]:              
                self.Backword()
                if keys[pygame.K_RIGHT]:
                    self.Left()
                if keys[pygame.K_LEFT]:
                    self.Right()
               
    def rotate(self,degrees = 0):
        self.current_angle = (self.current_angle + degrees) % 360
        self.rotated_offset = self.offset.rotate(self.current_angle)
        self.rotate_surface = pygame.transform.rotozoom(self.surface, -self.current_angle, 1)  
        self.rect = self.rotate_surface.get_rect(center=self.source + self.rotated_offset)  
         
    def draw_Car(self): 
        # pygame.draw.rect(self.screen,(255,0,0),self.rect)
        self.screen.blit(self.rotate_surface, self.rect)   
        # pygame.draw.line(self.screen,(255,0,0),self.rect.center, self.destination, 1)
        pygame.draw.circle(self.screen,BLUE,self.destination,9,0)
        pygame.draw.circle(self.screen,GREEN,self.rect.center,5,0)
        # pygame.draw.circle(self.screen,WHITE,self.source + self.rotated_offset,5,0)
        # pygame.draw.circle(self.screen,BLUE,self.radar,2,0) 
        # pygame.draw.line(self.screen,(0,255,0),self.rect.center, self.radar, 1)
        self.draw_radar()
        
    def update_map(self,map):
        self.map = map
        
    def update_radars(self,front=1,back=1):
        if front == 1:
            self.front_radars.clear()
            for degree in [-45,0,45]:
                self.check_radars(degree,200,1)
            self.back_radars.clear()
        else:
            self.front_radars.clear()
        if back == 1:    
            self.back_radars.clear()
            for degree in [135,-135]:
                self.check_radars(degree,100,-1)
        else:
            self.back_radars.clear()
            
    def turn_radar_off(self,front = 1,back = 1):
            if front == 1:
                self.front_radars.clear()
            if back == 1:
                self.back_radars.clear()
                
    def check_radars(self,degree = 0, radar_length = 100,radar_type=0):
        self.max_radar = radar_length
        self.radar_length = 0
        radian = math.radians(self.current_angle + degree)
        dx,dy = int(math.cos(radian) * self.radar_length),int(math.sin(radian) * self.radar_length)
        self.radar = x,y = self.rect.center[0] + dx, self.rect.center[1] + dy
        while not self.map.get_at((x, y)) == WHITE and self.radar_length < self.max_radar:
            self.radar_length += 1
            radian = math.radians(self.current_angle + degree)
            dx,dy = int(math.cos(radian) * self.radar_length),int(math.sin(radian) * self.radar_length)
            x,y = self.rect.center[0] + dx, self.rect.center[1] + dy  
            if not (0<x<self.map_W and 0<y<self.map_H):
                break

        radar_distance = int(math.hypot(x - self.rect.center[0],y - self.rect.center[1]))  
        # self.radars.append([(x,y),radar_distance])
        if radar_type == -1:
            self.back_radars.append([(x,y),radar_distance])
        elif radar_type == 1:
            self.front_radars.append([(x,y),radar_distance])

    def draw_radar(self):
        self.update_radars()
        for r in self.front_radars:
            pos = r[0]
            if r[1] < 70:color = RED
            else : color = GREEN
            pygame.draw.line(self.screen, color, self.rect.center, pos, 1)
            pygame.draw.circle(self.screen, color, pos, 5)  
        for r in self.back_radars:
            pos = r[0]
            if r[1] < 70:color = RED
            else : color = BLUE
            pygame.draw.line(self.screen, color, self.rect.center, pos, 1)
            pygame.draw.circle(self.screen, color, pos, 5)  
  
    def get_max_back_destination(self):  
        self.update_radars()
        back_radar_distances = [i[1] for i in self.back_radars]
        back_destination = self.back_radars[back_radar_distances.index(max(back_radar_distances))][0] 
        
        return [back_destination,max(back_radar_distances)]
    
    def check_obstacle(self):
        self.obstacle = False
        for radar in self.front_radars:
            if radar[1] < 50:
                self.obstacle = True
                break
        
    def get_destination(self):
        self.update_radars()
        front_radar_distances = [i[1] for i in self.front_radars]
        max_back_destination,max_back_distance = self.get_max_back_destination()
        # print(max_back_distance,max(front_radar_distances))
        if front_radar_distances[1] == max(front_radar_distances):
            destination = self.front_radars[1][0]
        elif max(front_radar_distances) < max_back_distance:
            destination = max_back_destination
        
        else:
            destination = self.front_radars[front_radar_distances.index(max(front_radar_distances))][0] 
            
        return destination
    
    def calculate_angle_of_rotation(self):
        if self.calculate_rotation :
            self.distance = 0
            self.directions *= 0
            delta = self.destination - self.source
            self.new_angle = int(math.degrees(math.atan2(delta[1], delta[0])))
            self.angle_of_rotation =(self.new_angle - self.current_angle) % 360
            if abs(self.angle_of_rotation) > 180:
                self.angle_of_rotation = int(self.angle_of_rotation - (360 * (self.angle_of_rotation/abs(self.angle_of_rotation))))
            
            self.angle_of_rotation = (self.new_angle - self.current_angle) % 180
            if abs(self.angle_of_rotation) > abs(abs(self.angle_of_rotation) - 180):
                self.angle_of_rotation = int(abs(abs(self.angle_of_rotation) - 180) * -(abs(self.angle_of_rotation)/self.angle_of_rotation))

            self.calculate_rotation = False
            
    def calculate_directions(self): 
        if self.calculate_direction_and_distance :
            delta = self.destination - self.source
            radians = math.atan2(delta[1],delta[0])
            self.distance = int(math.hypot(delta[0],delta[1]))  
            self.directions += (math.cos(radians),math.sin(radians))
            self.calculated_destination = self.source + self.directions * self.distance      
            self.calculate_direction_and_distance = False

    def rotate_car(self):
        if not round(self.angle_of_rotation) == 0:
            self.speed = self.angle_of_rotation / self.time
            self.current_angle += self.speed
            self.rotate()
            self.angle_of_rotation -= self.speed 
                             
    def move_car_to_point(self):
        if not self.distance == 0 and round(self.angle_of_rotation) == 0 :    
            self.speed = self.distance / self.time
            self.source += self.directions * self.speed
            self.rect = self.rotate_surface.get_rect(center=self.source + self.rotated_offset)  
            self.destination_reached()
            self.distance -= self.speed
            
    def brake_car(self):
        self.destination = self.source
        self.distance = self.angle_of_rotation = 0
        self.brakes = True
        
    def destination_reached(self):
        if self.source == self.calculated_destination:
            self.reached = True
        else: 
            self.reached = False
            
    def movecar(self):
        self.calculate_angle_of_rotation()
        self.calculate_directions()
        self.rotate_car()
        self.check_obstacle()
        if self.obstacle:
            self.brake_car()
            return
        self.move_car_to_point()
             
    def set_destination(self,point = None ):
        if point == None or point == self.source or self.brakes:
            self.brake_car()
            return
        elif point == self.destination:
            self.calculate_rotation = False
            self.calculate_direction_and_distance = False
        self.destination = point 
        self.movecar()   

    def prepare_car(self):    
        self.brakes = False
        self.calculate_rotation = True
        self.calculate_direction_and_distance = True 
    
    def get_steps(self,index = 0,list_of_steps = []):
        if index > len(list_of_steps)-1 or len(list_of_steps) == 0:
            return None
        return list_of_steps.pop(index)
    
def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W,H))
pygame.display.set_caption("distance and direction")
map = pygame.image.load('map.png')
FPS = 120
car = Car(DS,map)
points = [(60, 360), (60, 330), (60, 300), (60, 270), (60, 240), (60, 210), (60, 180), (90, 180), (120, 180), (150, 180), (180, 180), (210, 180), (240, 180), (270, 180), (300, 180), (330, 180), (360, 180)]
points.reverse()
point = HW,HH
click = True
while True :
    events()
    map = pygame.image.load('map.png')
    DS.blit(map, (0, 0))
    m =pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    if m[2]:
        if car.reached:
            point = car.get_steps(0,points)
            print(point)
            car.reached = False
        car.prepare_car()
    elif m[0] :
        point = mouse
        car.prepare_car()
    car.set_destination(point)
    car.move()
    car.draw_Car()
    car.update_map(map)
    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)