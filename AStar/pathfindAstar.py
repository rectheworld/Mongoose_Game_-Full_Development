"""
Created on:  March 4, 2014
Created by:  Alex Neuenkirk
"""
import math
import random
def getEstimate(current,goal):
    """
    :type current: list
    :rtype: int
    """
    cX = current[0]
    cY = current[1]
    gX = goal[0]
    gY = goal[1]
    estimate = math.sqrt((cX-gX)**2 + (cY - gY)**2)
    return int(estimate*10)
class newAgent():

    def __init__(self, startPosition, goalPosition):
        """
        :param startPosition: list
        :param goalPosition: list
        """
        self.start = startPosition
        self.goal = goalPosition

    def getPath(self, board):
        # create a new object with the agent's starting position information
        startRecord = TileRecord(self.start, None, 0, self.goal)
        # create an open list instance...
        openList = PathfindingList()
        # ...and insert the starting record into it
        openList.addToOpen(startRecord)
        # create a closed list instance
        closedList = PathfindingList()
        #Get the TileRecords until we move the goal TileRecord into the closed list or run out of items in the open list
        while openList.getSize() > 1:
            # print "\t\nGetsmallest has been called this many times: ", openList.getSmallestCount
            global current
            current = openList.getSmallest()
            # print "\n   CURRENT PARENT IS: ", current.location, "WITH COST OF:", current.estimatedTotalCost
            if current.location == current.goal:
                break
            connections = board.getConnections(current)
            for connection in connections:
                # print "\nWe are now looking at: ", connection.location
                compare = closedList.compareInClosed(connection)
                # print "Compare in the closed list yielded: ", compare
                if isinstance(compare, bool):
                    if compare:
                        # print "\tWe have found this location in the closed list, moving to next connection"
                        continue
                else:
                    # print "\tWe are switching", closedList[compare].costSoFar, "with", connection.costSoFar
                    closedList.switchInClosed(compare,connection)

                compare = openList.compareInOpen(connection)
                # print "Compare in the open list yielded: ", compare
                # Check if the returned value stored in compare is boolean or an integer
                # if compare is boolean
                if isinstance(compare, bool):
                    # if the value of compare is false then no path to connection's location is found in the OL
                    if not compare:
                        #so we will add it
                        # print "\tWe are adding", connection.location, connection.estimatedTotalCost, "to the openList"
                        openList.addToOpen(connection)
                    # otherwise, connection's location is already in the OL with a cheaper estimatedTotalCost
                    else:
                        # print "\tFound in the OL with a cheaper cost than: ", connection.estimatedTotalCost
                        continue
                # however, if compare is an integer (representing the index of the item in the closed list we
                #                                    need to switch with connection)
                else:
                    # print "we are switching", openList[compare].estimatedTotalCost, "with", connection.estimatedTotalCost
                    openList.switchInOpen(compare,connection)
            closedList.addToClosed(current)
        # Now, retrieve the path from the closed list
        path = []
        while current.location != self.start:
            path.insert(0,current.location)
            current = current.parent
        return path
class PathfindingList():
    """
    Creates a priority queue that assists in optimizing A* pathfinding.
    """
    def __init__(self):
        # None type is the first element to make indexing easier
        self.items = [None]
    def getSmallest(self):
        """
        Pops and returns the smallest item from the open list and then re-sorts
        the list so that it is a complete binary heap holding the TileRecord
        with the smallest estimatedTotalCost in the first position (index 1)
        :rtype : TileRecord
        """
        # Set our first index to 1, the first TileRecord in the binary heap
        i = 1
        # Set complete to true
        complete = True
        # Save to return later
        item = self.items[i]
        # Remove it from the list
        self.items.pop(i)
        # Re-sort the binary tree so that it stays complete
        if len(self.items) > 2:
            complete = False
        while not complete:
            # First check if the parent has only one child
            if 2*i+1 == len(self.items):
                # If it only has one child, see if the parent's value is less than the child's
                if self.items[i].estimatedTotalCost > self.items[2*i].estimatedTotalCost:
                    # if it is, swap them and we are finished
                    parent = self.items[2*i]
                    self.items[2*i] = self.items[i]
                    self.items[i] = parent
                complete = True
            # Check if parent has no children
            elif 2*i >= len(self.items):
                # If yes, we are done
                complete = True
            # If the parent has more than one child and at least one has a lower value than the parent
            elif self.items[i].estimatedTotalCost > self.items[2*i].estimatedTotalCost or \
                    self.items[i].estimatedTotalCost > self.items[2*i+1].estimatedTotalCost:
                parent = self.items[i]
                child1 = self.items[2*i]
                child2 = self.items[2*i+1]
              #find out which one has the lower value and swap that one with the parent
                if child1.estimatedTotalCost < child2.estimatedTotalCost:
                    self.items[i] = child1
                    self.items[2*i] = parent
                    i *= 2
                else:
                    self.items[i] = child2
                    self.items[2*i+1] = parent
                    i = 2*i+1
            # If the parent is already the lowest of its children, we are done
            else:
                complete = True
        # return the lowest item that was removed at the start
        return item
    def compareInClosed(self, record):
        for index in range(1,len(self.items)):
            # check if the record's location is in the closed list already
            if self.items[index].location == record.location:
                # if yes, then compare its costs to our current record
                if self.items[index].costSoFar > record.costSoFar:
                    # if its cost is greater than our current record, return its index
                    return index
                # otherwise we have already found a cheaper path to this TileRecord's location
                return True
        # if its not in the CL at all, return false so we can check the open list
        return False
    def compareInOpen(self, record):
        for index in range(1,len(self.items)):
            # check if the record's location is in the open list already
            if self.items[index].location == record.location:
                # if it is, then compare its total estimated costs to our current record
                # if its costs are greater than our current record, return its index
                if self.items[index].estimatedTotalCost > record.estimatedTotalCost:
                    return index
                # otherwise it will stay in the OL, return True
                return True
        # if its not in the OL at all, return false
        return False
    def switchInClosed(self,i,replacingRecord):
        self.items[i] = replacingRecord
        # while self.items[i/2].costSoFar > self.items[i].costSoFar:
        #     parent = self.items[i/2]
        #     self.items[i/2] = replacingRecord
        #     self.items[i] = parent
        #     i /= 2
        #     if i <= 1:
        #         break
    def switchInOpen(self,i,replacingRecord):
        """
        Switches a TileRecord in the open list with one that has the same location and a lower
            estimatedTotalCost, then re-sorts the list to maintain a complete binary heap.
        :param i: the index of the TileRecord in the open list we need to remove
        :param replacingRecord: the TileRecord we are replacing the deleted one with
        :return: void
        """
        self.items[i] = replacingRecord
        while self.items[i/2].estimatedTotalCost > self.items[i].estimatedTotalCost:
            parent = self.items[i/2]
            self.items[i/2] = replacingRecord
            self.items[i] = parent
            i /= 2
            if i<=1:
                break
    def getSize(self):
        """
        :rtype int
        :returns The length of the list, including its None item at position 0
        """
        return len(self.items)
    def addToOpen(self, tile):
        """
        Adds a tile to the open list and re-sorts the list to maintain a complete binary heap.
        :type tile: TileRecord
        """
        cost = tile.estimatedTotalCost
        self.items.append(tile)
        if len(self.items) > 2:
            i = len(self.items) - 1
            while i/2 >= 1:
                if cost < self.items[i/2].estimatedTotalCost:
                    child = self.items[i/2]
                    self.items[i/2] = tile
                    self.items[i] = child
                    i /= 2
                else:
                    break
    def addToClosed(self, tile):
        """
        Adds a TileRecord instance to the closed list
        :type tile: TileRecord
        :rtype void
        """
        self.items.append(tile)

    def __getitem__(self, index):
        """
        :rtype TileRecord
        :returns An object of type TileRecord located at the passed in index.
        """
        return self.items[index]
class Board():
    obstacles = []
    rocks = []
    cacti = []
    def __init__(self, width=32, height=24):
        """
        :type width: int
        :type height: int
        """
        self.width = width
        self.height = height

    def createVertical(self):
        self.rocks = []
        randY = random.randint(0,self.height)
        randX = random.randint(0,self.width)
        for i in range(8):
            if randY+i >= self.height:
                i *= -1
            self.rocks.append([randX,randY+i])
            # If the board is big, make the L wider
            if self.height > 30:
                self.rocks.append([randX+1,randY+i])


    def createHorizontal(self):
        randY = random.randint(0,self.height)
        randX = random.randint(0,self.width)
        for i in range(random.randint(self.width/15,self.width/5)):
            if randX+i >= self.width:
                i *= -1
            self.rocks.append([randX+i,randY])
            if self.width > 50:
                self.rocks.append([randX+i,randY+1])

    def createCacti(self):
        iterations = self.height
        for i in range(iterations):
            randX = random.randint(1,self.width)
            randY = random.randint(1,self.height)
            if not [randX,randY] in self.rocks:
                self.cacti.append([randX,randY])


    def generateObstacles(self, goalList = []):
        self.createVertical()
        self.createHorizontal()
        self.createCacti()
        popList = []
        for i in range(len(self.rocks)):
            if self.rocks[i] in goalList:
                popList.append(i)
                continue
            self.obstacles.append(self.rocks[i])
        popList.reverse()
        for index in popList:
            self.rocks.pop(index)
        popList = []
        for i in range(len(self.cacti)):
            if not self.cacti[i] in self.obstacles:
                if self.cacti[i] in goalList:
                    popList.append(i)
                    continue
                self.obstacles.append(self.cacti[i])
        popList.reverse()
        for index in popList:
            self.cacti.pop(index)

    def getCacti(self):
        return self.cacti

    def getRocks(self):
        return self.rocks

    def getConnections(self, fromTile):
        """
        :type fromTile: TileRecord
        :rtype connections: list
        """
        # declare a list of all possible connections from the parentTile
        connections = []
        # get the position of the parentTile
        position = fromTile.location
        # save new position coordinates to be used to check if connection is off the board
        left = position[0] - 1
        right = position[0] + 1
        up = position[1] - 1
        down = position[1] + 1
        up_left = [left,up]
        up_right = [right,up]
        down_left = [left,down]
        down_right = [right,down]
        # check if the position is off the board or inside of obstacles
        if left >= 0 and not [left,position[1]] in self.obstacles:
            nextTile = TileRecord([left,position[1]],fromTile,fromTile.costSoFar+10,fromTile.goal)
            connections.append(nextTile)
        if right < self.width and not [right,position[1]] in self.obstacles:
            nextTile = TileRecord([right,position[1]],fromTile,
                                  fromTile.costSoFar+10,fromTile.goal)
            connections.append(nextTile)
        if up >= 0 and not [position[0],up] in self.obstacles:
            nextTile = TileRecord([position[0],up],fromTile,
                                  fromTile.costSoFar+10,fromTile.goal)
            connections.append(nextTile)
        if down < self.height and not [position[0],down] in self.obstacles:
            nextTile = TileRecord([position[0],down],fromTile,
                                  fromTile.costSoFar+10,fromTile.goal)
            connections.append(nextTile)
        if left >= 0 and up >= 0 and not up_left in self.obstacles:
            nextTile = TileRecord(up_left,fromTile,
                                  fromTile.costSoFar+14,fromTile.goal)
            connections.append(nextTile)
        if right < self.width and up >= 0 and not up_right in self.obstacles:
            nextTile = TileRecord(up_right,fromTile,
                                  fromTile.costSoFar+14,fromTile.goal)
            connections.append(nextTile)
        if left >= 0 and down < self.height and not down_left in self.obstacles:
            nextTile = TileRecord(down_left,fromTile,
                                  fromTile.costSoFar+14,fromTile.goal)
            connections.append(nextTile)
        if right < self.width and down < self.height and not down_right in self.obstacles:
            nextTile = TileRecord(down_right,fromTile,
                                  fromTile.costSoFar+14,fromTile.goal)
            connections.append(nextTile)
        return connections
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getObstacles(self):
        """
        Returns the list of obstacle coordinates in the format [[column,row],[column,row]...]
        :returns list
        """
        return self.obstacles
class TileRecord():
    """
    Creates an object of type TileRecord, which holds important information used in pathfinding.
    """
    def __init__(self, location, parent, costSoFar, goal):
        """
        Constructor for the TileRecord class.
        :type location: list
        :type parent: TileRecord
        :type costSoFar: int
        :type goal: list
        :rtype : void
        """
        self.location = location
        self.parent = parent
        self.costSoFar = costSoFar
        self.goal = goal
        self.estimatedTotalCost = costSoFar + getEstimate(location, goal)

    def setLocation(self, coords):
        """
        Sets the coordinate location in the form of a 2D graph [column,row]
        :type coords: list
        :rtype void
        """
        self.location = coords

    def setParent(self, parent):
        """
        Saves the TileRecord instance of parent tile to be used in pathfinding.
        :type parent: TileRecord
        :rtype void
        """
        self.parent = parent

    def setCostSoFar(self, costSoFar, thisCost = 0):
        """
        Calculates and sets the costSoFar for a tile.  If thisCost is omitted it defaults to 0.
        :type costSoFar: int
        :type thisCost: int
        :rtype void
        """
        self.costSoFar = costSoFar + thisCost

    def setEstimatedTotalCost(self):
        """
        Calculates and sets the estimatedTotalCost for TileRecord object.
        :rtype void
        """
        estimate = getEstimate(self.location, self.goal)
        self.estimatedTotalCost = self.costSoFar + estimate