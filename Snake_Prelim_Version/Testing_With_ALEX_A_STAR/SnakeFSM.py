"""
FSM for the Snake
"""

import Vector_Class 
import math



def distance(point1,point2):
	"""
	Returns the distance between two points.

	"""
	distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return distance 

def getAngle(x1,y1, x2, y2):
    # Return value is 0 for right, 90 for up, 180 for left, and 270 for down (and all values between 0 and 360)
    #PS -- thank you past ren for commenting this for me -- Present Ren 
    rise = y1 - y2
    run = x1 - x2
    angle = math.atan2(run, rise) # get the angle in radians
    angle = angle * (180 / math.pi) # convert to degrees
    angle = (angle + 90) % 360 # adjust for a right-facing sprite
    return angle

def offensive_relations(degrees_differnence, distance, headx, heady):
	from Mongoose import goal 
	degrees_around_goal = getAngle(goal[0],goal[1], headx, heady)

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


State = type("State", (object,), {}) # no idea what this is 

class Traveling(State,):
	def Execute(self):
		"""
		I think at some some point this will contain the 
		movment peramitors for the traveling Snake
		"""
		from Mongoose import snake

		
		ABvector = Vector_Class.Vector(snake.A,snake.B)
		BCvector = Vector_Class.Vector(snake.B,snake.C)
		CDvector = Vector_Class.Vector(snake.C,snake.D)
		DEvector = Vector_Class.Vector(snake.D,snake.E)
		EFvector = Vector_Class.Vector(snake.E,snake.F)
		FGvector = Vector_Class.Vector(snake.F,snake.G)
		"""
		#Gets the forward momnet of the snakes head as a vector
		"""
		head_new_vector = Vector_Class.Vector([snake.point_x_speed,0], [0,snake.point_y_speed])

		"""
		#vector addition to get the resulting vectors from adding the bodys portions current 
		#direction and the perceding vectors direction
		"""  
		resulting_vector = ABvector.vector_addition(head_new_vector) # connects AB to head movemnet 
		resulting_vectorBC = BCvector.vector_addition(ABvector)# relates BC to AB
		resulting_vectorCD = CDvector.vector_addition(BCvector)
		resulting_vectorDE = DEvector.vector_addition(CDvector)
		resulting_vectorEF = EFvector.vector_addition(DEvector)
		resulting_vectorFG = FGvector.vector_addition(EFvector)



		if distance(snake.A, snake.B) >= 10:
			snake.B = [snake.B[0] + resulting_vector[0], snake.B[1] + resulting_vector[1]]
		if distance(snake.B, snake.C) >= 10:
			snake.C = [snake.C[0] + resulting_vectorBC[0], snake.C[1] + resulting_vectorBC[1]]
		if distance(snake.C, snake.D) >= 10:
			snake.D = [snake.D[0] + resulting_vectorCD[0], snake.D[1] + resulting_vectorCD[1]]
		if distance(snake.D, snake.E) >= 10:
			snake.E = [snake.E[0] + resulting_vectorDE[0], snake.E[1] + resulting_vectorDE[1]]
		if distance(snake.E, snake.F) >= 10:
			snake.F = [snake.F[0] + resulting_vectorEF[0], snake.F[1] + resulting_vectorEF[1]]
		if distance(snake.F, snake.G) >= 10:
			snake.G = [snake.G[0] + resulting_vectorFG[0], snake.G[1] + resulting_vectorFG[1]]
		snake.Execute()

		#print resulting_vector[0], resulting_vector[1]

		


		
class Offense(State):
	def Execute(self):
		"""
		I think at some some point this will contain the 
		movment peramitors for the Offense Snake
		"""
		print "Nag is Offensive"

		from Mongoose import snake

		"""
		These are used when the snake is offensive 
		"""

		Bprime = offensive_relations(90, 100, snake.headx, snake.heady) # B 
		Cprime = offensive_relations(20, 75, snake.headx, snake.heady) # C 
		Dprime = offensive_relations(5, 125, snake.headx, snake.heady) # D 
		Eprime = offensive_relations(25, 100, snake.headx, snake.heady) # E 
		Fprime = offensive_relations(90, 150, snake.headx, snake.heady) # F 
		Gprime = offensive_relations(30, 125, snake.headx, snake.heady) # G 


		ABvector = Vector_Class.Vector(snake.A,snake.B)
		BprimeAvector = Vector_Class.Vector(Bprime,snake.A)
		resulting_vectorBBprime = ABvector.vector_addition(BprimeAvector)

		ACvector = Vector_Class.Vector(snake.A,snake.C)
		CprimeAvector = Vector_Class.Vector(Cprime, snake.A)
		resulting_vectorCCprime = ACvector.vector_addition(CprimeAvector)


		ADvector = Vector_Class.Vector(snake.A,snake.D)
		DprimeAvector = Vector_Class.Vector(Dprime, snake.A)
		resulting_vectorDDprime = ADvector.vector_addition(DprimeAvector)

		AEvector = Vector_Class.Vector(snake.A, snake.E)
		EprimeAvector = Vector_Class.Vector(Eprime, snake.A)
		resulting_vectorEEprime = AEvector.vector_addition(EprimeAvector)

		AFvector = Vector_Class.Vector(snake.A,snake.F)
		FprimeAvector = Vector_Class.Vector(Fprime, snake.A)
		resulting_vectorFFprime = AFvector.vector_addition(FprimeAvector)

		AGvector = Vector_Class.Vector(snake.A,snake.G)
		GprimeAvector = Vector_Class.Vector(Gprime, snake.A)
		resulting_vectorGGprime = AGvector.vector_addition(GprimeAvector)

		FprimeBvector = Vector_Class.Vector(Fprime, snake.B)
		BFvector = Vector_Class.Vector(snake.B, snake.F)
		resulting_vectorBF = FprimeBvector.vector_addition(BFvector)

		head_new_vector = Vector_Class.Vector([snake.point_x_speed,0], [0,snake.point_y_speed])


		ABvector = Vector_Class.Vector(snake.A,snake.B)
		BCvector = Vector_Class.Vector(snake.B,snake.C)
		CDvector = Vector_Class.Vector(snake.C,snake.D)
		DEvector = Vector_Class.Vector(snake.D,snake.E)
		EFvector = Vector_Class.Vector(snake.E,snake.F)
		FGvector = Vector_Class.Vector(snake.F,snake.G)

		"""
		#vector addition to get the resulting vectors from adding the bodys portions current 
		#direction and the perceding vectors direction
		"""  
		resulting_vector = ABvector.vector_addition(head_new_vector) # connects AB to head movemnet 
		resulting_vectorBC = BCvector.vector_addition(ABvector)# relates BC to AB
		resulting_vectorCD = CDvector.vector_addition(BCvector)
		resulting_vectorDE = DEvector.vector_addition(CDvector)
		resulting_vectorEF = EFvector.vector_addition(DEvector)
		resulting_vectorFG = FGvector.vector_addition(EFvector)

	
		if distance(snake.B, Bprime) > 25:
			#print distance(snake.B,Bprime) 

			snake.B = [snake.B[0] + resulting_vectorBBprime[0], snake.B[1] + resulting_vectorBBprime[1]]
			snake.C = [snake.C[0] + resulting_vectorCCprime[0], snake.C[1] + resulting_vectorCCprime[1]]
			snake.D = [snake.D[0] + resulting_vectorDDprime[0], snake.D[1] + resulting_vectorDDprime[1]]	

			#if distance(C,D) >= 50:
			#	D = [D[0] + resulting_vectorCD[0], D[1] + resulting_vectorCD[1]]
			if distance(snake.D,snake.E ) >= 50:
				snake.E = [snake.E[0] + resulting_vectorDE[0], snake.E[1] + resulting_vectorDE[1]]
				#D = [D[0] + point_x_speed, D[1] + point_y_speed]
			if distance(snake.E, snake.F) >= 25:
				snake.F = [snake.F[0] + resulting_vectorEF[0], snake.F[1] + resulting_vectorEF[1]]
			if distance(snake.F,snake.G) >= 75:
				snake.G = [snake.G[0] + resulting_vectorFG[0], snake.G[1] + resulting_vectorFG[1]]

		if distance(snake.C, Cprime) <= 35:

			snake.E = [snake.E[0] + resulting_vectorEEprime[0], snake.E[1] + resulting_vectorEEprime[1]]	

		if distance(snake.C, Cprime) <= 25:
			snake.B = [snake.B[0] + resulting_vectorBBprime[0], snake.B[1] + resulting_vectorBBprime[1]]
			snake.C = [snake.C[0] + resulting_vectorCCprime[0], snake.C[1] + resulting_vectorCCprime[1]]
			snake.E = [snake.E[0] + resulting_vectorEEprime[0], snake.E[1] + resulting_vectorEEprime[1]]	
			snake.F = [snake.F[0] + resulting_vectorFFprime[0], snake.F[1] + resulting_vectorFFprime[1]]
			snake.G = [snake.G[0] + resulting_vectorGGprime[0], snake.G[1] + resulting_vectorGGprime[1]]	

		snake.Execute()

class Defensive(State):
	def Execute(self):
		"""
		I think at some some point this will contain the 
		movment peramitors for the Defensive Snake
		"""
		#print "Nag is Defensive"


###################################################################

###################################################################

class Transition(object):
	def __init__(self, nextState):
		self.nextState = nextState

	def Execute(self):
		"""
		I think at some some point this will contain infomation nessary to 
		move from one state to another 
		"""
		#print "Transitioning..."




###################################################################
class SnakeFSM(object):
	"""
	Char = Agent ie the snake 

	"""
	def __init__(self, char):	#
		self.char = char
		self.states = {"Traveling": Traveling(), "Offense": Offense(), "Defensive":Defensive()}
		self.transitions = {"To_Offense":Transition("Offense"), "To_Defensive": Transition("Defensive"), "To_Traveling": Transition("Traveling")}
		self.trans_name = {"To_Offense": "Offense", "To_Defensive": "Defensive", "To_Traveling":"Traveling"}
		self.cur_state_name = None

		self.curState = None
		self.trans = None 

	def SetState(self, stateName):
		#"Sets current state to passed in state "
		self.curState = self.states[stateName]
		self.cur_state_name = stateName

	
	def Transition(self, transName):
		# sets the stansitions state? 
		self.trans = self.transitions[transName]
		self.cur_state_name = self.trans_name[transName]

	"""
	Will finish later -- a function to test if we are currently in a state: will require some restruturring 

	def Check_Current_State(self, state):
		if self.cur_state_name != state:
			self.Transition()
	"""

	def Execute(self):
		# If there is a transition stored within self.trans, 
		if (self.trans):
			self.trans.Execute()
			self.SetState(self.trans.nextState)
			self.trans = None 
		self.curState.Execute()