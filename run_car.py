import pygame
import sys
from Car import Car
import math

screen_width = 600
screen_height = 600

# Init my game
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
generation_font = pygame.font.SysFont("Arial", 70)
font = pygame.font.SysFont("Arial", 30)
map = pygame.image.load('ring3.png')
car = Car()

color = (255,255,255,255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    screen.fill((0,0,0))
    screen.blit(map, (0, 0))
    car.draw(screen)
    car.update(map,screen)
    car.move(screen)
    car.auto_move()
    clock.tick(0)
    pygame.display.update()

