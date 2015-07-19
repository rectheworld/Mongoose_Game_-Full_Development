import pygame

class Baby(pygame.sprite.Sprite):
    stoic = 1
    afraid = -1
    seeking = 5
    dead = 0
    spawnLocations = [[1,0],[10,0],[5,6],[33,5],[27,12],[17,13]]
    currentLocations = []
    spriteTransitioner = 1


    def __init__(self, pos, deltaTime=0):
        """
        Constructor for the baby mongoose class for the Mongoose game.
        :param tileX: the x-coordinate for the tile position to render the baby
        :param tileY: the y-coordinate for the tile position to render the baby
        :return:
        """
        self.x = pos[0]
        self.y = pos[1]
        self.currentState = self.stoic
        self.birthTime = deltaTime
        self.lastUpdateTime = deltaTime
        self.spriteIndex = 0
        
    def updateRendering(self, deltaTime):
        """
        Updates the sprite data for the baby mongoose based on frames.
        :rtype : sprite subsurface for current frameset
        :param deltaTime: The change in frames since the game began running.
        :return: the updated sprite to be used for rendering the baby mongoose.
        """
        spriteSet = []
        if self.currentState == self.stoic:
            spriteSet = Baby.stoicSprites
        elif self.currentState == self.seeking:
            seeking()

        if deltaTime - self.lastUpdateTime > 5:
            if self.spriteIndex >= len(spriteSet)-1:
                self.spriteTransitioner = -1
            elif self.spriteIndex == 0:
                self.spriteTransitioner = 1
            self.spriteIndex += self.spriteTransitioner
            self.lastUpdateTime = deltaTime
        return spriteSet[self.spriteIndex]
    def updateState(self, board):
        """
        Updates the state of the baby mongoose based on several conditions on the board.
        :param: board, the board used in the mongoose game.
        :return: none
        """
        if self.currentState != self.seeking:
            num = random.randint(0, 115)
            if num == 42:
                self.currentState = self.seeking
                strawX = random.randint(1, board.width - 1)
                strawY = random.randint(1, board.height - 1)
                board.setStrawberry([strawX, strawY])

    @staticmethod
    def checkForStrawberry(self):
        """
        Uses a random number generator to update the boolean value of whether or not there is a strawberry on the board,
        changes the state to "seeking".
        :return: True or False
        """


    @staticmethod
    def load_sprites():
        """
        Loads the sprites needed to portray a baby on the board.
        :param None
        :return: none
        """
        baby_spritesheet = pygame.image.load("babies.png").convert_alpha()
        # Sprites
        n0 = baby_spritesheet.subsurface(pygame.Rect((2,1152),(50,50))) # facing front
        n1 = baby_spritesheet.subsurface(pygame.Rect((2,1037),(43,50))) # turned right
        n3 = baby_spritesheet.subsurface(pygame.Rect((50,1154),(50,50))) # facing front and squinting

        Baby.stoicSprites = [n0,n1,n0,n3]