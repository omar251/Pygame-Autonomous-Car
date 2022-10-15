from turtle import right
import pygame
import math

os = [700, 650]
screen_width =  600
screen_height = 600
generation = 0
class Car:
    def __init__(self):
        self.surface = pygame.image.load("car.png")
        self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.rotate_surface = self.surface
        self.pos = [250, 250]
        self.angle = 0
        self.speed = 0
        self.center = [self.pos[0] + 50, self.pos[1] + 50]
        self.radars = []
        self.radars_for_draw = []
        self.is_alive = True
        self.goal = False
        self.distance = 0
        self.time_spent = 0

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
        self.draw_radar(screen)

    def draw_radar(self, screen):
        for r in self.radars:
            pos = r[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, pos, 1)
            pygame.draw.circle(screen, (0, 255, 0), pos, 5)

    def check_collision(self, map):
        self.is_alive = True
        for p in self.four_points:
            if map.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
                self.is_alive = False
                break

    def check_radar(self, degree, map):
        len = 0
        x = int(self.center[0])
        y = int(self.center[1])
        
        while not map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
            len = len + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self, map,screen):
        #check speed
        self.speed = 1

        #check position
        # self.rotate_surface = self.rot_center(self.surface, self.angle)
        # self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        # if self.pos[0] < 20:
        #     self.pos[0] = 20
        # elif self.pos[0] > screen_width - 120:
        #     self.pos[0] = screen_width - 120

        # self.distance += self.speed
        # self.time_spent += 1
        # self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        # if self.pos[1] < 20:
        #     self.pos[1] = 20
        # elif self.pos[1] > screen_height - 120:
        #     self.pos[1] = screen_height - 120

        # # caculate 4 collision points
        # self.center = [int(self.pos[0]) + 50, int(self.pos[1]) + 50]
        # len = 40
        # left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        # right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        # left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        # right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        # self.four_points = [left_top, right_top, left_bottom, right_bottom]
        self.corners(screen)
        self.check_collision(map)
        self.radars.clear()

        for d in range(-90, 120, 45):
            self.check_radar(d, map)

    def get_data(self):
        radars = self.radars
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(radars):
            ret[i] = int(r[1] / 30)

        return ret

    def get_alive(self):
        return self.is_alive

    def get_reward(self):
        return self.distance / 50.0

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def move(self,screen):
         keys = pygame.key.get_pressed()
         border = False
         if self.pos[0] < 20 or self.pos[0] > screen_width - 120 or self.pos[1] > screen_height - 120 or self.pos[1] < 20:
             border = True
         if self.pos[0] < 20:
            self.pos[0] = 20
         elif self.pos[0] > screen_width - 120:
            self.pos[0] = screen_width - 120
            
         if self.pos[1] < 20:
            self.pos[1] = 20
         elif self.pos[1] > screen_height - 120:
            self.pos[1] = screen_height - 120
         
         if not border:
            self.reset_angle()
            if keys[pygame.K_RIGHT]:
                self.Right(10)
            if keys[pygame.K_LEFT]:
                self.Left(10)
            if keys[pygame.K_UP]:
                self.Forword(10)
            if keys[pygame.K_DOWN]:
                self.Backword(10)
    def auto_move(self):
        left = self.get_data()[0]+self.get_data()[1]
        right = self.get_data()[3]+self.get_data()[4]
        self.reset_angle()
        if right < left and right > 10 and left > 10:
            self.Right(2)
        if right > left and right > 10 and left > 10:
            self.Left(3)
        if self.get_data()[2] >= 3 :
            self.Forword(0)
        if self.get_data()[2] < 1 or (left == right):
            self.Backword(0)
    def corners(self,screen):
        self.center = [int(self.pos[0]) + 50, int(self.pos[1]) + 50]
        len = 40
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        self.four_points = [left_top, right_top, left_bottom, right_bottom]
        pygame.draw.circle(screen,(0,255,0),(left_top[0],left_top[1]),5)
        pygame.draw.circle(screen,(0,255,0),(right_top[0],right_top[1]),5)
        pygame.draw.circle(screen,(0,255,0),(left_bottom[0],left_bottom[1]),5)
        pygame.draw.circle(screen,(0,255,0),(right_bottom[0],right_bottom[1]),5)
        
    def reset_angle(self):
        if self.angle == 360 or self.angle == -360:
            self.angle =  0
    def Right(self,speed = 1):
        self.angle += -speed
        self.rotate_surface = self.rot_center(self.surface,self.angle)
    def Left(self,speed = 1):
        self.angle += speed
        self.rotate_surface = self.rot_center(self.surface,self.angle)
    def Forword(self,speed = 1):
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * speed
    def Backword(self,speed = 1):
        self.pos[0] -= math.cos(math.radians(360 - self.angle)) * speed
        self.pos[1] -= math.sin(math.radians(360 - self.angle)) * speed