#Vector

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
		new_x = (self.x + new_vector.x)/ 10  # the denominator must be the cell size 
		new_y = (self.y + new_vector.y)/ 10
		vector = [new_x, new_y]
		return vector