import math
import pygame
BLACK =(0,0,0,255)
WHITE =(255,255,255,255)
RED = (255,0,0,255)
BLUE = (0,0,255,255)
GREEN = (0,255,0,255)
W,H =600,600
car_shift = 100,100
HW,HH =(W/2)+car_shift[0],(H/2)+car_shift[1]
AREA = W * H
class Car:
    def __init__(self,screen,map):
        self.map = map
        self.map_H,self.map_W = map.get_height(),map.get_width()
        self.screen  = screen
        self.destination =[]
        self.source =[]
        self.front_radars =[]
        self.back_radars = []
        self.radars =[]
        self.radar = HW,HH
        self.angle_count = 0
        self.dx,self.dy = 0,0
        self.distance = 0
        self.speed = self.calculated_speed = 1
        self.surface = pygame.image.load("car.png")
        self.rotate_surface = self.surface = pygame.transform.scale(self.surface, (50, 50))
        self.rect = self.rotate_surface.get_rect()  
        self.rect.center = self.source = self.destination = self.x,self.y = HW,HH 
        self.angle_of_rotation = self.current_angle = self.new_angle = self.rot_angle = 0 
        self.rotation_speed = 1    
        self.brakes = False
        self.obstacle = False
        self.calculate = True
        self.calculate_rotation = True
        self.calculate_direction_and_distance = True
        self.reached = True
        self.logs = False
        self.radar_length = self.max_radar = 100
    
    def Right(self,speed = 3):   
        self.angle_of_rotation = -speed
        self.calculate_rotation_speed()
        self.current_angle = (self.current_angle - speed) % 360
        self.rotate_surface = self.rot_center(self.surface,self.current_angle)
   
    def Left(self,speed = 3):
        self.angle_of_rotation = speed
        self.calculate_rotation_speed()
        self.current_angle = (self.current_angle + speed) % 360
        self.rotate_surface = self.rot_center(self.surface,self.current_angle)
       
    def Forword(self,speed = 5):
        self.x += int(math.cos(math.radians(360 - self.current_angle)) * speed)
        self.y += int(math.sin(math.radians(360 - self.current_angle)) * speed)
        self.rect.center = self.source = self.x,self.y
        
    def Backword(self,speed = 5):
        self.x -= int(math.cos(math.radians(360 - self.current_angle)) * speed)
        self.y -= int(math.sin(math.radians(360 - self.current_angle)) * speed)
        self.rect.center = self.source = self.x,self.y

    def move(self):
        keys = pygame.key.get_pressed()
        border = False
        
        if self.x < 20 or self.x > W - 20 or self.y > H - 20 or self.y < 20: border = True
        
        if self.x < 20: self.x = 20
        elif self.x > W - 20: self.x = W - 20
        
        if self.y < 20: self.y= 20
        elif self.y > H - 20: self.y = H - 20
        
        if not border:
            if keys[pygame.K_UP]:
                self.Forword()
                if keys[pygame.K_RIGHT]:
                    self.Right()
                if keys[pygame.K_LEFT]:
                    self.Left()
                self.angle_of_rotation = self.distance = 0
    
            if keys[pygame.K_DOWN]:              
                self.Backword()
                if keys[pygame.K_RIGHT]:
                    self.Left()
                if keys[pygame.K_LEFT]:
                    self.Right()
                self.angle_of_rotation = self.distance = 0
            
            
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
        radian =math.radians(self.rotation_speed - self.current_angle + degree)
        dx,dy = int(math.cos(radian) * self.radar_length),int(math.sin(radian) * self.radar_length)
        self.radar = x,y = self.rect.center[0] + dx, self.rect.center[1] + dy
        while not self.map.get_at((x, y)) == WHITE and self.radar_length < self.max_radar:
            self.radar_length += 1
            radian =math.radians(self.rotation_speed - self.current_angle + degree)
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
            print("##########################calculating angle of rotation",self.calculate_rotation,"##########################") if self.logs else 0
            # self.new_angle = self.rot_angle = int(math.degrees(math.atan2(-(self.destination[1] - self.rect.center[1]), self.destination[0] - self.rect.center[0])))
            self.distance = self.dx = self.dy = 0
            self.new_angle = int(math.degrees(math.atan2(-(self.destination[1] - self.source[1]), self.destination[0] - self.source[0])))
            self.angle_of_rotation =(self.new_angle - self.current_angle) % 360
            if abs(self.angle_of_rotation) > 180:
                self.angle_of_rotation = int(self.angle_of_rotation - (360 * (self.angle_of_rotation/abs(self.angle_of_rotation))))
            
            self.angle_of_rotation = (self.new_angle - self.current_angle) % 180
            if abs(self.angle_of_rotation) > abs(abs(self.angle_of_rotation) - 180):
                self.angle_of_rotation = int(abs(abs(self.angle_of_rotation) - 180) * -(abs(self.angle_of_rotation)/self.angle_of_rotation))
            print("angle of rotation = ",self.angle_of_rotation)if self.logs else 0
            self.calculate_rotation = False
    def calculate_directions(self): 
        if self.calculate_direction_and_distance :
            print("##########################calculating distance:",self.calculate,"##########################")if self.logs else 0
            print("between ",self.source,"and",self.destination)if self.logs else 0
            self.distance = int(math.hypot(self.destination[0] - self.source[0],self.destination[1] - self.source[1]))  
            print("distance = ",self.distance)if self.logs else 0
            
            print("calculating directions")if self.logs else 0
            radians =math.atan2(self.destination[1] - self.source[1],self.destination[0] - self.source[0])
            self.dx = math.cos(radians) 
            self.dy = math.sin(radians) 
            print("direction in x = ",self.dx,"in y = ",self.dy)if self.logs else 0
            self.calculated_destination = round(self.x + (self.dx * self.distance)),round(self.y +(self.dy * self.distance))
            self.calculate_direction_and_distance = False

    def rotate_car(self):
        if not self.angle_of_rotation == 0:
            self.calculate_rotation_speed()
            self.current_angle += self.rotation_speed
            self.current_angle = self.current_angle % 360
            self.angle_of_rotation -= self.rotation_speed
            self.rotate_surface = self.rot_center(self.surface,self.current_angle) 
            print("angle of rotation : ",self.angle_of_rotation,"and rotation speed = ",-self.rotation_speed) if self.logs else 0
            print("current angle =     ",self.current_angle) if self.logs else 0
    def calculate_rotation_speed(self):
        speeds = []
        if self.angle_of_rotation == 0:
            self.rotation_speed = 0
        else:
            for i in range(1,abs(int(self.angle_of_rotation))+1,1):
                if abs(self.angle_of_rotation)%i == 0:
                    speeds.append(self.angle_of_rotation/i)
            if(len(speeds)>0):
                self.rotation_speed = int(speeds.pop(int((len(speeds))/2)))
    def calculate_speed(self):
        speeds = []
        if self.distance == 0:
            self.calculated_speed = 0
        else:
            for i in range(1,int(abs(self.distance)+1),1):
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
            self.rect.center = self.source = (round(self.x),round(self.y))
            print("distance of :       ",self.distance,"with speed = ",-self.calculated_speed) if self.logs else 0
            print("current position =  ",self.source,"destination = ",self.calculated_destination)if self.logs else 0
            self.destination_reached()
    def brake_car(self):
        print("braking car")if self.logs else 0
        self.destination = self.rect.center
        self.distance = self.angle_of_rotation = 0
        self.brakes = True
    def destination_reached(self):
        if self.source == self.calculated_destination:
            self.reached = True
            print("reached destination:",self.source,"=",self.calculated_destination)if self.logs else 0
        else: 
            self.reached = False
    def movecar(self):
        self.calculate_angle_of_rotation()
        self.calculate_directions()
        self.rotate_car()
        self.check_obstacle()
        if self.obstacle:
            self.brake_car()
            print("obstacle:",self.obstacle)if self.logs else 0
            return
        self.move_car_to_point()
        
        
    def set_destination(self,point = None ):
        if point == None or point == self.rect.center or self.brakes:
            self.brake_car()
            return
        elif point == self.destination:
            self.calculate_rotation = False
            self.calculate_direction_and_distance = False
        print("##########################destination point = ", point,"##########################")if self.logs else 0
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