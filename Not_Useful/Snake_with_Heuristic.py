import math
import copy
import pygame
import sys
import random

"""


"""
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255 ,0 ,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
LIGHT_BLUE = (0, 128, 255)
BROWN = (185, 122, 87)
DK_BROWN = (116, 71, 48)
GLD_YELLOW = (255, 201, 14)


A = [5, 5] # Start Point
B = [5, 10] # Control point
C = [10, 10] # Endpoint
D = [15, 10] # Control point 
E = [15, 15]
F = [15, 20] # Control Point 
G = [20, 20]

grid_width = 30
grid_height = 30
cell_size = 20
margin = 0
obstacles = []



A_pixals = [A[0] * cell_size, A[1] * cell_size]
B_pixals = [B[0] * cell_size, B[1] * cell_size]
C_pixals = [C[0] * cell_size, C[1] * cell_size]
D_pixals = [D[0] * cell_size, D[1] * cell_size]
E_pixals = [E[0] * cell_size, E[1] * cell_size]
F_pixals = [F[0] * cell_size, F[1] * cell_size]
G_pixals = [G[0] * cell_size, G[1] * cell_size]




current_pt = [0,0]

colors = {'white':(255,255,255),
	'black':(0,0,0),
	'red':(255,0,0),
	'yellow':(255,255,0),
	'orange':(255,128,192),
	'green':(0,255,0),
	'blue':(0,0,255),
	'pink':(255,128,192),
	'purple':(128,0,255),
	'light_blue':(0,128,255),
	'cyan':(0,255,255),
	'blood':(175,0,0),
	'gray':(25,25,25),}



#
point_x_speed = 0
point_y_speed = 0

'''[[6,5],[7,5],[8,5],[6,6],[6,7],
			 [6,8],[6,9],[6,10],[6,11],
			 [20,25],[20,26],[20,27],[19,27],[19,28],[19,29],
			 [18,1],[18,2],[18,3],[19,3],[20,3]]'''

class Snake_Body(pygame.sprite.Sprite):
	def __init__(self, Start_Point_A, Contral_Point_B, End_Point_C):
		'''
		 These control points are given in terms of the grid system
		'''
		self.Start_Point_A = Start_Point_A 
		self.Contral_Point_B = Contral_Point_B 
		self.End_Point_C = End_Point_C 	


#MATHS
	def bezier(self, A, B, C, t):
	    """A B and C being 2-tuples, t being a float between 0 and 1"""
	    x = int((1 - t)**2 * A[0] + 2 * t * (1 - t) * B[0] + t**2 * C[0])
	    y = int((1 - t)**2 * A[1] + 2 * t * (1 - t) * B[1] + t**2 * C[1])
	    current_pt = (x,y)
	    return current_pt

	def cubicBezier(self, A, B, C, D, t):
	    x = int((1-t)**3 * A[0] + 3*t*(1-t)**2 * B[0] + 3*t**2*(1-t) * C[0] + t**3*D[0])
	    y = int((1-t)**3 * A[1] + 3*t*(1-t)**2 * B[1] + 3*t**2*(1-t) * C[1] + t**3*D[1])
	    current_pt = (x,y)
	    return current_pt


	def update(self, A, B, C):
		ptlist = []
		steps = 0
		t = 0 
		while steps <= 9:
			t += .1
			current_pt = self.bezier(A,B,C,t)
			ptlist.append(current_pt)
			steps += 1 
		return ptlist

def getAngle(x1,y1, x2, y2):
    # Return value is 0 for right, 90 for up, 180 for left, and 270 for down (and all values between 0 and 360)
    rise = y1 - y2
    run = x1 - x2
    angle = math.atan2(run, rise) # get the angle in radians
    angle = angle * (180 / math.pi) # convert to degrees
    angle = (angle + 90) % 360 # adjust for a right-facing sprite
    return angle
def rotate(headx, heady, degrees):
	rotate_surface = pygame.transform.rotate(head_surface, degrees)
	rotate_rect = rotate_surface.get_rect()
	rotate_rect.center = (headx, heady)
	screen.blit(rotate_surface, rotate_rect)

def neck_roation(headx,heady,degrees):
	if (headx <= A_pixals[0] and heady >= A_pixals[1]): # I quadrent 
		if degrees >= 0 and degrees <= 90:  
			rotate(headx, heady, degrees)
		elif degrees >= 90 and degrees <= 225:
			degrees = 90
		elif degrees >= 225:
			degrees = 0
		rotate(headx, heady, degrees)
	elif (headx >= A_pixals[0] and heady <= A_pixals[1]): # III quadrant 
		if (degrees >= 180 and degrees <= 270):
			rotate(headx, headx, degrees)
		elif degrees >= 45 and degrees <= 180:
			degrees = 180
		elif degrees <= 45 or degrees >= 270:
			degrees = 270
		rotate(headx, heady, degrees)
	elif (headx <= A_pixals[0] and heady <= A_pixals[1]): # IV Quadrant 
		if degrees >= 270:
			rotate(headx, heady, degrees)
		elif degrees >= 135 and degrees <= 270:
			degrees = 270
		elif degrees >= 0 and degrees <= 135:
			degrees = 0 
		rotate(headx, heady, degrees) # II Quadrant 
	elif (headx >= A_pixals[0] and heady >= A_pixals[1]):
		if degrees >= 90 and degrees <= 180:
			rotate(headx, heady, degrees)
		elif degrees >= 180 and degrees <= 360:
			degrees = 180
		elif degrees <= 90 or degrees >= 375:
			degrees = 90
		rotate(headx, heady, degrees)
# Draw Head
headx = 0
heady = 0
# Rotaable Surface for the Snakes head 
head_surface = pygame.Surface((100, 30))
head_surface.fill(WHITE)
pygame.draw.ellipse(head_surface, BROWN, (headx + 35, heady, 60, 30))
# Eyes 
pygame.draw.ellipse(head_surface, GLD_YELLOW, (62, 18, 15, 10))
pygame.draw.ellipse(head_surface, GLD_YELLOW, (62,1, 15, 10))
pygame.draw.ellipse(head_surface, BLACK, (67, 20, 7, 9))
pygame.draw.ellipse(head_surface, BLACK, (67, 3, 7, 9))
# Nostirl 
pygame.draw.ellipse(head_surface, BLACK, (83, 18, 7, 2))
pygame.draw.ellipse(head_surface, BLACK, (83, 10, 7, 2))

Snake_Body_One = Snake_Body(A_pixals,B_pixals,C_pixals)
Snake_Body_Two = Snake_Body(C_pixals,D_pixals,E_pixals)
Snake_butt = Snake_Body(E_pixals,F_pixals,G_pixals)


# format of the open list is 
# openlist: 

class A_Star(object):
	def __init__(self, grid_height, grid_width, starting_position, goal_pos):
		self.grid_height = grid_height
		self.grid_width = grid_height
		self.starting_position = starting_position
		self.goal_pos = goal_pos

		self.open_list = []
		self.closed_list = []
		#path = []

		self.grid = self.heuristic_est(goal_pos,self.create_grid())
		self.open_list.append([starting_position, self.get_heur_cost(starting_position)])

	def create_grid(self):
		'''
		Creates a 2-dimensional grid of cells.  Output is of the form [[column,row],[column,row]...]
		'''
		grid = []
		for i in range(grid_width):
			for j in range(grid_height):
				grid.append([i,j])
		return grid

	def heuristic_est(self, goal_pos, grid):
		"""
		Inputs:
			goal_pos: a list in the format of [column#, row#] that holds the cell coordinates for a goal cell.
			grid: a list of lists in the format [[x,y][x,y]...] with the address for each cell in a 2 dimensional grid system.
		Output:
			returns the grid with an estimated heuristic cost as the third element, i.e. [[x,y,cost][x,y,cost]...]
		"""
		new_grid =[]
		for x in range(grid_width):
			for y in range(grid_height):
				cost = math.sqrt(abs((goal_pos[0]-x)**2 + (goal_pos[1]-y)**2))
				new_grid.append( [[x,y],round(cost,3)])
		return new_grid


	def get_heur_cost(self, position):
		'''
		Returns the estimated heuristic cost of a desired cell (position) by searching through a list of lists (grid)
		'''
		for element in self.grid:
			if element[0] == position:
				return element[1]

	def find_available_cells(self, position):
		'''
		Returns True for any adjacent cell that is available to move to from the current position.  Allows for the immediate first the left, right,
		up, and down directions.  Does not allow for diagonals.  Returns False if the adjacent space is not on the grid (an edge).
		'''
		LEFT = False 
		RIGHT = False
		UP = False
		DOWN = False
		left = position[0] - 1
		right = position[0] + 1
		up = position[1] - 1
		down = position[1] + 1

		if left >= 0 and not [left,position[1]] in obstacles:
			LEFT = True
		if right < grid_width and not [right,position[1]] in obstacles:
			RIGHT = True
		if position[1] - 1 >= 0 and not [position[0],up] in obstacles:
			UP = True
		if position[1] + 1 < grid_height and not [position[0],down] in obstacles:
			DOWN = True
		return LEFT, RIGHT, UP, DOWN

	def add_successors(self, next_position_value):
		'''
		Checks each cell available to move to and compares their estimated heuristic cost.  Returns a list of
		the position, (i.e. [column, row]) with the lowest cost.
		'''
		position = next_position_value[-2]
		LEFT, RIGHT, UP, DOWN = self.find_available_cells(position)
		available = []

		if LEFT:
			left_pos = [position[0]-1,position[1]]
			available.append(left_pos)
		if RIGHT:
			right_pos = [position[0]+1,position[1]]
			available.append(right_pos)
		if UP:
			up_pos = [position[0],position[1]-1]
			available.append(up_pos)
		if DOWN:
			down_pos = [position[0],position[1]+1]
			available.append(down_pos)

		for pos in available:
			successor = copy.copy(next_position_value)
			cost = self.get_heur_cost(pos)
			successor.insert(-1,pos)
			successor[-1] += cost
			self.open_list.append(successor)

	def choose_next_to_close(self):
		'''
		Returns the index value for the successor with the lowest cost in the open list.  In the event that more than one cell
		holds the lowest cost, it will return the smaller of the index values.
		'''
		lowest_index = 0
		if len(self.open_list) == 0:
			print "Error: The open list is empty"
		else:
			for i in range(1,len(self.open_list)):
			    if self.open_list[i][-1] < self.open_list[lowest_index][-1]:
			        lowest_index = i
			return lowest_index

	def update_closed(self, next_position_value):
		'''
		Moves the next cell to check into the appropriate list within the closed lists.
		'''
		if len(self.closed_list) == 0:
			self.closed_list.append(next_position_value)
			return
		else:
			final_position = next_position_value[-2]
			final_cost = next_position_value[-1]
			for i in range(len(self.closed_list)):
				if self.closed_list[i][-2] == final_position:
					if final_cost < self.closed_list[i][-1]:
						self.closed_list.pop(i)
						self.closed_list.append(next_position_value)
					return
		self.closed_list.append(next_position_value)

	def update_open(self, next_position_index):
		'''
		Removes the current path in consideration from the open list and also removes any paths from the open list whose last position has 
		already been accessed via a less expensive path.
		'''
		pop_list = []
		self.open_list.pop(next_position_index)
		for i in range(len(self.open_list)):
			for j in range(len(self.closed_list)):
				if self.open_list[i][-2] == self.closed_list[j][-2]:
					if self.open_list[i][-1] > self.closed_list[j][-1]:
						if not i in pop_list:
							pop_list.append(i)
		if len(pop_list) != 0:
			pop_list.reverse()
			for index in pop_list:
				self.open_list.pop(index)

	def update_lists(self):
		'''
		Chooses the next successor in the open list, moves it to the closed list, and adds its successors to the open list.
		'''
		next_position_index = self.choose_next_to_close() #saves the index location of the list in the open_list that we are using as the current position
		next_position_value = self.open_list[next_position_index] #saves the value of the list from the open_list to manipulate later on
		next_position = next_position_value[-2] # the actual [x,y] coordinates of the next position

		self.add_successors(next_position_value) # adds the successors of the cheapest path in the open list to the open list
		self.update_closed(next_position_value) # adds the cheapest path to the closed list
		self.update_open(next_position_index) # see function notes for details

	def check_for_goal(self):
		'''
		Searches the closed list for the goal position.
		'''
		for item in self.closed_list:
			if item[-2] == self.goal_pos:
				return True
		return False

	def find_path(self):
		'''
		Searches until the closed list contains the goal position, returns the first path that contains the goal 
		position with the last element (cost) removed.
		'''
		goal = False

		while goal == False:
			SEARCH.update_lists()
			goal = self.check_for_goal()

		for i in range(len(self.closed_list)):
			if self.closed_list[i][-2] == goal_pos:
				return self.closed_list[i][:-1]

def draw_rect(color,location):
	'''
	Draws a rectangle of the selected color in the specified cell location.

	input
		color:  the border and fill color of the desired rectangle in (R,G,B) format, i.e. (255,255,255) for white
		location:  a list in the format of [column#, row#] containing the cell location of the desired square, i.e. , [0,0] for the upperleftmost cell.

	outputs
		None
	'''
	pygame.draw.rect(screen, color, (margin+(location[0]*cell_size), margin+(location[1]*cell_size), cell_size-2*margin, cell_size-2*margin))		

def random_position():
	while True:
		column = random.randint(0,grid_width-1)
		row = random.randint(0,grid_height-1)
		if not [column,row] in obstacles:
			return [column,row]

# Global Variables
goal_pos = random_position()
# goal_pos = [7,7]
# starting_position = [0,0]
starting_position = random_position()




SEARCH = A_Star(grid_height,grid_width, starting_position, goal_pos)

""" 
Pygame Housekeeping
"""
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((grid_width*cell_size, grid_height*cell_size))
pygame.display.set_caption("MONGOOSE")

path = []

DONE = False
while DONE == False:
	'''
	The game loop.
	'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			DONE = True
		elif event.type == pygame.KEYDOWN:
			#determine if the keydown is an arrow key. if yes, adjust speed 
			if event.key == pygame.K_LEFT:
				point_x_speed =- 1
			elif event.key == pygame.K_RIGHT:
				point_x_speed = 1
			elif event.key == pygame.K_UP:
				point_y_speed =- 1
			elif event.key == pygame.K_DOWN: 
				point_y_speed = 1
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

	point = A
	A = [point[0] + point_x_speed, point[1] + point_y_speed]
	A_pixals = [A[0] * cell_size, A[1] * cell_size]

	screen.fill(WHITE)
		#draws the default rectangles on the pygame screen
	default_color = colors['light_blue'] #this is the default rectangle color
	
	"""
	for column in range(grid_width):
		for row in range(grid_height):
			if [column,row] in obstacles:
				color = colors['gray']
			else:
				color = default_color
			draw_rect(color, [column,row])
	"""
	current_color = colors['yellow'] #this is the color of the current cell rectangle
	goal_color = colors['pink'] #this is the color of the goal cell rectangle
	
	
	if len(path) == 0: #checks to see if there is no path
		path = SEARCH.find_path()

	"""This draws the demostration blocks"""
	'''
	draw_rect(current_color, [path[0][0],path[0][1]]) #draws the current location of the agent based on the path built above
	draw_rect(goal_color, [goal_pos[0],goal_pos[1]]) #draws the location of the goal rectangle
	'''

	path.pop(0)

	"""This draws the snake"""

	mx, my = pygame.mouse.get_pos()
	
	ptlist = Snake_Body_One.update(A_pixals,B_pixals,C_pixals)
	ptlist_mid = Snake_Body_Two.update(C_pixals,D_pixals,E_pixals)
	ptlist_mid[0] = ptlist[-1]

	ptlist_butt = Snake_butt.update(E_pixals,F_pixals,G_pixals)
	ptlist_butt[0] = ptlist_mid[-1]


	headx, heady = ptlist[0][0], ptlist[0][1]

	degrees = getAngle(headx, heady, mx, my)

	neck_roation(headx, heady, degrees)
	
	# Snake Body and Detail


	
	pygame.draw.lines(screen, BROWN, False, ptlist, 15)
	pygame.draw.lines(screen, DK_BROWN, False, ptlist, 5)

	pygame.draw.lines(screen, BROWN, False, ptlist_mid, 13)
	pygame.draw.lines(screen, DK_BROWN, False, ptlist_mid, 4)

	pygame.draw.lines(screen, BROWN, False, ptlist_butt, 11)
	pygame.draw.lines(screen, DK_BROWN, False, ptlist_butt, 3)
	
	
	#Endpoints are GREEN 

	pygame.draw.circle(screen, GREEN, ptlist[0], 8, 0)
	pygame.draw.circle(screen, GREEN, (A_pixals[0], A_pixals[1]), 4, 0)
	
	pygame.draw.circle(screen, GREEN, (C_pixals[0], C_pixals[1]), 4, 0)
	pygame.draw.circle(screen, GREEN, (E_pixals[0], E_pixals[1]), 4, 0)
	pygame.draw.circle(screen, GREEN, (G_pixals[0], G_pixals[1]), 4, 0)
	
	#Control Points are Blue 
	pygame.draw.circle(screen, BLUE, (B_pixals[0], B_pixals[1]), 4, 0)
	pygame.draw.circle(screen, BLUE, (D_pixals[0], D_pixals[1]), 4, 0)
	pygame.draw.circle(screen, BLUE, (F_pixals[0], F_pixals[1]), 4, 0)

	


	clock.tick(10)
	pygame.display.flip()

sys.exit()
pygame.quit()