"""
Spline Practice
"""

from scipy.interpolate import interp1d
import pygame 
import numpy as np
import math

#Colors 
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255 ,0 ,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
BROWN = (185, 122, 87)
DK_BROWN = (116, 71, 48)
GLD_YELLOW = (255, 201, 14)

SIZE = (800,800)
 
screen = pygame.display.set_mode(SIZE)


A = [350, 350] # Start Point
B = [150, 500] # Control point
C = [400, 400] # Endpoint
D = [600, 400]


current_pt = [0,0]
points_list = []


#MATHS
def bezier(A, B, C, t):
    """A B and C being 2-tuples, t being a float between 0 and 1"""
    x = int((1 - t)**2 * A[0] + 2 * t * (1 - t) * B[0] + t**2 * C[0])
    y = int((1 - t)**2 * A[1] + 2 * t * (1 - t) * B[1] + t**2 * C[1])
    current_pt = (x,y)
    return current_pt

def cubicBezier(A, B, C, D, t):
    x = int((1-t)**3 * A[0] + 3*t*(1-t)**2 * B[0] + 3*t**2*(1-t) * C[0] + t**3*D[0])
    y = int((1-t)**3 * A[1] + 3*t*(1-t)**2 * B[1] + 3*t**2*(1-t) * C[1] + t**3*D[1])
    current_pt = (x,y)
    return current_pt


def update():
	ptlist = []
	steps = 0
	t = 0 
	while steps <= 9:
		t += .1
		current_pt = bezier(A,B,C,t)
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

A_x_speed = 0
A_y_speed = 0

clock = pygame.time.Clock()

done = False 

while done != True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True 
		elif event.type == pygame.KEYDOWN:
			#determine if the keydown is an arrow key. if yes, adjust speed 
			if event.key == pygame.K_LEFT:
				A_x_speed =- 20
			elif event.key == pygame.K_RIGHT:
				A_x_speed = 20
			elif event.key == pygame.K_UP:
				A_y_speed =- 20
			elif event.key == pygame.K_DOWN: 
				A_y_speed = 20
			# User let up on a key 
		elif event.type == pygame.KEYUP:
			# if it is an arrow key, reset vector back to zero
			if event.key == pygame.K_LEFT:
				A_x_speed = 0
			elif event.key == pygame.K_RIGHT:
				A_x_speed = 0
			elif event.key == pygame.K_UP:
				A_y_speed = 0
			elif event.key == pygame.K_DOWN:
				A_y_speed = 0

	A = [A[0] + A_x_speed, A[1] + A_y_speed]
	
	mx, my = pygame.mouse.get_pos()

	screen.fill(WHITE)
	ptlist = update()
	headx, heady = ptlist[0][0],ptlist[0][1]

	degrees = getAngle(headx, heady, mx, my)

	neck_roation(headx, heady, degrees)

	pygame.draw.lines(screen, BROWN, False, ptlist, 15)
	pygame.draw.lines(screen, DK_BROWN, False, ptlist, 5)
	pygame.draw.circle(screen, GREEN, ptlist[0], 8, 0)
	pygame.draw.circle(screen, GREEN, A, 4, 0)
	pygame.draw.circle(screen, BLUE, B, 4, 0)
	pygame.draw.circle(screen, GREEN, C, 4, 0)

	clock.tick(10)

	pygame.display.flip()

pygame.quit()


