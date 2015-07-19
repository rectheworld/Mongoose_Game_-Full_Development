"""
Created on:  March 4, 2014
Created by:  Alex Neuenkirk and Ren C'DeBaca
"""
import sys
import pathfindAstar as pathfinder
import pygame
from pygame.locals import *
import math
import Snake_Class
import Vector_Class
from baby_mongoose import Baby
import random



def draw_rect(color,location):
	'''
	Fills the cell at location [column,row] with the indicated color.
	'''
	pygame.draw.rect(screen, color, ((location[0]*tile_size),
									 (location[1]*tile_size + zoneHeight), tile_size-2*margin, tile_size-2*margin))
colors = {'white':(255,255,255),
	'black':(0,0,0),
	'red':(255,0,0),
	'yellow':(255,255,0),
	'orange':(255,127,39),
	'green':(0,255,0),
	'blue':(0,0,255),
	'pink':(255,128,192),
	'purple':(128,0,255),
	'light_blue':(0,128,255),
	'cyan':(0,255,255),
	'blood':(175,0,0),
	'gray':(25,25,25),
	'bufferZone':(70,35,0),
	'bufferFill':(21,11,0)}

DK_BROWN = (116, 71, 48)

# CREATE THE BOARD
board = pathfinder.Board(35,19)
board.generateObstacles()

# DISPLAY VARIABLES
board_width = board.width
board_height = board.height
tile_size = 35 # The size of each square cell in the grid 
margin = 0
zoneHeight = 50 # The height of the Blank Zone at the Top of the Game 
deltaTime = 0 # A variable used to keep time. Will be used to animate the sprites 

# PYGAME VARIABLES
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((board_width*tile_size, board_height*tile_size))
Snake_Class.snake.screen = screen # feeds the screen variable to the snake instance in Snake_Class
pygame.display.set_caption("MONGOOSE")
screen.fill(colors['bufferFill'])

# SPRITES
desert_sprite = pygame.image.load("desert1.png").convert_alpha()
cacti_sprites = pygame.image.load("cacti.png").convert_alpha()
Baby.load_sprites()

# SPRITE IMAGES
background = desert_sprite.subsurface(pygame.Rect((14,76),(50,56)))
rock = desert_sprite.subsurface(pygame.Rect((170,230),(25,25)))
cactus = cacti_sprites.subsurface(pygame.Rect((0,0),(38,50))).convert_alpha()


"""
The Following section creates the Baby Mongooses

First, it inilized the starting positions. The five babies can each appear in each 
one of 6 positions on the board.

Next, these positions are saved in a list for convienence.

Finally, instances of the class Baby is greated with the starting positions.
These objects are then put into
"""
# INITIALIZE POSITIONS AND GOALS
babyStart1 = Baby.spawnLocations.pop(random.randint(0,len(Baby.spawnLocations)-1))
babyStart2 = Baby.spawnLocations.pop(random.randint(0,len(Baby.spawnLocations)-1))
babyStart3 = Baby.spawnLocations.pop(random.randint(0,len(Baby.spawnLocations)-1))
babyStart4 = Baby.spawnLocations.pop(random.randint(0,len(Baby.spawnLocations)-1))
babyStart5 = Baby.spawnLocations.pop(random.randint(0,len(Baby.spawnLocations)-1))

# Save these positions in a list
babyStarts = [babyStart1 , babyStart2, babyStart3, babyStart4, babyStart5]
# Add these positions to class Baby's list of currentLocations
for i in range(len(babyStarts)):
    Baby.currentLocations.append(babyStarts[i])

# CREATE AGENT OBJECTS AND GET A PATH TO EACH OF THEIR GOALS
baby1 = Baby(babyStart1)
baby2 = Baby(babyStart2)
baby3 = Baby(babyStart3)
baby4 = Baby(babyStart4)
baby5 = Baby(babyStart5)

# Put the baby agents into a list
babies = [baby1, baby2, baby3, baby4, baby5]

# GET OBSTACLE LOCATION INFORMATION FROM THE BOARD
rocks = board.rocks
cacti = board.cacti
	# All obstacle locations
obstacles = board.obstacles


def update(point, goal):
	"""
	This functon takes in two parameters, each of which is a two tuple 
	list representing a point on the screen.

	The function returns the direction the point needs to move in in 
	order to be closer to the gaol. 

	The direction is returned as a point_x_speed, and a point_y_speed
	""" 
	point_x_speed = 0
	point_y_speed = 0
	if (point[0] < goal[0]) and (point[1] < goal[1]):
		point_x_speed += tile_size
		point_y_speed += tile_size
	elif (point[0] < goal[0]) and (point[1] > goal[1]):
		point_x_speed += tile_size
		point_y_speed -= tile_size
	elif (point[0] > goal[0]) and (point[1] > goal[1]):
		point_x_speed -= tile_size
		point_y_speed -= tile_size
	elif point[0] > goal[0] and point[1] < goal[1]:
		point_x_speed -= tile_size
		point_y_speed += tile_size
	elif point[0] < goal[0]:
		point_x_speed += tile_size
	elif point[0] > goal[0]:
		point_x_speed -= tile_size
	elif point[1] < goal[1]:
		point_y_speed += tile_size
	elif point[1] > goal[1]:
		point_y_speed -= tile_size

	return [point_x_speed, point_y_speed]
def distance(point1,point2):
	"""
	Returns the distance between two points.

	"""
	distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return distance 

def line_of_sight(point1, point2): # made sure this imput is in grid terms
	bad = 0
	listbad = []
	if point1[0] <= point2[0]:
		i = point1[0]
		while i <= point2[0]:
			test_point = [i, point1[1]]
			listbad.append(test_point)
			if test_point in obstacles:
				bad +=1
			i +=1
	elif point1[0] >= point2[0]:
		i = point2[0]
		while i <= point1[0]:
			test_point = [i, point2[1]]
			listbad.append(test_point)
			if test_point in obstacles:
				bad +=1
			i +=1
	if point1[1] <= point2[1]:
		i = point1[1]
		while i <= point2[1]:
			test_point = [point1[0], i]
			listbad.append(test_point)
			if test_point in obstacles:
				bad +=1
			i +=1
	if point1[1] >= point2[1]:
		i = point2[1]
		while i <= point1[1]:
			test_point = [point2[0], i]
			listbad.append(test_point)
			if test_point in obstacles:
				bad +=1
			i +=1
	for item in listbad:
		print item

	if bad > 0:
		return True 

for item in obstacles:
	print item
print "__________________________"
"""
The section below creates the first goal for the snake.

Fisrst, the list of babies is searched for the baby that is closest to the snake.
next, a path is found to that baby
"""

for item in babyStarts:
	Snake_Class.snake.goal_list.append(item)

goal_grid =  Snake_Class.snake.getDistance(babyStarts)
Snake_Class.snake.getGoalGrid(goal_grid) 

snake_agent = pathfinder.newAgent([Snake_Class.snake.A[0]/ tile_size, (Snake_Class.snake.A[1] + 50)/ tile_size], goal_grid)
snake_path = snake_agent.getPath(board)

Csnake_agent = pathfinder.newAgent([Snake_Class.snake.C[0]/ tile_size, (Snake_Class.snake.C[1] + 50)/ tile_size], goal_grid)
Csnake_path = snake_agent.getPath(board)
Cindex = 1 


"""
Cmove = False 
Cindex = 1
C_snake_path = []
"""

index = 1 # Used to access item in the snake_path list 


# PLAY THE GAME
while True:
	paths = [snake_path] #[agent1path, agent2path, agent3path]
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	'''
		elif event.type == pygame.KEYDOWN:
		#determine if the keydown is an arrow key. if yes, adjust speed 
			if event.key == pygame.K_LEFT:
				point_x_speed =- 25
			elif event.key == pygame.K_RIGHT:
				point_x_speed = 25
			elif event.key == pygame.K_UP:
				point_y_speed =- 25
			elif event.key == pygame.K_DOWN: 
				point_y_speed = 25
			# User let up on a key 
		elif event.type == pygame.KEYUP:
			# if it is an arrow key, reset vector back to zero
			if event.key == pygame.K_LEFT:
				point_x_speed = 0
			elif event.key == pygame.K_RIGHT:
				point_x_speed = 0
			elif event.key == pygame.K_UP:
				point_y_speed = 0
			elif event.key == pygame.K_DOWN:
				point_y_speed = 0
	'''
	
	#point = goal
	"""
	if len(snake.goal_list) > 0:
		goal = [point[0] + point_x_speed, point[1] + point_y_speed]
		snake.goal = goal 
		goal_grid = [(goal[0] / 25), (goal[1] / 25)]
	#print len(snake.goal_list)
	"""
	
	# Draw the desert background
	for i in range(board_width):
		xStart = i*50
		for j in range(board_height):
			yStart = zoneHeight + j*56
			screen.blit(background,(xStart,yStart))

	# Draw the rock obstacles
	for r in rocks:
		screen.blit(rock, (r[0] * tile_size, zoneHeight + r[1] * tile_size))

	# Draw the cacti
	for cact in cacti:
		# -3 and -15 below are for improved graphics based on the tile size and the size of the cactus image
		screen.blit(cactus,(cact[0] * tile_size - 3, zoneHeight + cact[1] * tile_size - 15))

	# Draw the babies
	for baby in babies:
		screen.blit(baby.updateRendering(deltaTime), (baby.x * tile_size, zoneHeight + baby.y * tile_size))

	# Draw the buffer zone at the top of the board
	pygame.draw.rect(screen, colors['bufferZone'], (0, 0, board.width * tile_size , zoneHeight),10)
	pygame.draw.rect(screen, colors['bufferFill'], (10,10,board.width * tile_size - 20, zoneHeight-10))
	
	

	"""
	The if Statment below will mensure the distance between A and the goal and set the X-speed and 
	Y- speed acordanly. 

	Next it will take the next item in the snake's A-Star path and multiply each element by 25 to 
	convert the element to a pixal on the screen. 

	finally the index in incremented 
	"""
	if distance(Snake_Class.snake.A, Snake_Class.snake.goal) >= 70: 
		if index <= len(snake_path):
			Snake_Class.snake.point_x_speed = update(Snake_Class.snake.A, Snake_Class.snake.goal)[0]
			Snake_Class.snake.point_y_speed = update(Snake_Class.snake.A, Snake_Class.snake.goal)[1]
			Snake_Class.snake.A = [snake_path[index - 1][0] * tile_size, (snake_path[index - 1][1] * tile_size) + 50]	
			index +=1
		if Cindex <= len(Csnake_path):
			Snake_Class.snake.C = [Csnake_path[index - 1][0] * tile_size, (Csnake_path[index - 1][1] * tile_size) + 50]	
			Cindex +=1
		"""
		if Cindex <= len(C_snake_path): 
			if index <= len(C_snake_path):
				Snake_Class.snake.C = [C_snake_path[index - 1][0] * tile_size, (C_snake_path[index - 1][1] * tile_size) + 50]	
				Cindex +=1
			else:
				Cmove = False
				Cindex = 1
				snake_path = []
		"""


	#transition triggers
	if distance(Snake_Class.snake.A, ((Snake_Class.snake.goal[0]), (Snake_Class.snake.goal[1]))) < 150:
		"""
		if the snake is not already in Offense State, switch to an offensive State
		"""
		if Snake_Class.snake.FSM.cur_state_name != "Offense": 
			Snake_Class.snake.FSM.Transition("To_Offense")
			Snake_Class.snake.FSM.Traveling = False 
			Snake_Class.snake.FSM.Attack = False
			print "Nag is Offensive"
			
		
		if Snake_Class.snake.FSM.cur_state_name == "Offense":
			if Snake_Class.timer.delta_time_Attack(10000) == True:
				Snake_Class.snake.FSM.Transition("To_Attack")
				Snake_Class.snake.FSM.Traveling = False
				Snake_Class.snake.FSM.Attack = False 
				print "Nag is Attacking!!!!"
				if Snake_Class.snake.collision() == True: 
					Snake_Class.snake.FSM.Transition("To_Traveling")
					Snake_Class.snake.FSM.Offense = False 
					Snake_Class.snake.FSM.Attack = False
					
					babyStarts.remove(goal_grid)

					goal_grid =  Snake_Class.snake.getDistance(babyStarts)
					Snake_Class.snake.getGoalGrid(goal_grid)

					snake_agent = pathfinder.newAgent([Snake_Class.snake.A[0]/ tile_size, Snake_Class.snake.A[1]/ tile_size], goal_grid)
					snake_path = snake_agent.getPath(board)
					index = 1 

					Csnake_agent = pathfinder.newAgent([Snake_Class.snake.C[0]/ tile_size, Snake_Class.snake.C[1]/ tile_size], goal_grid)
					Csnake_path = Csnake_agent.getPath(board)
					Cindex = 1 


		Snake_Class.snake.FSM.Execute()
	
	else: 
		if Snake_Class.snake.FSM.cur_state_name != "Traveling":
			Snake_Class.snake.FSM.Transition("To_Traveling")
			Snake_Class.snake.FSM.Offense = False 
			Snake_Class.snake.FSM.Attack = False
			index = 1
			print "Nag is Traveling"

		"""
		if len(C_snake_path) == 0:
			if line_of_sight((Snake_Class.snake.A[0] / tile_size, (Snake_Class.snake.A[1] / tile_size)), (Snake_Class.snake.C[0] / tile_size, (Snake_Class.snake.C[1] / tile_size))) == True:
				Cmove = True 
				Atemp = (Snake_Class.snake.A[0] / tile_size, (Snake_Class.snake.A[1] / tile_size))
				C_snake_agent = pathfinder.newAgent([Snake_Class.snake.C[0]/ tile_size, Snake_Class.snake.C[1]/ tile_size], goal_grid)
				C_snake_path = C_snake_agent.getPath(board)
		"""
		Snake_Class.snake.FSM.Execute()
	
	
	Snake_Class.snake.head_circle = pygame.Rect(Snake_Class.snake.A[0]-40, Snake_Class.snake.A[1]-40, 40*2, 40*2)
	
	#pygame.draw.rect(screen, (255, 255, 255), Snake_Class.snake.head_circle)
	"""
	for item in C_snake_path:
		pygame.draw.rect(screen, (255, 255, 255), (item[0] * 35, (item[1] * 35) + 50, 35, 35))
	"""
	
		
	deltaTime += 1

	clock.tick(6)
	pygame.display.flip()

pygame.quit()
sys.exit()