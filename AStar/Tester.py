import pygame
from pygame.locals import *
import sys


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

pygame.init()
width = 1000
height = 560
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

desert_sprite = pygame.image.load("desert1.png").convert_alpha()
image = desert_sprite.subsurface(pygame.Rect((14,76),(50,56)))





# screen.blit(image, (0,0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for i in range(20):
        x_start = i*50
        for j in range(10):
            y_start = j*56
            screen.blit(image,(x_start,y_start))

    pygame.display.flip()