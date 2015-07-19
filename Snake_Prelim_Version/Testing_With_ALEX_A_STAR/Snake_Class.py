"""
Snake_Class
""" 

import math
import Vector_Class
import pygame
import SnakeFSM


BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255 ,0 ,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
BROWN = (185, 122, 87)
DK_BROWN = (116, 71, 48)
GLD_YELLOW = (255, 201, 14)


"""
A = [350, 350] # Start Point
B = [370, 370] # Control point
C = [390, 390] # Endpoint
D = [410, 410] # Control point 
E = [430, 430]
F = [450, 450] # Control Point 
G = [470, 470]
"""





class Snake_Body(pygame.sprite.Sprite):
	def __init__(self, Start_Point_A, Contral_Point_B, End_Point_C):
		self.Start_Point_A = Start_Point_A
		self.Contral_Point_B = Contral_Point_B
		self.End_Point_C = End_Point_C 	
		""""
		The snake does not have its own class yet, so the FSM is going to
		be  an atribute of the snakes body for now
		""" 
		

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

class Snake (pygame.sprite.Sprite):
	def __init__(self, A, B, C, D, E, F, G):
		"""
		The Snake's Body segments are created below.

		Each segment is composed of a begining point, and control point, and
		an endpoint.

		The control point is a feature of benzier curves that controls the slope of
		the curve

		"""
		self.A = A
		self.B = B
		self.C = C
		self.D = D
		self.E = E
		self.F = F
		self.G = G

		self.point_x_speed = 0
		self.point_y_speed = 0 
		
		self.headx = 0
		self.heady = 0

		self.screen = None
		self.goal = None 

		self.Snake_Body_One = Snake_Body(self.A, self.B, self.C)
		self.Snake_Body_Two = Snake_Body(self.C, self.D, self.E)
		self.Snake_butt = Snake_Body(self.E, self.F, self.G)


		self.head_surface = pygame.Surface((70, 35))
		self.head_surface.fill(WHITE)
		self.head_surface.set_colorkey(WHITE)




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
		self.screen.blit(rotate_surface, rotate_rect)

	def neck_roation(self, headx,heady,degrees):
		"""
		This function prevents the snakes head from pulling an Exorsit movement. 
		Head roation is limited in refrence to the control point A. 
		"""
		if (headx <= self.A[0] and heady >= self.A[1]): # I quadrent 
			if degrees >= 0 and degrees <= 90:  
				self.rotate(headx, heady, degrees)
			elif degrees >= 90 and degrees <= 225:
				degrees = 90
			elif degrees >= 225:
				degrees = 0
			self.rotate(headx, heady, degrees)
		elif (headx >= self.A[0] and heady <= self.A[1]): # III quadrant 
			if (degrees >= 180 and degrees <= 270):
				self.rotate(headx, headx, degrees)
			elif degrees >= 45 and degrees <= 180:
				degrees = 180
			elif degrees <= 45 or degrees >= 270:
				degrees = 270
			self.rotate(headx, heady, degrees)
		elif (headx <= self.A[0] and heady <= self.A[1]): # IV Quadrant 
			if degrees >= 270:
				self.rotate(headx, heady, degrees)
			elif degrees >= 135 and degrees <= 270:
				degrees = 270
			elif degrees >= 0 and degrees <= 135:
				degrees = 0 
			self.rotate(headx, heady, degrees) # II Quadrant 
		elif (headx >= self.A[0] and heady >= self.A[1]):
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
		pygame.draw.ellipse(self.head_surface, BROWN, (self.headx + 20, self.heady + 8, 45, 20))
		

		# Eyes 
		"""
		pygame.draw.ellipse(self.head_surface, GLD_YELLOW, (62, 18, 15, 10))
		pygame.draw.ellipse(self.head_surface, GLD_YELLOW, (62,1, 15, 10))
		pygame.draw.ellipse(self.head_surface, BLACK, (67, 20, 7, 9))
		pygame.draw.ellipse(self.head_surface, BLACK, (67, 3, 7, 9))
		# Nostirl 
		pygame.draw.ellipse(self.head_surface, BLACK, (83, 18, 7, 2))
		pygame.draw.ellipse(self.head_surface, BLACK, (83, 10, 7, 2))
		"""

		
	def draw_snake(self):
			#Draw Snakes Body 
		ptlist = self.Snake_Body_One.update(self.A,self.B,self.C)
		ptlist_mid = self.Snake_Body_Two.update(self.C,self.D,self.E)
		ptlist_mid[0] = ptlist[-1]

		ptlist_butt = self.Snake_butt.update(self.E,self.F,self.G)
		ptlist_butt[0] = ptlist_mid[-1]

		self.headx, self.heady = ptlist[0][0], ptlist[0][1]


		degrees = self.getAngle(self.headx, self.heady, self.goal[0], self.goal[1])

		self.neck_roation(self.headx, self.heady, degrees)

		# Snake Body and Detail
		pygame.draw.lines(self.screen, BROWN, False, ptlist, 10)
		pygame.draw.lines(self.screen, DK_BROWN, False, ptlist, 5)

		pygame.draw.lines(self.screen, BROWN, False, ptlist_mid, 8)
		pygame.draw.lines(self.screen, DK_BROWN, False, ptlist_mid, 4)

		pygame.draw.lines(self.screen, BROWN, False, ptlist_butt, 6)
		pygame.draw.lines(self.screen, DK_BROWN, False, ptlist_butt, 3)
		
		#Endpoints are GREEN 
		pygame.draw.circle(self.screen, GREEN, ptlist[0], 8, 0)
		pygame.draw.circle(self.screen, GREEN, self.A, 4, 0)
		pygame.draw.circle(self.screen, GREEN, self.C, 4, 0)
		pygame.draw.circle(self.screen, GREEN, self.E, 4, 0)
		pygame.draw.circle(self.screen, GREEN, self.G, 4, 0)
		
		#Control Points are Blue 
		pygame.draw.circle(self.screen, BLUE, self.B, 4, 0)
		pygame.draw.circle(self.screen, BLUE, self.D, 4, 0)
		pygame.draw.circle(self.screen, BLUE, self.F, 4, 0)


	
	def Execute(self):
		self.draw_head()
		self.draw_snake()



