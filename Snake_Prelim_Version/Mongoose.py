"""
Created on:  March 4, 2014
Created by:  Alex Neuenkirk
"""
import sys
import pathfindAstar as pathfinder
import pygame
from pygame.locals import *
import math 
import Snake_Class
import Vector_Class 

def draw_rect(color,location):
	'''
	Fills the cell at location [column,row] with the indicated color.
	'''
	pygame.draw.rect(screen, color, (margin+(location[0]*tile_size),
									 margin+(location[1]*tile_size), tile_size-2*margin, tile_size-2*margin))
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
	'gray':(25,25,25)}

DK_BROWN = (116, 71, 48)
# INITIALIZE POSITIONS AND GOALS
agent1start = [10,0]
agent1goal = [20,17]

agent2start = [0,0]
agent2goal = [20,17]

agent3start = [0,18]
agent3goal = [20,17]
goals = [agent1goal, agent2goal, agent3goal]

goal = [1000, 200]

A = [350, 350] # Start Point
B = [370, 370] # Control point
C = [390, 390] # Endpoint
D = [410, 410] # Control point 
E = [430, 430]
F = [450, 450] # Control Point 
G = [470, 470]


# CREATE THE BOARD
board = pathfinder.Board(64,33) #you can input width and height, but it will default to 32 columns by 24 rows if omitted
board.generateObstacles(goals)

# CREATE OBSTACLES
rocks = board.getRocks()
cacti = board.getCacti()
obstacles = board.getObstacles()

# CREATE AGENT OBJECTS AND GET A PATH TO EACH OF THEIR GOALS

agent1 = pathfinder.newAgent(agent1start,agent1goal)
agent1path = agent1.getPath(board)
agent2 = pathfinder.newAgent(agent2start,agent2goal)
agent2path = agent2.getPath(board)
agent3 = pathfinder.newAgent(agent3start,agent3goal)
agent3path = agent3.getPath(board)

# DISPLAY VARIABLES
board_width = board.getWidth()
board_height = board.getHeight()
tile_size = 25
margin = 0.5
default_color = colors['light_blue']
agent1_color = colors['green']
agent2_color = colors['yellow']
agent3_color = colors['purple']
goal_color = colors['pink']
obstacle_color = colors['gray']

# PYGAME VARIABLES
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((board_width*tile_size, board_height*tile_size))
pygame.display.set_caption("MONGOOSE")
screen.fill(colors['black'])
# SPRITES
desert_sprite = pygame.image.load("desert1.png").convert_alpha()
# SPRITE IMAGES
background = desert_sprite.subsurface(pygame.Rect((14,76),(50,56)))
rock = desert_sprite.subsurface(pygame.Rect((170,230),(25,25)))
cactus = desert_sprite.subsurface(pygame.Rect((5,6),(25,26))).convert_alpha()

"""
def update(point, goal):
	if (point[0] < goal[0]) and (point[1] < goal[1]):
		point[0] += 15
		point[1] += 15
	elif (point[0] < goal[0]) and (point[1] > goal[1]):
		point[0] += 15
		point[1] -= 15
	elif (point[0] > goal[0]) and (point[1] > goal[1]):
		point[0] -= 15
		point[1] -= 15
	elif point[0] > goal[0] and point[1] < goal[1]:
		point[0]-= 15
		point[1] += 15
	elif point[0] < goal[0]:
		point[0] += 15
	elif point[0] > goal[0]:
		point[0] -= 15 
	elif point[1] < goal[1]:
		point[1] += 15
	elif point[1] > goal[1]:
		point[1] -= 15

	return [point[0], point[1]]

"""
def update(point, goal):
	point_x_speed = 0
	point_y_speed = 0
	if (point[0] < goal[0]) and (point[1] < goal[1]):
		point_x_speed += 15
		point_y_speed += 15
	elif (point[0] < goal[0]) and (point[1] > goal[1]):
		point_x_speed += 15
		point_y_speed -= 15
	elif (point[0] > goal[0]) and (point[1] > goal[1]):
		point_x_speed -= 15
		point_y_speed -= 15
	elif point[0] > goal[0] and point[1] < goal[1]:
		point_x_speed -= 15
		point_y_speed += 15
	elif point[0] < goal[0]:
		point_x_speed += 15
	elif point[0] > goal[0]:
		point_x_speed -= 15 
	elif point[1] < goal[1]:
		point_y_speed += 15
	elif point[1] > goal[1]:
		point_y_speed -= 15

	return [point_x_speed, point_y_speed]


def distance(point1,point2):
	"""
	Returns the distance between two points.

	"""
	distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return distance 

# SPRITE CLASSES - NOT YET USED
class Background(pygame.sprite.Sprite):
	"""
	Subclass of pygame's Sprite class for rending the background of the Mongoose game.
	"""
	def __init__(self):
		# call the parent class constructor
		# super().__init__()

		# Load the spritesheet
		self.image = pygame.image.load("desert1.png").convert()
		# Set our transparent color
		self.image.set_colorkey(colors['white'])
		# Fetch the rectangle object that has the dimensions of the image
		self.rect = self.image.get_rect()

snake = Snake_Class.Snake(A, B, C, D, E, F, G)
snake.screen = screen
snake.goal = goal
snake.FSM.SetState("Traveling")

point_x_speed = 0
point_y_speed = 0 
# PLAY THE GAME
while True:
	paths = [agent1path, agent2path, agent3path]
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
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
	
	point = goal
	

	

	goal = [point[0] + point_x_speed, point[1] + point_y_speed]

	# Draw the desert background
	for i in range(board_width/2):
		xStart = i*50
		for j in range(board_height/2):
			yStart = j*56
			screen.blit(background,(xStart,yStart))

	# Draw the rock obstacles
	for r in rocks:
		screen.blit(rock,(r[0]*25,r[1]*25))

	for cact in cacti:
		screen.blit(cactus,(cact[0]*25,cact[1]*25))

	# draw a rectangle to represent each tile's attributes (goal, agent, obstacle, empty)
	for column in range(board_width):
		for row in range(board_height):
			if [column,row] == agent1path[0]:
				color = agent1_color
			elif [column,row] == agent2path[0]:
				color = agent2_color
			elif [column,row] == agent3path[0]:
				color = agent3_color
			elif [column,row] in goals:
				color = goal_color
			# elif [column,row] in board.getObstacles():
			# 	screen.blit(obstacle,(column*25,row*25))
			else:
				continue
			draw_rect(color, [column,row])

	for index in range(len(paths)):
		paths[index].pop(0)
		if len(paths[index]) == 0:
			if index == 0:
				agent1path = agent1.getPath(board)
			elif index == 1:
				agent2path = agent2.getPath(board)
			else:
				agent3path = agent3.getPath(board)

	if distance(snake.A, goal) >= 100:
		snake.point_x_speed = update(snake.A, goal)[0]
		snake.point_y_speed = update(snake.A, goal)[1]
		snake.A = [snake.A[0] + snake.point_x_speed, snake.A[1] + snake.point_y_speed]

	


	pygame.draw.rect(screen, DK_BROWN,(goal[0], goal[1], 15, 15), 0)

	#transition triggers
	if distance(snake.A, goal) < 100:
		if snake.FSM.cur_state_name != "Offense": 
			snake.FSM.Transition("To_Offense")
			snake.FSM.Traveling = False 
			print "Nag is Offensive"
		snake.FSM.Execute()


	else: 
		if snake.FSM.cur_state_name != "Traveling":
			snake.FSM.Transition("To_Traveling")
			snake.FSM.Offense = False 
			snake.FSM.Defensive = False

			print "Nag is Traveling"
		snake.FSM.Execute()
	


	clock.tick(6)
	pygame.display.flip()

pygame.quit()