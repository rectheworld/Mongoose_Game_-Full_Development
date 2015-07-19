"""
Spline Practice
"""

from scipy.interpolate import interp1d
import pygame 
#import numpy as np
import math
import os
import SnakeFSM

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


A = [350, 350] # Start Point
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
		self.FSM = SnakeFSM.SnakeFSM(self)

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

class Vector(object):	
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2
		self.x = self.point1[0] - self.point2[0] 
		self.y = self.point1[1] - self.point2[1] 
		self.vector = [self.x, self.y]

		

	def vector_addition(self, new_vector):
		new_x = (self.x + new_vector.x)/ 20
		new_y = (self.y + new_vector.y)/ 20
		vector = [new_x, new_y]
		return vector



Snake_Body_One = Snake_Body(A,B,C)
Snake_Body_Two = Snake_Body(C,D,E)
Snake_butt = Snake_Body(E,F,G)




def getAngle(x1,y1, x2, y2):
    # Return value is 0 for right, 90 for up, 180 for left, and 270 for down (and all values between 0 and 360)
    rise = y1 - y2
    run = x1 - x2
    angle = math.atan2(run, rise) # get the angle in radians
    angle = angle * (180 / math.pi) # convert to degrees
    angle = (angle + 90) % 360 # adjust for a right-facing sprite
    return angle


# Draw Head
headx = 0
heady = 0
# Rotaable Surface for the Snakes head 
head_surface = pygame.Surface((100, 30))
head_surface.fill(WHITE)
head_surface.set_colorkey(WHITE)
pygame.draw.ellipse(head_surface, BROWN, (headx + 35, heady, 60, 30))
# Eyes 
pygame.draw.ellipse(head_surface, GLD_YELLOW, (62, 18, 15, 10))
pygame.draw.ellipse(head_surface, GLD_YELLOW, (62,1, 15, 10))
pygame.draw.ellipse(head_surface, BLACK, (67, 20, 7, 9))
pygame.draw.ellipse(head_surface, BLACK, (67, 3, 7, 9))
# Nostirl 
pygame.draw.ellipse(head_surface, BLACK, (83, 18, 7, 2))
pygame.draw.ellipse(head_surface, BLACK, (83, 10, 7, 2))


def rotate(headx, heady, degrees):
	rotate_surface = pygame.transform.rotate(head_surface, degrees)
	rotate_rect = rotate_surface.get_rect()
	rotate_rect.center = (headx, heady)
	screen.blit(rotate_surface, rotate_rect)

def neck_roation(headx,heady,degrees):
	if (headx <= A[0] and heady >= A[1]): # I quadrent 
		if degrees >= 0 and degrees <= 90:  
			rotate(headx, heady, degrees)
		elif degrees >= 90 and degrees <= 225:
			degrees = 90
		elif degrees >= 225:
			degrees = 0
		rotate(headx, heady, degrees)
	elif (headx >= A[0] and heady <= A[1]): # III quadrant 
		if (degrees >= 180 and degrees <= 270):
			rotate(headx, headx, degrees)
		elif degrees >= 45 and degrees <= 180:
			degrees = 180
		elif degrees <= 45 or degrees >= 270:
			degrees = 270
		rotate(headx, heady, degrees)
	elif (headx <= A[0] and heady <= A[1]): # IV Quadrant 
		if degrees >= 270:
			rotate(headx, heady, degrees)
		elif degrees >= 135 and degrees <= 270:
			degrees = 270
		elif degrees >= 0 and degrees <= 135:
			degrees = 0 
		rotate(headx, heady, degrees) # II Quadrant 
	elif (headx >= A[0] and heady >= A[1]):
		if degrees >= 90 and degrees <= 180:
			rotate(headx, heady, degrees)
		elif degrees >= 180 and degrees <= 360:
			degrees = 180
		elif degrees <= 90 or degrees >= 375:
			degrees = 90
		rotate(headx, heady, degrees)


def distance(point1,point2):
	distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return distance 


# Set State 
Snake_Body_One.FSM.SetState("Traveling")


point_x_speed = 0
point_y_speed = 0


clock = pygame.time.Clock()

done = False 

while done != True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True 
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


# vector point from point b to point a 
	ABvector = Vector(A,B)
	BCvector = Vector(B,C)
	CDvector = Vector(C,D)
	DEvector = Vector(D,E)
	EFvector = Vector(E,F)
	FGvector = Vector(F,G)
	
	head_new_vector = Vector([point_x_speed,0], [0,point_y_speed])
	


	#vector addition 
	

	resulting_vector = ABvector.vector_addition(head_new_vector) # connects AB to head movemnet 
	resulting_vectorBC = BCvector.vector_addition(ABvector)# relates BC to AB
	resulting_vectorCD = CDvector.vector_addition(BCvector)
	resulting_vectorDE = DEvector.vector_addition(CDvector)
	resulting_vectorEF = EFvector.vector_addition(DEvector)
	resulting_vectorFG = FGvector.vector_addition(EFvector)


	point = A
	A = [point[0] + point_x_speed, point[1] + point_y_speed]
	
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


	#transition triggers
	if A[0] <= 400 and A[1] >= 400:
		if Snake_Body_One.FSM.cur_state_name != "Offense": 
			Snake_Body_One.FSM.Transition("To_Offense")
			Snake_Body_One.FSM.Traveling = False 

	elif A[0] >= 600 and A[1] <= 400:
		if Snake_Body_One.FSM.cur_state_name != "Defensive": 
			Snake_Body_One.FSM.Transition("To_Defensive")
			Snake_Body_One.FSM.Traveling = False 

	else: 
		if Snake_Body_One.FSM.cur_state_name != "Traveling":
			Snake_Body_One.FSM.Transition("To_Traveling")
			Snake_Body_One.FSM.Offense = False 
			Snake_Body_One.FSM.Defensive = False 
	Snake_Body_One.FSM.Execute()









	mx, my = pygame.mouse.get_pos()

	screen.fill(WHITE)
	pygame.draw.rect(screen, RED, (0,400, 400, 400), 0)
	pygame.draw.rect(screen, GREEN, (600,0, 400, 400), 0)
	
	

	ptlist = Snake_Body_One.update(A,B,C)
	ptlist_mid = Snake_Body_Two.update(C,D,E)
	ptlist_mid[0] = ptlist[-1]

	ptlist_butt = Snake_butt.update(E,F,G)
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
	pygame.draw.circle(screen, GREEN, A, 4, 0)
	pygame.draw.circle(screen, GREEN, C, 4, 0)
	pygame.draw.circle(screen, GREEN, E, 4, 0)
	pygame.draw.circle(screen, GREEN, G, 4, 0)
	
	#Control Points are Blue 
	pygame.draw.circle(screen, BLUE, B, 4, 0)
	pygame.draw.circle(screen, BLUE, D, 4, 0)
	pygame.draw.circle(screen, BLUE, F, 4, 0)
	

	clock.tick(10)

	pygame.display.flip()


pygame.quit()


