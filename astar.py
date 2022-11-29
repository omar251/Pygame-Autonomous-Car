import pygame
import math
from queue import PriorityQueue
# from Car import Car
from car_fallow_point import Car
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = BLACK
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == WHITE

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = BLACK

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = WHITE

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# path = []
def reconstruct_path(came_from, current, draw):
    # global path
    path = []
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path.append((current.x+15,current.y+15))
        draw()
  


def algorithm(draw, grid, start, end,path):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            # path = reconstruct_path(came_from, end, draw)
            
            while current in came_from:
                current = came_from[current]
                current.make_path()
                path.append((current.x+15,current.y+15))
                # draw()
            path.reverse()
            end.make_end()
            return True ,path
        

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        # draw()

        if current != start:
            current.make_closed()

    return False,path

def make_grid(rows, width):
    return [[Spot(i, j, width // rows, rows) for j in range(rows)] for i in range(rows)]

def draw_grid(win, rows, width):
    for y in range(rows):pygame.draw.line(win, RED, (0, y * width // rows), (width, y * width // rows))
    for x in range(rows):pygame.draw.line(win, RED, (x * width // rows, 0), (x * width // rows, width))


def draw(win, grid, rows, width,car,path):
    win.fill(BLACK)

    for row in grid:
        for spot in row:
            spot.draw(win)
    # draw_grid(win, rows, width)
    pygame.image.save(win,"map.png")
    car.update_map(pygame.image.load('map.png'))
    car.draw_path(path)
    car.draw_Car()
    car.draw_radar()
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	return pos[0] // gap, pos[1] // gap


def main(win, width):
    ROWS = 20
    grid = make_grid(ROWS, width)
    car = Car(win,pygame.image.load('map.png'))
    point = None
    start = None
    end = None
    # global path
    # path.reverse()
    path = []
    run = True
    while run:
        draw(win, grid, ROWS, width,car,path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                r,c =get_clicked_pos((int(car.source[0]),int(car.source[1])), ROWS, width)
                startspot = grid[r][c]
                start = startspot
                start.make_start()
                if not start and spot != end:
                    pass

                elif not end and spot != start:
                    path.clear()
                    end = spot
                    end.make_end()

                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE :
                #         spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            elif pygame.mouse.get_pressed()[1]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.make_barrier()

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE :
                #     make_barrier = True
                #     spot.make_barrier()
                if event.key == pygame.K_c :
                        path.clear()
                        point = None
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)
                        car.reached = True
                        
            if start and end:
                for row in grid:
                    for spot in row:
                        spot.update_neighbors(grid)

                _,path = algorithm(lambda: draw(win, grid, ROWS, width,car), grid, start, end ,path)
                end = None
                print(len(path))

                

        if car.reached:
            point = car.get_steps(0,path)
        
        car.prepare_car()
        car.set_destination(point)
        # print(path,point,car.reached,len(path))

    pygame.quit()

main(WIN, WIDTH)