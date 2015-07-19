

DK_BROWN = (116, 71, 48)


Snake_Class.snake.screen = screen # feeds the screen variable to the snake instance in Snake_Class

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

index = 1 # Used to access item in the snake_path list 


	#########################
	In GAME LOOP
	#########################

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
	
	