"""
Created on:  March 4, 2014
Created by:  Alex Neuenkirk
"""
import sys
import pathfindAstar as pathfinder
import pygame
from pygame.locals import *

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
# INITIALIZE POSITIONS AND GOALS
agent1start = [10,0]
agent1goal = [20,17]

agent2start = [0,0]
agent2goal = [20,17]

agent3start = [0,18]
agent3goal = [20,17]
goals = [agent1goal, agent2goal, agent3goal]

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

# PLAY THE GAME
while True:
	paths = [agent1path, agent2path, agent3path]
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

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

	clock.tick(6)
	pygame.display.flip()

pygame.quit()