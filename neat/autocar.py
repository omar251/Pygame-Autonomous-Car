import pygame
import math
import pygame
import sys

import neat
os = [700, 650]
screen_width =  600
screen_height = 600
generation = 0
class Car:
    def __init__(self):
        self.surface = pygame.image.load("car.png")
        self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.rotate_surface = self.surface
        self.pos = [200, 400]
        self.angle = 0
        self.speed = 0
        self.center = [self.pos[0] + 50, self.pos[1] + 50]
        self.center_old = [self.pos[0] + 50, self.pos[1] + 50]
        self.radars = []
        self.radars_for_draw = []
        self.is_alive = True
        self.goal = False
        self.distance = 0
        self.time_spent = 0
        self.direction = ""
        self.count_R = 0
        self.count_L = 0

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
        self.move(screen)

        disp = int(math.sqrt(math.pow(self.center_old[0] - self.center[0], 2) + math.pow(self.center_old[1] - self.center[1], 2)))
        
        if disp < 50 :
            disp = 0
            
        self.distance += disp
        self.time_spent += 1
        
        self.center_old = self.center
        
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

    def a_move(self,output):
        # self.Forword(5)
        # r,l,f,b,s = output[0],output[1],output[2],output[3],output[4]*10
        self.speed = output[4]*10
        i = output.index(max(output))

        if i == 0 : 
            self.Right(self.speed)
            self.direction = "R"
        elif i == 1 : 
            self.Left(self.speed)
            self.direction = "L"
        elif i == 2 : 
            self.Forword(self.speed)
            self.direction = "F"
        elif i == 3 : 
            self.Backword(self.speed)
            self.direction = "B"
    def corners(self,screen):
        self.center = [int(self.pos[0]) + 50, int(self.pos[1]) + 50]
        len = 70
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
        # print("R")
    def Left(self,speed = 1):
        self.angle += speed
        self.rotate_surface = self.rot_center(self.surface,self.angle)
        # print("L")
    def Forword(self,speed = 1):
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * speed
        # print("F")
    def Backword(self,speed = 1):
        self.pos[0] -= math.cos(math.radians(360 - self.angle)) * speed
        self.pos[1] -= math.sin(math.radians(360 - self.angle)) * speed
        # print("B")
generation = 0
def run_car(genomes, config):
    screen_width = 600
    screen_height = 600
    
    nets = []
    cars = []
    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 70)
    font = pygame.font.SysFont("Arial", 30)
    map = pygame.image.load('ring4.png')
    
    global generation
    generation += 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        
        screen.fill((0,0,0))
         # Input my data and get result from network
        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_data())
            car.a_move(output)
                
        # Update car and fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if car.get_alive():
                remain_cars += 1
                car.update(map,screen)
                genomes[i][1].fitness += car.get_reward()
        # check
        if remain_cars == 0:
            break
        # Drawing
        screen.blit(map, (0, 0))
        for car in cars:
            if car.get_alive():
                car.draw(screen)
                car.corners(screen)
        
        text = generation_font.render("Generation : " + str(generation), True, (255, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width/2, 100)
        screen.blit(text, text_rect)

        text = font.render("remain cars : " + str(remain_cars), True, (0, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width/2, 200)
        screen.blit(text, text_rect)   
        # for i in range(0,3,1):  
        #     print("genomes ",i," = ",genomes[i][1].fitness)  
           
        clock.tick(0)
        pygame.display.update()

if __name__ == "__main__":
    # Set configuration file
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(run_car, 1000)
