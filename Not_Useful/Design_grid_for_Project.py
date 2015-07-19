"""
Uses an array to back a grid on-screen
Rattle snake video Traxxas e-Revo Rattlesnake Encounter
"""

#import Pygame
import pygame 

#Colors!!!!
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

#set width and hight of each grid location 
width = 20
height = 20

#sets the margin between each cell
margin = 0

#Create a 2 dimensional array. (lists of lists)
grid = []
for row in range(35):
	# Add an empty array that will hold each cell in this row
	grid.append([])
	for col in range(50): # fix
		grid[row].append(0) # append a cell
		grid[row][col] = '0'
 


# Create Bushes 




#initiate pygame
pygame.init()

#clock 
clock = pygame.time.Clock()

#set the hight and width of the screen 
SIZE = [1000,700]
screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption("Array Backed Grid")

#snake head cordinates on grid 
head_x_grid = 4 
head_y_grid = 4

#Mongoose Cordonites via grid measure
mon_x_grid = 10
mon_y_grid = 10

#Speed in Pixals per frame 
head_x_speed = 0 
head_y_speed = 0 

mon_x_speed = 0
mon_y_speed = 0

#spite practice 
class Snake(pygame.sprite.Sprite):
	def __init__(self):
		self.x = head_x_grid
		self.y = head_y_grid
		#self.center = (self.x, self.y)

	def render(self):
		pygame.draw.circle(screen, RED, (self.x * width, self.y * width), width / 2 ,0)

	def update(self):
		global mongoose
		if (self.x < mon_x_grid) and (self.y < mon_y_grid):
			self.x += 1
			self.y += 1
		elif (self.x < mon_x_grid) and (self.y > mon_y_grid):
			self.x += 1
			self.y -= 1
		elif (self.x > mon_x_grid) and (self.y > mon_y_grid):
			self.x -= 1
			self.y -= 1
		elif self.x > mon_x_grid and self.y < mon_y_grid:
			self.x -= 1
			self.y += 1
		elif self.x < mon_x_grid:
			self.x += 1
		elif self.x > mon_x_grid:
			self.x -= 1 
		elif self.y < mon_y_grid:
			self.y += 1 
		elif self.y > mon_y_grid:
			self -= 1


class Snake_Mid(pygame.sprite.Sprite):
	def __init__(self):
		self.x = mon_x
		self.y = mon_y

	def render(self):
			pygame.draw.circle(screen, RED, (self.x, self.y), width / 2 ,0)		


class Mongoose(pygame.sprite.Sprite):
	def __init__(self):
		self.x = mon_x_grid
		self.y = mon_y_grid

	def render(self):
		pygame.draw.circle(screen, GREEN, (mon_x_grid * width, mon_y_grid * width), (width / 2), 0)



#


#Calling our Characters 
snake = Snake()
mongoose = Mongoose()


#Loop until the user click the close button
done = False 

# GAME LOOP 
while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			#determine if the keydown is an arrow key. if yes, adjust speed 
			if event.key == pygame.K_LEFT:
				mon_x_speed =- 2
			elif event.key == pygame.K_RIGHT:
				mon_x_speed = 2
			elif event.key == pygame.K_UP:
				mon_y_speed =- 2
			elif event.key == pygame.K_DOWN: 
				mon_y_speed = 2

			# User let up on a key 
		elif event.type == pygame.KEYUP:
			# if it is an arrow key, reset vector back to zero
			if event.key == pygame.K_LEFT:
				mon_x_speed = 0
			elif event.key == pygame.K_RIGHT:
				mon_x_speed = 0
			elif event.key == pygame.K_UP:
				mon_y_speed = 0
			elif event.key == pygame.K_DOWN:
				mon_y_speed = 0


	mon_x_grid = (mon_x_grid + mon_x_speed) 
	mon_y_grid = (mon_y_grid + mon_y_speed)
	
	
	grid[head_x_grid][head_y_grid] = "S"
	grid[mon_x_grid][mon_y_grid] = "M"


	#fill screen 
	screen.fill(BLACK)

	#draw the grid 
	for row in range(35):
		for column in range(50):
			color = WHITE
			if grid[row][column] == 1:
				color = GREEN
			pygame.draw.rect(screen, color, [(margin +width)*column+margin, (margin + height)* row +margin, width, height])

	
	snake.update()
	snake.render()

	mongoose.render()

	#snake_mid_one.render()
	#snake_mid_two.render()
	#clock 
	clock.tick(4)

	pygame.display.flip()

pygame.quit()


