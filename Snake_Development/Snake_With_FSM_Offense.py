"""
Spline Practice
"""

from scipy.interpolate import interp1d
import pygame 
#import numpy as np
import math
import os
import SnakeFSM
import Snake_Class

#Colors 
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255 ,0 ,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
BROWN = (185, 122, 87)
DK_BROWN = (116, 71, 48)
GLD_YELLOW = (255, 201, 14)

SIZE = (1000,800)
 
screen = pygame.display.set_mode(SIZE)


A = [340, 340] # Start Point
B = [150, 500] # Control point
C = [400, 400] # Endpoint
D = [500, 400] # Control point 
E = [400, 450]
F = [150, 600] # Control Point 
G = [450, 550]

#current_pt = [0,0]


class Snake_Body(pygame.sprite.Sprite):
	def __init__(self, Start_Point_A, Contral_Point_B, End_Point_C):
		self.Start_Point_A = Start_Point_A
		self.Contral_Point_B = Contral_Point_B
		self.End_Point_C = End_Point_C 	
		""""
		The snake does not have its own class yet, so the FSM is going to
		be  an atribute of the snakes body for now
		""" 
		self.FSM = SnakeFSM.SnakeFSM(self)

#MATHS
	def bezier(self, A, B, C, t):
	    """A B and C being 2-tuples, t being a float between 0 and 1"""
	    x = int((1 - t)**2 * A[0] + 2 * t * (1 - t) * B[0] + t**2 * C[0])
	    y = int((1 - t)**2 * A[1] + 2 * t * (1 - t) * B[1] + t**2 * C[1])
	    current_pt = (x,y)
	    return current_pt

	"""
	 This function is not currently used

	def cubicBezier(self, A, B, C, D, t):
	    x = int((1-t)**3 * A[0] + 3*t*(1-t)**2 * B[0] + 3*t**2*(1-t) * C[0] + t**3*D[0])
	    y = int((1-t)**3 * A[1] + 3*t*(1-t)**2 * B[1] + 3*t**2*(1-t) * C[1] + t**3*D[1])
	    current_pt = (x,y)
	    return current_pt
	"""

	def update(self, A, B, C):
		""" 
		This function take in the three body points of the snake and 
		returns the list of points that constitude the benzier curve.

		later, theres points will be connected with line segments to create the curve of the 
		snakes body
		"""
		ptlist = []
		steps = 0 # this is the number of t segments that compose each curve 
		t = 0 
		while steps <= 9:
			t += .1
			current_pt = self.bezier(A,B,C,t)
			ptlist.append(current_pt)
			steps += 1 
		return ptlist

class Snake(pygame.sprite.Sprite):
	def __init__(self):
		"""
		The Snake's Body segments are created below.

		Each segment is composed of a begining point, and control point, and
		an endpoint.

		The control point is a feature of benzier curves that controls the slope of
		the curve

		"""
		self.Snake_Body_One = Snake_Body(A,B,C)
		self.Snake_Body_Two = Snake_Body(C,D,E)
		self.Snake_butt = Snake_Body(E,F,G)


		self.head_surface = pygame.Surface((100, 30))
		self.head_surface.fill(WHITE)
		self.head_surface.set_colorkey(WHITE)


		self.headx = 0
		self.heady = 0 


		self.FSM = SnakeFSM.SnakeFSM(self)

	def getAngle(self,x1,y1, x2, y2):
	    # Return value is 0 for right, 90 for up, 180 for left, and 270 for down (and all values between 0 and 360)
	    #PS -- thank you past ren for commenting this for me -- Present Ren 
	    rise = y1 - y2
	    run = x1 - x2
	    angle = math.atan2(run, rise) # get the angle in radians
	    angle = angle * (180 / math.pi) # convert to degrees
	    angle = (angle + 90) % 360 # adjust for a right-facing sprite
	    return angle
	

	def rotate(self, headx, heady, degrees):
		"""
		This funtion takes in the position of the snakes head, and then 
		rotates the head's surface.
		"""
		rotate_surface = pygame.transform.rotate(self.head_surface, degrees)
		rotate_rect = rotate_surface.get_rect()
		rotate_rect.center = (headx, heady)
		screen.blit(rotate_surface, rotate_rect)

	def neck_roation(self, headx,heady,degrees):
		"""
		This function prevents the snakes head from pulling an Exorsit movement. 
		Head roation is limited in refrence to the control point A. 
		"""
		if (headx <= A[0] and heady >= A[1]): # I quadrent 
			if degrees >= 0 and degrees <= 90:  
				self.rotate(headx, heady, degrees)
			elif degrees >= 90 and degrees <= 225:
				degrees = 90
			elif degrees >= 225:
				degrees = 0
			self.rotate(headx, heady, degrees)
		elif (headx >= A[0] and heady <= A[1]): # III quadrant 
			if (degrees >= 180 and degrees <= 270):
				self.rotate(headx, headx, degrees)
			elif degrees >= 45 and degrees <= 180:
				degrees = 180
			elif degrees <= 45 or degrees >= 270:
				degrees = 270
			self.rotate(headx, heady, degrees)
		elif (headx <= A[0] and heady <= A[1]): # IV Quadrant 
			if degrees >= 270:
				self.rotate(headx, heady, degrees)
			elif degrees >= 135 and degrees <= 270:
				degrees = 270
			elif degrees >= 0 and degrees <= 135:
				degrees = 0 
			self.rotate(headx, heady, degrees) # II Quadrant 
		elif (headx >= A[0] and heady >= A[1]):
			if degrees >= 90 and degrees <= 180:
				self.rotate(headx, heady, degrees)
			elif degrees >= 180 and degrees <= 360:
				degrees = 180
			elif degrees <= 90 or degrees >= 375:
				degrees = 90
			self.rotate(headx, heady, degrees)

	def draw_head(self):

		#head_surface = pygame.Surface((100, 30))
		#self.head_surface.fill(WHITE)
		#self.head_surface.set_colorkey(WHITE)
		pygame.draw.ellipse(self.head_surface, BROWN, (self.headx + 35, self.heady, 60, 30))
		

		# Eyes 
		pygame.draw.ellipse(self.head_surface, GLD_YELLOW, (62, 18, 15, 10))
		pygame.draw.ellipse(self.head_surface, GLD_YELLOW, (62,1, 15, 10))
		pygame.draw.ellipse(self.head_surface, BLACK, (67, 20, 7, 9))
		pygame.draw.ellipse(self.head_surface, BLACK, (67, 3, 7, 9))
		# Nostirl 
		pygame.draw.ellipse(self.head_surface, BLACK, (83, 18, 7, 2))
		pygame.draw.ellipse(self.head_surface, BLACK, (83, 10, 7, 2))

		pygame.draw.ellipse(self.head_surface, BROWN, (self.headx + 35, self.heady, 60, 30))
	def draw_snake(self):
			#Draw Snakes Body 
		ptlist = self.Snake_Body_One.update(A,B,C)
		ptlist_mid = self.Snake_Body_Two.update(C,D,E)
		ptlist_mid[0] = ptlist[-1]

		ptlist_butt = self.Snake_butt.update(E,F,G)
		ptlist_butt[0] = ptlist_mid[-1]

		self.headx, self.heady = ptlist[0][0], ptlist[0][1]

		degrees = snake.getAngle(self.headx, self.heady, goal[0], goal[1])

		self.neck_roation(self.headx, self.heady, degrees)

		# Snake Body and Detail
		pygame.draw.lines(screen, BROWN, False, ptlist, 15)
		pygame.draw.lines(screen, DK_BROWN, False, ptlist, 5)

		pygame.draw.lines(screen, BROWN, False, ptlist_mid, 13)
		pygame.draw.lines(screen, DK_BROWN, False, ptlist_mid, 4)

		pygame.draw.lines(screen, BROWN, False, ptlist_butt, 11)
		pygame.draw.lines(screen, DK_BROWN, False, ptlist_butt, 3)
		
		#Endpoints are GREEN 
		pygame.draw.circle(screen, GREEN, ptlist[0], 8, 0)
		pygame.draw.circle(screen, GREEN, A, 4, 0)
		pygame.draw.circle(screen, GREEN, C, 4, 0)
		pygame.draw.circle(screen, GREEN, E, 4, 0)
		pygame.draw.circle(screen, GREEN, G, 4, 0)
		
		#Control Points are Blue 
		pygame.draw.circle(screen, BLUE, B, 4, 0)
		pygame.draw.circle(screen, BLUE, D, 4, 0)
		pygame.draw.circle(screen, BLUE, F, 4, 0)
	
	def Execute(self):
		snake.FSM.Execute()
		snake.draw_head()
		snake.draw_snake()
		

class Vector(object):
	"""
	This is the Vector class. The Vector class will control the ability of the 
	snakes's body to follow it's head

	The contrustor takes to points as parameters and then constructs a vector 
	out of them. 
	"""
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2
		self.x = self.point1[0] - self.point2[0] 
		self.y = self.point1[1] - self.point2[1] 
		self.vector = [self.x, self.y]

	def vector_addition(self, new_vector):
		"""
		This function adds two vectors together.
		The resulting tuple is divided by 20 because the sanke moves in 20 
		pixal incraments
		"""
		new_x = (self.x + new_vector.x)/ 20
		new_y = (self.y + new_vector.y)/ 20
		vector = [new_x, new_y]
		return vector

	def vector_magnatude(self):
		"""
		This fucntion returns the magnatude of the vector
		"""
		mag = math.sqrt((self.x**2) + (self.y**2)) 
		return mag





def distance(point1,point2):
	"""
	Returns the distance between two points.

	"""
	distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return distance 

def quadrant_correction(point, refrence):
	x_cor = 1
	y_cor = 1
	
	if point[0] < refrence[0]:
		x_cor *= 0
	elif point[0] > refrence[0]:
		x_cor *= 0
	elif point[1] < refrence[1]:
		y_cor *= 0
	elif point[1] > refrence[1]:
		y_cor *= 0
	"""
	if (point[0] < refrence[0]) and (point[1] < refrence[1]): # QII
		x_cor *= -1 
		y_cor *= -1
	elif (point[0] < refrence[0]) and (point[1] > refrence[1]): # QIII
		x_cor *= -1
		y_cor *= 1
	elif (point[0] > refrence[0]) and (point[1] > refrence[1]): # QIV
		x_cor *= 1
		y_cor *= 1
	elif point[0] > refrence[0] and point[1] < refrence[1]: # QI
		x_cor *= 1
		y_cor *= -1
	"""
	result = [x_cor, y_cor]
	return result 
	


def update(point, refrence):
	if (point[0] < refrence[0]) and (point[1] < refrence[1]):  # Q II
		point[0] += 20
		point[1] += 20
	elif (point[0] < refrence[0]) and (point[1] > refrence[1]): # 
		point[0] += 20
		point[1] -= 20
	elif (point[0] > refrence[0]) and (point[1] > refrence[1]):
		point[0] -= 20
		point[1] -= 20
	elif point[0] > refrence[0] and point[1] < refrence[1]:
		point[0]-= 20
		point[1] += 20
	elif point[0] < refrence[0]:
		point[0] += 20
	elif point[0] > refrence[0]:
		point[0] -= 20 
	elif point[1] < refrence[1]:
		point[1] += 20
	elif point[1] > refrence[1]:
		point[1] -= 20
	return [point[0], point[1]]

def offensive_relations(point, degrees_differnence, distance):
	degrees_around_goal = snake.getAngle(goal[0],goal[1],snake.headx, snake.heady)

	degrees = degrees_around_goal - degrees_differnence
	if degrees < 0:
		degrees = 360 + degrees
	
	if degrees >= 0 and degrees <= 90:   # I quadrent 
		angle = degrees
		changex = math.cos(math.radians(angle))
		changey = -math.sin(math.radians(angle))

	elif degrees > 90 and degrees <= 180: # II Quadrant 
		angle = 180 - degrees
		changex = -math.cos(math.radians(angle))
		changey = -math.sin(math.radians(angle))


	elif (degrees > 180 and degrees <= 270):  # III quadrant 
		angle = degrees - 180 
		changex = -math.cos(math.radians(angle))
		changey = math.sin(math.radians(angle))

	elif degrees > 270: # IV quadrant 
		angle = 360 - degrees
		changex = math.cos(math.radians(angle))
		changey = math.sin(math.radians(angle))

	#print changex, changey

	primex = int(goal[0] + changex * distance)
	primey = int(goal[1] + changey * distance)

	return [primex, primey]

snake = Snake()

"""
Initiates the States of the Snake
"""
snake.FSM.SetState("Traveling")
print "Nag is Traveling"


point_x_speed = 0
point_y_speed = 0


clock = pygame.time.Clock()

done = False 

goal = [100, 100]


"""
MAIN GAME LOOP
"""

while done != True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True 
		"""
		elif event.type == pygame.KEYDOWN:
			#determine if the keydown is an arrow key. if yes, adjust speed 
			if event.key == pygame.K_LEFT:
				point_x_speed =- 20
			elif event.key == pygame.K_RIGHT:
				point_x_speed = 20
			elif event.key == pygame.K_UP:
				point_y_speed =- 20
			elif event.key == pygame.K_DOWN: 
				point_y_speed = 20
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
		"""
	

	if distance(A, goal) >= 200:
		A = update(A,goal)
	
	#elif distance(C, goal) > 100:
	#	resulting_vectorAGoal = ABvector.vector_addition(AGoalvector)
	#	C = [C[0] + resulting_vectorAGoal[0], C[1] + resulting_vectorAGoal[1]]




	"""
	Creates vectors between adjacent points
	""" 
	ABvector = Vector(A,B)
	BCvector = Vector(B,C)
	CDvector = Vector(C,D)
	DEvector = Vector(D,E)
	EFvector = Vector(E,F)
	FGvector = Vector(F,G)

	"""
	Vector between A and Goal 
	"""
	AGoalvector = Vector(A,goal)

	"""
	Gets the forward momnet of the snakes head as a vector
	"""
	head_new_vector = Vector([point_x_speed,0], [0,point_y_speed])

	"""vector addition to get the resulting vectors from adding the bodys portions current 
	direction and the perceding vectors direction
	"""  
	resulting_vector = ABvector.vector_addition(head_new_vector) # connects AB to head movemnet 
	resulting_vectorBC = BCvector.vector_addition(ABvector)# relates BC to AB
	resulting_vectorCD = CDvector.vector_addition(BCvector)
	resulting_vectorDE = DEvector.vector_addition(CDvector)
	resulting_vectorEF = EFvector.vector_addition(DEvector)
	resulting_vectorFG = FGvector.vector_addition(EFvector)

	"""
	These two lines allow me to move the snakes head with the keys
	"""
	point = A
	A = [point[0] + point_x_speed, point[1] + point_y_speed]

	"""
	OFfesnive Testing 
	"""
	Bdegree = 90
	Cdegree = 30
	Ddegree = 5
	Edegree = 30
	Fdegree = 90
	Gdegree = 30

	Bradi = 200
	Cradi = 150
	Dradi = 250
	Eradi = 200
	Fradi = 300
	Gradi = 250

	if point_x_speed != 0 or point_y_speed != 0:
		Bprime = offensive_relations(B, 90, 200)
		Cprime = offensive_relations(C, 20, 150)
		Dprime = offensive_relations(D, 5, 250)
		Eprime = offensive_relations(E, 25, 200)
		Fprime = offensive_relations(F, 90, 300)
		Gprime = offensive_relations(G, 30, 250)
	

	"""
	These if statments say that if the distance between two adjacent points 
	are greater than 100, start moving the latter point in the direction of the 
	resulting vector (which we calulated abouve)
	"""
	if distance((snake.headx, snake.heady), goal) >= 300:
		if distance(A,B) >= 100:
			B = [B[0] + resulting_vector[0], B[1] + resulting_vector[1]]
		if distance(B,C) >= 100:
			C = [C[0] + resulting_vectorBC[0], C[1] + resulting_vectorBC[1]]
		if distance(C,D) >= 100:
			D = [D[0] + resulting_vectorCD[0], D[1] + resulting_vectorCD[1]]
		if distance(D,E) >= 100:
			E = [E[0] + resulting_vectorDE[0], E[1] + resulting_vectorDE[1]]
			#D = [D[0] + point_x_speed, D[1] + point_y_speed]
		if distance(E,F) >= 100:
			F = [F[0] + resulting_vectorEF[0], F[1] + resulting_vectorEF[1]]
		if distance(F,G) >= 100:
			G = [G[0] + resulting_vectorFG[0], G[1] + resulting_vectorFG[1]]
			#F = [F[0] + resulting_vector[0], F[1] + resulting_vector[1]]
		"""
		if distance((snake.headx, snake.heady), goal) < 300:
			B = [B[0] + resulting_vectorABprime[0], B[1] + resulting_vectorABprime[1]]
		if distance((snake.headx, snake.heady), goal) < 290:
			C = [C[0] + resulting_vectorACprime[0], C[1] + resulting_vectorACprime[1]]
		"""
	elif distance((snake.headx, snake.heady), goal) < 300:
		Aprime = offensive_relations(A,30, 130)
		Bprime = offensive_relations(B, 90, 200)
		Cprime = offensive_relations(C, 30, 150)
		Dprime = offensive_relations(D, 5, 250)
		Eprime = offensive_relations(E, 30, 170)
		Fprime = offensive_relations(F, 70, 250)
		Gprime = offensive_relations(G, 30, 190)

		"""
		These are test vectors for offensive movmnt 
		"""
		ABvector = Vector(A,B)
		BprimeAvector = Vector(Bprime,A)
		resulting_vectorBBprime = ABvector.vector_addition(BprimeAvector)

		ACvector = Vector(A,C)
		CprimeAvector = Vector(Cprime, A)
		resulting_vectorCCprime = ACvector.vector_addition(CprimeAvector)


		ADvector = Vector(A,D)
		DprimeAvector = Vector(Dprime, A)
		resulting_vectorDDprime = ADvector.vector_addition(DprimeAvector)

		AEvector = Vector(A, E)
		EprimeAvector = Vector(Eprime, A)
		resulting_vectorEEprime = AEvector.vector_addition(EprimeAvector)

		AFvector = Vector(A,F)
		FprimeAvector = Vector(Fprime, A)
		resulting_vectorFFprime = AFvector.vector_addition(FprimeAvector)

		AGvector = Vector(A,G)
		GprimeAvector = Vector(Gprime, A)
		resulting_vectorGGprime = AGvector.vector_addition(GprimeAvector)

		FprimeBvector = Vector(Fprime,B)
		BFvector = Vector(B,F)
		resulting_vectorBF = FprimeBvector.vector_addition(BFvector)



		if distance(B, Bprime) > 50:
			print distance(B,Bprime) 

			B = [B[0] + resulting_vectorBBprime[0], B[1] + resulting_vectorBBprime[1]]
			C = [C[0] + resulting_vectorCCprime[0], C[1] + resulting_vectorCCprime[1]]
			D = [D[0] + resulting_vectorDDprime[0], D[1] + resulting_vectorDDprime[1]]	


			#if distance(C,D) >= 50:
			#	D = [D[0] + resulting_vectorCD[0], D[1] + resulting_vectorCD[1]]
			if distance(D,E) >= 100:
				E = [E[0] + resulting_vectorDE[0], E[1] + resulting_vectorDE[1]]
				#D = [D[0] + point_x_speed, D[1] + point_y_speed]
			if distance(E,F) >= 50:
				F = [F[0] + resulting_vectorEF[0], F[1] + resulting_vectorEF[1]]
			if distance(F,G) >= 150:
				G = [G[0] + resulting_vectorFG[0], G[1] + resulting_vectorFG[1]]

		if distance(C, Cprime) <= 70:

			E = [E[0] + resulting_vectorEEprime[0], E[1] + resulting_vectorEEprime[1]]	

		if distance(C, Cprime) <= 50:
			B = [B[0] + resulting_vectorBBprime[0], B[1] + resulting_vectorBBprime[1]]
			C = [C[0] + resulting_vectorCCprime[0], C[1] + resulting_vectorCCprime[1]]
			E = [E[0] + resulting_vectorEEprime[0], E[1] + resulting_vectorEEprime[1]]	
			F = [F[0] + resulting_vectorFFprime[0], F[1] + resulting_vectorFFprime[1]]	
			G = [G[0] + resulting_vectorGGprime[0], G[1] + resulting_vectorGGprime[1]]	


	#transition triggers
	if A[0] <= 400 and A[1] >= 400:
		if snake.FSM.cur_state_name != "Offense": 
			snake.FSM.Transition("To_Offense")
			snake.FSM.Traveling = False 
			print "Nag is Offensive"

	elif A[0] >= 600 and A[1] <= 400:
		if snake.FSM.cur_state_name != "Defensive": 
			snake.FSM.Transition("To_Defensive")
			snake.FSM.Traveling = False 
			print "Nag is Defensive"

	else: 
		if snake.FSM.cur_state_name != "Traveling":
			snake.FSM.Transition("To_Traveling")
			snake.FSM.Offense = False 
			snake.FSM.Defensive = False 
			print "Nag is Traveling"
	


	screen.fill(WHITE)

	


	"""
	Fake State zones used for testing FSM
	"""
	pygame.draw.rect(screen, RED, (0,400, 400, 400), 0)
	pygame.draw.rect(screen, GREEN, (600,0, 400, 400), 0)

	"""
	Stand in Mongoose
	"""
	pygame.draw.rect(screen, DK_BROWN,(goal[0], goal[1], 10, 10), 0)



	#pygame.draw.circle(screen, GLD_YELLOW, (int(Cprime[0]), int(Cprime[1])), 10, 0)

	#pygame.draw.circle(screen, GLD_YELLOW, (int(Bprime[0]), int(Bprime[1])), 8, 0)

	
	snake.FSM.Execute()

	snake.Execute()

	clock.tick(10)

	pygame.display.flip()


pygame.quit()


