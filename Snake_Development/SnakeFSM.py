"""
FSM for the Snake
"""

State = type("State", (object,), {}) # no idea what this is 

class Traveling(State):
	def Execute(self):
		"""
		I think at some some point this will contain the 
		movment peramitors for the traveling Snake
		"""
		print "Nag is Traveling"

class Offense(State):
	def Execute(self):
		"""
		I think at some some point this will contain the 
		movment peramitors for the Offense Snake
		"""
		print "Nag is Offensive"

class Defensive(State):
	def Execute(self):
		"""
		I think at some some point this will contain the 
		movment peramitors for the Defensive Snake
		"""
		print "Nag is Defensive"


###################################################################
# Ren Fucking Off 
'''
class States(object):
	def __init__ (self):
		self.pass = pass 
		self.edges = {}

	def Execute(self):
		""" 
		Does Some shit that should happen in this class

		"""

		print "I'm executing!"
	def Transition(self, transName):
		self.edges[transName]
		

Traveling = State()
Traveling.edges["To_Offense"] = "Offense"
Traveling.edges["To_Defensive"] = "To_Defensive"

Offense = State()
Traveling.edges["To_Traveling"] = "Traveling"
Traveling.edges["To_Defensive"] = "To_Defensive"

Defensive = State()
Traveling.edges["To_Offense"] = "Offense"
Traveling.edges["To_Traveling"] = "Traveling"

'''
###################################################################

class Transition(object):
	def __init__(self, nextState):
		self.nextState = nextState

	def Execute(self):
		"""
		I think at some some point this will contain infomation nessary to 
		move from one state to another 
		"""
		print "Transitioning..."




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