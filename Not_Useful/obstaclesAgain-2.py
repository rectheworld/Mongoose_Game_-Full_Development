import math
import copy
import pygame
import sys
import random

"""
pop_list = 














"""
# format of the open list is 
# openlist: 
def heuristic_est(goal_pos, grid):
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

def create_grid():
	'''
	Creates a 2-dimensional grid of cells.  Output is of the form [[column,row],[column,row]...]
	'''
	grid = []
	for i in range(grid_width):
		for j in range(grid_height):
			grid.append([i,j])
	return grid

def get_heur_cost(position):
	'''
	Returns the estimated heuristic cost of a desired cell (position) by searching through a list of lists (grid)
	'''
	for element in grid:
		if element[0] == position:
			return element[1]

def find_available_cells(position):
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

def add_successors(next_position_value):
	'''
	Checks each cell available to move to and compares their estimated heuristic cost.  Returns a list of
	the position, (i.e. [column, row]) with the lowest cost.
	'''
	position = next_position_value[-2]
	LEFT, RIGHT, UP, DOWN = find_available_cells(position)
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
		cost = get_heur_cost(pos)
		successor.insert(-1,pos)
		successor[-1] += cost
		open_list.append(successor)

def choose_next_to_close():
	'''
	Returns the index value for the successor with the lowest cost in the open list.  In the event that more than one cell
	holds the lowest cost, it will return the smaller of the index values.
	'''
	lowest_index = 0
	if len(open_list) == 0:
		print "Error: The open list is empty"
	else:
		for i in range(1,len(open_list)):
		    if open_list[i][-1] < open_list[lowest_index][-1]:
		        lowest_index = i
		return lowest_index

def update_closed(next_position_value):
	'''
	Moves the next cell to check into the appropriate list within the closed lists.
	'''
	if len(closed_list) == 0:
		closed_list.append(next_position_value)
		return
	else:
		final_position = next_position_value[-2]
		final_cost = next_position_value[-1]
		for i in range(len(closed_list)):
			if closed_list[i][-2] == final_position:
				if final_cost < closed_list[i][-1]:
					closed_list.pop(i)
					closed_list.append(next_position_value)
				return
	closed_list.append(next_position_value)

def update_open(next_position_index):
	'''
	Removes the current path in consideration from the open list and also removes any paths from the open list whose last position has 
	already been accessed via a less expensive path.
	'''
	pop_list = []
	open_list.pop(next_position_index)
	for i in range(len(open_list)):
		for j in range(len(closed_list)):
			if open_list[i][-2] == closed_list[j][-2]:
				if open_list[i][-1] > closed_list[j][-1]:
					if not i in pop_list:
						pop_list.append(i)
	if len(pop_list) != 0:
		pop_list.reverse()
		for index in pop_list:
			open_list.pop(index)

def update_lists():
	'''
	Chooses the next successor in the open list, moves it to the closed list, and adds its successors to the open list.
	'''
	next_position_index = choose_next_to_close() #saves the index location of the list in the open_list that we are using as the current position
	next_position_value = open_list[next_position_index] #saves the value of the list from the open_list to manipulate later on
	next_position = next_position_value[-2] # the actual [x,y] coordinates of the next position

	add_successors(next_position_value) # adds the successors of the cheapest path in the open list to the open list
	update_closed(next_position_value) # adds the cheapest path to the closed list
	update_open(next_position_index) # see function notes for details

def check_for_goal():
	'''
	Searches the closed list for the goal position.
	'''
	for item in closed_list:
		if item[-2] == goal_pos:
			return True
	return False

def find_path():
	'''
	Searches until the closed list contains the goal position, returns the first path that contains the goal 
	position with the last element (cost) removed.
	'''
	goal = False

	while goal == False:
		update_lists()
		goal = check_for_goal()

	for i in range(len(closed_list)):
		if closed_list[i][-2] == goal_pos:
			return closed_list[i][:-1]

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
	'gray':(25,25,25)}

grid_width = 25
grid_height = 15
cell_size = 40
margin = 1
obstacles = [[6,5],[7,5],[8,5],[6,6],[6,7],
			 [6,8],[6,9],[6,10],[6,11],
			 [20,10],[20,11],[20,12],[19,12],[19,13],[19,14],
			 [18,1],[18,2],[18,3],[19,3],[20,3]]

goal_pos = random_position()
# goal_pos = [7,7]
# starting_position = [0,0]
starting_position = random_position()
open_list = []
closed_list = []


grid = heuristic_est(goal_pos,create_grid())
open_list.append([starting_position, get_heur_cost(starting_position)])

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((grid_width*cell_size, grid_height*cell_size))
pygame.display.set_caption("MONGOOSE")
screen.fill(colors['black'])
path = []
while True:
	'''
	The game loop.
	'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	#draws the default rectangles on the pygame screen
	default_color = colors['light_blue'] #this is the default rectangle color
	for column in range(grid_width):
		for row in range(grid_height):
			if [column,row] in obstacles:
				color = colors['gray']
			else:
				color = default_color
			draw_rect(color, [column,row])
	
	current_color = colors['yellow'] #this is the color of the current cell rectangle
	goal_color = colors['pink'] #this is the color of the goal cell rectangle
	if len(path) == 0: #checks to see if there is no path
		path = find_path()
	draw_rect(current_color, [path[0][0],path[0][1]]) #draws the current location of the agent based on the path built above
	draw_rect(goal_color, [goal_pos[0],goal_pos[1]]) #draws the location of the goal rectangle
	path.pop(0)

	clock.tick(5)
	pygame.display.flip()

pygame.quit()